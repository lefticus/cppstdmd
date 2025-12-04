#!/usr/bin/env python3
"""
generate_adventure_data.py

Generate game data for the C++ Standard Adventure Game.

This script extracts sections from markdown files and generates JSON data files
for the adventure game: world map, NPCs, items, quests, and puzzles.

Uses the existing LabelIndexer for extracting label→chapter mappings from
the LaTeX source, ensuring consistency with the main conversion pipeline.

Usage:
    python3 generate_adventure_data.py [--output DIR] [--versions DIR...]
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

import yaml

# Add src to path so we can import from cpp_std_converter
sys.path.insert(0, str(Path(__file__).parent / "src"))

from cpp_std_converter.utils import iter_section_headings

try:
    from cpp_std_converter.label_indexer import LabelIndexer

    HAS_LABEL_INDEXER = True
except ImportError:
    HAS_LABEL_INDEXER = False

# Realm theming - maps stable name prefix to (display_name, description, theme)
REALM_THEMES: dict[str, tuple[str, str, str]] = {
    "intro": ("The Grand Entrance", "Where all journeys through the Standard begin", "welcoming"),
    "lex": ("Lexicon Tower", "A tall library of lexical knowledge and tokens", "scholarly"),
    "basic": ("The Foundations", "Ancient temple ruins inscribed with fundamental laws", "ancient"),
    "expr": (
        "Expression Fields",
        "Open testing grounds for expressions and operators",
        "experimental",
    ),
    "stmt": ("Statement Sanctum", "Control flow chambers with branching paths", "labyrinthine"),
    "dcl": ("Declaration Domain", "Bureaucratic halls of formal declarations", "governmental"),
    "class": ("Class Citadel", "Medieval castle with towers of inheritance", "medieval"),
    "over": ("Overload Observatory", "Where function signatures are matched", "observatory"),
    "temp": ("Template Tundra", "Frozen crystalline structures of abstract patterns", "arctic"),
    "except": ("Exception Caverns", "Underground tunnels with try-catch bridges", "subterranean"),
    "cpp": ("Preprocessor Catacombs", "Ancient tunnels of macro magic", "underground"),
    "module": ("Module Mountains", "Modern peaks of code organization", "mountainous"),
    "concepts": ("Concept Cathedral", "Grand cathedral of constraints and requirements", "gothic"),
    "library": ("The Standard Library", "Grand entrance hall to the library realms", "grand"),
    "support": ("Support Chambers", "Foundation utilities and type support", "utility"),
    "concepts.lib": ("Library Concepts Hall", "Where library concepts are defined", "academic"),
    "diagnostics": ("Diagnostics Den", "Where errors and exceptions are catalogued", "medical"),
    "mem": ("Memory Depths", "Deep caverns of memory management", "cavernous"),
    "utilities": ("Utility Workshop", "Inventor's workshop with tools", "workshop"),
    "strings": ("String Springs", "Flowing waters of text manipulation", "aquatic"),
    "containers": ("Container Harbor", "Docks with different container ships", "nautical"),
    "iterators": ("Iterator Isle", "Bridge-connected islands of traversal", "archipelago"),
    "ranges": ("Range Frontier", "New frontier territory of composable views", "frontier"),
    "algorithms": ("Algorithm Academy", "Training grounds for algorithmic arts", "athletic"),
    "numerics": ("Numerics Nexus", "Mathematical computation center", "mathematical"),
    "time": ("Chrono Clocktower", "Giant clockwork tower of time utilities", "clockwork"),
    "locales": ("Locale Lands", "International territories of localization", "international"),
    "input": ("Input Streams", "Rivers flowing into the program", "riverside"),
    "output": ("Output Streams", "Rivers flowing out to the world", "riverside"),
    "re": ("Regex Realm", "Pattern matching territories", "mystical"),
    "atomics": ("Atomic Arenas", "Where indivisible operations occur", "futuristic"),
    "thread": ("Thread Nexus", "Multi-dimensional concurrent hub", "futuristic"),
    "exec": ("Execution Engine", "Where senders and receivers connect", "mechanical"),
}

# Era mappings
ERA_NAMES: dict[str, str] = {
    "n3337": "C++11",
    "n4140": "C++14",
    "n4659": "C++17",
    "n4861": "C++20",
    "n4950": "C++23",
    "trunk": "C++26",
}


def get_label_to_chapter_from_latex(cplusplus_draft_dir: Path) -> dict[str, str]:
    """
    Use LabelIndexer to get the authoritative label→chapter mapping from LaTeX source.

    Args:
        cplusplus_draft_dir: Path to the cplusplus-draft repository

    Returns:
        Dict mapping stable name → chapter name (e.g., "class.copy" → "class")
    """
    if not HAS_LABEL_INDEXER:
        return {}

    source_dir = cplusplus_draft_dir / "source"
    if not source_dir.exists():
        return {}

    try:
        indexer = LabelIndexer(source_dir)
        indexer.build_index(use_stable_names=True)
        return indexer.label_to_file
    except Exception as e:
        print(f"Warning: Failed to use LabelIndexer: {e}")
        return {}


def extract_sections_from_markdown(
    md_dir: Path, label_to_chapter: dict[str, str] | None = None
) -> dict[str, dict[str, Any]]:
    """Extract all sections with metadata from markdown files.

    Uses the centralized iter_section_headings() from utils.py to correctly
    handle titles containing < characters (like `<initializer_list>`).
    """
    sections: dict[str, dict[str, Any]] = {}

    for md_file in sorted(md_dir.glob("*.md")):
        chapter = md_file.stem
        content = md_file.read_text(encoding="utf-8")

        # Use centralized heading parser from utils.py
        headings = list(iter_section_headings(content))

        for i, heading in enumerate(headings):
            # Extract section content (up to next section)
            section_start = heading.match_end
            if i + 1 < len(headings):
                section_end = headings[i + 1].match_start
            else:
                section_end = len(content)

            section_content = content[section_start:section_end]

            # Find cross-references in content
            cross_refs = list(set(re.findall(r"\[\[([^\]]+)\]\]", section_content)))

            # Use LabelIndexer mapping if available, fallback to current file
            actual_chapter = chapter
            if label_to_chapter and heading.stable_name in label_to_chapter:
                actual_chapter = label_to_chapter[heading.stable_name]

            sections[heading.stable_name] = {
                "chapter": actual_chapter,
                "title": heading.title,
                "stableName": heading.stable_name,
                "headingLevel": heading.level,
                "crossReferences": cross_refs,
                "contentLength": len(section_content),
            }

    return sections


def infer_hierarchy(sections: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Infer parent-child relationships from stable names."""
    for stable_name, data in sections.items():
        parts = stable_name.split(".")

        # Parent is the stable name with one fewer part
        if len(parts) > 1:
            potential_parent = ".".join(parts[:-1])
            if potential_parent in sections:
                data["parent"] = potential_parent
            else:
                data["parent"] = parts[0] if parts[0] in sections else None
        else:
            data["parent"] = None

        # Children are sections that have this as their parent
        data["children"] = [name for name, d in sections.items() if d.get("parent") == stable_name]

    return sections


def generate_connections(sections: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Generate north/south/east/west connections between sections."""
    # Group sections by chapter
    by_chapter: dict[str, list[str]] = {}
    for name, data in sections.items():
        chapter = data["chapter"]
        if chapter not in by_chapter:
            by_chapter[chapter] = []
        by_chapter[chapter].append(name)

    # Within each chapter, sections connect sequentially (north/south)
    for name, data in sections.items():
        chapter_sections = by_chapter[data["chapter"]]
        try:
            idx = chapter_sections.index(name)
        except ValueError:
            idx = -1

        data["connections"] = {
            "north": chapter_sections[idx - 1] if idx > 0 else None,
            "south": chapter_sections[idx + 1] if idx < len(chapter_sections) - 1 else None,
            "east": None,
            "west": None,
        }

        # Cross-references become east/west connections (first 2)
        for ref in data.get("crossReferences", [])[:2]:
            if ref in sections and ref != name:
                if data["connections"]["east"] is None:
                    data["connections"]["east"] = ref
                elif data["connections"]["west"] is None:
                    data["connections"]["west"] = ref

    return sections


def get_realm_info(stable_name: str) -> tuple[str, str, str]:
    """Get realm display name, description, and theme for a stable name."""
    parts = stable_name.split(".")
    realm_key = parts[0]

    # Try increasingly specific prefixes
    for i in range(len(parts), 0, -1):
        prefix = ".".join(parts[:i])
        if prefix in REALM_THEMES:
            return REALM_THEMES[prefix]

    # Fallback
    if realm_key in REALM_THEMES:
        return REALM_THEMES[realm_key]

    return (realm_key.title(), f"The {realm_key} area", "default")


def generate_display_name(title: str, stable_name: str) -> str:
    """Generate a thematic display name for a section."""
    # Map common terms to thematic alternatives
    theme_map = {
        "general": "Main Hall",
        "overview": "Observation Deck",
        "introduction": "Welcome Chamber",
        "preamble": "Entry Hall",
        "requirements": "Standards Hall",
        "constructors": "Constructor Forge",
        "destructor": "Destructor Crypt",
        "members": "Member Hall",
        "copy": "Duplication Chamber",
        "move": "Transfer Station",
        "assignment": "Assignment Alcove",
        "virtual": "Phantom Tower",
        "derived": "Inheritance Gates",
        "access": "Access Control",
        "special": "Special Functions Chamber",
        "operators": "Operator Arena",
        "declarations": "Declaration Hall",
        "definitions": "Definition Chamber",
        "scope": "Scope Tower",
        "lookup": "Lookup Library",
        "templates": "Template Workshop",
        "concepts": "Concept Shrine",
        "constraints": "Constraint Chamber",
    }

    title_lower = title.lower()
    for key, value in theme_map.items():
        if key in title_lower:
            return value

    # Default: use title directly
    return title


def detect_era_availability(stable_name: str, version_dirs: list[Path]) -> list[str]:
    """Detect which C++ versions contain this section."""
    available = []
    for version_dir in version_dirs:
        if not version_dir.exists():
            continue
        # Check if any markdown file in this version contains the stable name
        for md_file in version_dir.glob("*.md"):
            content = md_file.read_text(encoding="utf-8")
            if f'id="{stable_name}"' in content:
                available.append(version_dir.name)
                break
    return available


def generate_world_map(
    primary_version_dir: Path,
    all_version_dirs: list[Path],
    cplusplus_draft_dir: Path | None = None,
) -> dict[str, Any]:
    """Generate the complete world map from markdown content."""
    # Get authoritative label→chapter mapping from LaTeX source if available
    label_to_chapter: dict[str, str] = {}
    if cplusplus_draft_dir:
        label_to_chapter = get_label_to_chapter_from_latex(cplusplus_draft_dir)
        if label_to_chapter:
            print(f"  Using LabelIndexer: {len(label_to_chapter)} labels mapped")

    sections = extract_sections_from_markdown(primary_version_dir, label_to_chapter)
    sections = infer_hierarchy(sections)
    sections = generate_connections(sections)

    world_map: dict[str, Any] = {
        "version": "1.0.0",
        "primaryEra": primary_version_dir.name,
        "eras": ERA_NAMES,
        "realms": {},
        "sections": {},
    }

    for stable_name, data in sections.items():
        realm_key = stable_name.split(".")[0]

        # Initialize realm if needed
        if realm_key not in world_map["realms"]:
            realm_name, realm_desc, realm_theme = get_realm_info(realm_key)
            world_map["realms"][realm_key] = {
                "name": realm_name,
                "description": realm_desc,
                "theme": realm_theme,
                "sections": [],
            }

        world_map["realms"][realm_key]["sections"].append(stable_name)

        # Build section entry
        world_map["sections"][stable_name] = {
            "stableName": stable_name,
            "displayName": generate_display_name(data["title"], stable_name),
            "title": data["title"],
            "realm": realm_key,
            "chapter": data["chapter"],
            "parent": data.get("parent"),
            "children": data.get("children", []),
            "connections": data.get("connections", {}),
            "availableIn": detect_era_availability(stable_name, all_version_dirs),
            "description": f"Section covering {data['title'].lower()}.",
            "npcs": [],
            "items": [],
            "puzzles": [],
        }

    return world_map


def load_yaml_content(game_content_dir: Path) -> dict[str, Any]:
    """Load hand-crafted content from YAML files if they exist."""
    content: dict[str, Any] = {
        "npcs": [],
        "quests": [],
        "items": [],
        "puzzles": [],
        "realms": {},
    }

    if not game_content_dir.exists():
        return content

    # Load NPCs
    npcs_dir = game_content_dir / "npcs"
    if npcs_dir.exists():
        for yaml_file in npcs_dir.glob("*.yaml"):
            try:
                data = yaml.safe_load(yaml_file.read_text())
                if data and "npcs" in data:
                    content["npcs"].extend(data["npcs"])
            except Exception as e:
                print(f"Warning: Failed to load {yaml_file}: {e}")

    # Load quests
    quests_dir = game_content_dir / "quests"
    if quests_dir.exists():
        for yaml_file in quests_dir.rglob("*.yaml"):
            try:
                data = yaml.safe_load(yaml_file.read_text())
                if data and "id" in data:
                    content["quests"].append(data)
            except Exception as e:
                print(f"Warning: Failed to load {yaml_file}: {e}")

    # Load items
    items_dir = game_content_dir / "items"
    if items_dir.exists():
        for yaml_file in items_dir.glob("*.yaml"):
            try:
                data = yaml.safe_load(yaml_file.read_text())
                if data and "items" in data:
                    content["items"].extend(data["items"])
            except Exception as e:
                print(f"Warning: Failed to load {yaml_file}: {e}")

    # Load puzzles
    puzzles_dir = game_content_dir / "puzzles"
    if puzzles_dir.exists():
        for yaml_file in puzzles_dir.rglob("*.yaml"):
            try:
                data = yaml.safe_load(yaml_file.read_text())
                if data and "id" in data:
                    content["puzzles"].append(data)
            except Exception as e:
                print(f"Warning: Failed to load {yaml_file}: {e}")

    # Load realm overrides
    realms_file = game_content_dir / "realms.yaml"
    if realms_file.exists():
        try:
            data = yaml.safe_load(realms_file.read_text())
            if data and "realms" in data:
                content["realms"] = data["realms"]
        except Exception as e:
            print(f"Warning: Failed to load {realms_file}: {e}")

    return content


def merge_content(world_map: dict[str, Any], yaml_content: dict[str, Any]) -> dict[str, Any]:
    """Merge hand-crafted YAML content into the world map."""
    # Override realm info from YAML
    for realm_key, realm_data in yaml_content.get("realms", {}).items():
        if realm_key in world_map["realms"]:
            world_map["realms"][realm_key].update(realm_data)

    # Add NPCs to their locations
    for npc in yaml_content.get("npcs", []):
        npc_id = npc.get("id")
        locations = npc.get("locations", [])
        for loc in locations:
            if loc == "*":
                # NPC appears everywhere - handled by game client
                continue
            if loc in world_map["sections"]:
                if npc_id not in world_map["sections"][loc]["npcs"]:
                    world_map["sections"][loc]["npcs"].append(npc_id)

    # Add items to their source sections
    for item in yaml_content.get("items", []):
        source = item.get("sourceSection")
        if source and source in world_map["sections"]:
            item_id = item.get("id")
            if item_id not in world_map["sections"][source]["items"]:
                world_map["sections"][source]["items"].append(item_id)

    # Add puzzles to their locations
    for puzzle in yaml_content.get("puzzles", []):
        location = puzzle.get("location")
        if location and location in world_map["sections"]:
            puzzle_id = puzzle.get("id")
            if puzzle_id not in world_map["sections"][location]["puzzles"]:
                world_map["sections"][location]["puzzles"].append(puzzle_id)

    return world_map


def copy_source_files(source_dir: Path, output_dir: Path) -> None:
    """Copy adventure game source files to output directory."""
    if not source_dir.exists():
        print(f"  Warning: Source directory not found: {source_dir}")
        return

    # Copy HTML
    html_src = source_dir / "index.html"
    if html_src.exists():
        html_dst = output_dir / "adventure"
        html_dst.mkdir(parents=True, exist_ok=True)
        shutil.copy2(html_src, html_dst / "index.html")

    # Copy JavaScript
    js_src = source_dir / "js"
    if js_src.exists():
        js_dst = output_dir / "js" / "adventure"
        js_dst.mkdir(parents=True, exist_ok=True)
        for js_file in js_src.glob("*.js"):
            shutil.copy2(js_file, js_dst / js_file.name)

    # Copy CSS
    css_src = source_dir / "css"
    if css_src.exists():
        css_dst = output_dir / "css"
        css_dst.mkdir(parents=True, exist_ok=True)
        for css_file in css_src.glob("*.css"):
            shutil.copy2(css_file, css_dst / css_file.name)


def generate_adventure_data(
    output_dir: Path,
    primary_version: str = "n4950",
    versions: list[str] | None = None,
    game_content_dir: Path | None = None,
) -> None:
    """Main entry point: generate all adventure game data files."""
    game_data_dir = output_dir / "data" / "game"
    game_data_dir.mkdir(parents=True, exist_ok=True)

    # Determine version directories
    base_dir = Path(__file__).parent
    if versions is None:
        versions = ["n3337", "n4140", "n4659", "n4861", "n4950", "trunk"]

    version_dirs = [base_dir / v for v in versions]
    primary_dir = base_dir / primary_version

    if not primary_dir.exists():
        print(f"Error: Primary version directory not found: {primary_dir}")
        sys.exit(1)

    # Find cplusplus-draft directory for LabelIndexer
    cplusplus_draft_dir = base_dir / "cplusplus-draft"
    if not cplusplus_draft_dir.exists():
        cplusplus_draft_dir = None

    print("Generating adventure game data...")
    print(f"  Primary version: {primary_version}")
    print(f"  Output directory: {game_data_dir}")
    if cplusplus_draft_dir:
        print(f"  LaTeX source: {cplusplus_draft_dir}")

    # Generate world map
    world_map = generate_world_map(primary_dir, version_dirs, cplusplus_draft_dir)
    print(f"  Extracted {len(world_map['sections'])} sections from markdown")

    # Load hand-crafted YAML content
    if game_content_dir is None:
        # Try default locations
        for candidate in [
            base_dir / "game-content",
            base_dir / "docs" / "adventure-game-design" / "game-content-examples",
        ]:
            if candidate.exists():
                game_content_dir = candidate
                break

    yaml_content: dict[str, Any] = {
        "npcs": [],
        "quests": [],
        "items": [],
        "puzzles": [],
        "realms": {},
    }
    if game_content_dir and game_content_dir.exists():
        yaml_content = load_yaml_content(game_content_dir)
        print(f"  Loaded YAML content from: {game_content_dir}")
        print(f"    NPCs: {len(yaml_content['npcs'])}")
        print(f"    Quests: {len(yaml_content['quests'])}")
        print(f"    Items: {len(yaml_content['items'])}")
        print(f"    Puzzles: {len(yaml_content['puzzles'])}")

    # Merge content
    world_map = merge_content(world_map, yaml_content)

    # Write output files
    with open(game_data_dir / "world-map.json", "w") as f:
        json.dump(world_map, f, indent=2)
    print(f"  Generated world-map.json ({len(world_map['sections'])} sections)")

    with open(game_data_dir / "npcs.json", "w") as f:
        json.dump(yaml_content["npcs"], f, indent=2)
    print(f"  Generated npcs.json ({len(yaml_content['npcs'])} NPCs)")

    with open(game_data_dir / "items.json", "w") as f:
        json.dump(yaml_content["items"], f, indent=2)
    print(f"  Generated items.json ({len(yaml_content['items'])} items)")

    with open(game_data_dir / "quests.json", "w") as f:
        json.dump(yaml_content["quests"], f, indent=2)
    print(f"  Generated quests.json ({len(yaml_content['quests'])} quests)")

    with open(game_data_dir / "puzzles.json", "w") as f:
        json.dump(yaml_content["puzzles"], f, indent=2)
    print(f"  Generated puzzles.json ({len(yaml_content['puzzles'])} puzzles)")

    # Copy source files (HTML, JS, CSS) from adventure-src to output
    adventure_src_dir = base_dir / "adventure-src"
    if adventure_src_dir.exists():
        copy_source_files(adventure_src_dir, output_dir)
        print(f"  Copied source files from {adventure_src_dir}")

    print("\nAdventure game data generation complete!")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate adventure game data from C++ standard markdown",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="site",
        help="Output directory (default: site/)",
    )
    parser.add_argument(
        "--primary",
        "-p",
        default="n4950",
        help="Primary C++ version to use (default: n4950)",
    )
    parser.add_argument(
        "--game-content",
        type=Path,
        help="Path to game-content YAML directory",
    )

    args = parser.parse_args()

    try:
        generate_adventure_data(
            output_dir=Path(args.output),
            primary_version=args.primary,
            game_content_dir=args.game_content,
        )
    except KeyboardInterrupt:
        print("\n\nGeneration interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
