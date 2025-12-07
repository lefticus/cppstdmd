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
generate_stable_name_files.py

Extract individual stable name sections from C++ standard markdown files
into separate files under build/<version>/<stable.name>.md

Usage:
    ./generate_stable_name_files.py                    # Process all versions
    ./generate_stable_name_files.py n4950             # Process specific version
    ./generate_stable_name_files.py --list            # List available versions
"""

import argparse
import sys
from pathlib import Path

from generate_diffs import VERSIONS, VERSION_ORDER, parse_stable_names
from src.cpp_std_converter.utils import ensure_dir


def extract_stable_names_for_version(version: str, output_base: Path) -> int:
    """
    Extract all stable name sections from a version's markdown files.

    Args:
        version: Version directory name (e.g., 'n4950')
        output_base: Base output directory (e.g., 'build')

    Returns:
        Number of files created
    """
    version_dir = Path(version)
    if not version_dir.exists():
        print(f"Error: Version directory not found: {version_dir}", file=sys.stderr)
        return 0

    output_dir = output_base / version
    ensure_dir(output_dir)

    version_name = VERSIONS.get(version, version)
    print(f"\nProcessing {version} ({version_name})...")

    # Collect all stable names from all chapter files
    all_sections = {}  # stable_name -> (chapter, content)

    chapter_files = sorted(version_dir.glob("*.md"))
    print(f"  Found {len(chapter_files)} chapter files")

    for chapter_file in chapter_files:
        chapter = chapter_file.stem
        sections = parse_stable_names(chapter_file)

        for stable_name, (content, start, end) in sections.items():
            all_sections[stable_name] = (chapter, content)

    print(f"  Found {len(all_sections)} stable name sections")

    # Write each section to its own file
    files_created = 0
    for stable_name, (chapter, content) in sorted(all_sections.items()):
        # Generate safe filename: stable.name -> stable.name.md
        # Replace any problematic characters
        safe_name = stable_name.replace("/", "_").replace("\\", "_")
        output_file = output_dir / f"{safe_name}.md"

        # Write content with metadata header
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)

        files_created += 1

    print(f"  Created {files_created} files in {output_dir}/")
    return files_created


def main():
    parser = argparse.ArgumentParser(
        description="Extract stable name sections into individual markdown files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ./generate_stable_name_files.py                    # Process all versions
  ./generate_stable_name_files.py n4950             # Process specific version
  ./generate_stable_name_files.py n3337 n4950       # Process multiple versions
  ./generate_stable_name_files.py --list            # List available versions

Output structure:
  build/sections/<version>/<stable.name>.md

For example:
  build/sections/n4950/array.md
  build/sections/n4950/class.copy.md
  build/sections/n4950/dcl.init.md
        """,
    )
    parser.add_argument(
        "versions",
        nargs="*",
        help="Versions to process (default: all known versions)",
    )
    parser.add_argument("--list", action="store_true", help="List available versions")
    parser.add_argument(
        "--output",
        "-o",
        default="build/sections",
        help="Output base directory (default: build/sections)",
    )

    args = parser.parse_args()

    if args.list:
        print("Available versions:")
        for version, name in VERSIONS.items():
            version_dir = Path(version)
            exists = "exists" if version_dir.exists() else "not found"
            print(f"  {version:8} - {name} ({exists})")
        return 0

    output_base = Path(args.output)

    # Determine which versions to process
    if args.versions:
        versions = args.versions
    else:
        # Process all versions that have directories
        versions = [v for v in VERSION_ORDER if Path(v).exists()]

    if not versions:
        print("No version directories found. Run ./setup-and-build.sh first.")
        return 1

    print(f"Processing {len(versions)} version(s)")
    print(f"Output directory: {output_base}")

    total_files = 0
    for version in versions:
        try:
            count = extract_stable_names_for_version(version, output_base)
            total_files += count
        except Exception as e:
            print(f"Error processing {version}: {e}", file=sys.stderr)
            continue

    print(f"\n{'=' * 50}")
    print(f"Total: {total_files} files created across {len(versions)} version(s)")
    print(f"Output: {output_base}/<version>/<stable.name>.md")
    print("\nStructure:")
    print("  build/")
    print("    sections/      # Stable name section files")
    print("    site/          # Generated HTML site")

    return 0


if __name__ == "__main__":
    sys.exit(main())
