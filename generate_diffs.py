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
generate_diffs.py

Generate comprehensive diffs between C++ standard versions.

Creates both per-chapter diffs (for GitHub viewing) and full-standard diffs
(for comprehensive analysis), along with summary changelogs.

Usage:
    ./generate_diffs.py                    # Generate all diffs
    ./generate_diffs.py n3337 n4950       # Generate specific version pair
"""

import argparse
import re
import sys
import tempfile
from pathlib import Path

from src.cpp_std_converter.utils import ensure_dir, run_command_silent

# Version metadata (in chronological order)
VERSIONS = {
    "n3337": "C++11",
    "n4140": "C++14",
    "n4659": "C++17",
    "n4861": "C++20",
    "n4950": "C++23",
    "trunk": "C++26 (working draft)",
}

# Ordered list of version tags for generating pairs
VERSION_ORDER = ["n3337", "n4140", "n4659", "n4861", "n4950", "trunk"]


def generate_all_version_pairs() -> list[tuple[str, str]]:
    """
    Generate all possible version pairs in chronological order.

    Returns pairs from older to newer versions.
    Example: (n3337, n4140), (n3337, n4659), ..., (n4950, trunk)
    """
    pairs = []
    for i, from_version in enumerate(VERSION_ORDER):
        for to_version in VERSION_ORDER[i + 1 :]:
            pairs.append((from_version, to_version))
    return pairs


# Default: Generate all pairs (15 total)
DEFAULT_PAIRS = generate_all_version_pairs()


def find_common_chapters(from_version: str, to_version: str) -> tuple[set[str], set[str], set[str]]:
    """
    Find common, removed, and added chapters between two versions.

    Returns:
        (common_chapters, removed_chapters, added_chapters)
    """
    from_dir = Path(from_version)
    to_dir = Path(to_version)

    if not from_dir.exists():
        raise FileNotFoundError(f"Version directory not found: {from_dir}")
    if not to_dir.exists():
        raise FileNotFoundError(f"Version directory not found: {to_dir}")

    from_chapters = {f.stem for f in from_dir.glob("*.md")}
    to_chapters = {f.stem for f in to_dir.glob("*.md")}

    common = from_chapters & to_chapters
    removed = from_chapters - to_chapters
    added = to_chapters - from_chapters

    return common, removed, added


def get_file_stats(file_path: Path) -> dict[str, int]:
    """Get statistics for a markdown file."""
    if not file_path.exists():
        return {"size": 0, "lines": 0}

    size = file_path.stat().st_size
    with open(file_path, encoding="utf-8") as f:
        lines = sum(1 for _ in f)

    return {"size": size, "lines": lines}


def format_size(bytes: int) -> str:
    """Format bytes as human-readable size."""
    for unit in ["B", "KB", "MB"]:
        if bytes < 1024:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024
    return f"{bytes:.1f} GB"


def parse_stable_names(markdown_file: Path) -> dict[str, tuple[str, int, int]]:
    """
    Parse markdown file and extract stable name sections.

    Returns:
        Dict mapping stable_name -> (content, start_line, end_line)
    """
    if not markdown_file.exists():
        return {}

    sections = {}

    with open(markdown_file, encoding="utf-8") as f:
        lines = f.readlines()

    # Pattern to match headings with stable name anchors
    # Format: ## Title <a id="stable.name">[[stable.name]]</a>
    heading_pattern = re.compile(r'^(#{1,6})\s+.*<a id="([^"]+)">.*</a>\s*$')

    # Track heading hierarchy
    current_sections = []  # Stack of (level, stable_name, start_line)

    for line_num, line in enumerate(lines, 1):
        match = heading_pattern.match(line)

        if match:
            level = len(match.group(1))  # Count # symbols
            stable_name = match.group(2)

            # Close any sections at same or deeper level
            while current_sections and current_sections[-1][0] >= level:
                old_level, old_name, old_start = current_sections.pop()
                # Extract content from old_start to line_num - 1
                content = "".join(lines[old_start - 1 : line_num - 1])
                sections[old_name] = (content, old_start, line_num - 1)

            # Start new section
            current_sections.append((level, stable_name, line_num))

    # Close remaining open sections
    while current_sections:
        level, stable_name, start_line = current_sections.pop()
        content = "".join(lines[start_line - 1 :])
        sections[stable_name] = (content, start_line, len(lines))

    return sections


def parse_tables(markdown_file: Path) -> dict[str, tuple[str, str, int, int]]:
    """
    Parse markdown file and extract table sections by label.

    Table structure in markdown:
    - Header: **Table: Caption** <a id="label">[label]</a>
    - Blank line
    - Table rows (lines starting with |)
    - Blank line (end of table)

    Returns:
        Dict mapping table_label -> (caption, content, start_line, end_line)
    """
    if not markdown_file.exists():
        return {}

    tables = {}

    with open(markdown_file, encoding="utf-8") as f:
        lines = f.readlines()

    # Pattern to match table headers with labels
    # Format: **Table: Caption** <a id="label">[label]</a>
    table_pattern = re.compile(r'^\*\*Table:\s*(.+?)\*\*\s*<a id="([^"]+)">')

    current_table = None  # (label, caption, start_line, seen_table_content)

    for line_num, line in enumerate(lines, 1):
        match = table_pattern.match(line)

        if match:
            # Close previous table if any
            if current_table:
                label, caption, start, _ = current_table
                content = "".join(lines[start - 1 : line_num - 1])
                tables[label] = (caption, content, start, line_num - 1)

            # Start new table
            caption = match.group(1).strip()
            label = match.group(2)
            current_table = (label, caption, line_num, False)  # Not seen table content yet

        elif current_table:
            label, caption, start, seen_table_content = current_table
            stripped = line.strip()

            # Check if this is a table row (starts with |)
            is_table_row = stripped.startswith("|") and "|" in stripped[1:]

            if is_table_row:
                # Mark that we've seen table content
                if not seen_table_content:
                    current_table = (label, caption, start, True)
            elif stripped == "" and seen_table_content:
                # Blank line after we've seen table content - table is complete
                content = "".join(lines[start - 1 : line_num])
                tables[label] = (caption, content, start, line_num)
                current_table = None

    # Close final table
    if current_table:
        label, caption, start, _ = current_table
        content = "".join(lines[start - 1 :])
        tables[label] = (caption, content, start, len(lines))

    return tables


def generate_chapter_diff(from_file: Path, to_file: Path, output_file: Path) -> bool:
    """
    Generate unified diff for a single chapter.

    Returns True if diff was generated successfully.
    """
    try:
        # Use git diff --no-index for better formatting
        success, stdout, stderr = run_command_silent(
            [
                "git",
                "diff",
                "--no-index",
                "--unified=3",
                "--ignore-all-space",
                str(from_file),
                str(to_file),
            ],
            timeout=60,
        )

        # git diff returns 1 when files differ (this is expected), 0 when identical
        # Only fail if git diff command itself failed (returncode > 1)
        if not success and stderr and "fatal" in stderr.lower():
            print(f"Warning: git diff failed for {from_file.stem}", file=sys.stderr)
            return False

        # Write diff output
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(stdout)

        return True

    except Exception as e:
        print(f"Error generating diff for {from_file.stem}: {e}", file=sys.stderr)
        return False


def generate_full_diff(from_version: str, to_version: str, output_file: Path) -> bool:
    """Generate diff for full standard files."""
    from_file = Path("full") / f"{from_version}.md"
    to_file = Path("full") / f"{to_version}.md"

    if not from_file.exists():
        print(f"Warning: Full file not found: {from_file}", file=sys.stderr)
        return False
    if not to_file.exists():
        print(f"Warning: Full file not found: {to_file}", file=sys.stderr)
        return False

    return generate_chapter_diff(from_file, to_file, output_file)


def generate_stable_name_diff(
    stable_name: str, from_content: str | None, to_content: str | None, output_file: Path
) -> bool:
    """
    Generate diff for a single stable name section.

    Returns True if diff was generated successfully.
    """
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)

            # Write content to temp files
            from_file = tmp_path / "from.md"
            to_file = tmp_path / "to.md"

            if from_content:
                from_file.write_text(from_content, encoding="utf-8")
            else:
                from_file.write_text("", encoding="utf-8")

            if to_content:
                to_file.write_text(to_content, encoding="utf-8")
            else:
                to_file.write_text("", encoding="utf-8")

            # Use git diff with high-quality options
            success, stdout, stderr = run_command_silent(
                [
                    "git",
                    "diff",
                    "--no-index",
                    "--patience",  # Better algorithm for moved sections
                    "--unified=5",  # More context lines
                    "--ignore-all-space",  # Ignore all whitespace differences
                    str(from_file),
                    str(to_file),
                ],
                timeout=30,
            )

            # git diff returns 1 when files differ (this is expected), 0 when identical
            # Only fail if git diff command itself failed
            if not success and stderr and "fatal" in stderr.lower():
                return False

            # Add header with stable name
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(f"# Diff for [{stable_name}]\n")
                f.write(f"# Stable name: {stable_name}\n\n")
                f.write(stdout)

            return True

    except Exception as e:
        print(f"Error generating diff for {stable_name}: {e}", file=sys.stderr)
        return False


def generate_stable_name_diffs(
    from_version: str, to_version: str, output_dir: Path, max_dots: int | None = None
) -> int:
    """
    Generate diffs for all stable names across all chapters.

    Args:
        from_version: Starting version directory
        to_version: Ending version directory
        output_dir: Output directory for diffs
        max_dots: Maximum number of dots in stable names (None = all levels)

    Returns the number of diffs successfully generated.
    """
    if max_dots is not None:
        print(f"  Generating stable name diffs (max {max_dots} dots)...")
    else:
        print("  Generating stable name diffs...")

    # Collect all stable names from both versions
    from_stable_names = {}  # stable_name -> (chapter, content, start, end)
    to_stable_names = {}

    # Parse all chapter files from both versions
    from_dir = Path(from_version)
    to_dir = Path(to_version)

    for chapter_file in sorted(from_dir.glob("*.md")):
        chapter = chapter_file.stem
        sections = parse_stable_names(chapter_file)
        for stable_name, (content, start, end) in sections.items():
            from_stable_names[stable_name] = (chapter, content, start, end)

    for chapter_file in sorted(to_dir.glob("*.md")):
        chapter = chapter_file.stem
        sections = parse_stable_names(chapter_file)
        for stable_name, (content, start, end) in sections.items():
            to_stable_names[stable_name] = (chapter, content, start, end)

    # Find all unique stable names
    all_stable_names = set(from_stable_names.keys()) | set(to_stable_names.keys())
    removed_names = all_stable_names - to_stable_names.keys()
    added_names = all_stable_names - from_stable_names.keys()

    print(f"    Found {len(all_stable_names)} unique stable names")
    print(f"    - {len(from_stable_names)} in {from_version}")
    print(f"    - {len(to_stable_names)} in {to_version}")
    print(f"    - {len(removed_names)} removed")
    print(f"    - {len(added_names)} added")

    # Filter by dot count if max_dots is specified
    if max_dots is not None:
        filtered_names = {name for name in all_stable_names if name.count(".") <= max_dots}
        print(f"    Filtering to {len(filtered_names)} stable names (max {max_dots} dots)")
        all_stable_names = filtered_names

    # Create output directory
    stable_name_dir = output_dir / "by_stable_name"
    ensure_dir(stable_name_dir)

    # Generate diff for each stable name
    success_count = 0
    diff_sizes = {}  # stable_name -> size

    for stable_name in sorted(all_stable_names):
        from_content = from_stable_names.get(stable_name, (None, None, None, None))[1]
        to_content = to_stable_names.get(stable_name, (None, None, None, None))[1]

        # Skip if both are empty or identical
        if from_content == to_content:
            continue

        # Generate safe filename from stable name
        safe_name = stable_name.replace("/", "_").replace("\\", "_")
        output_file = stable_name_dir / f"{safe_name}.diff"

        if generate_stable_name_diff(stable_name, from_content, to_content, output_file):
            success_count += 1
            diff_sizes[stable_name] = output_file.stat().st_size

    # Generate README for stable name diffs
    readme_path = stable_name_dir / "README.md"
    generate_stable_name_readme(
        from_version,
        to_version,
        readme_path,
        from_stable_names,
        to_stable_names,
        added_names,
        removed_names,
        diff_sizes,
    )

    print(f"  Generated {success_count} stable name diffs")
    return success_count


def generate_stable_name_readme(
    from_version: str,
    to_version: str,
    readme_path: Path,
    from_stable_names: dict,
    to_stable_names: dict,
    added_names: set[str],
    removed_names: set[str],
    diff_sizes: dict[str, int],
) -> None:
    """Generate README for stable name diffs directory."""
    from_name = VERSIONS.get(from_version, from_version)
    to_name = VERSIONS.get(to_version, to_version)

    lines = []
    lines.append(f"# Stable Name Diffs: {from_name} → {to_name}\n")
    lines.append(
        f"Comparison of individual stable name sections between {from_version} and {to_version}.\n"
    )
    lines.append("## Overview\n")
    lines.append(
        "This directory contains focused diffs for each stable name (section) in the C++ standard. "
    )
    lines.append(
        "Unlike chapter-level diffs which can be thousands of lines, these diffs focus on specific "
    )
    lines.append("sections like `[array]`, `[class.copy]`, or `[dcl.init]`.\n")
    lines.append("**Benefits:**\n")
    lines.append("- **Granular tracking**: See exactly how a specific feature evolved")
    lines.append("- **Reduced noise**: No shuffling between unrelated sections")
    lines.append("- **Educational**: Perfect for studying feature introduction and evolution")
    lines.append(
        "- **Cross-version analysis**: Easy to compare same stable name across multiple versions\n"
    )

    # Statistics
    lines.append("## Statistics\n")
    lines.append(f"- **Total stable names**: {len(from_stable_names | to_stable_names)}")
    lines.append(f"- **In {from_version}**: {len(from_stable_names)}")
    lines.append(f"- **In {to_version}**: {len(to_stable_names)}")
    lines.append(f"- **Added in {to_version}**: {len(added_names)}")
    lines.append(f"- **Removed in {to_version}**: {len(removed_names)}")
    lines.append(f"- **Modified**: {len(diff_sizes)}\n")

    # Top 20 largest changes
    if diff_sizes:
        lines.append("## Largest Changes\n")
        lines.append("Top 20 stable names by diff size:\n")
        sorted_by_size = sorted(diff_sizes.items(), key=lambda x: x[1], reverse=True)[:20]
        for i, (stable_name, size) in enumerate(sorted_by_size, 1):
            safe_name = stable_name.replace("/", "_").replace("\\", "_")
            size_kb = size / 1024
            lines.append(f"{i}. [`[{stable_name}]`]({safe_name}.diff) - {size_kb:.1f} KB")
        lines.append("")

    # New stable names
    if added_names:
        lines.append(f"## New Stable Names in {to_name}\n")
        lines.append(f"Stable names that didn't exist in {from_name}:\n")
        for stable_name in sorted(added_names)[:50]:  # Show first 50
            safe_name = stable_name.replace("/", "_").replace("\\", "_")
            # Get chapter
            chapter = to_stable_names.get(stable_name, (None,))[0]
            lines.append(f"- [`[{stable_name}]`]({safe_name}.diff) (from {chapter}.md)")
        if len(added_names) > 50:
            lines.append(f"\n*...and {len(added_names) - 50} more*")
        lines.append("")

    # Removed stable names
    if removed_names:
        lines.append(f"## Removed Stable Names in {to_name}\n")
        lines.append(f"Stable names that existed in {from_name} but not in {to_name}:\n")
        for stable_name in sorted(removed_names)[:50]:
            safe_name = stable_name.replace("/", "_").replace("\\", "_")
            chapter = from_stable_names.get(stable_name, (None,))[0]
            lines.append(f"- [`[{stable_name}]`]({safe_name}.diff) (was in {chapter}.md)")
        if len(removed_names) > 50:
            lines.append(f"\n*...and {len(removed_names) - 50} more*")
        lines.append("")

    # Usage examples
    lines.append("## How to Use\n")
    lines.append("**Example: Track `[array]` evolution**\n")
    lines.append("```bash")
    lines.append("# View how std::array changed from C++11 to C++23")
    lines.append("less array.diff")
    lines.append("```\n")
    lines.append("**Example: Find all changes to ranges**\n")
    lines.append("```bash")
    lines.append("# List all ranges-related stable names")
    lines.append("ls ranges*.diff")
    lines.append("")
    lines.append("# View a specific ranges section")
    lines.append("less ranges.general.diff")
    lines.append("```\n")
    lines.append(
        "**Diff Quality**: Generated with `git diff --patience --unified=5 --ignore-all-space` "
    )
    lines.append(
        "for best section matching and readability, ignoring all whitespace differences.\n"
    )

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def generate_table_diff(
    table_label: str,
    caption: str,
    from_content: str | None,
    to_content: str | None,
    output_file: Path,
) -> bool:
    """
    Generate diff for a single table.

    Returns True if diff was generated successfully.
    """
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)

            # Write content to temp files
            from_file = tmp_path / "from.md"
            to_file = tmp_path / "to.md"

            if from_content:
                from_file.write_text(from_content, encoding="utf-8")
            else:
                from_file.write_text("", encoding="utf-8")

            if to_content:
                to_file.write_text(to_content, encoding="utf-8")
            else:
                to_file.write_text("", encoding="utf-8")

            # Use git diff with high-quality options
            success, stdout, stderr = run_command_silent(
                [
                    "git",
                    "diff",
                    "--no-index",
                    "--patience",
                    "--unified=5",
                    "--ignore-all-space",
                    str(from_file),
                    str(to_file),
                ],
                timeout=30,
            )

            # git diff returns 1 when files differ (expected), 0 when identical
            if not success and stderr and "fatal" in stderr.lower():
                return False

            # Add header with table label and caption
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(f"# Diff for table [{table_label}]\n")
                f.write(f"# Table label: {table_label}\n")
                f.write(f"# Caption: {caption}\n\n")
                f.write(stdout)

            return True

    except Exception as e:
        print(f"Error generating diff for table {table_label}: {e}", file=sys.stderr)
        return False


def generate_table_diffs(from_version: str, to_version: str, output_dir: Path) -> int:
    """
    Generate diffs for all tables across all chapters.

    Returns the number of diffs successfully generated.
    """
    print("  Generating table diffs...")

    # Collect all tables from both versions
    # table_label -> (chapter, caption, content, start, end)
    from_tables: dict[str, tuple[str, str, str, int, int]] = {}
    to_tables: dict[str, tuple[str, str, str, int, int]] = {}

    from_dir = Path(from_version)
    to_dir = Path(to_version)

    for chapter_file in sorted(from_dir.glob("*.md")):
        chapter = chapter_file.stem
        tables = parse_tables(chapter_file)
        for label, (caption, content, start, end) in tables.items():
            from_tables[label] = (chapter, caption, content, start, end)

    for chapter_file in sorted(to_dir.glob("*.md")):
        chapter = chapter_file.stem
        tables = parse_tables(chapter_file)
        for label, (caption, content, start, end) in tables.items():
            to_tables[label] = (chapter, caption, content, start, end)

    # Find all unique table labels
    all_tables = set(from_tables.keys()) | set(to_tables.keys())
    removed_tables = all_tables - to_tables.keys()
    added_tables = all_tables - from_tables.keys()

    print(f"    Found {len(all_tables)} unique tables")
    print(f"    - {len(from_tables)} in {from_version}")
    print(f"    - {len(to_tables)} in {to_version}")
    print(f"    - {len(removed_tables)} removed")
    print(f"    - {len(added_tables)} added")

    # Create output directory
    table_dir = output_dir / "by_table"
    ensure_dir(table_dir)

    # Generate diff for each table
    success_count = 0
    diff_sizes: dict[str, int] = {}

    for label in sorted(all_tables):
        from_data = from_tables.get(label)
        to_data = to_tables.get(label)

        from_content = from_data[2] if from_data else None
        to_content = to_data[2] if to_data else None
        caption = to_data[1] if to_data else (from_data[1] if from_data else label)

        # Skip if both are empty or identical
        if from_content == to_content:
            continue

        # Generate safe filename from label
        safe_name = label.replace("/", "_").replace("\\", "_")
        output_file = table_dir / f"{safe_name}.diff"

        if generate_table_diff(label, caption, from_content, to_content, output_file):
            success_count += 1
            diff_sizes[label] = output_file.stat().st_size

    # Generate README for table diffs
    readme_path = table_dir / "README.md"
    generate_table_readme(
        from_version,
        to_version,
        readme_path,
        from_tables,
        to_tables,
        added_tables,
        removed_tables,
        diff_sizes,
    )

    print(f"  Generated {success_count} table diffs")
    return success_count


def generate_table_readme(
    from_version: str,
    to_version: str,
    readme_path: Path,
    from_tables: dict,
    to_tables: dict,
    added_tables: set[str],
    removed_tables: set[str],
    diff_sizes: dict[str, int],
) -> None:
    """Generate README for table diffs directory."""
    from_name = VERSIONS.get(from_version, from_version)
    to_name = VERSIONS.get(to_version, to_version)

    lines = []
    lines.append(f"# Table Diffs: {from_name} → {to_name}\n")
    lines.append(f"Comparison of individual tables between {from_version} and {to_version}.\n")
    lines.append("## Overview\n")
    lines.append("This directory contains focused diffs for each table in the C++ standard. ")
    lines.append(
        "Tables are tracked by their stable label (e.g., `support.summary`, `locale.category.facets`).\n"
    )

    # Statistics
    lines.append("## Statistics\n")
    lines.append(f"- **Total tables**: {len(from_tables | to_tables)}")
    lines.append(f"- **In {from_version}**: {len(from_tables)}")
    lines.append(f"- **In {to_version}**: {len(to_tables)}")
    lines.append(f"- **Added in {to_version}**: {len(added_tables)}")
    lines.append(f"- **Removed in {to_version}**: {len(removed_tables)}")
    lines.append(f"- **Modified**: {len(diff_sizes)}\n")

    # Top 20 largest changes
    if diff_sizes:
        lines.append("## Largest Changes\n")
        lines.append("Top 20 tables by diff size:\n")
        sorted_by_size = sorted(diff_sizes.items(), key=lambda x: x[1], reverse=True)[:20]
        for i, (label, size) in enumerate(sorted_by_size, 1):
            safe_name = label.replace("/", "_").replace("\\", "_")
            size_kb = size / 1024
            # Get caption
            caption = to_tables.get(label, from_tables.get(label, (None, label)))[1]
            lines.append(f"{i}. [`{label}`]({safe_name}.diff) - {caption} ({size_kb:.1f} KB)")
        lines.append("")

    # New tables
    if added_tables:
        lines.append(f"## New Tables in {to_name}\n")
        lines.append(f"Tables that didn't exist in {from_name}:\n")
        for label in sorted(added_tables)[:30]:
            safe_name = label.replace("/", "_").replace("\\", "_")
            chapter, caption = to_tables.get(label, (None, label))[:2]
            lines.append(f"- [`{label}`]({safe_name}.diff) - {caption} (from {chapter}.md)")
        if len(added_tables) > 30:
            lines.append(f"\n*...and {len(added_tables) - 30} more*")
        lines.append("")

    # Removed tables
    if removed_tables:
        lines.append(f"## Removed Tables in {to_name}\n")
        lines.append(f"Tables that existed in {from_name} but not in {to_name}:\n")
        for label in sorted(removed_tables)[:30]:
            safe_name = label.replace("/", "_").replace("\\", "_")
            chapter, caption = from_tables.get(label, (None, label))[:2]
            lines.append(f"- [`{label}`]({safe_name}.diff) - {caption} (was in {chapter}.md)")
        if len(removed_tables) > 30:
            lines.append(f"\n*...and {len(removed_tables) - 30} more*")
        lines.append("")

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def generate_summary(
    from_version: str,
    to_version: str,
    diff_dir: Path,
    common: set[str],
    removed: set[str],
    added: set[str],
) -> str:
    """Generate summary markdown for a version pair."""
    from_name = VERSIONS.get(from_version, from_version)
    to_name = VERSIONS.get(to_version, to_version)

    lines = []
    lines.append(f"# C++ Standard Evolution: {from_name} → {to_name}\n")
    lines.append(f"Comparison of {from_version} to {to_version}\n")

    # New chapters
    if added:
        lines.append("## New Chapters\n")
        for chapter in sorted(added):
            to_file = Path(to_version) / f"{chapter}.md"
            stats = get_file_stats(to_file)
            size_str = format_size(stats["size"])
            lines.append(f"- **{chapter}.md** ({size_str}, {stats['lines']:,} lines)")

            # Try to infer what the chapter is about from first heading
            try:
                with open(to_file, encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("# "):
                            title = line[2:].strip()
                            lines.append(f"  - {title}")
                            break
            except Exception:
                pass
        lines.append("")

    # Removed chapters
    if removed:
        lines.append("## Removed Chapters\n")
        for chapter in sorted(removed):
            from_file = Path(from_version) / f"{chapter}.md"
            stats = get_file_stats(from_file)
            size_str = format_size(stats["size"])
            lines.append(f"- **{chapter}.md** ({size_str}, {stats['lines']:,} lines)")
        lines.append("")

    # Changed chapters with statistics
    lines.append("## Modified Chapters\n")
    lines.append("| Chapter | Old Size | New Size | Change | Old Lines | New Lines | Change |")
    lines.append("|---------|----------|----------|--------|-----------|-----------|--------|")

    for chapter in sorted(common):
        from_file = Path(from_version) / f"{chapter}.md"
        to_file = Path(to_version) / f"{chapter}.md"

        from_stats = get_file_stats(from_file)
        to_stats = get_file_stats(to_file)

        size_change = to_stats["size"] - from_stats["size"]
        size_pct = (
            ((to_stats["size"] / from_stats["size"] - 1) * 100) if from_stats["size"] > 0 else 0
        )
        line_change = to_stats["lines"] - from_stats["lines"]
        line_pct = (
            ((to_stats["lines"] / from_stats["lines"] - 1) * 100) if from_stats["lines"] > 0 else 0
        )

        # Format changes
        size_change_str = (
            f"+{format_size(size_change)}" if size_change >= 0 else format_size(size_change)
        )
        size_pct_str = f"+{size_pct:.1f}%" if size_pct >= 0 else f"{size_pct:.1f}%"
        line_change_str = f"+{line_change:,}" if line_change >= 0 else f"{line_change:,}"
        line_pct_str = f"+{line_pct:.1f}%" if line_pct >= 0 else f"{line_pct:.1f}%"

        lines.append(
            f"| [{chapter}]({chapter}.diff) | "
            f"{format_size(from_stats['size'])} | "
            f"{format_size(to_stats['size'])} | "
            f"{size_change_str} ({size_pct_str}) | "
            f"{from_stats['lines']:,} | "
            f"{to_stats['lines']:,} | "
            f"{line_change_str} ({line_pct_str}) |"
        )

    lines.append("")

    # Stable name diffs section
    lines.append("## Stable Name Diffs\n")
    lines.append(
        "**[Browse diffs by stable name](by_stable_name/)** - Focused diffs for individual sections\n"
    )
    lines.append(
        "Instead of viewing entire chapter diffs, you can now view changes for specific stable names:"
    )
    lines.append("- Example: Track how `[array]` evolved from C++11 to C++23")
    lines.append("- Example: See all changes to `[class.copy]` or `[dcl.init]`")
    lines.append("- **Benefits**: Reduced noise, granular tracking, perfect for educational use\n")

    # Table diffs section
    lines.append("## Table Diffs\n")
    lines.append("**[Browse diffs by table](by_table/)** - Track changes to individual tables\n")
    lines.append(
        "Tables are tracked by their stable label (e.g., `support.summary`, `locale.category.facets`):"
    )
    lines.append("- See how specification tables evolved between versions")
    lines.append("- Track changes to type requirements, library summaries, and more")
    lines.append("- **Benefits**: Tables often contain critical specification details\n")

    # Full standard comparison
    lines.append("## Full Standard Comparison\n")
    lines.append("- [View complete diff](full_standard.diff) (all chapters concatenated)")
    lines.append("- Note: This file may be large and is best viewed locally\n")

    # Usage instructions
    lines.append("## How to Use These Diffs\n")
    lines.append("**On GitHub:**")
    lines.append("- Click any chapter link above to view the diff on GitHub")
    lines.append("- Per-chapter diffs render well in GitHub's web interface\n")
    lines.append("**Locally:**")
    lines.append("```bash")
    lines.append("# View specific chapter diff")
    lines.append(f"git diff --no-index {from_version}/class.md {to_version}/class.md")
    lines.append("")
    lines.append("# View with side-by-side comparison")
    lines.append(f"diff -y {from_version}/class.md {to_version}/class.md | less")
    lines.append("")
    lines.append("# View full standard diff")
    lines.append(f"less diffs/{from_version}_to_{to_version}/full_standard.diff")
    lines.append("```\n")

    return "\n".join(lines)


def generate_diff_pair(
    from_version: str, to_version: str, output_base: Path, max_dots: int | None = None
) -> None:
    """Generate all diffs for a version pair.

    Args:
        from_version: Starting version directory
        to_version: Ending version directory
        output_base: Output directory for diffs
        max_dots: Maximum number of dots in stable names (None = all levels)
    """
    from_name = VERSIONS.get(from_version, from_version)
    to_name = VERSIONS.get(to_version, to_version)

    print(f"\nGenerating diffs: {from_name} → {to_name}")
    print(f"  Output directory: {output_base}")

    # Create output directory
    ensure_dir(output_base)

    # Find common/added/removed chapters
    common, removed, added = find_common_chapters(from_version, to_version)

    print(f"  Common chapters: {len(common)}")
    print(f"  Removed chapters: {len(removed)}")
    print(f"  Added chapters: {len(added)}")

    # Generate per-chapter diffs
    print("  Generating per-chapter diffs...")
    success_count = 0
    for chapter in sorted(common):
        from_file = Path(from_version) / f"{chapter}.md"
        to_file = Path(to_version) / f"{chapter}.md"
        output_file = output_base / f"{chapter}.diff"

        if generate_chapter_diff(from_file, to_file, output_file):
            success_count += 1

    print(f"  Generated {success_count}/{len(common)} chapter diffs")

    # Generate full standard diff
    print("  Generating full standard diff...")
    full_diff_file = output_base / "full_standard.diff"
    if generate_full_diff(from_version, to_version, full_diff_file):
        print("  Generated full standard diff")
    else:
        print("  Warning: Could not generate full standard diff")

    # Generate stable name diffs
    generate_stable_name_diffs(from_version, to_version, output_base, max_dots=max_dots)

    # Generate table diffs
    generate_table_diffs(from_version, to_version, output_base)

    # Generate summary
    print("  Generating summary...")
    summary_file = output_base / "README.md"
    summary_content = generate_summary(
        from_version, to_version, output_base, common, removed, added
    )
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(summary_content)

    print(f"✓ Completed: {from_name} → {to_name}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate diffs between C++ standard versions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ./generate_diffs.py                    # Generate all 15 version pairs
  ./generate_diffs.py n3337 n4950       # Generate specific version pair
  ./generate_diffs.py n3337 n4950 --max-dots 1   # Only 0-1 dots
  ./generate_diffs.py --list            # List available versions

By default, generates all possible pairs (15 total):
  - Adjacent versions: C++11→C++14, C++14→C++17, etc.
  - Intermediate spans: C++11→C++17, C++14→C++20, etc.
  - Major evolution: C++11→C++23, C++17→C++26, etc.
        """,
    )
    parser.add_argument("from_version", nargs="?", help="Source version (e.g., n3337)")
    parser.add_argument("to_version", nargs="?", help="Target version (e.g., n4950)")
    parser.add_argument("--list", action="store_true", help="List available versions")
    parser.add_argument("--output", "-o", default="diffs", help="Output directory (default: diffs)")
    parser.add_argument(
        "--max-dots",
        type=int,
        metavar="N",
        help="Maximum number of dots in stable names (default: no limit, all levels)",
    )

    args = parser.parse_args()

    if args.list:
        print("Available versions:")
        for version, name in VERSIONS.items():
            print(f"  {version:8} - {name}")
        print(f"\nBy default, generates all {len(DEFAULT_PAIRS)} possible version pairs")
        return 0

    output_root = Path(args.output)

    # Generate specific pair or all default pairs
    if args.from_version and args.to_version:
        pairs = [(args.from_version, args.to_version)]
    else:
        pairs = DEFAULT_PAIRS

    print(f"Generating diffs for {len(pairs)} version pairs")
    print(f"Output directory: {output_root}")

    for from_v, to_v in pairs:
        output_dir = output_root / f"{from_v}_to_{to_v}"
        try:
            generate_diff_pair(from_v, to_v, output_dir, max_dots=args.max_dots)
        except Exception as e:
            print(f"Error generating diff pair {from_v} → {to_v}: {e}", file=sys.stderr)
            continue

    print(f"\n✓ All diffs generated in {output_root}/")
    print("\nView summaries:")
    for from_v, to_v in pairs:
        print(f"  {output_root}/{from_v}_to_{to_v}/README.md")

    return 0


if __name__ == "__main__":
    sys.exit(main())
