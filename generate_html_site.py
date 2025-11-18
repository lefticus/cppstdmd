#!/usr/bin/env python3
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <https://unlicense.org>

"""
generate_html_site.py

Generate static HTML site for C++ standard evolution viewer.

This script processes stable name diffs from the diffs/ directory and generates
a static HTML site with interactive side-by-side diff views using diff2html.

Usage:
    python3 generate_html_site.py [--output DIR] [--limit N] [--test]

Options:
    --output DIR    Output directory for generated site (default: site/)
    --limit N       Limit number of diffs per version pair (for testing)
    --test          Test mode: only process first 10 diffs from one version pair
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from jinja2 import Environment

from src.cpp_std_converter.utils import ensure_dir, run_command, run_command_silent

try:
    from bs4 import BeautifulSoup
    from jinja2 import FileSystemLoader
except ImportError as e:
    print(f"Error: Missing required package: {e}")
    print("Please install required packages:")
    print("  pip install jinja2 beautifulsoup4 lxml")
    sys.exit(1)


@dataclass
class VersionPairConfig:
    """Configuration for processing a version pair diff.

    Encapsulates all parameters needed for generate_version_pair() to reduce
    parameter count from 10 to 1.
    """

    from_tag: str  # e.g., 'n4950'
    to_tag: str  # e.g., 'trunk'
    from_name: str  # e.g., 'C++23'
    to_name: str  # e.g., 'C++26'
    slug: str  # e.g., 'cpp23-to-cpp26'
    output_path: Path
    env: Environment
    max_dots: int | None = None
    limit: int | None = None
    max_workers: int | None = None


# Version pairs (adjacent only) - these are the focus of the viewer
VERSION_PAIRS = [
    ("n3337", "n4140", "C++11", "C++14", "cpp11-to-cpp14"),
    ("n4140", "n4659", "C++14", "C++17", "cpp14-to-cpp17"),
    ("n4659", "n4861", "C++17", "C++20", "cpp17-to-cpp20"),
    ("n4861", "n4950", "C++20", "C++23", "cpp20-to-cpp23"),
    ("n4950", "trunk", "C++23", "Trunk", "cpp23-to-trunk"),
]

# Author branding configuration
# Update these URLs with your actual social media handles
AUTHOR_INFO = {
    "name": "Jason Turner",
    "tagline": "Professional C++ training and code review services",
    "links": {
        "twitter": "https://twitter.com/lefticus",
        "mastodon": "https://mastodon.social/@lefticus",  # UPDATE WITH YOUR HANDLE
        "bluesky": "https://bsky.app/profile/lefticus.bsky.social",  # UPDATE WITH YOUR HANDLE
        "linkedin": "https://linkedin.com/in/jasonturner",  # UPDATE WITH YOUR PROFILE
        "youtube": "https://youtube.com/@cppweekly",
        "github": "https://github.com/lefticus",
        "project_github": "https://github.com/lefticus/cppstdmd",
        "website": "https://emptycrate.com",
    },
}

# Font Awesome 7 Free icon mappings
# See: https://fontawesome.com/search?o=r&m=free
FONT_AWESOME_ICONS = {
    "home": "fa-solid fa-house",
    "link": "fa-solid fa-link",
    "book": "fa-solid fa-book",
    "markdown": "fa-brands fa-markdown",
    "warning": "fa-solid fa-triangle-exclamation",
    "twitter": "fa-brands fa-x-twitter",
    "mastodon": "fa-brands fa-mastodon",
    "bluesky": "fa-brands fa-bluesky",  # Butterfly icon! 🦋
    "linkedin": "fa-brands fa-linkedin",
    "youtube": "fa-brands fa-youtube",
    "github": "fa-brands fa-github",
    "website": "fa-solid fa-globe",
}


def create_icon(icon_name):
    """
    Create an <i> element with Font Awesome icon classes.

    Args:
        icon_name: Key from FONT_AWESOME_ICONS dict

    Returns:
        str: HTML <i> element with Font Awesome classes
    """
    icon_classes = FONT_AWESOME_ICONS.get(
        icon_name, "fa-solid fa-question"
    )  # Default to question mark
    return f'<i class="{icon_classes}"></i>'


def check_dependencies():
    """Check if required external tools are available."""
    # Check for diff2html-cli or npx
    success, stdout, stderr = run_command_silent(["diff2html", "--version"])
    if success:
        return  # diff2html is available

    # Try npx as fallback
    success, stdout, stderr = run_command_silent(["npx", "--version"])
    if success:
        return  # npx is available

    # Neither available
    print("Error: diff2html-cli is not installed and npx is not available")
    print()
    print("To install diff2html-cli:")
    print("  npm install -g diff2html-cli")
    print()
    print("Or install npx (part of npm):")
    print("  sudo apt install npm")
    sys.exit(1)


def extract_stable_name(diff_file: Path) -> str | None:
    """Extract stable name from diff header.

    Args:
        diff_file: Path to the diff file

    Returns:
        Stable name string, or None if not found
    """
    try:
        with open(diff_file, encoding="utf-8") as f:
            for line in f:
                if line.startswith("# Stable name:"):
                    return line.split(":", 1)[1].strip()
                # Only check first few lines
                if not line.startswith("#"):
                    break
    except Exception as e:
        print(f"Warning: Could not read {diff_file}: {e}")
    return None


def get_dot_count(name: str) -> int:
    """Count hierarchy depth by counting dots only (not :: or _).

    Args:
        name: Stable name string

    Returns:
        Number of dots in the name

    Examples:
        get_dot_count("alg.copy") -> 1
        get_dot_count("alg.find.first.of") -> 3
        get_dot_count("string::append") -> 0  # Legacy C++11 notation
        get_dot_count("alg.all_of") -> 1  # Underscore is within name
    """
    return name.count(".")


def sanitize_filename(name: str) -> str:
    """Convert stable name to safe filename.

    Args:
        name: Stable name (e.g., "array", "class.copy")

    Returns:
        Safe filename (same as input for most stable names)
    """
    # Most stable names are already safe, but handle edge cases
    return re.sub(r"[^\w.-]", "_", name)


# Stable name prefix to chapter mapping for special cases
STABLE_NAME_TO_CHAPTER = {
    # Top-level container types (no dots) map to containers chapter
    "array": "containers",
    "vector": "containers",
    "deque": "containers",
    "list": "containers",
    "forwardlist": "containers",
    "map": "containers",
    "multimap": "containers",
    "set": "containers",
    "multiset": "containers",
    "unord": "containers",
    "stack": "containers",
    "queue": "containers",
    "priority": "containers",
    # Container-related prefixes
    "container": "containers",
    "sequence": "containers",
    "associative": "containers",
    # Algorithm-related prefixes
    "alg": "algorithms",
    "algorithms": "algorithms",
    # Other top-level stable names
    "iterators": "iterators",
    "utilities": "utilities",
    "strings": "strings",
    "numerics": "numerics",
    "localization": "localization",
    "input": "input.output",
    "iostream": "input.output",
    "thread": "thread",
    "atomics": "atomics",
}


def get_chapter_from_stable_name(stable_name: str) -> str:
    """Map stable name to chapter file name.

    Uses the prefix before the first dot, with special cases for
    top-level stable names that don't follow the pattern.

    Args:
        stable_name: Stable name like "array.size" or "stmt.if"

    Returns:
        Chapter file name without extension (e.g., "containers", "stmt")

    Examples:
        "array" → "containers"
        "array.size" → "containers"
        "stmt.if" → "stmt"
        "dcl.ptr" → "dcl"
    """
    # Check direct lookup first (for special cases)
    if stable_name in STABLE_NAME_TO_CHAPTER:
        return STABLE_NAME_TO_CHAPTER[stable_name]

    # Extract prefix before first dot
    prefix = stable_name.split(".")[0]

    # Check prefix lookup
    if prefix in STABLE_NAME_TO_CHAPTER:
        return STABLE_NAME_TO_CHAPTER[prefix]

    # Default: prefix is the chapter name
    return prefix


def get_timsong_url(version: str, stable_name: str) -> str | None:
    """Generate URL to timsong-cpp.github.io archived standard.

    Args:
        version: Version tag (e.g., 'n4950', 'n3337')
        stable_name: Stable name (e.g., 'array.size')

    Returns:
        Full URL to archived version, or None if not available

    Examples:
        ('n3337', 'stmt.expr') → 'https://timsong-cpp.github.io/cppwp/n3337/stmt.expr'
    """
    # trunk is not published on timsong, skip it
    if version == "trunk":
        return None

    return f"https://timsong-cpp.github.io/cppwp/{version}/{stable_name}"


def get_github_markdown_url(
    version: str, stable_name: str, repo_owner: str = "lefticus", repo_name: str = "cppstdmd"
) -> str:
    """Generate GitHub URL to markdown source for a stable name.

    Args:
        version: Version tag (e.g., 'n4950', 'trunk')
        stable_name: Stable name (e.g., 'array.overview')
        repo_owner: GitHub repository owner
        repo_name: GitHub repository name

    Returns:
        Full GitHub URL with fragment anchor

    Examples:
        ('n4950', 'array.overview') →
            'https://github.com/lefticus/cppstdmd/blob/main/n4950/containers.md#array.overview'
    """
    chapter = get_chapter_from_stable_name(stable_name)
    return (
        f"https://github.com/{repo_owner}/{repo_name}/blob/main/"
        f"{version}/{chapter}.md#{stable_name}"
    )


def get_file_size_kb(path: Path) -> float:
    """Get file size in KB.

    Args:
        path: Path to file

    Returns:
        Size in KB, rounded to 1 decimal place
    """
    try:
        size_bytes = path.stat().st_size
        return round(size_bytes / 1024, 1)
    except Exception:
        return 0.0


def count_diff_lines(diff_file: Path) -> int:
    """Count number of lines in diff (excluding header).

    Args:
        diff_file: Path to diff file

    Returns:
        Number of diff lines (lines starting with +, -, or @)
    """
    try:
        count = 0
        with open(diff_file, encoding="utf-8") as f:
            in_header = True
            for line in f:
                if in_header and line.startswith("diff --git"):
                    in_header = False
                if not in_header and (
                    line.startswith("+") or line.startswith("-") or line.startswith("@@")
                ):
                    count += 1
        return count
    except Exception:
        return 0


def extract_diff_keywords(diff_file: Path) -> list[str]:
    """Extract C++ keywords, types, and identifiers from diff content.

    Args:
        diff_file: Path to .diff file

    Returns:
        List of unique keywords found in changed lines (max 150)
    """
    import re

    try:
        content = diff_file.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []

    keywords = set()

    # Extract changed lines only (+ or - markers)
    for line in content.split("\n"):
        if line.startswith("+") or line.startswith("-"):
            # Skip metadata lines
            if line.startswith("+++") or line.startswith("---"):
                continue

            clean_line = line[1:].strip()

            # Extract C++ identifiers: [A-Za-z_][A-Za-z0-9_]*
            identifiers = re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", clean_line)
            keywords.update(identifiers)

    # Filter out very common words and single characters
    stop_words = {
        "the",
        "and",
        "for",
        "this",
        "that",
        "with",
        "from",
        "have",
        "are",
        "was",
        "were",
        "been",
        "has",
        "had",
        "can",
        "may",
        "will",
    }
    keywords = {k for k in keywords if len(k) > 2 and k.lower() not in stop_words}

    # Limit to 150 most frequent keywords
    return sorted(keywords)[:150]


def generate_search_index(stable_names: list[dict], output_dir: Path, slug: str):
    """Generate JSON search index with keywords for each stable name.

    Args:
        stable_names: List of dicts with 'name' and 'path' keys
        output_dir: Directory to write search index JSON
        slug: Version pair slug (e.g., 'cpp11-to-cpp14')
    """
    search_index = []

    print("  Generating search index...")
    for item in stable_names:
        keywords = extract_diff_keywords(item["path"])
        search_index.append({"name": item["name"], "keywords": keywords})

    # Write JSON file
    index_file = output_dir / f"{slug}_search_index.json"
    index_file.write_text(json.dumps(search_index), encoding="utf-8")

    # Report size
    size_kb = index_file.stat().st_size / 1024
    print(f"  ✓ Generated search index: {len(search_index)} sections, {size_kb:.1f} KB")


def generate_diff_html(diff_file: Path, output_file: Path, context: dict) -> bool:
    """Generate HTML for a single diff using diff2html.

    Args:
        diff_file: Path to input diff file
        output_file: Path to output HTML file
        context: Dictionary with metadata for the diff

    Returns:
        True if successful, False otherwise
    """
    try:
        # Create output directory if needed
        ensure_dir(output_file.parent)

        # Try diff2html first, fall back to npx
        diff2html_cmd = None
        success, stdout, stderr = run_command_silent(["diff2html", "--version"])
        if success:
            diff2html_cmd = "diff2html"

        if diff2html_cmd is None:
            # Try npx
            success, stdout, stderr = run_command_silent(["npx", "--version"])
            if success:
                diff2html_cmd = "npx"
            else:
                return False

        if diff2html_cmd is None:
            return False

        # Build command
        cmd = ["npx", "diff2html"] if diff2html_cmd == "npx" else ["diff2html"]
        cmd.extend(["-i", "file", "-F", str(output_file), "-s", "side", "--", str(diff_file)])

        result = run_command(cmd, check=True)

        if result.returncode != 0:
            print(f"  Warning: diff2html returned {result.returncode}")
            return False

        return True

    except subprocess.CalledProcessError as e:
        print(f"  Error running diff2html: {e}")
        if e.stderr:
            print(f"  stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"  Error generating HTML: {e}")
        return False


def create_author_banner(soup):
    """Create the author banner that appears at the top of every page."""
    banner = soup.new_tag("div", **{"class": "author-banner"})
    banner_content = soup.new_tag("div", **{"class": "author-banner-content"})

    # Author name
    author_name = soup.new_tag("span", **{"class": "author-name"})
    author_name.string = f'From {AUTHOR_INFO["name"]}'
    banner_content.append(author_name)

    # Social links
    author_links = soup.new_tag("div", **{"class": "author-links"})

    icon_map = [
        ("twitter", "twitter", "Twitter/X"),
        ("mastodon", "mastodon", "Mastodon"),
        ("bluesky", "bluesky", "Bluesky"),
        ("linkedin", "linkedin", "LinkedIn"),
        ("youtube", "youtube", "YouTube"),
        ("github", "github", "GitHub"),
        ("website", "website", "Website"),
    ]

    for key, icon_name, title in icon_map:
        icon_link = soup.new_tag(
            "a",
            href=AUTHOR_INFO["links"][key],
            target="_blank",
            rel="noopener noreferrer",
            title=title,
        )

        icon_elem = soup.new_tag("i")
        icon_elem["class"] = FONT_AWESOME_ICONS[icon_name].split()
        icon_link.append(icon_elem)

        author_links.append(icon_link)

    banner_content.append(author_links)
    banner.append(banner_content)

    return banner


def inject_navigation(html_file: Path, context: dict, env: Environment) -> bool:
    """Inject custom navigation into generated HTML.

    This post-processes the diff2html output to add:
    - Breadcrumbs
    - Version timeline navigation
    - External links
    - Metadata

    Args:
        html_file: Path to HTML file to modify
        context: Dictionary with navigation data
        env: Jinja2 Environment for template rendering

    Returns:
        True if successful, False otherwise
    """
    try:
        with open(html_file, encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        # Create custom header
        header = soup.new_tag("header", **{"class": "custom-header"})

        # Breadcrumbs
        breadcrumb_nav = soup.new_tag("nav", **{"class": "breadcrumb"})

        # Add home icon
        home_icon = soup.new_tag("i")
        home_icon["class"] = FONT_AWESOME_ICONS["home"].split()
        breadcrumb_nav.append(home_icon)
        breadcrumb_nav.append(" ")

        home_link = soup.new_tag("a", href="../../index.html")
        home_link.string = "Home"
        breadcrumb_nav.append(home_link)
        breadcrumb_nav.append(" > ")

        version_link = soup.new_tag("a", href=f'../../versions/{context["version_slug"]}.html')
        version_link.string = f'{context["from_version"]} → {context["to_version"]}'
        breadcrumb_nav.append(version_link)
        breadcrumb_nav.append(" > ")

        stable_name_span = soup.new_tag("span", **{"class": "current"})
        stable_name_span.string = f'[{context["stable_name"]}]'
        breadcrumb_nav.append(stable_name_span)

        header.append(breadcrumb_nav)

        # Title section
        title_section = soup.new_tag("div", **{"class": "title-section"})
        title_h1 = soup.new_tag("h1")
        title_h1.string = f'[{context["stable_name"]}]'
        title_section.append(title_h1)

        # Metadata
        metadata_div = soup.new_tag("div", **{"class": "metadata"})

        version_badge = soup.new_tag("span", **{"class": "badge version-badge"})
        version_badge.string = f'{context["from_version"]} → {context["to_version"]}'
        metadata_div.append(version_badge)
        metadata_div.append(" ")

        size_badge = soup.new_tag("span", **{"class": "badge size-badge"})
        size_kb = context.get("file_size_kb", 0)
        size_badge.string = f"{size_kb} KB"
        if size_kb > 100:
            size_badge["class"] = "badge size-badge large"
        metadata_div.append(size_badge)

        if context.get("line_count", 0) > 0:
            metadata_div.append(" ")
            line_badge = soup.new_tag("span", **{"class": "badge line-badge"})
            line_badge.string = f'{context["line_count"]} lines'
            metadata_div.append(line_badge)

        title_section.append(metadata_div)
        header.append(title_section)

        # Version timeline navigation
        timeline_nav = soup.new_tag("nav", **{"class": "version-timeline"})
        timeline_label = soup.new_tag("span", **{"class": "timeline-label"})
        timeline_label.string = "Evolution Timeline: "
        timeline_nav.append(timeline_label)

        # Get availability lookup from context (pre-built to avoid race conditions)
        availability = context.get("stable_name_availability", {})

        for i, (_from_tag, _to_tag, from_name, to_name, slug) in enumerate(VERSION_PAIRS):
            if i > 0:
                timeline_nav.append(" | ")

            # Check if this version pair has this stable name (from pre-built lookup)
            is_available = availability.get(slug, False)
            is_current = slug == context["version_slug"]

            if is_available or is_current:
                # Create link for available diffs or current version
                timeline_link = soup.new_tag(
                    "a",
                    href=f'../{slug}/{context["stable_name_file"]}.html',
                    **{"class": "active" if is_current else ""},
                )
                timeline_link.string = f"{from_name}→{to_name}"
                timeline_nav.append(timeline_link)
            else:
                # Create disabled span for non-existent diffs
                disabled_span = soup.new_tag("span", **{"class": "disabled"})
                disabled_span.string = f"{from_name}→{to_name}"
                timeline_nav.append(disabled_span)

        header.append(timeline_nav)

        # External links
        links_div = soup.new_tag("div", **{"class": "external-links"})

        # Add link icon
        link_icon = soup.new_tag("i")
        link_icon["class"] = FONT_AWESOME_ICONS["link"].split()
        links_div.append(link_icon)
        links_div.append(" ")

        eelis_link = soup.new_tag(
            "a",
            href=f'https://eel.is/c++draft/{context["stable_name"]}',
            target="_blank",
            rel="noopener noreferrer",
        )
        eelis_link.string = "Current Draft"
        links_div.append(eelis_link)
        links_div.append(" | ")

        github_link = soup.new_tag(
            "a",
            href="https://github.com/cplusplus/draft",
            target="_blank",
            rel="noopener noreferrer",
        )
        github_link.string = "LaTeX Source"
        links_div.append(github_link)

        header.append(links_div)

        # Archived versions (timsong-cpp.github.io)
        from_timsong = get_timsong_url(context["from_tag"], context["stable_name"])
        to_timsong = get_timsong_url(context["to_tag"], context["stable_name"])

        if from_timsong or to_timsong:
            archived_div = soup.new_tag("div", **{"class": "external-links"})

            # Add book icon
            book_icon = soup.new_tag("i")
            book_icon["class"] = FONT_AWESOME_ICONS["book"].split()
            archived_div.append(book_icon)
            archived_div.append(" Archived: ")

            if from_timsong:
                from_archived_link = soup.new_tag(
                    "a", href=from_timsong, target="_blank", rel="noopener noreferrer"
                )
                from_archived_link.string = context["from_version"]
                archived_div.append(from_archived_link)

            if from_timsong and to_timsong:
                archived_div.append(" | ")

            if to_timsong:
                to_archived_link = soup.new_tag(
                    "a", href=to_timsong, target="_blank", rel="noopener noreferrer"
                )
                to_archived_link.string = context["to_version"]
                archived_div.append(to_archived_link)

            header.append(archived_div)

        # Markdown source links
        md_links_div = soup.new_tag("div", **{"class": "external-links"})

        # Add markdown icon
        markdown_icon = soup.new_tag("i")
        markdown_icon["class"] = FONT_AWESOME_ICONS["markdown"].split()
        md_links_div.append(markdown_icon)
        md_links_div.append(" Markdown: ")

        from_md_link = soup.new_tag(
            "a",
            href=get_github_markdown_url(context["from_tag"], context["stable_name"]),
            target="_blank",
            rel="noopener noreferrer",
        )
        from_md_link.string = context["from_version"]
        md_links_div.append(from_md_link)
        md_links_div.append(" | ")

        to_md_link = soup.new_tag(
            "a",
            href=get_github_markdown_url(context["to_tag"], context["stable_name"]),
            target="_blank",
            rel="noopener noreferrer",
        )
        to_md_link.string = context["to_version"]
        md_links_div.append(to_md_link)

        header.append(md_links_div)

        # Large file warning
        if size_kb > 100:
            warning_div = soup.new_tag("div", **{"class": "warning large-file-warning"})

            # Add warning icon
            warning_icon = soup.new_tag("i")
            warning_icon["class"] = FONT_AWESOME_ICONS["warning"].split()
            warning_div.append(warning_icon)
            warning_div.append(
                f" Large diff ({size_kb} KB) - rendering may be slow on some devices"
            )

            header.append(warning_div)

        # Insert author banner and header at beginning of body
        if soup.body:
            author_banner = create_author_banner(soup)
            soup.body.insert(0, header)
            soup.body.insert(0, author_banner)

            # Add main-content id to the diff div for skip-link
            diff_div = soup.find("div", id="diff")
            if diff_div:
                # Create a wrapper with main-content id
                wrapper = soup.new_tag("div", id="main-content")
                diff_div.wrap(wrapper)

        # Render footer from template
        footer_template = env.get_template("_footer.html")
        footer_html = footer_template.render(
            generated_date=context.get("generated_date", "recently")
        )
        footer_soup = BeautifulSoup(footer_html, "html.parser")

        # Insert footer at end of body
        if soup.body and footer_soup.footer:
            soup.body.append(footer_soup.footer)

        # Update page title
        if soup.title:
            soup.title.string = context.get("title", "C++ Standard Diff")
        elif soup.head:
            title_tag = soup.new_tag("title")
            title_tag.string = context.get("title", "C++ Standard Diff")
            soup.head.insert(0, title_tag)

        # Add meta tags
        if soup.head:
            # Theme color
            theme_meta = soup.new_tag("meta", attrs={"name": "theme-color", "content": "#00a500"})
            soup.head.append(theme_meta)

            # Canonical URL
            canonical_url = (
                f"https://cppstdmd.com/diffs/{context['version_slug']}/{Path(html_file).name}"
            )
            canonical_link = soup.new_tag("link", rel="canonical", href=canonical_url)
            soup.head.append(canonical_link)

            # Open Graph
            og_tags = [
                ("og:title", context.get("title", "C++ Standard Diff")),
                (
                    "og:description",
                    f"View changes in section {context['stable_name']} between {context['from_version']} and {context['to_version']}",
                ),
                ("og:type", "website"),
                ("og:url", canonical_url),
                ("og:site_name", "C++ Standard Evolution Viewer"),
            ]
            for prop, content_val in og_tags:
                og_meta = soup.new_tag("meta", property=prop, content=content_val)
                soup.head.append(og_meta)

            # Twitter Card
            twitter_tags = [
                ("twitter:card", "summary"),
                ("twitter:title", context.get("title", "C++ Standard Diff")),
                (
                    "twitter:description",
                    f"Changes in {context['stable_name']} between {context['from_version']} and {context['to_version']}",
                ),
                ("twitter:creator", "@lefticus"),
            ]
            for name, content_val in twitter_tags:
                twitter_meta = soup.new_tag("meta", attrs={"name": name, "content": content_val})
                soup.head.append(twitter_meta)

        # Add skip-to-content link at start of body
        if soup.body:
            skip_link = soup.new_tag("a", href="#main-content", **{"class": "skip-link"})
            skip_link.string = "Skip to main content"
            soup.body.insert(0, skip_link)

        # Add CSS links to head
        if soup.head:
            # Add Font Awesome CSS
            fa_css_link = soup.new_tag(
                "link", rel="stylesheet", href="../../css/fontawesome.min.css"
            )
            soup.head.append(fa_css_link)

            fa_solid_link = soup.new_tag("link", rel="stylesheet", href="../../css/solid.min.css")
            soup.head.append(fa_solid_link)

            fa_brands_link = soup.new_tag("link", rel="stylesheet", href="../../css/brands.min.css")
            soup.head.append(fa_brands_link)

            # Add custom CSS
            css_link = soup.new_tag("link", rel="stylesheet", href="../../css/custom.css")
            soup.head.append(css_link)

        # Add navigation.js script before closing body
        if soup.body:
            script_tag = soup.new_tag("script", src="../../js/navigation.js")
            soup.body.append(script_tag)

        # Write modified HTML
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(str(soup))

        return True

    except Exception as e:
        print(f"  Error injecting navigation: {e}")
        return False


def collect_stable_names(
    diff_dir: Path, max_dots: int | None = None, limit: int | None = None
) -> list[dict]:
    """Collect stable names from a diff directory.

    Args:
        diff_dir: Path to directory containing .diff files
        max_dots: Maximum number of dots allowed (None = no limit)
        limit: Maximum number of diffs to collect (for testing)

    Returns:
        List of dicts with stable name info
    """
    stable_names = []

    if not diff_dir.exists():
        print(f"Warning: Directory not found: {diff_dir}")
        return stable_names

    diff_files = sorted(diff_dir.glob("*.diff"))

    for diff_file in diff_files:
        name = extract_stable_name(diff_file)

        if not name:
            # Fallback: use filename
            name = diff_file.stem

        # Filter by dot count if max_dots is specified
        if max_dots is not None and get_dot_count(name) > max_dots:
            continue

        stable_names.append(
            {
                "name": name,
                "size_kb": get_file_size_kb(diff_file),
                "line_count": count_diff_lines(diff_file),
                "file": diff_file.stem,
                "path": diff_file,
            }
        )

        if limit and len(stable_names) >= limit:
            break

    return stable_names


def build_stable_name_availability(
    stable_name: str, version_pairs: list[tuple], base_diffs_path: Path
) -> dict[str, bool]:
    """Check which version pairs have this stable name by scanning .diff files.

    This pre-builds a lookup table to avoid race conditions during parallel
    HTML generation. Checks for the existence of .diff files (which are already
    generated) rather than .html files (which may be concurrently created).

    Args:
        stable_name: The stable name to check (e.g., "concepts", "alg.copy")
        version_pairs: List of version pair tuples from VERSION_PAIRS
        base_diffs_path: Base path to diffs directory (e.g., Path('diffs'))

    Returns:
        Dict mapping slug → exists (bool)
        Example: {'cpp11-to-cpp14': True, 'cpp14-to-cpp17': False, ...}
    """
    availability = {}
    safe_name = sanitize_filename(stable_name)

    for from_tag, to_tag, _from_name, _to_name, slug in version_pairs:
        diff_file = (
            base_diffs_path / f"{from_tag}_to_{to_tag}" / "by_stable_name" / f"{safe_name}.diff"
        )
        availability[slug] = diff_file.exists()

    return availability


def generate_single_diff(args: tuple) -> tuple[bool, str, str]:
    """Worker function to generate a single diff HTML (for parallel execution).

    This function is designed to be called from ProcessPoolExecutor.

    Args:
        args: Tuple of (item, diff_output_dir, context, templates_dir) where:
            item: Dict with stable name info (name, file, path, size_kb, line_count)
            diff_output_dir: Path to output directory for diff HTML files
            context: Dict with metadata for the diff
            templates_dir: Path to templates directory for Jinja2

    Returns:
        Tuple of (success, stable_name, message) for logging
    """
    item, diff_output_dir, context, templates_dir = args

    stable_name = item["name"]
    output_file = Path(diff_output_dir) / f'{item["file"]}.html'

    try:
        # Create Jinja2 environment for this worker
        from jinja2 import Environment, FileSystemLoader

        env = Environment(loader=FileSystemLoader(str(templates_dir)))

        # Generate HTML with diff2html
        if not generate_diff_html(item["path"], output_file, context):
            return (False, stable_name, "diff2html failed")

        # Inject custom navigation
        if not inject_navigation(output_file, context, env):
            return (False, stable_name, "navigation injection failed")

        return (True, stable_name, "success")

    except Exception as e:
        return (False, stable_name, f"exception: {e}")


def generate_version_pair(config: VersionPairConfig) -> dict:
    """Generate pages for one version pair.

    Args:
        config: VersionPairConfig with all necessary parameters

    Returns:
        Dictionary with statistics (count, total_size_kb, total_lines, sections, etc.)
    """
    print(f"\n📦 Processing {config.from_name} → {config.to_name}...")

    diff_dir = Path(f"diffs/{config.from_tag}_to_{config.to_tag}/by_stable_name")

    if not diff_dir.exists():
        print(f"  ⚠️  Directory not found: {diff_dir}")
        return {
            "count": 0,
            "total_size_kb": 0,
            "total_lines": 0,
            "avg_size_kb": 0,
            "sections": [],
            "from_name": config.from_name,
            "to_name": config.to_name,
            "slug": config.slug,
        }

    # Collect stable names
    stable_names = collect_stable_names(diff_dir, max_dots=config.max_dots, limit=config.limit)

    if config.max_dots is not None:
        print(f"  Found {len(stable_names)} stable names (max {config.max_dots} dots)")
    else:
        print(f"  Found {len(stable_names)} stable names")

    if not stable_names:
        return {
            "count": 0,
            "total_size_kb": 0,
            "total_lines": 0,
            "avg_size_kb": 0,
            "sections": [],
            "from_name": config.from_name,
            "to_name": config.to_name,
            "slug": config.slug,
        }

    # Generate overview page
    template = config.env.get_template("version_overview.html")
    generated_date = datetime.now().strftime("%Y-%m-%d")
    stats = {"generated_date": generated_date}
    content = template.render(
        from_name=config.from_name,
        to_name=config.to_name,
        from_tag=config.from_tag,
        to_tag=config.to_tag,
        slug=config.slug,
        stable_names=stable_names,
        version_pairs=VERSION_PAIRS,
        stats=stats,
        generated_date=generated_date,
    )

    version_dir = config.output_path / "versions"
    version_dir.mkdir(exist_ok=True, parents=True)
    overview_file = version_dir / f"{config.slug}.html"
    overview_file.write_text(content, encoding="utf-8")
    print(f"  ✓ Generated overview: {overview_file}")

    # Generate search index
    generate_search_index(stable_names, version_dir, config.slug)

    # Generate individual diff pages in parallel
    diff_output_dir = config.output_path / "diffs" / config.slug
    ensure_dir(diff_output_dir)

    # Prepare tasks for parallel execution
    tasks = []
    for item in stable_names:
        # Build availability lookup to avoid race conditions during parallel processing
        stable_name_availability = build_stable_name_availability(
            stable_name=item["name"],
            version_pairs=VERSION_PAIRS,
            base_diffs_path=config.output_path.parent / "diffs",
        )

        context = {
            "title": f'[{item["name"]}] - {config.from_name} → {config.to_name}',
            "stable_name": item["name"],
            "stable_name_file": item["file"],
            "from_version": config.from_name,
            "to_version": config.to_name,
            "from_tag": config.from_tag,
            "to_tag": config.to_tag,
            "version_slug": config.slug,
            "file_size_kb": item["size_kb"],
            "line_count": item["line_count"],
            "generated_date": datetime.now().strftime("%Y-%m-%d"),
            "stable_name_availability": stable_name_availability,
        }
        # Get templates directory from config.env.loader
        templates_dir = Path(config.env.loader.searchpath[0])
        tasks.append((item, str(diff_output_dir), context, str(templates_dir)))

    # Execute tasks in parallel
    success_count = 0
    completed_count = 0

    with ProcessPoolExecutor(max_workers=config.max_workers) as executor:
        # Submit all tasks
        future_to_name = {
            executor.submit(generate_single_diff, task): task[0]["name"] for task in tasks
        }

        # Process completed tasks
        for future in as_completed(future_to_name):
            completed_count += 1
            stable_name = future_to_name[future]

            try:
                success, name, message = future.result()
                status_symbol = "✓" if success else "✗"
                print(f"  [{completed_count}/{len(stable_names)}] [{name}] {status_symbol}")

                if success:
                    success_count += 1
                elif message != "success":
                    print(f"      └─ {message}")

            except Exception as e:
                print(f"  [{completed_count}/{len(stable_names)}] [{stable_name}] ✗")
                print(f"      └─ exception: {e}")

    print(f"  ✓ Successfully generated {success_count}/{len(stable_names)} diffs")

    # Calculate statistics
    total_size_kb = sum(item["size_kb"] for item in stable_names)
    total_lines = sum(item["line_count"] for item in stable_names)
    avg_size_kb = round(total_size_kb / len(stable_names), 1) if stable_names else 0

    # Build sections list for statistics
    sections = [
        {
            "name": item["name"],
            "size_kb": item["size_kb"],
            "lines": item["line_count"],
            "from_name": config.from_name,
            "to_name": config.to_name,
            "slug": config.slug,
        }
        for item in stable_names
    ]

    return {
        "count": success_count,
        "total_size_kb": round(total_size_kb, 1),
        "total_lines": total_lines,
        "avg_size_kb": avg_size_kb,
        "sections": sections,
        "from_name": config.from_name,
        "to_name": config.to_name,
        "slug": config.slug,
    }


def generate_landing_page(output_path: Path, env: Environment, stats: dict):
    """Generate the landing page.

    Args:
        output_path: Base output directory
        env: Jinja2 environment
        stats: Dictionary with statistics about generated pages
    """
    print("\n📄 Generating landing page...")

    template = env.get_template("index.html")
    content = template.render(
        version_pairs=VERSION_PAIRS,
        stats=stats,
        generated_date=stats.get("generated_date", "recently"),
    )

    index_file = output_path / "index.html"
    index_file.write_text(content, encoding="utf-8")
    print(f"  ✓ Generated: {index_file}")


def generate_statistics_page(output_path: Path, env: Environment, stats: dict):
    """Generate the statistics page with metrics and insights.

    Args:
        output_path: Base output directory
        env: Jinja2 environment
        stats: Dictionary with statistics about generated pages
    """
    print("\n📊 Generating statistics page...")

    # Add custom filter for number formatting (must be before template load)
    def format_number(value):
        """Format number with thousands separator."""
        try:
            return f"{int(value):,}"
        except (ValueError, TypeError):
            return str(value)

    env.filters["format_number"] = format_number

    # Calculate aggregate statistics
    all_sections = []
    total_size_kb = 0
    total_lines = 0

    for pair_stats in stats.get("version_pairs", []):
        total_size_kb += pair_stats.get("total_size_kb", 0)
        total_lines += pair_stats.get("total_lines", 0)

        # Collect all sections for top sections list
        for section in pair_stats.get("sections", []):
            all_sections.append(section)

    # Sort sections by size (descending)
    top_sections = sorted(all_sections, key=lambda x: x["size_kb"], reverse=True)

    # Find largest single diff
    largest_diff = top_sections[0] if top_sections else None

    # Find most active transition (by count)
    most_active = max(stats.get("version_pairs", []), key=lambda x: x.get("count", 0), default={})

    # Find largest transition (by total size)
    largest_transition = max(
        stats.get("version_pairs", []), key=lambda x: x.get("total_size_kb", 0), default={}
    )

    # Load template after adding filters
    template = env.get_template("statistics.html")

    content = template.render(
        version_pairs=stats.get("version_pairs", []),
        total_diffs=stats.get("total_diffs", 0),
        total_size_mb=round(total_size_kb / 1024, 1),
        total_lines=total_lines,
        top_sections=top_sections,
        largest_diff=largest_diff,
        most_active=most_active,
        largest_transition=largest_transition,
        generated_date=stats.get("generated_date", "recently"),
    )

    stats_file = output_path / "statistics.html"
    stats_file.write_text(content, encoding="utf-8")
    print(f"  ✓ Generated: {stats_file}")


def copy_static_assets(output_path: Path):
    """Copy CSS, JS, fonts, and webfonts assets to output directory.

    Args:
        output_path: Base output directory
    """
    print("\n📁 Copying static assets...")

    # Create directories
    css_dir = output_path / "css"
    js_dir = output_path / "js"
    css_dir.mkdir(exist_ok=True, parents=True)
    js_dir.mkdir(exist_ok=True, parents=True)

    # Copy Font Awesome CSS files (minified versions)
    fa_css_files = ["fontawesome.min.css", "solid.min.css", "brands.min.css"]
    for css_file in fa_css_files:
        src = Path(f"templates/css/{css_file}")
        if src.exists():
            shutil.copy(src, css_dir / css_file)
            print(f"  ✓ Copied {css_file}")

    # Copy custom CSS if exists
    if Path("templates/css/custom.css").exists():
        shutil.copy("templates/css/custom.css", css_dir / "custom.css")
        print("  ✓ Copied custom.css")

    # Copy JS if exists
    if Path("templates/js/navigation.js").exists():
        shutil.copy("templates/js/navigation.js", js_dir / "navigation.js")
        print("  ✓ Copied navigation.js")

    # Copy Source Sans Pro and Source Code Pro fonts
    fonts_src = Path("templates/fonts")
    if fonts_src.exists():
        fonts_dest = output_path / "fonts"
        fonts_dest.mkdir(exist_ok=True, parents=True)

        # Copy Source font files (keep pattern specific to avoid copying Nerd Fonts)
        for font_file in fonts_src.glob("Source*.woff2"):
            shutil.copy(font_file, fonts_dest / font_file.name)
            print(f"  ✓ Copied {font_file.name}")

    # Copy Font Awesome webfonts
    webfonts_src = Path("templates/webfonts")
    if webfonts_src.exists():
        webfonts_dest = output_path / "webfonts"
        webfonts_dest.mkdir(exist_ok=True, parents=True)

        # Copy Font Awesome font files
        fa_fonts = ["fa-solid-900.woff2", "fa-brands-400.woff2"]
        for font_file in fa_fonts:
            src = webfonts_src / font_file
            if src.exists():
                shutil.copy(src, webfonts_dest / font_file)
                print(f"  ✓ Copied {font_file}")

    # Copy 404 page
    src_404 = Path("templates/404.html")
    if src_404.exists():
        # Need to render it with Jinja2 first
        from jinja2 import Environment, FileSystemLoader

        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("404.html")
        content = template.render()
        (output_path / "404.html").write_text(content, encoding="utf-8")
        print("  ✓ Generated 404.html")

    # Create .nojekyll file to disable Jekyll processing
    nojekyll_file = output_path / ".nojekyll"
    nojekyll_file.touch()
    print("  ✓ Created .nojekyll")


def generate_seo_files(output_path: Path, stats: dict, base_url: str = "https://cppstdmd.com"):
    """Generate robots.txt and sitemap.xml for SEO.

    Args:
        output_path: Base output directory
        stats: Dictionary with statistics including generated pages
        base_url: Base URL of the deployed site
    """
    print("\n🔍 Generating SEO files...")

    # Generate robots.txt
    robots_content = f"""# Allow all crawlers
User-agent: *
Allow: /

# Sitemap location
Sitemap: {base_url}/sitemap.xml
"""

    robots_file = output_path / "robots.txt"
    robots_file.write_text(robots_content, encoding="utf-8")
    print("  ✓ Generated robots.txt")

    # Generate sitemap.xml
    sitemap_urls = []

    # Add homepage
    sitemap_urls.append({"loc": f"{base_url}/", "priority": "1.0", "changefreq": "weekly"})

    # Add version overview pages
    for _from_tag, _to_tag, _from_name, _to_name, slug in VERSION_PAIRS:
        sitemap_urls.append(
            {"loc": f"{base_url}/versions/{slug}.html", "priority": "0.8", "changefreq": "weekly"}
        )

    # Add all diff pages
    for pair_stats in stats.get("version_pairs", []):
        slug = pair_stats["slug"]
        diff_dir = output_path / "diffs" / slug
        if diff_dir.exists():
            for diff_file in sorted(diff_dir.glob("*.html")):
                sitemap_urls.append(
                    {
                        "loc": f"{base_url}/diffs/{slug}/{diff_file.name}",
                        "priority": "0.6",
                        "changefreq": "monthly",
                    }
                )

    # Build XML
    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for url_data in sitemap_urls:
        xml_lines.append("  <url>")
        xml_lines.append(f'    <loc>{url_data["loc"]}</loc>')
        xml_lines.append(f'    <priority>{url_data["priority"]}</priority>')
        xml_lines.append(f'    <changefreq>{url_data["changefreq"]}</changefreq>')
        xml_lines.append("  </url>")

    xml_lines.append("</urlset>")

    sitemap_content = "\n".join(xml_lines)
    sitemap_file = output_path / "sitemap.xml"
    sitemap_file.write_text(sitemap_content, encoding="utf-8")
    print(f"  ✓ Generated sitemap.xml ({len(sitemap_urls)} URLs)")


def generate_site(
    output_dir: str = "site",
    max_dots: int | None = None,
    limit: int | None = None,
    test_mode: bool = False,
    max_workers: int | None = None,
):
    """Main generation logic.

    Args:
        output_dir: Output directory for generated site
        max_dots: Maximum number of dots in stable names (None = all levels)
        limit: Maximum number of diffs per version pair (for testing)
        test_mode: If True, only process first version pair with limit=10
        max_workers: Number of parallel workers (defaults to CPU count)
    """
    # Check dependencies
    check_dependencies()

    # Setup Jinja2 environment
    templates_dir = Path("templates")
    if not templates_dir.exists():
        print(f"Error: Templates directory not found: {templates_dir}")
        print("Please ensure templates/ directory exists with required templates.")
        sys.exit(1)

    env = Environment(loader=FileSystemLoader(str(templates_dir)))

    # Create output directory
    output_path = Path(output_dir)
    ensure_dir(output_path)

    # Determine worker count
    if max_workers is None:
        max_workers = os.cpu_count()

    print("🚀 C++ Standard Evolution Viewer - Site Generator")
    print(f"   Output directory: {output_path.absolute()}")
    if max_dots is not None:
        print(f"   Max dots: {max_dots} (0-{max_dots} dots)")
    else:
        print("   Max dots: unlimited (all levels)")
    print(f"   Workers: {max_workers} (parallel processing)")
    if limit:
        print(f"   Limit: {limit} diffs per version pair")
    if test_mode:
        print("   Mode: TEST (first version pair, 10 diffs)")

    # Test mode: only process first version pair with small limit
    pairs_to_process = VERSION_PAIRS[:1] if test_mode else VERSION_PAIRS
    test_limit = 10 if test_mode else limit

    # Generate pages for each version pair
    stats = {
        "total_diffs": 0,
        "version_pairs": [],
        "generated_date": datetime.now().strftime("%Y-%m-%d"),
    }

    for from_tag, to_tag, from_name, to_name, slug in pairs_to_process:
        # Create configuration object for this version pair
        pair_config = VersionPairConfig(
            from_tag=from_tag,
            to_tag=to_tag,
            from_name=from_name,
            to_name=to_name,
            slug=slug,
            output_path=output_path,
            env=env,
            max_dots=max_dots,
            limit=test_limit,
            max_workers=max_workers,
        )

        pair_stats = generate_version_pair(pair_config)

        stats["total_diffs"] += pair_stats["count"]
        stats["version_pairs"].append(pair_stats)

    # Generate landing page
    generate_landing_page(output_path, env, stats)

    # Generate statistics page
    generate_statistics_page(output_path, env, stats)

    # Copy static assets
    copy_static_assets(output_path)

    # Generate SEO files
    generate_seo_files(output_path, stats)

    print("\n✅ Site generation complete!")
    print(f"   Total diffs generated: {stats['total_diffs']}")
    print(f"   Output directory: {output_path.absolute()}")
    print("\nTo view the site:")
    print(f"   cd {output_path}")
    print("   python3 -m http.server 8000")
    print("   Then open: http://localhost:8000")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate static HTML site for C++ standard evolution viewer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test mode: Generate 10 diffs from one version pair
  python3 generate_html_site.py --test

  # Generate site with all levels (no filtering)
  python3 generate_html_site.py --output site/

  # Generate site with only 0-1 dots (old Tier 1)
  python3 generate_html_site.py --output site/ --max-dots 1

  # Generate site with up to 2 dots
  python3 generate_html_site.py --output site/ --max-dots 2

  # Use more workers for faster generation
  python3 generate_html_site.py --output site/ --workers 8
        """,
    )

    parser.add_argument(
        "--output",
        "-o",
        default="site",
        help="Output directory for generated site (default: site/)",
    )
    parser.add_argument(
        "--max-dots",
        type=int,
        metavar="N",
        help="Maximum number of dots in stable names (default: no limit, all levels)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        metavar="N",
        help="Limit number of diffs per version pair (for testing)",
    )
    parser.add_argument(
        "--workers",
        "-w",
        type=int,
        metavar="N",
        help="Number of parallel workers (default: CPU count)",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test mode: only process first 10 diffs from one version pair",
    )

    args = parser.parse_args()

    try:
        generate_site(
            output_dir=args.output,
            max_dots=args.max_dots,
            limit=args.limit,
            test_mode=args.test,
            max_workers=args.workers,
        )
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
