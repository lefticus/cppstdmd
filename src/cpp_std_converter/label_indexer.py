"""
Label indexer for C++ standard cross-file references.

This module builds a mapping of section labels to their containing files,
enabling automatic conversion of cross-chapter references to proper relative links.
"""

import re
from pathlib import Path

from .stable_name import extract_stable_name_from_tex


class LabelIndexer:
    """Build and manage mappings of section labels to their containing files."""

    # Files to skip during indexing (not chapter files)
    SKIP_FILES = {
        "std",
        "layout",
        "macros",
        "config",
        "cover-reg",
        "cover-wd",
        "xrefdelta",
        "xrefindex",
        "front",
        "back",
        "tabbing-def",
    }

    def __init__(self, source_dir: Path):
        """
        Initialize the label indexer.

        Args:
            source_dir: Directory containing C++ standard .tex files
        """
        self.source_dir = Path(source_dir)
        self.label_to_file: dict[str, str] = {}
        self.file_labels: dict[str, set[str]] = {}
        self.duplicate_labels: dict[str, list] = {}

    def build_index(
        self, use_stable_names: bool = True, stable_name_map: dict[str, str] | None = None
    ) -> dict[str, str]:
        """
        Build label→filename mapping from LaTeX sources.

        Args:
            use_stable_names: If True, map to stable names (expr vs expressions)
            stable_name_map: Optional pre-computed mapping of tex_stem → stable_name
                           If provided, this is used instead of extracting stable names

        Returns:
            Dict mapping label → filename_stem
            Example: {"forward": "utilities", "declval": "utilities", ...}
        """
        # Step 1: Get stable name mapping
        if stable_name_map is None and use_stable_names:
            stable_name_map = self._extract_stable_names()
        elif stable_name_map is None:
            stable_name_map = {}

        # Step 2: Scan all files for labels
        for tex_file in self.source_dir.glob("*.tex"):
            if tex_file.stem in self.SKIP_FILES:
                continue

            # Get output filename (stable name or tex stem)
            output_name = stable_name_map.get(tex_file.stem, tex_file.stem)

            # Extract all labels from this file
            labels = self._extract_labels_from_file(tex_file)

            # Store in indices
            self.file_labels[output_name] = labels
            for label in labels:
                if label in self.label_to_file:
                    # Track duplicates
                    if label not in self.duplicate_labels:
                        self.duplicate_labels[label] = [self.label_to_file[label]]
                    self.duplicate_labels[label].append(output_name)
                else:
                    self.label_to_file[label] = output_name

        return self.label_to_file

    def _extract_stable_names(self) -> dict[str, str]:
        """
        Extract stable names for all chapters.

        Returns:
            Dict mapping tex_stem → stable_name
            Example: {"expressions": "expr", "statements": "stmt"}
        """
        stable_names = {}

        for tex_file in self.source_dir.glob("*.tex"):
            if tex_file.stem in self.SKIP_FILES:
                continue

            try:
                stable_name = extract_stable_name_from_tex(tex_file)
                if stable_name and stable_name != tex_file.stem:
                    stable_names[tex_file.stem] = stable_name
            except Exception:
                # If extraction fails, use filename as-is
                pass

        return stable_names

    def _extract_labels_from_file(self, tex_file: Path) -> set[str]:
        """
        Extract all section labels from a .tex file.

        Args:
            tex_file: Path to .tex file

        Returns:
            Set of section labels found in the file
        """
        labels = set()

        try:
            content = tex_file.read_text(encoding="utf-8", errors="ignore")

            # Find all \rSec patterns with labels
            # Matches: \rSec0[label], \rSec1[label], etc.
            for match in re.finditer(r"\\rSec\d+\[([^\]]+)\]", content):
                label = match.group(1)
                labels.add(label)

        except Exception as e:
            # Log error but continue
            import sys

            print(f"Warning: Error reading {tex_file}: {e}", file=sys.stderr)

        return labels

    def get_file_for_label(self, label: str) -> str | None:
        """
        Get the filename containing a label.

        Args:
            label: Section label to look up

        Returns:
            Filename stem containing the label, or None if not found
        """
        return self.label_to_file.get(label)

    def get_labels_for_file(self, filename: str) -> set[str]:
        """
        Get all labels defined in a file.

        Args:
            filename: Filename stem

        Returns:
            Set of labels defined in that file
        """
        return self.file_labels.get(filename, set())

    def write_lua_table(self, output_file: Path) -> None:
        """
        Write label index as Lua table file.

        Args:
            output_file: Path to write Lua table
        """
        with open(output_file, "w") as f:
            f.write("-- Auto-generated label→file mapping for C++ standard\n")
            f.write("-- Do not edit manually\n\n")
            f.write("return {\n")

            for label in sorted(self.label_to_file.keys()):
                file = self.label_to_file[label]
                # Escape special characters for Lua string
                escaped_label = label.replace("\\", "\\\\").replace('"', '\\"')
                escaped_file = file.replace("\\", "\\\\").replace('"', '\\"')
                f.write(f'  ["{escaped_label}"] = "{escaped_file}",\n')

            f.write("}\n")

    def get_statistics(self) -> dict[str, int]:
        """
        Get statistics about the index.

        Returns:
            Dict with counts of files, labels, duplicates
        """
        return {
            "files": len(self.file_labels),
            "labels": len(self.label_to_file),
            "duplicates": len(self.duplicate_labels),
        }
