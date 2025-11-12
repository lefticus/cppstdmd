#!/usr/bin/env python3
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
import os
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    from jinja2 import Environment, FileSystemLoader
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"Error: Missing required package: {e}")
    print("Please install required packages:")
    print("  pip install jinja2 beautifulsoup4 lxml")
    sys.exit(1)


# Version pairs (adjacent only) - these are the focus of the viewer
VERSION_PAIRS = [
    ('n3337', 'n4140', 'C++11', 'C++14', 'cpp11-to-cpp14'),
    ('n4140', 'n4659', 'C++14', 'C++17', 'cpp14-to-cpp17'),
    ('n4659', 'n4861', 'C++17', 'C++20', 'cpp17-to-cpp20'),
    ('n4861', 'n4950', 'C++20', 'C++23', 'cpp20-to-cpp23'),
    ('n4950', 'trunk', 'C++23', 'C++26', 'cpp23-to-cpp26'),
]


def check_dependencies():
    """Check if required external tools are available."""
    # Check for diff2html-cli
    try:
        result = subprocess.run(['diff2html', '--version'],
                              capture_output=True, text=True, check=False)
        if result.returncode != 0:
            raise FileNotFoundError()
    except FileNotFoundError:
        print("Error: diff2html-cli is not installed or not in PATH")
        print()
        print("To install diff2html-cli:")
        print("  npm install -g diff2html-cli")
        print()
        print("Or using npx (no installation required):")
        print("  The script will use 'npx diff2html' if available")
        sys.exit(1)


def extract_stable_name(diff_file: Path) -> Optional[str]:
    """Extract stable name from diff header.

    Args:
        diff_file: Path to the diff file

    Returns:
        Stable name string, or None if not found
    """
    try:
        with open(diff_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('# Stable name:'):
                    return line.split(':', 1)[1].strip()
                # Only check first few lines
                if not line.startswith('#'):
                    break
    except Exception as e:
        print(f"Warning: Could not read {diff_file}: {e}")
    return None


def classify_stable_name(name: str) -> int:
    """Determine tier (1 = featured, 2 = detailed).

    Tier 1: 0-1 dots (e.g., "array", "class.copy")
    Tier 2: 2+ dots (e.g., "class.copy.ctor", "alg.binary.search")

    Args:
        name: Stable name string

    Returns:
        Tier number (1 or 2)
    """
    dot_count = name.count('.')
    return 1 if dot_count <= 1 else 2


def sanitize_filename(name: str) -> str:
    """Convert stable name to safe filename.

    Args:
        name: Stable name (e.g., "array", "class.copy")

    Returns:
        Safe filename (same as input for most stable names)
    """
    # Most stable names are already safe, but handle edge cases
    return re.sub(r'[^\w.-]', '_', name)


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
        with open(diff_file, 'r', encoding='utf-8') as f:
            in_header = True
            for line in f:
                if in_header and line.startswith('diff --git'):
                    in_header = False
                if not in_header and (line.startswith('+') or
                                     line.startswith('-') or
                                     line.startswith('@@')):
                    count += 1
        return count
    except Exception:
        return 0


def generate_diff_html(diff_file: Path, output_file: Path, context: Dict) -> bool:
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
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Use diff2html-cli to generate HTML
        cmd = [
            'diff2html',
            '-i', 'file',
            '-F', str(output_file),
            '-s', 'side',
            '--',
            str(diff_file)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

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


def inject_navigation(html_file: Path, context: Dict) -> bool:
    """Inject custom navigation into generated HTML.

    This post-processes the diff2html output to add:
    - Breadcrumbs
    - Version timeline navigation
    - External links
    - Metadata

    Args:
        html_file: Path to HTML file to modify
        context: Dictionary with navigation data

    Returns:
        True if successful, False otherwise
    """
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Create custom header
        header = soup.new_tag('header', **{'class': 'custom-header'})

        # Breadcrumbs
        breadcrumb_nav = soup.new_tag('nav', **{'class': 'breadcrumb'})
        breadcrumb_nav.append('🏠 ')
        home_link = soup.new_tag('a', href='../../index.html')
        home_link.string = 'Home'
        breadcrumb_nav.append(home_link)
        breadcrumb_nav.append(' > ')

        version_link = soup.new_tag('a', href=f'../../versions/{context["version_slug"]}.html')
        version_link.string = f'{context["from_version"]} → {context["to_version"]}'
        breadcrumb_nav.append(version_link)
        breadcrumb_nav.append(' > ')

        stable_name_span = soup.new_tag('span', **{'class': 'current'})
        stable_name_span.string = f'[{context["stable_name"]}]'
        breadcrumb_nav.append(stable_name_span)

        header.append(breadcrumb_nav)

        # Title section
        title_section = soup.new_tag('div', **{'class': 'title-section'})
        title_h1 = soup.new_tag('h1')
        title_h1.string = f'[{context["stable_name"]}]'
        title_section.append(title_h1)

        # Metadata
        metadata_div = soup.new_tag('div', **{'class': 'metadata'})

        version_badge = soup.new_tag('span', **{'class': 'badge version-badge'})
        version_badge.string = f'{context["from_version"]} → {context["to_version"]}'
        metadata_div.append(version_badge)
        metadata_div.append(' ')

        size_badge = soup.new_tag('span', **{'class': 'badge size-badge'})
        size_kb = context.get('file_size_kb', 0)
        size_badge.string = f'{size_kb} KB'
        if size_kb > 100:
            size_badge['class'] = 'badge size-badge large'
        metadata_div.append(size_badge)

        if context.get('line_count', 0) > 0:
            metadata_div.append(' ')
            line_badge = soup.new_tag('span', **{'class': 'badge line-badge'})
            line_badge.string = f'{context["line_count"]} lines'
            metadata_div.append(line_badge)

        title_section.append(metadata_div)
        header.append(title_section)

        # Version timeline navigation
        timeline_nav = soup.new_tag('nav', **{'class': 'version-timeline'})
        timeline_label = soup.new_tag('span', **{'class': 'timeline-label'})
        timeline_label.string = 'Evolution Timeline: '
        timeline_nav.append(timeline_label)

        for i, (from_tag, to_tag, from_name, to_name, slug) in enumerate(VERSION_PAIRS):
            if i > 0:
                timeline_nav.append(' | ')

            timeline_link = soup.new_tag('a',
                href=f'../{slug}/{context["stable_name_file"]}.html',
                **{'class': 'active' if slug == context['version_slug'] else ''})
            timeline_link.string = f'{from_name}→{to_name}'
            timeline_nav.append(timeline_link)

        header.append(timeline_nav)

        # External links
        links_div = soup.new_tag('div', **{'class': 'external-links'})
        links_div.append('🔗 ')

        eelis_link = soup.new_tag('a',
            href=f'https://eel.is/c++draft/{context["stable_name"]}',
            target='_blank',
            rel='noopener noreferrer')
        eelis_link.string = 'Current Draft'
        links_div.append(eelis_link)
        links_div.append(' | ')

        github_link = soup.new_tag('a',
            href=f'https://github.com/cplusplus/draft',
            target='_blank',
            rel='noopener noreferrer')
        github_link.string = 'GitHub Source'
        links_div.append(github_link)

        header.append(links_div)

        # Large file warning
        if size_kb > 100:
            warning_div = soup.new_tag('div', **{'class': 'warning large-file-warning'})
            warning_div.string = f'⚠️ Large diff ({size_kb} KB) - rendering may be slow on some devices'
            header.append(warning_div)

        # Insert header at beginning of body
        if soup.body:
            soup.body.insert(0, header)

        # Add custom CSS link to head
        if soup.head:
            css_link = soup.new_tag('link',
                rel='stylesheet',
                href='../../css/custom.css')
            soup.head.append(css_link)

        # Write modified HTML
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(str(soup))

        return True

    except Exception as e:
        print(f"  Error injecting navigation: {e}")
        return False


def collect_stable_names(diff_dir: Path, tier: int = 1, limit: Optional[int] = None) -> List[Dict]:
    """Collect stable names from a diff directory.

    Args:
        diff_dir: Path to directory containing .diff files
        tier: Tier to filter (1 or 2)
        limit: Maximum number of diffs to collect (for testing)

    Returns:
        List of dicts with stable name info
    """
    stable_names = []

    if not diff_dir.exists():
        print(f"Warning: Directory not found: {diff_dir}")
        return stable_names

    diff_files = sorted(diff_dir.glob('*.diff'))

    for diff_file in diff_files:
        name = extract_stable_name(diff_file)

        if not name:
            # Fallback: use filename
            name = diff_file.stem

        if classify_stable_name(name) != tier:
            continue

        stable_names.append({
            'name': name,
            'size_kb': get_file_size_kb(diff_file),
            'line_count': count_diff_lines(diff_file),
            'file': diff_file.stem,
            'path': diff_file
        })

        if limit and len(stable_names) >= limit:
            break

    return stable_names


def generate_version_pair(from_tag: str, to_tag: str, from_name: str,
                         to_name: str, slug: str, output_path: Path,
                         env: Environment, tier: int = 1,
                         limit: Optional[int] = None) -> int:
    """Generate pages for one version pair.

    Args:
        from_tag: Starting version tag (e.g., 'n4950')
        to_tag: Ending version tag (e.g., 'trunk')
        from_name: Human-readable start version (e.g., 'C++23')
        to_name: Human-readable end version (e.g., 'C++26')
        slug: URL slug for this pair (e.g., 'cpp23-to-cpp26')
        output_path: Base output directory
        env: Jinja2 environment
        tier: Tier to filter (1 or 2)
        limit: Maximum number of diffs to process (for testing)

    Returns:
        Number of diffs successfully generated
    """
    print(f"\n📦 Processing {from_name} → {to_name}...")

    diff_dir = Path(f'diffs/{from_tag}_to_{to_tag}/by_stable_name')

    if not diff_dir.exists():
        print(f"  ⚠️  Directory not found: {diff_dir}")
        return 0

    # Collect Tier 1 stable names
    stable_names = collect_stable_names(diff_dir, tier=tier, limit=limit)

    print(f"  Found {len(stable_names)} Tier {tier} stable names")

    if not stable_names:
        return 0

    # Generate overview page
    template = env.get_template('version_overview.html')
    content = template.render(
        from_name=from_name,
        to_name=to_name,
        from_tag=from_tag,
        to_tag=to_tag,
        slug=slug,
        stable_names=stable_names,
        version_pairs=VERSION_PAIRS
    )

    version_dir = output_path / 'versions'
    version_dir.mkdir(exist_ok=True, parents=True)
    overview_file = version_dir / f'{slug}.html'
    overview_file.write_text(content, encoding='utf-8')
    print(f"  ✓ Generated overview: {overview_file}")

    # Generate individual diff pages
    diff_output_dir = output_path / 'diffs' / slug
    diff_output_dir.mkdir(parents=True, exist_ok=True)

    success_count = 0

    for i, item in enumerate(stable_names, 1):
        print(f"  [{i}/{len(stable_names)}] Processing [{item['name']}]...", end='')

        context = {
            'title': f'[{item["name"]}] - {from_name} → {to_name}',
            'stable_name': item['name'],
            'stable_name_file': item['file'],
            'from_version': from_name,
            'to_version': to_name,
            'from_tag': from_tag,
            'to_tag': to_tag,
            'version_slug': slug,
            'file_size_kb': item['size_kb'],
            'line_count': item['line_count']
        }

        output_file = diff_output_dir / f'{item["file"]}.html'

        # Generate HTML with diff2html
        if generate_diff_html(item['path'], output_file, context):
            # Inject custom navigation
            if inject_navigation(output_file, context):
                print(" ✓")
                success_count += 1
            else:
                print(" ⚠️ (navigation injection failed)")
        else:
            print(" ✗ (diff2html failed)")

    print(f"  ✓ Successfully generated {success_count}/{len(stable_names)} diffs")
    return success_count


def generate_landing_page(output_path: Path, env: Environment, stats: Dict):
    """Generate the landing page.

    Args:
        output_path: Base output directory
        env: Jinja2 environment
        stats: Dictionary with statistics about generated pages
    """
    print("\n📄 Generating landing page...")

    template = env.get_template('index.html')
    content = template.render(
        version_pairs=VERSION_PAIRS,
        stats=stats
    )

    index_file = output_path / 'index.html'
    index_file.write_text(content, encoding='utf-8')
    print(f"  ✓ Generated: {index_file}")


def copy_static_assets(output_path: Path):
    """Copy CSS and JS assets to output directory.

    Args:
        output_path: Base output directory
    """
    print("\n📁 Copying static assets...")

    # Create directories
    css_dir = output_path / 'css'
    js_dir = output_path / 'js'
    css_dir.mkdir(exist_ok=True, parents=True)
    js_dir.mkdir(exist_ok=True, parents=True)

    # Copy CSS if exists
    if Path('templates/css/custom.css').exists():
        shutil.copy('templates/css/custom.css', css_dir / 'custom.css')
        print(f"  ✓ Copied custom.css")

    # Copy JS if exists
    if Path('templates/js/navigation.js').exists():
        shutil.copy('templates/js/navigation.js', js_dir / 'navigation.js')
        print(f"  ✓ Copied navigation.js")

    # Create .nojekyll file to disable Jekyll processing
    nojekyll_file = output_path / '.nojekyll'
    nojekyll_file.touch()
    print(f"  ✓ Created .nojekyll")


def generate_site(output_dir: str = 'site', tier: int = 1,
                 limit: Optional[int] = None, test_mode: bool = False):
    """Main generation logic.

    Args:
        output_dir: Output directory for generated site
        tier: Tier to filter (1 or 2)
        limit: Maximum number of diffs per version pair (for testing)
        test_mode: If True, only process first version pair with limit=10
    """
    # Check dependencies
    check_dependencies()

    # Setup Jinja2 environment
    templates_dir = Path('templates')
    if not templates_dir.exists():
        print(f"Error: Templates directory not found: {templates_dir}")
        print("Please ensure templates/ directory exists with required templates.")
        sys.exit(1)

    env = Environment(loader=FileSystemLoader(str(templates_dir)))

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"🚀 C++ Standard Evolution Viewer - Site Generator")
    print(f"   Output directory: {output_path.absolute()}")
    print(f"   Tier: {tier} (0-{1 if tier == 1 else '2+'} dots)")
    if limit:
        print(f"   Limit: {limit} diffs per version pair")
    if test_mode:
        print(f"   Mode: TEST (first version pair, 10 diffs)")

    # Test mode: only process first version pair with small limit
    pairs_to_process = VERSION_PAIRS[:1] if test_mode else VERSION_PAIRS
    test_limit = 10 if test_mode else limit

    # Generate pages for each version pair
    stats = {
        'total_diffs': 0,
        'version_pairs': []
    }

    for from_tag, to_tag, from_name, to_name, slug in pairs_to_process:
        count = generate_version_pair(
            from_tag, to_tag, from_name, to_name, slug,
            output_path, env, tier=tier, limit=test_limit
        )

        stats['total_diffs'] += count
        stats['version_pairs'].append({
            'from_name': from_name,
            'to_name': to_name,
            'slug': slug,
            'count': count
        })

    # Generate landing page
    generate_landing_page(output_path, env, stats)

    # Copy static assets
    copy_static_assets(output_path)

    print(f"\n✅ Site generation complete!")
    print(f"   Total diffs generated: {stats['total_diffs']}")
    print(f"   Output directory: {output_path.absolute()}")
    print(f"\nTo view the site:")
    print(f"   cd {output_path}")
    print(f"   python3 -m http.server 8000")
    print(f"   Then open: http://localhost:8000")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Generate static HTML site for C++ standard evolution viewer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test mode: Generate 10 diffs from one version pair
  python3 generate_html_site.py --test

  # Generate full Tier 1 site (all 5 version pairs)
  python3 generate_html_site.py --output site/

  # Generate with limit (for debugging)
  python3 generate_html_site.py --output site/ --limit 50
        """
    )

    parser.add_argument('--output', '-o', default='site',
                       help='Output directory for generated site (default: site/)')
    parser.add_argument('--tier', type=int, default=1, choices=[1, 2],
                       help='Tier to generate: 1 (0-1 dots) or 2 (2+ dots) (default: 1)')
    parser.add_argument('--limit', type=int, metavar='N',
                       help='Limit number of diffs per version pair (for testing)')
    parser.add_argument('--test', action='store_true',
                       help='Test mode: only process first 10 diffs from one version pair')

    args = parser.parse_args()

    try:
        generate_site(
            output_dir=args.output,
            tier=args.tier,
            limit=args.limit,
            test_mode=args.test
        )
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
