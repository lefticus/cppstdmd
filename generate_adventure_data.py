#!/usr/bin/env python3
"""
generate_adventure_data.py

Generate game data for the C++ Standard Adventure Game.

This script extracts sections from markdown files and generates JSON data files
for the adventure game: world map, NPCs, items, quests, and puzzles.

Uses the cpp_std_labels.lua file generated during markdown conversion to get
the correct label→chapter mappings (stable names to markdown file stems).

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


def load_label_to_chapter_from_lua(md_dir: Path) -> dict[str, str]:
    """
    Load the label→chapter mapping from cpp_std_labels.lua in the markdown directory.

    This file is generated during markdown conversion and contains the correct
    mapping of stable names to markdown file stems (not LaTeX filenames).

    Args:
        md_dir: Path to the markdown output directory (e.g., n4950/)

    Returns:
        Dict mapping stable name → markdown file stem (e.g., "dcl.dcl" → "dcl")
    """
    lua_file = md_dir / "cpp_std_labels.lua"
    if not lua_file.exists():
        return {}

    content = lua_file.read_text(encoding="utf-8")

    # Parse the Lua table format: return { ["key"] = "value", ... }
    result = {}
    for match in re.finditer(r'\["([^"]+)"\]\s*=\s*"([^"]+)"', content):
        label, chapter = match.groups()
        result[label] = chapter

    return result


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
                "documentOrder": i,  # Position within chapter for ordering
                "crossReferences": cross_refs,
                "contentLength": len(section_content),
            }

    return sections


def build_hierarchy_from_levels(sections: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Build parent-child relationships using actual heading levels.

    This correctly handles cases where a child's stable name doesn't start with
    the parent's prefix (e.g., basic.lval under expr.prop).
    """
    from collections import defaultdict

    # Group sections by chapter and sort by document order
    by_chapter: dict[str, list[tuple[str, dict]]] = defaultdict(list)
    for name, data in sections.items():
        by_chapter[data["chapter"]].append((name, data))

    for chapter, chapter_sections in by_chapter.items():
        # Sort by document order within chapter
        chapter_sections.sort(key=lambda x: x[1]["documentOrder"])

        # Use a stack to track the hierarchy based on heading levels
        # Stack contains (stable_name, level) tuples
        stack: list[tuple[str, int]] = []

        for name, data in chapter_sections:
            level = data["headingLevel"]

            # Pop stack until we find a parent (level < current level)
            while stack and stack[-1][1] >= level:
                stack.pop()

            # Parent is top of stack (or None if empty)
            parent = stack[-1][0] if stack else None
            data["parent"] = parent

            # Initialize children list
            data["children"] = []

            # Add ourselves to parent's children list
            if parent and parent in sections:
                sections[parent]["children"].append(name)

            # Push ourselves onto the stack
            stack.append((name, level))

    return sections


def infer_hierarchy(sections: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Infer parent-child relationships - delegates to build_hierarchy_from_levels."""
    return build_hierarchy_from_levels(sections)


def generate_connections(
    sections: dict[str, dict[str, Any]], chapter_order: list[str] | None = None
) -> dict[str, dict[str, Any]]:
    """Generate north/south/east/west connections between sections.

    Navigation semantics:
    - North/South: Previous/next sibling (same parent, same level)
    - East/West: Previous/next chapter (based on std.tex order)
    - Up (parent field): Go to parent section
    - Down (children[0]): Go to first child

    Args:
        sections: Section data with parent/children already populated
        chapter_order: List of chapter names in std.tex order (for E/W navigation)
    """
    # Build chapter → root section mapping for E/W navigation
    chapter_roots: dict[str, str] = {}
    for name, data in sections.items():
        if data.get("parent") is None:
            # This is a root section (no parent within this chapter)
            chapter = data["chapter"]
            # First root section in document order becomes the chapter entry point
            if chapter not in chapter_roots:
                chapter_roots[chapter] = name

    # Generate connections for each section
    for name, data in sections.items():
        parent = data.get("parent")
        chapter = data["chapter"]

        # Get siblings (sections with same parent)
        if parent and parent in sections:
            siblings = sections[parent].get("children", [])
        else:
            # Top-level: no siblings for N/S (only E/W for chapter navigation)
            siblings = []

        # Find position among siblings
        try:
            idx = siblings.index(name)
        except ValueError:
            idx = -1

        # North/South: sibling navigation (null at chapter root level)
        north = siblings[idx - 1] if idx > 0 else None
        south = siblings[idx + 1] if 0 <= idx < len(siblings) - 1 else None

        # East/West: chapter navigation
        east = None
        west = None
        if chapter_order:
            try:
                chapter_idx = chapter_order.index(chapter)
                # West = previous chapter's root section
                if chapter_idx > 0:
                    prev_chapter = chapter_order[chapter_idx - 1]
                    west = chapter_roots.get(prev_chapter)
                # East = next chapter's root section
                if chapter_idx < len(chapter_order) - 1:
                    next_chapter = chapter_order[chapter_idx + 1]
                    east = chapter_roots.get(next_chapter)
            except ValueError:
                pass  # Chapter not in order list

        data["connections"] = {
            "north": north,
            "south": south,
            "east": east,
            "west": west,
        }

    return sections


def get_chapter_order_from_std_tex(draft_dir: Path) -> list[str]:
    """Extract chapter order from std.tex file.

    Returns list of chapter stable names (markdown file stems) in document order.
    """
    std_tex = draft_dir / "std.tex"
    if not std_tex.exists():
        return []

    content = std_tex.read_text(encoding="utf-8")

    # Extract \include{filename} in order
    includes = re.findall(r"\\include\{([^}]+)\}", content)

    # Map LaTeX filenames to markdown chapter names
    # Most map directly, but some have special handling
    latex_to_md = {
        "expressions": "expr",
        "statements": "stmt",
        "declarations": "dcl",
        "classes": "class",
        "overloading": "over",
        "templates": "temp",
        "exceptions": "except",
        "preprocessor": "cpp",
        "modules": "module",
        "lib-intro": "library",
        "concepts": "concepts",
        "diagnostics": "diagnostics",
        "memory": "mem",
        "utilities": "utilities",
        "strings": "strings",
        "containers": "containers",
        "iterators": "iterators",
        "ranges": "ranges",
        "algorithms": "algorithms",
        "numerics": "numerics",
        "locales": "locales",
        "iostreams": "input",  # input.output -> input
        "regex": "re",
        "threads": "thread",
        "grammar": "grammar",
        "limits": "limits",
        "compatibility": "compatibility",
        "future": "future",
        # These are their own names
        "intro": "intro",
        "lex": "lex",
        "basic": "basic",
        "support": "support",
        "meta": "meta",
        "time": "time",
        "uax31": "uax31",
        "front": "front",
        "back": "back",
    }

    chapter_order = []
    for inc in includes:
        md_name = latex_to_md.get(inc, inc)
        chapter_order.append(md_name)

    return chapter_order


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
    draft_dir: Path | None = None,
) -> dict[str, Any]:
    """Generate the complete world map from markdown content."""
    # Get label→chapter mapping from the generated Lua file
    label_to_chapter = load_label_to_chapter_from_lua(primary_version_dir)
    if label_to_chapter:
        print(f"  Loaded {len(label_to_chapter)} label mappings from cpp_std_labels.lua")

    sections = extract_sections_from_markdown(primary_version_dir, label_to_chapter)
    sections = infer_hierarchy(sections)

    # Get chapter order for E/W navigation
    chapter_order = []
    if draft_dir:
        chapter_order = get_chapter_order_from_std_tex(draft_dir)
        if chapter_order:
            print(f"  Loaded chapter order from std.tex ({len(chapter_order)} chapters)")

    sections = generate_connections(sections, chapter_order)

    world_map: dict[str, Any] = {
        "version": "1.0.0",
        "primaryEra": primary_version_dir.name,
        "eras": ERA_NAMES,
        "stableNameAliases": {},  # Will be populated later from aliases data
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


def copy_version_markdown(version_dirs: list[Path], output_dir: Path) -> None:
    """Copy markdown files from version directories to output for deployment.

    This replaces symlinks with actual file copies so the site is fully deployable.
    Only copies .md and .lua files needed by the adventure game.
    """
    for version_dir in version_dirs:
        if not version_dir.exists():
            continue

        version_name = version_dir.name
        dst_dir = output_dir / version_name

        # Remove existing symlink if present
        if dst_dir.is_symlink():
            dst_dir.unlink()

        # Create directory
        dst_dir.mkdir(parents=True, exist_ok=True)

        # Copy markdown files
        md_count = 0
        for md_file in version_dir.glob("*.md"):
            shutil.copy2(md_file, dst_dir / md_file.name)
            md_count += 1

        # Copy lua files (cpp_std_labels.lua)
        for lua_file in version_dir.glob("*.lua"):
            shutil.copy2(lua_file, dst_dir / lua_file.name)

        print(f"  Copied {md_count} markdown files to {version_name}/")


def load_or_generate_aliases(
    game_data_dir: Path, base_dir: Path, versions: list[str]
) -> dict[str, Any]:
    """Load existing aliases or generate new ones.

    Returns the aliases data structure with forward_aliases and bidirectional maps.
    """
    alias_file = game_data_dir / "stable-name-aliases.json"

    # Import the generator function
    from generate_stable_name_aliases import generate_aliases

    # Generate aliases (will write to file)
    return generate_aliases(
        base_dir=base_dir,
        output_file=alias_file,
        versions=versions,
    )


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

    print("Generating adventure game data...")
    print(f"  Primary version: {primary_version}")
    print(f"  Output directory: {game_data_dir}")

    # Generate stable name aliases
    print("\n  Generating stable name aliases...")
    aliases_data = load_or_generate_aliases(game_data_dir, base_dir, versions)

    # Find draft directory for std.tex (chapter ordering)
    draft_dir = base_dir / "cplusplus-draft" / "source"
    if not draft_dir.exists():
        draft_dir = None
        print("  Warning: cplusplus-draft/source not found, chapter order unavailable")

    # Generate world map
    world_map = generate_world_map(primary_dir, version_dirs, draft_dir)
    print(f"  Extracted {len(world_map['sections'])} sections from markdown")

    # Add stable name aliases to world map for timeshift navigation
    world_map["stableNameAliases"] = aliases_data.get("bidirectional", {})

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

    # Copy markdown files from version directories (replaces symlinks for deployment)
    existing_version_dirs = [d for d in version_dirs if d.exists()]
    if existing_version_dirs:
        print("  Copying markdown files for deployment...")
        copy_version_markdown(existing_version_dirs, output_dir)

    print("\nAdventure game data generation complete!")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate adventure game data from C++ standard markdown",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="build/site",
        help="Output directory (default: build/site/)",
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
