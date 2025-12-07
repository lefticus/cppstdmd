# Technical Architecture

## File Structure

### New Files to Create

```
cppstdmd/
├── templates/
│   ├── adventure.html              # Standalone adventure page template
│   └── _adventure_widget.html      # Embeddable widget partial
│
├── build/site/
│   ├── js/
│   │   └── adventure/
│   │       ├── game.js             # Main game engine & orchestration
│   │       ├── world.js            # World map & navigation
│   │       ├── player.js           # Player state management
│   │       ├── quests.js           # Quest tracking & progression
│   │       ├── npcs.js             # NPC interaction system
│   │       ├── puzzles.js          # Puzzle presentation & validation
│   │       ├── inventory.js        # Item management
│   │       ├── time-travel.js      # Era switching mechanics
│   │       ├── terminal.js         # Terminal UI & command parser
│   │       ├── markdown-loader.js  # Section content fetching
│   │       └── save-system.js      # localStorage persistence
│   │
│   ├── css/
│   │   └── adventure.css           # Adventure-specific styles
│   │
│   ├── adventure/
│   │   └── index.html              # Generated standalone page
│   │
│   └── data/
│       └── game/
│           ├── world-map.json      # Generated navigation graph
│           ├── npcs.json           # NPC definitions
│           ├── quests.json         # Quest data
│           ├── items.json          # Knowledge items
│           └── puzzles.json        # Puzzle content
│
└── docs/
    └── adventure-game-design/      # This documentation
        ├── README.md
        ├── 01-game-world.md
        ├── 02-rpg-systems.md
        ├── 03-technical-architecture.md
        └── 04-implementation-phases.md
```

### Files to Modify

| File | Changes |
|------|---------|
| `generate_html_site.py` | Add `generate_adventure_data()` and `generate_adventure_page()` |
| `templates/index.html` | Add adventure section with link to `/adventure/` |
| `build/site/js/navigation.js` | Add widget toggle button initialization |
| `build/site/css/custom.css` | Add widget button and panel base styles |

---

## Data Generation Pipeline

### Overview

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Markdown Files │────▶│ generate_html_   │────▶│  JSON Data      │
│  (n4950/*.md)   │     │ site.py          │     │  (world-map,    │
│                 │     │                  │     │   npcs, quests) │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌──────────────────┐
                        │  adventure/      │
                        │  index.html      │
                        └──────────────────┘
```

### Implementation in generate_html_site.py

```python
# Add to generate_html_site.py

from pathlib import Path
import json
import re
from dataclasses import dataclass, asdict
from typing import Optional

# ============================================================================
# Adventure Game Data Generation
# ============================================================================

@dataclass
class WorldSection:
    """Represents a navigable section in the game world."""
    stable_name: str
    display_name: str
    realm: str
    parent: Optional[str]
    children: list[str]
    connections: dict[str, Optional[str]]  # north/south/east/west
    available_in: list[str]
    description: str
    npcs: list[str]
    items: list[str]
    puzzles: list[str]


# Realm theming
REALM_THEMES = {
    "basic": ("The Foundations", "Ancient temple ruins with fundamental laws"),
    "lex": ("Lexicon Tower", "Tall library with lexical knowledge"),
    "expr": ("Expression Fields", "Testing grounds for expressions"),
    "stmt": ("Statement Sanctum", "Control flow chambers"),
    "dcl": ("Declaration Domain", "Halls of formal declarations"),
    "class": ("Class Citadel", "Castle with inheritance towers"),
    "temp": ("Template Tundra", "Frozen crystalline structures"),
    "except": ("Exception Caverns", "Underground try-catch tunnels"),
    "library": ("The Standard Library", "Grand entrance hall"),
    "utilities": ("Utility Workshop", "Inventor's workshop"),
    "containers": ("Container Harbor", "Docks with container ships"),
    "algorithms": ("Algorithm Academy", "Training grounds"),
    "iterators": ("Iterator Isle", "Bridge-connected islands"),
    "ranges": ("Range Frontier", "New frontier territory"),
    "concepts": ("Concept Cathedral", "Grand cathedral of constraints"),
    "thread": ("Thread Nexus", "Multi-dimensional hub"),
    "time": ("Chrono Clocktower", "Giant clockwork tower"),
    "mem": ("Memory Depths", "Caverns of memory management"),
    "input": ("Stream Rivers", "Rivers of data flow"),
}


def extract_sections_from_markdown(md_dir: Path) -> dict[str, dict]:
    """Extract all sections with metadata from markdown files."""
    sections = {}

    for md_file in sorted(md_dir.glob("*.md")):
        chapter = md_file.stem
        content = md_file.read_text(encoding="utf-8")

        # Pattern: ## Title <a id="stable.name">[[stable.name]]</a>
        pattern = r'(#{1,4})\s+([^<\n]+)<a id="([^"]+)">\[\[([^\]]+)\]\]</a>'

        for match in re.finditer(pattern, content):
            heading_level = len(match.group(1))
            title = match.group(2).strip()
            anchor = match.group(3)
            stable_name = match.group(4)

            # Extract cross-references from section content
            section_start = match.end()
            next_section = re.search(r'\n#{1,4}\s+[^<\n]+<a id="', content[section_start:])
            section_end = section_start + next_section.start() if next_section else len(content)
            section_content = content[section_start:section_end]

            cross_refs = re.findall(r'\[\[([^\]]+)\]\]', section_content)

            sections[stable_name] = {
                "chapter": chapter,
                "title": title,
                "stable_name": stable_name,
                "heading_level": heading_level,
                "cross_references": list(set(cross_refs)),
                "content_length": len(section_content)
            }

    return sections


def infer_hierarchy(sections: dict) -> dict[str, dict]:
    """Infer parent-child relationships from stable names."""
    for stable_name, data in sections.items():
        parts = stable_name.split(".")

        # Parent is the stable name with one fewer part
        if len(parts) > 1:
            potential_parent = ".".join(parts[:-1])
            if potential_parent in sections:
                data["parent"] = potential_parent
            else:
                data["parent"] = parts[0]  # Fall back to realm
        else:
            data["parent"] = None

        # Children are sections that have this as their parent
        data["children"] = [
            name for name, d in sections.items()
            if d.get("parent") == stable_name
        ]

    return sections


def generate_connections(sections: dict) -> dict[str, dict]:
    """Generate north/south/east/west connections between sections."""
    # Group sections by chapter
    by_chapter = {}
    for name, data in sections.items():
        chapter = data["chapter"]
        if chapter not in by_chapter:
            by_chapter[chapter] = []
        by_chapter[chapter].append(name)

    # Within each chapter, sections connect sequentially (north/south)
    for name, data in sections.items():
        chapter_sections = by_chapter[data["chapter"]]
        idx = chapter_sections.index(name)

        data["connections"] = {
            "north": chapter_sections[idx - 1] if idx > 0 else None,
            "south": chapter_sections[idx + 1] if idx < len(chapter_sections) - 1 else None,
            "east": None,
            "west": None
        }

        # Cross-references become east/west connections
        for ref in data.get("cross_references", [])[:2]:
            if ref in sections and ref != name:
                if data["connections"]["east"] is None:
                    data["connections"]["east"] = ref
                elif data["connections"]["west"] is None:
                    data["connections"]["west"] = ref

    return sections


def detect_era_availability(stable_name: str, version_dirs: list[Path]) -> list[str]:
    """Detect which C++ versions contain this section."""
    available = []
    for version_dir in version_dirs:
        # Check if any markdown file in this version contains the stable name
        for md_file in version_dir.glob("*.md"):
            content = md_file.read_text(encoding="utf-8")
            if f'id="{stable_name}"' in content:
                available.append(version_dir.name)
                break
    return available


def generate_display_name(title: str, stable_name: str) -> str:
    """Generate a thematic display name for a section."""
    # Map common terms to thematic alternatives
    theme_map = {
        "General": "Main Hall",
        "Overview": "Observation Deck",
        "Introduction": "Welcome Chamber",
        "Requirements": "Standards Hall",
        "Constructors": "Constructor Forge",
        "Destructor": "Destructor Crypt",
        "Members": "Member Hall",
        "Copy": "Duplication Chamber",
        "Move": "Transfer Station",
        "Assignment": "Assignment Alcove",
        "Virtual": "Phantom Tower",
        "Derived": "Inheritance Gates",
        "Access": "Access Control",
    }

    for key, value in theme_map.items():
        if key.lower() in title.lower():
            return value

    # Default: use title with "Chamber/Hall/etc" suffix based on depth
    depth = stable_name.count(".")
    suffixes = ["Realm", "Zone", "Chamber", "Room", "Alcove"]
    suffix = suffixes[min(depth, len(suffixes) - 1)]

    return f"{title} {suffix}"


def generate_world_map(output_dir: Path, version_dirs: list[Path]) -> dict:
    """Generate the complete world map from markdown content."""
    # Use the latest version as the primary source
    primary_version = version_dirs[-1]  # e.g., n4950

    sections = extract_sections_from_markdown(primary_version)
    sections = infer_hierarchy(sections)
    sections = generate_connections(sections)

    world_map = {
        "version": "1.0.0",
        "primaryEra": primary_version.name,
        "realms": {},
        "sections": {}
    }

    for stable_name, data in sections.items():
        realm = stable_name.split(".")[0]

        # Initialize realm if needed
        if realm not in world_map["realms"]:
            theme = REALM_THEMES.get(realm, (realm.title(), f"The {realm} area"))
            world_map["realms"][realm] = {
                "name": theme[0],
                "description": theme[1],
                "sections": []
            }

        world_map["realms"][realm]["sections"].append(stable_name)

        # Build section entry
        world_map["sections"][stable_name] = {
            "stableName": stable_name,
            "displayName": generate_display_name(data["title"], stable_name),
            "realm": realm,
            "parent": data.get("parent"),
            "children": data.get("children", []),
            "connections": data.get("connections", {}),
            "availableIn": detect_era_availability(stable_name, version_dirs),
            "description": f"Section covering {data['title'].lower()}.",
            "npcs": [],      # Populated by NPC generation
            "items": [],     # Populated by item generation
            "puzzles": []    # Populated by puzzle generation
        }

    return world_map


def generate_npcs(world_map: dict) -> list[dict]:
    """Generate NPC data based on world structure."""
    npcs = []

    # Compiler spirits (appear everywhere)
    for compiler in [("gcc_ghost", "GCC Ghost"), ("clang_specter", "Clang Specter")]:
        npcs.append({
            "id": compiler[0],
            "name": compiler[1],
            "type": "compiler_spirit",
            "locations": ["*"],
            "dialogue": {
                "greeting": f"Greetings, I am the spirit of {compiler[1].split()[0]}.",
                "topics": {}
            }
        })

    # Concept personifications based on realm
    concept_npcs = {
        "class": ("raii_guardian", "RAII Guardian", "Resource management wisdom"),
        "iterators": ("iterator_wanderer", "Iterator Wanderer", "Iterator patterns"),
        "temp": ("template_sage", "Template Sage", "Template metaprogramming"),
        "concepts": ("concept_keeper", "Concept Keeper", "Constraints and concepts"),
        "ranges": ("range_ranger", "Range Ranger", "Ranges library"),
        "thread": ("concurrency_spirit", "Concurrency Spirit", "Thread safety"),
    }

    for realm, (npc_id, name, specialty) in concept_npcs.items():
        if realm in world_map["realms"]:
            locations = world_map["realms"][realm]["sections"][:3]  # First 3 sections
            npcs.append({
                "id": npc_id,
                "name": name,
                "type": "concept_personification",
                "locations": locations,
                "specialty": specialty,
                "dialogue": {
                    "greeting": f"Welcome to the {REALM_THEMES.get(realm, (realm,))[0]}. I am the {name}.",
                    "topics": {}
                }
            })

            # Add NPC to section data
            for loc in locations:
                if loc in world_map["sections"]:
                    world_map["sections"][loc]["npcs"].append(npc_id)

    return npcs


def generate_items(world_map: dict) -> list[dict]:
    """Generate collectible items from section structure."""
    items = []

    for stable_name, section in world_map["sections"].items():
        # Generate an item for notable sections
        if section["children"] or len(stable_name.split(".")) <= 2:
            item_id = stable_name.replace(".", "_") + "_scroll"
            items.append({
                "id": item_id,
                "name": f"{section['displayName']} Scroll",
                "category": "language_scroll",
                "rarity": "common" if len(stable_name.split(".")) > 2 else "uncommon",
                "sourceSection": stable_name,
                "description": f"Knowledge from {section['displayName']}.",
                "effects": {"statBoost": {"fundamentals": 1}}
            })

            section["items"].append(item_id)

    return items


def generate_quests(world_map: dict) -> list[dict]:
    """Generate quests from world structure."""
    quests = []

    # Exploration quest for each realm
    for realm, realm_data in world_map["realms"].items():
        sections = realm_data["sections"][:5]  # First 5 sections
        if len(sections) >= 3:
            quests.append({
                "id": f"explore_{realm}",
                "title": f"Tour of {realm_data['name']}",
                "description": f"Explore the key areas of {realm_data['name']}.",
                "type": "exploration",
                "difficulty": "easy",
                "minLevel": 1,
                "steps": [
                    {"instruction": f"Visit {world_map['sections'][s]['displayName']}",
                     "target": {"section": s}}
                    for s in sections[:3]
                ],
                "rewards": {
                    "experience": 100,
                    "items": [f"{realm}_explorer_badge"]
                }
            })

    # Time travel quest
    quests.append({
        "id": "lambda_evolution",
        "title": "The Lambda Chronicles",
        "description": "Trace the evolution of lambdas through C++ history.",
        "type": "time_travel",
        "difficulty": "medium",
        "minLevel": 10,
        "steps": [
            {"instruction": "Witness lambdas in C++11", "target": {"section": "expr.prim.lambda", "era": "n3337"}},
            {"instruction": "See generic lambdas in C++14", "target": {"section": "expr.prim.lambda", "era": "n4140"}},
            {"instruction": "Discover constexpr lambdas in C++17", "target": {"section": "expr.prim.lambda", "era": "n4659"}}
        ],
        "rewards": {
            "experience": 500,
            "items": ["lambda_master_crystal"],
            "title": "Lambda Historian"
        }
    })

    return quests


def generate_puzzles(world_map: dict) -> list[dict]:
    """Generate puzzles from content structure."""
    puzzles = []

    # Iterator category matching puzzle
    puzzles.append({
        "id": "iterator_categories",
        "type": "matching",
        "location": "iterators",
        "difficulty": "medium",
        "question": "Match each iterator category with its key capability:",
        "pairs": [
            ["Input Iterator", "Single-pass read"],
            ["Forward Iterator", "Multi-pass"],
            ["Bidirectional Iterator", "Move backwards"],
            ["Random Access Iterator", "O(1) arbitrary access"],
            ["Contiguous Iterator", "Elements stored contiguously"]
        ],
        "rewards": {"xp": 50}
    })

    # Timeline puzzle
    puzzles.append({
        "id": "feature_timeline",
        "type": "timeline",
        "location": "intro",
        "difficulty": "hard",
        "question": "Order these features by when they were added:",
        "items": [
            {"name": "Lambdas", "era": "n3337"},
            {"name": "Concepts", "era": "n4861"},
            {"name": "Structured bindings", "era": "n4659"},
            {"name": "Ranges", "era": "n4861"}
        ],
        "rewards": {"xp": 100}
    })

    return puzzles


def generate_adventure_data(output_dir: Path, version_dirs: list[Path]):
    """Main entry point: generate all adventure game data files."""
    game_data_dir = output_dir / "data" / "game"
    game_data_dir.mkdir(parents=True, exist_ok=True)

    print("Generating adventure game data...")

    # Generate world map
    world_map = generate_world_map(output_dir, version_dirs)
    with open(game_data_dir / "world-map.json", "w") as f:
        json.dump(world_map, f, indent=2)
    print(f"  Generated world-map.json ({len(world_map['sections'])} sections)")

    # Generate NPCs
    npcs = generate_npcs(world_map)
    with open(game_data_dir / "npcs.json", "w") as f:
        json.dump(npcs, f, indent=2)
    print(f"  Generated npcs.json ({len(npcs)} NPCs)")

    # Generate items
    items = generate_items(world_map)
    with open(game_data_dir / "items.json", "w") as f:
        json.dump(items, f, indent=2)
    print(f"  Generated items.json ({len(items)} items)")

    # Generate quests
    quests = generate_quests(world_map)
    with open(game_data_dir / "quests.json", "w") as f:
        json.dump(quests, f, indent=2)
    print(f"  Generated quests.json ({len(quests)} quests)")

    # Generate puzzles
    puzzles = generate_puzzles(world_map)
    with open(game_data_dir / "puzzles.json", "w") as f:
        json.dump(puzzles, f, indent=2)
    print(f"  Generated puzzles.json ({len(puzzles)} puzzles)")

    # Update world map with NPC/item references
    with open(game_data_dir / "world-map.json", "w") as f:
        json.dump(world_map, f, indent=2)

    print("Adventure game data generation complete!")
```

---

## Client-Side Architecture

### Module Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        game.js (Main Engine)                     │
│  - Initializes all modules                                       │
│  - Game loop                                                     │
│  - Command routing                                               │
└─────────────────────────────────────────────────────────────────┘
         │
         ├──────────────┬──────────────┬──────────────┬────────────┐
         ▼              ▼              ▼              ▼            ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐  ┌─────────┐
│ terminal.js │  │  world.js   │  │  player.js  │  │npcs.js  │  │quests.js│
│ - UI render │  │ - Navigation│  │ - State     │  │- Dialog │  │- Track  │
│ - Input     │  │ - Map       │  │ - Stats     │  │- Trade  │  │- Reward │
│ - History   │  │ - Locations │  │ - Level     │  │         │  │         │
└─────────────┘  └─────────────┘  └─────────────┘  └─────────┘  └─────────┘
         │              │              │
         │              │              │
         ▼              ▼              ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ markdown-   │  │time-travel.js│ │ inventory.js│
│ loader.js   │  │ - Era switch │  │ - Items    │
│ - Fetch     │  │ - Effects    │  │ - Equip    │
│ - Parse     │  │              │  │            │
└─────────────┘  └─────────────┘  └─────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     save-system.js                               │
│  - localStorage persistence                                      │
│  - Import/Export                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Core Module: game.js

```javascript
// build/site/js/adventure/game.js

/**
 * Main game engine - coordinates all modules
 */
class AdventureGame {
    constructor(containerElement, contentPanel) {
        this.container = containerElement;
        this.contentPanel = contentPanel;

        // Initialize modules
        this.terminal = new Terminal(containerElement);
        this.saveSystem = new SaveSystem();
        this.player = new Player(this.saveSystem);
        this.world = new World();
        this.inventory = new Inventory(this.player);
        this.timeTravel = new TimeTravel(this.player, this.world);
        this.npcs = new NPCSystem(this.world);
        this.quests = new QuestSystem(this.player);
        this.puzzles = new PuzzleSystem();
        this.markdownLoader = new MarkdownLoader();

        // Command registry
        this.commands = this.buildCommandRegistry();

        // Bind events
        this.terminal.onCommand = (cmd) => this.handleCommand(cmd);
    }

    async init() {
        // Load game data
        await Promise.all([
            this.world.loadWorldMap(),
            this.npcs.loadNPCs(),
            this.quests.loadQuests(),
            this.puzzles.loadPuzzles()
        ]);

        // Load or create player save
        await this.player.load();

        // Show welcome
        this.terminal.print("Welcome to the C++ Standard Adventure!");
        this.terminal.print("Type 'help' for commands.\n");

        // Show current location
        this.showLocation();
    }

    buildCommandRegistry() {
        return {
            // Navigation
            'look': () => this.cmdLook(),
            'go': (args) => this.cmdGo(args),
            'enter': (args) => this.cmdEnter(args),
            'exit': () => this.cmdExit(),
            'warp': (args) => this.cmdWarp(args),
            'map': () => this.cmdMap(),
            'where': () => this.cmdWhere(),

            // Time travel
            'timeshift': (args) => this.cmdTimeshift(args),
            'era': () => this.cmdEra(),

            // Interaction
            'talk': (args) => this.cmdTalk(args),
            'ask': (args) => this.cmdAsk(args),

            // Items
            'inventory': () => this.cmdInventory(),
            'examine': (args) => this.cmdExamine(args),
            'take': (args) => this.cmdTake(args),

            // Quests
            'journal': () => this.cmdJournal(),
            'quest': (args) => this.cmdQuest(args),

            // Puzzles
            'solve': (args) => this.cmdSolve(args),
            'hint': () => this.cmdHint(),

            // Player
            'stats': () => this.cmdStats(),
            'achievements': () => this.cmdAchievements(),

            // System
            'help': () => this.cmdHelp(),
            'save': () => this.cmdSave(),
            'load': () => this.cmdLoad(),
            'clear': () => this.terminal.clear()
        };
    }

    async handleCommand(input) {
        const parts = input.trim().toLowerCase().split(/\s+/);
        const cmd = parts[0];
        const args = parts.slice(1);

        if (this.commands[cmd]) {
            await this.commands[cmd](args);
        } else {
            this.terminal.print(`Unknown command: ${cmd}. Type 'help' for commands.`);
        }

        // Auto-save after each command
        this.player.save();
    }

    // --- Command Implementations ---

    async cmdLook() {
        const section = this.world.getSection(this.player.currentLocation);
        const era = this.player.currentEra;

        // Show location description
        this.terminal.print(`\n[${this.timeTravel.getEraName(era)}] ${section.displayName}`);
        this.terminal.print(`[[${section.stableName}]]`);
        this.terminal.print("═".repeat(50));
        this.terminal.print(section.description);

        // Show exits
        const exits = this.world.getExits(section);
        this.terminal.print(`\nExits: ${exits.join(", ") || "none"}`);

        // Show NPCs
        if (section.npcs.length > 0) {
            const npcNames = section.npcs.map(id => this.npcs.getNPC(id)?.name).filter(Boolean);
            this.terminal.print(`You see: ${npcNames.join(", ")}`);
        }

        // Show items
        if (section.items.length > 0) {
            this.terminal.print(`Items here: ${section.items.length} item(s)`);
        }

        // Load and display markdown content in side panel
        const content = await this.markdownLoader.loadSection(section.stableName, era);
        this.contentPanel.render(content, section.stableName);
    }

    cmdGo(args) {
        if (args.length === 0) {
            this.terminal.print("Go where? (north, south, east, west)");
            return;
        }

        const direction = args[0];
        const section = this.world.getSection(this.player.currentLocation);
        const target = section.connections[direction];

        if (!target) {
            this.terminal.print(`You cannot go ${direction} from here.`);
            return;
        }

        // Check era availability
        const targetSection = this.world.getSection(target);
        if (!targetSection.availableIn.includes(this.player.currentEra)) {
            this.terminal.print(`That area doesn't exist in ${this.timeTravel.getEraName(this.player.currentEra)}.`);
            return;
        }

        this.player.moveTo(target);
        this.terminal.print(`\nYou travel ${direction}...`);
        this.cmdLook();
    }

    async cmdTimeshift(args) {
        if (args.length === 0) {
            this.terminal.print("Timeshift to which era? (cpp11, cpp14, cpp17, cpp20, cpp23, cpp26)");
            return;
        }

        const result = this.timeTravel.shift(args[0]);
        if (result.success) {
            this.terminal.print("\n*The world ripples as you shift through time...*\n");
            await this.cmdLook();
        } else {
            this.terminal.print(result.message);
        }
    }

    cmdHelp() {
        this.terminal.print(`
NAVIGATION
  look              - View current location and content
  go <direction>    - Move north/south/east/west
  enter <zone>      - Enter a child section
  exit              - Return to parent section
  warp <name>       - Fast travel to visited location
  map               - Show current realm overview
  where             - Show location in hierarchy

TIME TRAVEL
  timeshift <era>   - Travel to C++ era (cpp11-cpp26)
  era               - Show current era info

INTERACTION
  talk <npc>        - Talk to an NPC
  ask about <topic> - Ask NPC about a topic
  take <item>       - Pick up an item
  examine <item>    - Look at an item closely

PLAYER
  inventory         - View your items
  journal           - View active quests
  stats             - View character stats
  achievements      - View badges and certificates

SYSTEM
  help              - Show this help
  save              - Save game
  clear             - Clear terminal
`);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    const terminal = document.getElementById('adventure-terminal');
    const content = document.getElementById('adventure-content');

    if (terminal && content) {
        window.game = new AdventureGame(terminal, content);
        window.game.init();
    }
});
```

### Terminal Module: terminal.js

```javascript
// build/site/js/adventure/terminal.js

/**
 * Terminal UI component with command input and output
 */
class Terminal {
    constructor(container) {
        this.container = container;
        this.history = [];
        this.historyIndex = -1;
        this.onCommand = null;

        this.render();
        this.bindEvents();
    }

    render() {
        this.container.innerHTML = `
            <div class="terminal-output" id="terminal-output"></div>
            <div class="terminal-input-line">
                <span class="terminal-prompt">&gt;</span>
                <input type="text" class="terminal-input" id="terminal-input"
                       placeholder="Type a command..." autocomplete="off">
            </div>
        `;

        this.output = this.container.querySelector('#terminal-output');
        this.input = this.container.querySelector('#terminal-input');
    }

    bindEvents() {
        this.input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                const cmd = this.input.value.trim();
                if (cmd) {
                    this.history.push(cmd);
                    this.historyIndex = this.history.length;
                    this.print(`> ${cmd}`, 'command');
                    this.input.value = '';
                    if (this.onCommand) {
                        this.onCommand(cmd);
                    }
                }
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                if (this.historyIndex > 0) {
                    this.historyIndex--;
                    this.input.value = this.history[this.historyIndex];
                }
            } else if (e.key === 'ArrowDown') {
                e.preventDefault();
                if (this.historyIndex < this.history.length - 1) {
                    this.historyIndex++;
                    this.input.value = this.history[this.historyIndex];
                } else {
                    this.historyIndex = this.history.length;
                    this.input.value = '';
                }
            }
        });

        // Focus input on container click
        this.container.addEventListener('click', () => {
            this.input.focus();
        });
    }

    print(text, className = '') {
        const line = document.createElement('div');
        line.className = `terminal-line ${className}`;
        line.textContent = text;
        this.output.appendChild(line);
        this.output.scrollTop = this.output.scrollHeight;
    }

    printHTML(html) {
        const line = document.createElement('div');
        line.className = 'terminal-line';
        line.innerHTML = html;
        this.output.appendChild(line);
        this.output.scrollTop = this.output.scrollHeight;
    }

    clear() {
        this.output.innerHTML = '';
    }

    focus() {
        this.input.focus();
    }
}
```

### Markdown Loader: markdown-loader.js

```javascript
// build/site/js/adventure/markdown-loader.js

/**
 * Loads and parses markdown content from section files
 */
class MarkdownLoader {
    constructor() {
        this.cache = new Map();
        this.baseUrls = {
            n3337: '/n3337/',
            n4140: '/n4140/',
            n4659: '/n4659/',
            n4861: '/n4861/',
            n4950: '/n4950/',
            trunk: '/trunk/'
        };

        // Stable name to chapter mapping (simplified - full version in world-map.json)
        this.chapterMap = null;
    }

    async loadChapterMap() {
        if (this.chapterMap) return;

        const response = await fetch('/data/game/world-map.json');
        const worldMap = await response.json();

        this.chapterMap = {};
        for (const [stableName, section] of Object.entries(worldMap.sections)) {
            // Extract chapter from world map data
            this.chapterMap[stableName] = section.realm;
        }
    }

    getChapterFromStableName(stableName) {
        if (this.chapterMap && this.chapterMap[stableName]) {
            return this.chapterMap[stableName];
        }
        // Fallback: use first part of stable name
        return stableName.split('.')[0];
    }

    async loadSection(stableName, era = 'n4950') {
        const cacheKey = `${era}:${stableName}`;

        if (this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }

        await this.loadChapterMap();

        const chapter = this.getChapterFromStableName(stableName);
        const url = `${this.baseUrls[era]}${chapter}.md`;

        try {
            const response = await fetch(url);
            if (!response.ok) {
                return { found: false, content: `Section not found in ${era}` };
            }

            const markdown = await response.text();
            const section = this.extractSection(markdown, stableName);

            const result = {
                found: !!section,
                content: section || `Could not find [[${stableName}]] in ${chapter}.md`,
                stableName,
                era,
                chapter
            };

            this.cache.set(cacheKey, result);
            return result;

        } catch (error) {
            return { found: false, content: `Error loading: ${error.message}` };
        }
    }

    extractSection(markdown, stableName) {
        // Find section by anchor: <a id="stable.name">
        // Then extract until the next section of same or higher level
        const anchorPattern = `<a id="${this.escapeRegex(stableName)}">`;
        const anchorIndex = markdown.indexOf(anchorPattern);

        if (anchorIndex === -1) {
            return null;
        }

        // Find the heading level of this section
        const beforeAnchor = markdown.substring(Math.max(0, anchorIndex - 100), anchorIndex);
        const headingMatch = beforeAnchor.match(/(#{1,6})\s+[^\n]+$/);
        const headingLevel = headingMatch ? headingMatch[1].length : 2;

        // Find the start of the heading line
        const lineStart = markdown.lastIndexOf('\n', anchorIndex) + 1;

        // Find the next heading of same or higher level
        const afterSection = markdown.substring(anchorIndex);
        const nextHeadingPattern = new RegExp(`^#{1,${headingLevel}}\\s+`, 'm');
        const nextMatch = afterSection.match(nextHeadingPattern);

        let sectionEnd;
        if (nextMatch) {
            sectionEnd = anchorIndex + nextMatch.index;
        } else {
            sectionEnd = markdown.length;
        }

        return markdown.substring(lineStart, sectionEnd).trim();
    }

    escapeRegex(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    clearCache() {
        this.cache.clear();
    }
}
```

---

## State Management

### Player State (localStorage)

```javascript
// build/site/js/adventure/save-system.js

/**
 * Handles save/load to localStorage
 */
class SaveSystem {
    constructor() {
        this.storageKey = 'cppevo_adventure_save';
        this.version = '1.0.0';
    }

    getDefaultState() {
        return {
            version: this.version,
            timestamp: Date.now(),
            player: {
                name: "Traveler",
                title: "Novice Programmer",
                level: 1,
                experience: 0,
                stats: {
                    fundamentals: 10,
                    library: 10,
                    metaprogramming: 10,
                    modernCpp: 10
                },
                currentLocation: "intro",
                currentEra: "n4950",
                inventory: [],
                badges: [],
                certificates: []
            },
            world: {
                sectionsVisited: [],
                sectionsCompleted: [],
                unlockedAreas: [],
                npcInteractions: {}
            },
            quests: {
                active: [],
                completed: [],
                questProgress: {}
            },
            settings: {
                terminalFontSize: 14,
                autoSave: true,
                showHints: true
            }
        };
    }

    save(state) {
        try {
            state.timestamp = Date.now();
            state.version = this.version;
            localStorage.setItem(this.storageKey, JSON.stringify(state));
            return { success: true };
        } catch (error) {
            console.error('Save failed:', error);
            return { success: false, error: error.message };
        }
    }

    load() {
        try {
            const saved = localStorage.getItem(this.storageKey);
            if (!saved) {
                return { found: false, state: this.getDefaultState() };
            }

            const state = JSON.parse(saved);

            // Version migration if needed
            if (state.version !== this.version) {
                return { found: true, state: this.migrate(state) };
            }

            return { found: true, state };

        } catch (error) {
            console.error('Load failed:', error);
            return { found: false, state: this.getDefaultState(), error: error.message };
        }
    }

    migrate(oldState) {
        // Handle version migrations
        const newState = this.getDefaultState();

        // Copy over compatible fields
        if (oldState.player) {
            Object.assign(newState.player, oldState.player);
        }
        if (oldState.world) {
            Object.assign(newState.world, oldState.world);
        }
        if (oldState.quests) {
            Object.assign(newState.quests, oldState.quests);
        }

        return newState;
    }

    export() {
        const state = this.load().state;
        const blob = new Blob([JSON.stringify(state, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = `cppevo-adventure-save-${new Date().toISOString().slice(0, 10)}.json`;
        a.click();

        URL.revokeObjectURL(url);
    }

    async import(file) {
        const text = await file.text();
        const state = JSON.parse(text);
        return this.save(state);
    }

    reset() {
        localStorage.removeItem(this.storageKey);
        return this.getDefaultState();
    }
}
```

---

## UI Layout

### Standalone Page Template

```html
<!-- templates/adventure.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>C++ Standard Adventure - cppevo</title>

    <!-- Styles -->
    <link rel="stylesheet" href="/css/custom.css">
    <link rel="stylesheet" href="/css/adventure.css">

    <!-- Markdown rendering -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

    <!-- Syntax highlighting -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/prismjs@1/themes/prism.min.css">
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1/prism.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1/components/prism-cpp.min.js"></script>
</head>
<body class="adventure-page">
    <header class="adventure-header">
        <a href="/" class="logo">cppevo</a>
        <h1>C++ Standard Adventure</h1>
        <div class="player-status" id="player-status">
            <span class="era-badge" id="era-badge">C++23</span>
            <span class="level-badge" id="level-badge">Level 1</span>
        </div>
    </header>

    <main class="adventure-main">
        <!-- Left: Terminal -->
        <section class="adventure-terminal-container">
            <div id="adventure-terminal" class="adventure-terminal"></div>
        </section>

        <!-- Right: Content Panel -->
        <section class="adventure-content-container">
            <div class="content-header">
                <h2 id="content-title">Welcome</h2>
                <button id="content-toggle" class="content-toggle">
                    <i class="fa-solid fa-expand"></i>
                </button>
            </div>
            <div id="adventure-content" class="adventure-content">
                <p>Type <code>look</code> to view the current section's content.</p>
            </div>
        </section>
    </main>

    <!-- Game scripts -->
    <script src="/js/adventure/save-system.js"></script>
    <script src="/js/adventure/terminal.js"></script>
    <script src="/js/adventure/markdown-loader.js"></script>
    <script src="/js/adventure/world.js"></script>
    <script src="/js/adventure/player.js"></script>
    <script src="/js/adventure/inventory.js"></script>
    <script src="/js/adventure/time-travel.js"></script>
    <script src="/js/adventure/npcs.js"></script>
    <script src="/js/adventure/quests.js"></script>
    <script src="/js/adventure/puzzles.js"></script>
    <script src="/js/adventure/game.js"></script>
</body>
</html>
```

### Adventure CSS

```css
/* build/site/css/adventure.css */

/* Layout */
.adventure-page {
    margin: 0;
    padding: 0;
    height: 100vh;
    display: flex;
    flex-direction: column;
    background: #1a1a2e;
    color: #eee;
}

.adventure-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.5rem 1rem;
    background: #16213e;
    border-bottom: 1px solid #0f3460;
}

.adventure-header .logo {
    font-weight: bold;
    color: #00a500;
    text-decoration: none;
}

.adventure-header h1 {
    margin: 0;
    font-size: 1.2rem;
    flex: 1;
}

.player-status {
    display: flex;
    gap: 0.5rem;
}

.era-badge, .level-badge {
    padding: 0.25rem 0.75rem;
    border-radius: 4px;
    font-size: 0.8rem;
}

.era-badge {
    background: #0f3460;
    color: #4fc3f7;
}

.level-badge {
    background: #1a472a;
    color: #81c784;
}

/* Main layout: split screen */
.adventure-main {
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1px;
    background: #0f3460;
    overflow: hidden;
}

/* Terminal side */
.adventure-terminal-container {
    background: #0d1b2a;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.adventure-terminal {
    flex: 1;
    display: flex;
    flex-direction: column;
    font-family: 'Source Code Pro', 'Consolas', monospace;
    font-size: 14px;
    padding: 1rem;
    overflow: hidden;
}

.terminal-output {
    flex: 1;
    overflow-y: auto;
    padding-bottom: 0.5rem;
}

.terminal-line {
    white-space: pre-wrap;
    word-wrap: break-word;
    line-height: 1.5;
}

.terminal-line.command {
    color: #4fc3f7;
}

.terminal-input-line {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    border-top: 1px solid #0f3460;
    padding-top: 0.5rem;
}

.terminal-prompt {
    color: #00a500;
    font-weight: bold;
}

.terminal-input {
    flex: 1;
    background: transparent;
    border: none;
    color: #eee;
    font-family: inherit;
    font-size: inherit;
    outline: none;
}

.terminal-input::placeholder {
    color: #666;
}

/* Content side */
.adventure-content-container {
    background: #1a1a2e;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.content-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.5rem 1rem;
    background: #16213e;
    border-bottom: 1px solid #0f3460;
}

.content-header h2 {
    margin: 0;
    font-size: 1rem;
    color: #4fc3f7;
}

.content-toggle {
    background: transparent;
    border: none;
    color: #888;
    cursor: pointer;
    padding: 0.25rem;
}

.content-toggle:hover {
    color: #eee;
}

.adventure-content {
    flex: 1;
    padding: 1rem;
    overflow-y: auto;
    line-height: 1.6;
}

.adventure-content h1,
.adventure-content h2,
.adventure-content h3 {
    color: #4fc3f7;
    border-bottom: 1px solid #0f3460;
    padding-bottom: 0.5rem;
    margin-top: 1.5rem;
}

.adventure-content code {
    background: #0d1b2a;
    padding: 0.1rem 0.3rem;
    border-radius: 3px;
    font-family: 'Source Code Pro', monospace;
}

.adventure-content pre {
    background: #0d1b2a;
    padding: 1rem;
    border-radius: 4px;
    overflow-x: auto;
}

/* Responsive */
@media (max-width: 900px) {
    .adventure-main {
        grid-template-columns: 1fr;
        grid-template-rows: 1fr 1fr;
    }
}
```

---

## Widget Integration

### Widget Toggle (added to navigation.js)

```javascript
// Addition to build/site/js/navigation.js

function initAdventureWidget() {
    // Check if adventure is enabled
    const adventureEnabled = localStorage.getItem('cppevo_adventure_enabled') !== 'false';

    // Create toggle button
    const toggle = document.createElement('button');
    toggle.id = 'adventure-widget-toggle';
    toggle.innerHTML = '<i class="fa-solid fa-scroll"></i>';
    toggle.title = 'Open Adventure Mode';
    toggle.setAttribute('aria-label', 'Toggle C++ Adventure Game');

    toggle.addEventListener('click', () => {
        const panel = document.getElementById('adventure-widget-panel');
        if (panel) {
            panel.classList.toggle('open');
            toggle.classList.toggle('active');
        }
    });

    document.body.appendChild(toggle);

    // Create widget panel (lazy-loaded)
    const panel = document.createElement('div');
    panel.id = 'adventure-widget-panel';
    panel.className = 'adventure-widget-panel';
    panel.innerHTML = `
        <div class="widget-header">
            <span>C++ Adventure</span>
            <a href="/adventure/" target="_blank" title="Open full version">
                <i class="fa-solid fa-expand"></i>
            </a>
        </div>
        <div class="widget-terminal" id="widget-terminal"></div>
    `;
    document.body.appendChild(panel);
}

// Add to init()
// initAdventureWidget();
```

### Widget Styles (added to custom.css)

```css
/* Addition to build/site/css/custom.css */

/* Adventure widget toggle */
#adventure-widget-toggle {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: #00a500;
    color: white;
    border: none;
    cursor: pointer;
    font-size: 1.2rem;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    z-index: 1000;
    transition: transform 0.2s, background 0.2s;
}

#adventure-widget-toggle:hover {
    transform: scale(1.1);
    background: #00c700;
}

#adventure-widget-toggle.active {
    background: #16213e;
}

/* Adventure widget panel */
.adventure-widget-panel {
    position: fixed;
    bottom: 80px;
    right: 20px;
    width: 400px;
    height: 500px;
    background: #0d1b2a;
    border: 1px solid #0f3460;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    z-index: 999;
    display: none;
    flex-direction: column;
    overflow: hidden;
}

.adventure-widget-panel.open {
    display: flex;
}

.adventure-widget-panel .widget-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 1rem;
    background: #16213e;
    border-bottom: 1px solid #0f3460;
    color: #eee;
}

.adventure-widget-panel .widget-terminal {
    flex: 1;
    overflow: hidden;
}
```
