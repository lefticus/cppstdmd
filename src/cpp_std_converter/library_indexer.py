#!/usr/bin/env python3
"""
library_indexer.py

Extract library entity index from C++ Standard LaTeX source files.
Maps library entities (types, functions, member functions) to their
defining sections for search functionality.
"""

import re
from collections import defaultdict
from pathlib import Path


class LibraryIndexer:
    """Extract library entity index from LaTeX source."""

    # Patterns for different index entry types
    # \indexlibraryglobal{name} - global functions/types
    # \indexlibrarymember{class}{member} - member functions
    # \indexlibraryctor{class} - constructors
    # \indexlibrarydtor{class} - destructors
    # \indexlibrary{\idxcode{name}...} - generic entries

    PATTERNS = [
        # Global entities: \indexlibraryglobal{name}
        (r"\\indexlibraryglobal\{([^}]+)\}", "global"),
        # Member functions: \indexlibrarymember{member}{class}
        (r"\\indexlibrarymember\{([^}]+)\}\{([^}]+)\}", "member"),
        # Constructors: \indexlibraryctor{class}
        (r"\\indexlibraryctor\{([^}]+)\}", "ctor"),
        # Destructors: \indexlibrarydtor{class}
        (r"\\indexlibrarydtor\{([^}]+)\}", "dtor"),
        # Generic with idxcode: \indexlibrary{\idxcode{name}...}
        (r"\\indexlibrary\{\\idxcode\{([^}]+)\}[^}]*\}", "code"),
        # Generic with idxhdr: \indexlibrary{\idxhdr{header}}
        (r"\\indexlibrary\{\\idxhdr\{([^}]+)\}\}", "header"),
        # Header index: \indexheader{header}
        (r"\\indexheader\{([^}]+)\}", "header"),
    ]

    # Pattern to find section labels: \rSecN[label] where N is 0-5
    SECTION_PATTERN = re.compile(r"\\rSec\d\[([^\]]+)\]")

    def __init__(self):
        self.compiled_patterns = [
            (re.compile(pattern), entry_type)
            for pattern, entry_type in self.PATTERNS
        ]

    def extract_from_file(
        self, tex_path: Path, chapter_name: str
    ) -> list[tuple[str, str, str]]:
        """Extract library entities from a tex file.

        Returns list of (entity_name, entity_type, section_label) tuples.
        """
        content = tex_path.read_text(encoding="utf-8", errors="replace")
        results = []

        # Find all section labels with their positions
        section_positions = []
        for match in self.SECTION_PATTERN.finditer(content):
            section_positions.append((match.start(), match.group(1)))

        # If no sections found, use chapter name as fallback
        if not section_positions:
            section_positions = [(0, chapter_name)]

        def get_section_at_pos(pos: int) -> str:
            """Find the section label that contains the given position."""
            current_section = chapter_name
            for sec_pos, sec_label in section_positions:
                if sec_pos <= pos:
                    current_section = sec_label
                else:
                    break
            return current_section

        # Extract all library entities
        for pattern, entry_type in self.compiled_patterns:
            for match in pattern.finditer(content):
                section = get_section_at_pos(match.start())

                if entry_type == "member":
                    # Format is \indexlibrarymember{member}{class}
                    member, class_name = match.group(1), match.group(2)
                    # Store both the member name and class::member
                    results.append((member, entry_type, section))  # member name
                    results.append((f"{class_name}::{member}", entry_type, section))  # class::member
                elif entry_type == "ctor":
                    class_name = match.group(1)
                    results.append((class_name, entry_type, section))
                    results.append((f"{class_name}::{class_name}", entry_type, section))
                elif entry_type == "dtor":
                    class_name = match.group(1)
                    results.append((f"~{class_name}", entry_type, section))
                    results.append((f"{class_name}::~{class_name}", entry_type, section))
                elif entry_type == "header":
                    header = match.group(1)
                    results.append((f"<{header}>", entry_type, section))
                    results.append((header, entry_type, section))
                else:
                    # Global or code entity
                    entity = match.group(1)
                    results.append((entity, entry_type, section))

        return results

    def build_index(self, source_dir: Path) -> dict[str, list[str]]:
        """Build entity -> [sections] mapping from all tex files.

        Args:
            source_dir: Path to directory containing .tex source files

        Returns:
            Dictionary mapping entity names to list of section labels
        """
        index: dict[str, set[str]] = defaultdict(set)

        # Process all tex files
        for tex_file in sorted(source_dir.glob("*.tex")):
            chapter_name = tex_file.stem
            entries = self.extract_from_file(tex_file, chapter_name)

            for entity, entry_type, section in entries:
                # Normalize entity name
                entity_normalized = entity.strip()
                if entity_normalized:
                    index[entity_normalized].add(section)

        # Convert sets to sorted lists
        return {
            entity: sorted(sections) for entity, sections in sorted(index.items())
        }


def main():
    """Test the library indexer."""
    import json
    import sys

    if len(sys.argv) < 2:
        print("Usage: library_indexer.py <source_dir>")
        sys.exit(1)

    source_dir = Path(sys.argv[1])
    if not source_dir.exists():
        print(f"Error: {source_dir} does not exist")
        sys.exit(1)

    indexer = LibraryIndexer()
    index = indexer.build_index(source_dir)

    print(f"Extracted {len(index)} unique entities")
    print("\nSample entries:")
    sample_entities = ["vector", "push_back", "endl", "cout", "sort", "find"]
    for entity in sample_entities:
        if entity in index:
            print(f"  {entity}: {index[entity]}")

    # Write full index to stdout if requested
    if "--json" in sys.argv:
        print("\n" + json.dumps(index, indent=2))


if __name__ == "__main__":
    main()
