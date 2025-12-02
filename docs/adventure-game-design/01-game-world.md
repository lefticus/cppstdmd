# Game World Design

## World Structure

The game world maps directly to the C++ standard's hierarchical structure, with thematic names that make navigation memorable and fun.

### Hierarchy

```
Realm (Chapter)
  └── Zone (Major Section - 1 dot in stable name)
        └── Room (Subsection - 2+ dots in stable name)
```

### Realms

Each top-level chapter becomes a themed "Realm":

| Realm Name | Chapter | Stable Name Prefix | Theme/Description |
|------------|---------|-------------------|-------------------|
| The Foundations | `basic` | `basic.*` | Ancient temple ruins with fundamental laws |
| Lexicon Tower | `lex` | `lex.*` | Tall library/archives with lexical knowledge |
| Expression Fields | `expr` | `expr.*` | Open testing grounds for magical expressions |
| Statement Sanctum | `stmt` | `stmt.*` | Control flow chambers with branching paths |
| Declaration Domain | `dcl` | `dcl.*` | Bureaucratic halls of formal declarations |
| Class Citadel | `class` | `class.*` | Medieval castle with inheritance towers |
| Template Tundra | `temp` | `temp.*` | Frozen crystalline structures, abstract patterns |
| Exception Caverns | `except` | `except.*` | Underground tunnels with try-catch bridges |
| The Standard Library | `library` | `library.*` | Grand entrance hall to the library |
| Utility Workshop | `utilities` | `utilities.*` | Inventor's workshop with tools |
| Container Harbor | `containers` | `container.*`, `array.*`, `vector.*` | Docks with different container ships |
| Algorithm Academy | `algorithms` | `alg.*` | Training grounds for algorithmic arts |
| Iterator Isle | `iterators` | `iterator.*` | Bridge-connected islands |
| Range Frontier | `ranges` | `ranges.*` | New frontier territory (C++20+) |
| Concept Cathedral | `concepts` | `concepts.*` | Grand cathedral (C++20+) |
| Thread Nexus | `thread` | `thread.*` | Multi-dimensional concurrent hub |
| Chrono Clocktower | `time` | `time.*` | Giant clockwork tower |
| Memory Depths | `mem` | `mem.*` | Deep caverns of memory management |
| Input/Output Streams | `input` | `istream.*`, `ostream.*` | Rivers and waterfalls of data |

### Zones (Example: Class Citadel)

Within each Realm, zones correspond to major sections:

| Zone Name | Stable Name | Description |
|-----------|-------------|-------------|
| Member Hall | `class.mem` | Great hall where members gather |
| Duplication Chamber | `class.copy` | Workshops for copy operations |
| Phantom Tower | `class.virtual` | Ethereal tower of virtual functions |
| Inheritance Gates | `class.derived` | Gates connecting to derived classes |
| Constructor Forge | `class.ctor` | Forge where objects are created |
| Destructor Crypt | `class.dtor` | Where objects go to rest |
| Access Control | `class.access` | Guards controlling member access |

### Rooms (Example: Duplication Chamber)

Deeper subsections become individual rooms:

| Room Name | Stable Name | Description |
|-----------|-------------|-------------|
| Copy Constructor Workshop | `class.copy.ctor` | Where copies are crafted |
| Assignment Alcove | `class.copy.assign` | Chamber of assignment operations |
| Move Semantics Lab | `class.copy.move` | Modern laboratory (C++11+) |
| Elision Observatory | `class.copy.elision` | Watch copies vanish |

---

## Navigation Model

### Data Structure

```javascript
const WorldNode = {
    stableName: "class.copy",           // [[class.copy]] from markdown
    displayName: "Duplication Chamber",
    realm: "class",
    parent: "class",                    // Parent stable name
    children: [                         // Child stable names
        "class.copy.ctor",
        "class.copy.assign"
    ],
    connections: {                      // Adjacent sections for cardinal nav
        north: "class.mem",
        south: "class.dtor",
        east: "class.virtual",
        west: null
    },
    availableIn: ["n3337", "n4140", "n4659", "n4861", "n4950", "trunk"],
    description: "Workshops dedicated to the art of object duplication.",
    npcs: ["copy_wizard"],              // NPCs present here
    items: ["copy_elision_scroll"],     // Items that can be found
    puzzles: ["copy_vs_move_quiz"]      // Puzzles available
};
```

### Navigation Commands

| Command | Syntax | Description |
|---------|--------|-------------|
| `look` | `look` | View current location description + rendered markdown |
| `go` | `go <direction>` | Move north/south/east/west to connected section |
| `enter` | `enter <zone>` | Enter a child section |
| `exit` | `exit` or `leave` | Return to parent section |
| `warp` | `warp <stable.name>` | Fast travel to any visited location |
| `map` | `map` | Show current realm overview |
| `where` | `where` or `whereami` | Show current location in hierarchy |

### Connection Generation

Connections between sections are inferred from:
1. **Document order** - Sequential sections connect north/south
2. **Hierarchy** - Parent/child relationships connect via enter/exit
3. **Cross-references** - `[[stable.name]]` links create east/west connections
4. **Thematic grouping** - Related sections cluster together

```python
def generate_connections(sections: list[str]) -> dict:
    """Generate navigation connections between sections."""
    connections = {}

    for i, section in enumerate(sections):
        connections[section] = {
            "north": sections[i-1] if i > 0 else None,
            "south": sections[i+1] if i < len(sections)-1 else None,
            "east": None,  # Filled from cross-references
            "west": None   # Filled from cross-references
        }

    return connections
```

---

## Time Travel Mechanics

### The Chrono Compass

Players receive this artifact after completing the tutorial (visiting 5 sections).

**Capabilities:**
- Shift between C++ eras: C++11, C++14, C++17, C++20, C++23, C++26
- View section content as it existed in each era
- Some sections only exist in certain eras
- NPCs have era-appropriate dialogue

### Era Identifiers

| Era Name | Tag | Year | Key Features |
|----------|-----|------|--------------|
| C++11 | `n3337` | 2011 | Move semantics, lambdas, auto |
| C++14 | `n4140` | 2014 | Generic lambdas, relaxed constexpr |
| C++17 | `n4659` | 2017 | Structured bindings, if constexpr |
| C++20 | `n4861` | 2020 | Concepts, ranges, coroutines |
| C++23 | `n4950` | 2023 | std::expected, deducing this |
| C++26 | `trunk` | 2026 | Working draft |

### Time Travel Command

```
> timeshift cpp20
*The world ripples as you shift through time...*

[C++20] You are in the Concept Cathedral [[concepts]]
The grand cathedral stands before you, its spires reaching toward
the sky of constrained templates. This magnificent structure was
built in this very era.

Exits: south to Library Entrance
You see: The Concept Guardian (NPC)
```

### Era-Specific Effects

1. **Missing Locations**: Some sections don't exist in older eras
   ```
   > timeshift cpp11
   > warp concepts
   The Concept Cathedral does not exist in this era.
   It will be built in C++20.
   ```

2. **Changed Content**: `look` shows era-appropriate content from that version's markdown

3. **NPC Dialogue**: NPCs reference era-appropriate features
   ```
   [C++11] Copy Wizard: "Move semantics are revolutionary!
   Finally we can transfer resources efficiently."

   [C++20] Copy Wizard: "Move semantics? That's old news.
   Have you seen what concepts can do?"
   ```

4. **Temporal Artifacts**: Some items exist differently across eras (collectibles)

### Time Travel Quests

Example quest requiring time travel:

```javascript
const Quest = {
    id: "lambda_evolution",
    title: "The Lambda Chronicles",
    description: "Trace the evolution of lambdas through the ages.",
    steps: [
        {
            instruction: "Visit expr.prim.lambda in C++11 to witness their birth",
            target: { section: "expr.prim.lambda", era: "n3337" }
        },
        {
            instruction: "See generic lambdas emerge in C++14",
            target: { section: "expr.prim.lambda", era: "n4140" }
        },
        {
            instruction: "Discover constexpr lambdas in C++17",
            target: { section: "expr.prim.lambda", era: "n4659" }
        },
        {
            instruction: "Witness template lambdas in C++20",
            target: { section: "expr.prim.lambda", era: "n4861" }
        }
    ],
    rewards: {
        experience: 500,
        item: "lambda_mastery_crystal",
        title: "Lambda Historian"
    }
};
```

---

## Location Descriptions

Each location has multiple description components:

```javascript
const LocationDescription = {
    // Static atmospheric description
    atmosphere: "Ancient stone walls covered in fundamental runes...",

    // Dynamic based on player state
    dynamic: (player) => {
        if (player.hasItem("torch")) {
            return "Your torch reveals hidden inscriptions.";
        }
        return "The shadows hide many secrets.";
    },

    // Exits listing
    exits: ["north to Member Hall", "south to Destructor Crypt"],

    // NPCs present
    npcs: ["The Copy Wizard stands by the workbench."],

    // Items visible
    items: ["A glowing scroll lies on the table."],

    // Era-specific additions
    eraEffects: {
        "n3337": "The room feels young, full of new possibilities.",
        "n4950": "Years of refinement show in every detail."
    }
};
```

### Sample Location Output

```
[C++23] Duplication Chamber [[class.copy]]
========================================

You stand in the Duplication Chamber, where the arts of copying
and moving are practiced. Workbenches line the walls, each
dedicated to different copy operations.

In this modern era, move semantics have largely replaced the
older copy traditions, though both are still honored.

Exits: north to Member Hall, south to Destructor Crypt,
       east to Phantom Tower
       enter: Copy Constructor Workshop, Assignment Alcove

You see:
  - The Copy Wizard (NPC)
  - Copy Elision Scroll (item)

> look content
[Displays rendered markdown of [[class.copy]] section]
```
