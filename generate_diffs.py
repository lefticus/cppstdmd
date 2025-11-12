#!/usr/bin/env python3
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
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Set


# Version metadata (in chronological order)
VERSIONS = {
    'n3337': 'C++11',
    'n4140': 'C++14',
    'n4659': 'C++17',
    'n4861': 'C++20',
    'n4950': 'C++23',
    'trunk': 'C++26 (working draft)',
}

# Ordered list of version tags for generating pairs
VERSION_ORDER = ['n3337', 'n4140', 'n4659', 'n4861', 'n4950', 'trunk']


def generate_all_version_pairs() -> List[Tuple[str, str]]:
    """
    Generate all possible version pairs in chronological order.

    Returns pairs from older to newer versions.
    Example: (n3337, n4140), (n3337, n4659), ..., (n4950, trunk)
    """
    pairs = []
    for i, from_version in enumerate(VERSION_ORDER):
        for to_version in VERSION_ORDER[i + 1:]:
            pairs.append((from_version, to_version))
    return pairs


# Default: Generate all pairs (15 total)
DEFAULT_PAIRS = generate_all_version_pairs()


def find_common_chapters(from_version: str, to_version: str) -> Tuple[Set[str], Set[str], Set[str]]:
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

    from_chapters = {f.stem for f in from_dir.glob('*.md')}
    to_chapters = {f.stem for f in to_dir.glob('*.md')}

    common = from_chapters & to_chapters
    removed = from_chapters - to_chapters
    added = to_chapters - from_chapters

    return common, removed, added


def get_file_stats(file_path: Path) -> Dict[str, int]:
    """Get statistics for a markdown file."""
    if not file_path.exists():
        return {'size': 0, 'lines': 0}

    size = file_path.stat().st_size
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = sum(1 for _ in f)

    return {'size': size, 'lines': lines}


def format_size(bytes: int) -> str:
    """Format bytes as human-readable size."""
    for unit in ['B', 'KB', 'MB']:
        if bytes < 1024:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024
    return f"{bytes:.1f} GB"


def generate_chapter_diff(from_file: Path, to_file: Path, output_file: Path) -> bool:
    """
    Generate unified diff for a single chapter.

    Returns True if diff was generated successfully.
    """
    try:
        # Use git diff --no-index for better formatting
        result = subprocess.run(
            ['git', 'diff', '--no-index', '--unified=3', str(from_file), str(to_file)],
            capture_output=True,
            text=True,
            timeout=60
        )

        # git diff returns 1 when files differ (this is expected)
        if result.returncode not in [0, 1]:
            print(f"Warning: git diff failed for {from_file.stem}", file=sys.stderr)
            return False

        # Write diff output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result.stdout)

        return True

    except Exception as e:
        print(f"Error generating diff for {from_file.stem}: {e}", file=sys.stderr)
        return False


def generate_full_diff(from_version: str, to_version: str, output_file: Path) -> bool:
    """Generate diff for full standard files."""
    from_file = Path('full') / f'{from_version}.md'
    to_file = Path('full') / f'{to_version}.md'

    if not from_file.exists():
        print(f"Warning: Full file not found: {from_file}", file=sys.stderr)
        return False
    if not to_file.exists():
        print(f"Warning: Full file not found: {to_file}", file=sys.stderr)
        return False

    return generate_chapter_diff(from_file, to_file, output_file)


def generate_summary(from_version: str, to_version: str, diff_dir: Path,
                     common: Set[str], removed: Set[str], added: Set[str]) -> str:
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
            size_str = format_size(stats['size'])
            lines.append(f"- **{chapter}.md** ({size_str}, {stats['lines']:,} lines)")

            # Try to infer what the chapter is about from first heading
            try:
                with open(to_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.startswith('# '):
                            title = line[2:].strip()
                            lines.append(f"  - {title}")
                            break
            except:
                pass
        lines.append("")

    # Removed chapters
    if removed:
        lines.append("## Removed Chapters\n")
        for chapter in sorted(removed):
            from_file = Path(from_version) / f"{chapter}.md"
            stats = get_file_stats(from_file)
            size_str = format_size(stats['size'])
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

        size_change = to_stats['size'] - from_stats['size']
        size_pct = ((to_stats['size'] / from_stats['size'] - 1) * 100) if from_stats['size'] > 0 else 0
        line_change = to_stats['lines'] - from_stats['lines']
        line_pct = ((to_stats['lines'] / from_stats['lines'] - 1) * 100) if from_stats['lines'] > 0 else 0

        # Format changes
        size_change_str = f"+{format_size(size_change)}" if size_change >= 0 else format_size(size_change)
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

    # Full standard comparison
    lines.append("## Full Standard Comparison\n")
    lines.append(f"- [View complete diff](full_standard.diff) (all chapters concatenated)")
    lines.append(f"- Note: This file may be large and is best viewed locally\n")

    # Usage instructions
    lines.append("## How to Use These Diffs\n")
    lines.append("**On GitHub:**")
    lines.append("- Click any chapter link above to view the diff on GitHub")
    lines.append("- Per-chapter diffs render well in GitHub's web interface\n")
    lines.append("**Locally:**")
    lines.append("```bash")
    lines.append(f"# View specific chapter diff")
    lines.append(f"git diff --no-index {from_version}/class.md {to_version}/class.md")
    lines.append("")
    lines.append(f"# View with side-by-side comparison")
    lines.append(f"diff -y {from_version}/class.md {to_version}/class.md | less")
    lines.append("")
    lines.append(f"# View full standard diff")
    lines.append(f"less diffs/{from_version}_to_{to_version}/full_standard.diff")
    lines.append("```\n")

    return '\n'.join(lines)


def generate_diff_pair(from_version: str, to_version: str, output_base: Path) -> None:
    """Generate all diffs for a version pair."""
    from_name = VERSIONS.get(from_version, from_version)
    to_name = VERSIONS.get(to_version, to_version)

    print(f"\nGenerating diffs: {from_name} → {to_name}")
    print(f"  Output directory: {output_base}")

    # Create output directory
    output_base.mkdir(parents=True, exist_ok=True)

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
        print(f"  Generated full standard diff")
    else:
        print(f"  Warning: Could not generate full standard diff")

    # Generate summary
    print("  Generating summary...")
    summary_file = output_base / "README.md"
    summary_content = generate_summary(from_version, to_version, output_base,
                                      common, removed, added)
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_content)

    print(f"✓ Completed: {from_name} → {to_name}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate diffs between C++ standard versions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ./generate_diffs.py                    # Generate all 15 version pairs
  ./generate_diffs.py n3337 n4950       # Generate specific version pair
  ./generate_diffs.py --list            # List available versions

By default, generates all possible pairs (15 total):
  - Adjacent versions: C++11→C++14, C++14→C++17, etc.
  - Intermediate spans: C++11→C++17, C++14→C++20, etc.
  - Major evolution: C++11→C++23, C++17→C++26, etc.
        """
    )
    parser.add_argument('from_version', nargs='?', help='Source version (e.g., n3337)')
    parser.add_argument('to_version', nargs='?', help='Target version (e.g., n4950)')
    parser.add_argument('--list', action='store_true', help='List available versions')
    parser.add_argument('--output', '-o', default='diffs', help='Output directory (default: diffs)')

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
            generate_diff_pair(from_v, to_v, output_dir)
        except Exception as e:
            print(f"Error generating diff pair {from_v} → {to_v}: {e}", file=sys.stderr)
            continue

    print(f"\n✓ All diffs generated in {output_root}/")
    print(f"\nView summaries:")
    for from_v, to_v in pairs:
        print(f"  {output_root}/{from_v}_to_{to_v}/README.md")

    return 0


if __name__ == '__main__':
    sys.exit(main())
