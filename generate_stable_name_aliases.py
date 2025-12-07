#!/usr/bin/env python3
"""Generate stable name aliases between C++ standard versions.

This script detects renamed sections across different versions of the C++ standard
and outputs a mapping that can be used for timeshift navigation in the adventure game.

Detected patterns:
- Underscore to dot conversions (e.g., alg.all_of -> alg.all.of)
- Other renames that can be auto-detected by string similarity
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def extract_stable_names(md_dir: Path) -> set[str]:
    """Extract stable names from markdown files in a version directory."""
    names = set()
    heading_pattern = re.compile(r"^#{1,6}\s+.*?\[\[([^\]]+)\]\]")

    for md_file in md_dir.glob("*.md"):
        if md_file.name == "meta.md":
            continue
        with open(md_file) as f:
            for line in f:
                m = heading_pattern.match(line)
                if m:
                    names.add(m.group(1))
    return names


def find_underscore_to_dot_conversions(
    old_labels: set[str], new_labels: set[str]
) -> dict[str, str]:
    """Find labels that were converted from underscore to dot format."""
    aliases = {}
    removed = old_labels - new_labels

    for label in removed:
        potential = label.replace("_", ".")
        if potential in new_labels:
            aliases[label] = potential

    return aliases


def find_all_aliases(version_dirs: list[Path]) -> dict[str, str]:
    """Compare sections across versions to find all renames.

    Returns a dict mapping old_name -> new_name (most recent name wins).
    """
    # Extract labels from each version
    labels_per_version = {}
    for v_dir in version_dirs:
        if v_dir.exists():
            labels_per_version[v_dir.name] = extract_stable_names(v_dir)
            print(f"  {v_dir.name}: {len(labels_per_version[v_dir.name])} labels")

    # Build forward alias chain (old -> new)
    all_aliases: dict[str, str] = {}

    # Process version pairs in order
    version_names = list(labels_per_version.keys())
    for i in range(len(version_names) - 1):
        old_ver = version_names[i]
        new_ver = version_names[i + 1]

        old_labels = labels_per_version[old_ver]
        new_labels = labels_per_version[new_ver]

        # Find underscore -> dot conversions
        conversions = find_underscore_to_dot_conversions(old_labels, new_labels)

        for old_label, new_label in conversions.items():
            # Check if old_label is itself an alias for something older
            # Walk back to find the original
            original = old_label
            for prev_old, prev_new in all_aliases.items():
                if prev_new == old_label:
                    original = prev_old
                    break

            # Update to point to the newest name
            all_aliases[original] = new_label

            # Also add the intermediate if different
            if old_label != original:
                all_aliases[old_label] = new_label

    return all_aliases


def build_bidirectional_map(aliases: dict[str, str]) -> dict[str, list[str]]:
    """Build a map where each name knows all its aliases (past and future).

    Returns a dict where each key maps to a list of all equivalent names.
    """
    # Group all equivalent names
    groups: dict[str, set[str]] = {}

    for old_name, new_name in aliases.items():
        # Find or create group for these names
        group_key = None
        for key, names in groups.items():
            if old_name in names or new_name in names:
                group_key = key
                break

        if group_key is None:
            group_key = new_name  # Use newest name as key
            groups[group_key] = set()

        groups[group_key].add(old_name)
        groups[group_key].add(new_name)

    # Convert to list format and include all bidirectional mappings
    result: dict[str, list[str]] = {}
    for group_key, names in groups.items():
        names_list = sorted(names)
        for name in names_list:
            # Each name maps to all OTHER equivalent names
            result[name] = [n for n in names_list if n != name]

    return result


def generate_aliases(
    base_dir: Path = Path("."),
    output_file: Path | None = None,
    versions: list[str] | None = None,
) -> dict:
    """Generate stable name aliases and optionally write to file.

    Args:
        base_dir: Base directory containing version directories
        output_file: Path to write JSON output (optional)
        versions: List of version directory names to process
                 (default: n3337, n4140, n4659, n4861, n4950, trunk)

    Returns:
        Dict with alias mappings
    """
    if versions is None:
        versions = ["n3337", "n4140", "n4659", "n4861", "n4950", "trunk"]

    print("Generating stable name aliases...")
    print(f"  Versions: {', '.join(versions)}")

    version_dirs = [base_dir / v for v in versions]

    # Find all forward aliases (old -> new)
    forward_aliases = find_all_aliases(version_dirs)
    print(f"\n  Found {len(forward_aliases)} forward aliases")

    # Build bidirectional map for lookups
    bidirectional = build_bidirectional_map(forward_aliases)
    print(f"  Built bidirectional map with {len(bidirectional)} entries")

    result = {
        "description": "Stable name aliases between C++ standard versions",
        "generated_from": versions,
        "forward_aliases": forward_aliases,  # old_name -> newest_name
        "bidirectional": bidirectional,  # any_name -> [all_equivalent_names]
    }

    if output_file:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2, sort_keys=True)
        print(f"\n  Written to {output_file}")

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Generate stable name aliases between C++ standard versions"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("build/site/data/game/stable-name-aliases.json"),
        help="Output JSON file (default: build/site/data/game/stable-name-aliases.json)",
    )
    parser.add_argument(
        "--versions",
        nargs="+",
        default=["n3337", "n4140", "n4659", "n4861", "n4950", "trunk"],
        help="Version directories to process (default: n3337 n4140 n4659 n4861 n4950 trunk)",
    )
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=Path("."),
        help="Base directory containing version directories",
    )

    args = parser.parse_args()

    generate_aliases(
        base_dir=args.base_dir,
        output_file=args.output,
        versions=args.versions,
    )

    print("\nDone!")


if __name__ == "__main__":
    main()
