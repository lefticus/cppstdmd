# Content Format Specification

This document defines the human-editable format for adventure game content. All game entities (NPCs, quests, items, puzzles) are defined in YAML files, making it easy for contributors to expand the game without modifying code.

---

## Overview

### Data-Driven Design

The adventure game uses a **hybrid content system**:

1. **Auto-generated content** - World map, navigation, and basic items are extracted from the C++ standard markdown files
2. **Hand-crafted content** - NPCs, quests, puzzles, and special items are defined in YAML files

Hand-crafted content **merges with and overrides** auto-generated content, allowing rich customization while maintaining a baseline from the standard's structure.

### Production Directory Structure

When implemented, the game content lives at the project root:

```
game-content/
├── npcs/
│   ├── compiler-spirits.yaml      # GCC Ghost, Clang Specter, MSVC Wraith
│   ├── concept-guides.yaml        # RAII Guardian, Template Sage, etc.
│   └── historical-figures.yaml    # Bjarne, Alexander, Herb
│
├── quests/
│   ├── exploration/
│   │   └── container-tour.yaml
│   ├── time-travel/
│   │   └── lambda-chronicles.yaml
│   ├── learning/
│   │   └── move-semantics.yaml
│   └── collection/
│       └── iterator-scrolls.yaml
│
├── items/
│   ├── scrolls.yaml               # Language knowledge scrolls
│   ├── crystals.yaml              # Pattern crystals
│   ├── tomes.yaml                 # Library tomes
│   └── certificates.yaml          # Achievement certificates
│
├── puzzles/
│   ├── matching/
│   │   └── iterator-categories.yaml
│   ├── timeline/
│   │   └── feature-ordering.yaml
│   ├── quiz/
│   │   └── move-semantics-quiz.yaml
│   └── code-completion/
│       └── vector-operations.yaml
│
└── realms.yaml                    # Realm themes and descriptions
```

### Validation

JSON Schema files are provided for IDE autocomplete and validation. Configure your editor to use them:

```yaml
# yaml-language-server: $schema=./schemas/npc.schema.json
npcs:
  - id: example_npc
    ...
```

---

## Content Types

### NPCs

NPCs (Non-Player Characters) provide dialogue, hints, quests, and items.

**File location:** `game-content/npcs/*.yaml`

#### NPC Types

| Type | Description | Example |
|------|-------------|---------|
| `compiler_spirit` | Compiler personifications, appear everywhere | GCC Ghost |
| `concept_personification` | Abstract concepts given form | RAII Guardian |
| `historical_figure` | C++ history and lore | Bjarne |
| `bug_creature` | Challenges to overcome | Memory Leak Slime |

#### Schema

```yaml
npcs:
  - id: string                    # Unique identifier (snake_case)
    name: string                  # Display name
    type: string                  # One of the types above
    appearance: string            # Visual description (optional)
    locations:                    # Where the NPC can be found
      - stable.name               # Use "*" for everywhere

    dialogue:
      greeting:                   # Said when player uses "talk" command
        default: string           # Default greeting
        n3337: string             # Era-specific (optional)
        n4950: string

      topics:                     # Responses to "ask about X"
        topic_name: string        # Topic key → response text

    quests:                       # Quest IDs this NPC gives (optional)
      - quest_id

    trades:                       # Item IDs this NPC can give (optional)
      - item_id
```

#### Example

```yaml
npcs:
  - id: raii_guardian
    name: RAII Guardian
    type: concept_personification
    appearance: An armored figure holding a smart pointer as a shield
    locations:
      - mem.res
      - class.dtor
      - class.ctor

    dialogue:
      greeting:
        default: Welcome, traveler! I am the guardian of resources.
        n3337: |
          Welcome to C++11! unique_ptr and shared_ptr are
          our finest new tools against memory leaks.
        n4950: |
          Greetings! We now have pmr allocators, fancy pointers,
          and std::expected for error handling.

      topics:
        raii: |
          Resource Acquisition Is Initialization. Never forget:
          acquire in constructor, release in destructor.
        smart_pointers: |
          unique_ptr for exclusive ownership,
          shared_ptr for shared ownership,
          weak_ptr to break cycles.
        leaks: |
          Memory leaks are the enemy. RAII is your shield.
          Let destructors do the cleanup automatically.

    quests:
      - memory_guardian_quest

    trades:
      - smart_pointer_scroll
```

---

### Quests

Quests are multi-step objectives with rewards.

**File location:** `game-content/quests/<type>/*.yaml`

#### Quest Types

| Type | Description | Example |
|------|-------------|---------|
| `exploration` | Visit a set of sections | Tour of Container Harbor |
| `time_travel` | Compare sections across eras | Lambda Chronicles |
| `learning` | Read and understand content | Move Semantics Mastery |
| `collection` | Gather specific items | Iterator Scroll Collection |
| `puzzle` | Solve related puzzles | Template Deduction Trials |

#### Step Target Types

| Target | Fields | Description |
|--------|--------|-------------|
| Visit section | `section` | Go to a location |
| Visit in era | `section`, `era` | Go to location in specific C++ version |
| Read content | `section`, `read: true` | View section content with `look` |
| Solve puzzle | `puzzle` | Complete a puzzle |
| Collect item | `item` | Obtain a specific item |
| Talk to NPC | `npc`, `topic` | Ask NPC about a topic |

#### Schema

```yaml
id: string                        # Unique identifier (snake_case)
title: string                     # Display title
description: string               # Quest description
type: string                      # One of the types above
difficulty: easy | medium | hard | legendary
minLevel: number                  # Required player level (optional)
prerequisites:                    # Required completed quests (optional)
  - quest_id

giver: string                     # NPC who gives quest (optional)
giverLocation: string             # Where to find the giver (optional)

steps:
  - instruction: string           # Shown to player
    target:
      section: stable.name        # Section to visit
      era: n3337 | n4950 | ...    # Required era (optional)
      read: boolean               # Must read content (optional)
      puzzle: puzzle_id           # Puzzle to solve (optional)
      item: item_id               # Item to collect (optional)
      npc: npc_id                 # NPC to talk to (optional)
      topic: string               # Topic to ask about (optional)
    onComplete:                   # Triggered when step completes (optional)
      dialogue: string            # Message shown
      xp: number                  # Bonus XP for this step
      item: item_id               # Item given

rewards:
  experience: number              # Total XP reward
  items:                          # Items given on completion
    - item_id
  title: string                   # Player title unlocked (optional)
  statBoost:                      # Stat increases (optional)
    fundamentals: number
    library: number
    metaprogramming: number
    modernCpp: number
  unlocks:                        # Hidden sections unlocked (optional)
    - stable.name
```

#### Example

```yaml
id: lambda_evolution
title: The Lambda Chronicles
description: Trace the evolution of lambdas through C++ history.
type: time_travel
difficulty: medium
minLevel: 10
prerequisites:
  - basic_exploration

giver: template_sage
giverLocation: expr.prim.lambda

steps:
  - instruction: Visit expr.prim.lambda in C++11 to witness lambda's birth
    target:
      section: expr.prim.lambda
      era: n3337
    onComplete:
      dialogue: |
        Lambdas! A revolutionary way to write inline functions.
        Notice the capture syntax with square brackets.
      xp: 50

  - instruction: See generic lambdas emerge in C++14
    target:
      section: expr.prim.lambda
      era: n4140
    onComplete:
      dialogue: |
        With auto parameters, lambdas become truly generic.
        No more writing out explicit types!
      xp: 75

  - instruction: Witness template lambdas in C++20
    target:
      section: expr.prim.lambda
      era: n4861
    onComplete:
      dialogue: |
        Template syntax in lambdas - the circle is complete.
        Lambdas can now have explicit template parameters.
      xp: 100
      item: lambda_template_shard

rewards:
  experience: 500
  items:
    - lambda_mastery_crystal
  title: Lambda Historian
  statBoost:
    modernCpp: 5
```

---

### Items

Items are collectible knowledge objects with effects.

**File location:** `game-content/items/*.yaml`

#### Item Categories

| Category | Icon | Description |
|----------|------|-------------|
| `language_scroll` | 📜 | Core language feature knowledge |
| `library_tome` | 📕 | Standard library documentation |
| `pattern_crystal` | 💎 | Design patterns and idioms |
| `temporal_fragment` | ⏳ | Era-specific knowledge |
| `puzzle_key` | 🔑 | Items needed to solve puzzles |
| `certificate` | 🏆 | Major milestone completions |

#### Rarity

| Rarity | Drop Rate | Typical Stat Boost |
|--------|-----------|-------------------|
| `common` | 60% | +1 |
| `uncommon` | 25% | +2 |
| `rare` | 12% | +3-5 |
| `legendary` | 3% | +5-10 |

#### Schema

```yaml
items:
  - id: string                    # Unique identifier (snake_case)
    name: string                  # Display name
    category: string              # One of the categories above
    rarity: common | uncommon | rare | legendary
    description: string           # Short description
    lore: string                  # Detailed text for "examine" (optional)

    sourceSection: stable.name    # Where to find it (optional)
    sourceQuest: quest_id         # Quest that rewards it (optional)
    sourceEra: n3337 | n4950      # Only in specific era (optional)

    effects:
      statBoost:                  # Stats increased on pickup (optional)
        fundamentals: number
        library: number
        metaprogramming: number
        modernCpp: number
      unlocks:                    # Sections unlocked (optional)
        - stable.name
      questProgress:              # Quests advanced (optional)
        - quest_id

    usable: boolean               # Can be "used" (optional, default false)
    useEffect: string             # What happens on use (optional)
```

#### Example

```yaml
items:
  - id: raii_scroll
    name: RAII Scroll
    category: language_scroll
    rarity: uncommon
    description: Fundamental wisdom about resource management.
    lore: |
      "In ancient times, resources were managed by hand,
       leading to leaks and corruption. Then came RAII:
       acquire in constructor, release in destructor.
       The destructor always runs. Always."

    sourceSection: class.dtor

    effects:
      statBoost:
        fundamentals: 2

  - id: lambda_mastery_crystal
    name: Lambda Mastery Crystal
    category: pattern_crystal
    rarity: rare
    description: Crystallized understanding of lambda expressions.
    lore: |
      "From simple captures to generic templates,
       the lambda evolved into one of C++'s most
       powerful tools for functional programming."

    sourceQuest: lambda_evolution

    effects:
      statBoost:
        modernCpp: 5
```

---

### Puzzles

Puzzles are interactive challenges based on standard content.

**File location:** `game-content/puzzles/<type>/*.yaml`

#### Puzzle Types

| Type | Description | Answer Format |
|------|-------------|---------------|
| `matching` | Match pairs | `1A 2B 3C` |
| `timeline` | Order by date | `A B C D` |
| `quiz` | True/false questions | `T F T` |
| `code_completion` | Fill in blanks | Text answer |
| `bug_hunt` | Find the error | Line number |

#### Schema

```yaml
id: string                        # Unique identifier
type: string                      # One of the types above
location: stable.name             # Where puzzle is found
difficulty: easy | medium | hard
minLevel: number                  # Required level (optional)

question: string                  # Main question text

# Type-specific fields:

# For matching:
pairs:
  - [left, right]

# For timeline:
items:
  - name: string
    era: n3337 | n4140 | ...

# For quiz:
questions:
  - q: string
    a: boolean
    explanation: string           # Shown after answer

# For code_completion:
code: string                      # Code with ______ blanks
answer: string
alternateAnswers:                 # Other accepted answers
  - string

# For bug_hunt:
code: string
answer:
  line: number
  issue: string
  explanation: string

hints:                            # Progressive hints (optional)
  - string
  - string

rewards:
  xp: number
  item: item_id                   # Optional item reward
  badge: string                   # Optional badge name
  statBoost:
    stat_name: number
```

#### Example

```yaml
id: iterator_categories
type: matching
location: iterators.requirements
difficulty: medium

question: |
  Match each iterator category with its key capability:

pairs:
  - [Input Iterator, Single-pass read]
  - [Forward Iterator, Multi-pass traversal]
  - [Bidirectional Iterator, Move backwards]
  - [Random Access Iterator, O(1) arbitrary access]
  - [Contiguous Iterator, Elements stored contiguously]

hints:
  - Read [[iterator.requirements]] for the detailed requirements.
  - Think about what operations each category supports.

rewards:
  xp: 50
  item: iterator_mastery_scroll
  statBoost:
    library: 2
```

---

### Realms

Realm definitions provide theming for top-level chapters.

**File location:** `game-content/realms.yaml`

#### Schema

```yaml
realms:
  realm_key:                      # First part of stable name (e.g., "class")
    name: string                  # Display name
    description: string           # Atmospheric description
    theme: string                 # One-word theme (optional)
    ambiance: string              # Environmental details (optional)
```

#### Example

```yaml
realms:
  basic:
    name: The Foundations
    description: Ancient temple ruins inscribed with fundamental laws
    theme: ancient
    ambiance: |
      Stone tablets line the walls, each bearing a core truth
      of the language. The air hums with primordial definitions.

  class:
    name: Class Citadel
    description: Medieval castle with towers of inheritance
    theme: medieval
    ambiance: |
      Banners bearing class hierarchies hang from the battlements.
      The sound of constructors forging echoes from the depths.

  temp:
    name: Template Tundra
    description: Frozen crystalline structures of abstract patterns
    theme: arctic
    ambiance: |
      Ice formations take the shape of template parameters.
      Each crystal reflects infinite instantiation possibilities.

  concepts:
    name: Concept Cathedral
    description: Grand cathedral of constraints and requirements
    theme: gothic
    ambiance: |
      Stained glass windows depict constraint expressions.
      This magnificent structure was built in the C++20 era.
```

---

## Integration Flow

```
game-content/*.yaml  ──┐
                       ├──▶ generate_html_site.py ──▶ build/site/data/game/*.json
Markdown sections    ──┘    (load, merge, validate)
```

### Processing Order

1. **Extract sections** from markdown files (auto-generate world map)
2. **Load YAML files** from `game-content/`
3. **Merge content** - hand-crafted overrides auto-generated
4. **Validate** against JSON schemas
5. **Output JSON** to `build/site/data/game/`

### Merge Rules

| Content Type | Auto-generated | Hand-crafted |
|--------------|----------------|--------------|
| Sections | Yes (from markdown) | Descriptions only |
| NPCs | No | Yes (fully) |
| Items | Basic scrolls | Rich items |
| Quests | Simple exploration | All quest types |
| Puzzles | No | Yes (fully) |

---

## Contributor Guidelines

### Adding an NPC

1. Choose the appropriate file in `game-content/npcs/`
2. Add entry following the schema
3. Set `locations` to relevant stable names
4. Write era-specific dialogue for key eras
5. Reference any quests or items they provide

### Adding a Quest

1. Create a new file in `game-content/quests/<type>/`
2. Define clear step instructions
3. Use existing section stable names for targets
4. Set appropriate difficulty and level requirements
5. Balance rewards with difficulty

### Adding an Item

1. Add to appropriate file in `game-content/items/`
2. Choose category and rarity
3. Write engaging lore text
4. Set reasonable stat effects
5. Link to source section or quest

### Adding a Puzzle

1. Create file in `game-content/puzzles/<type>/`
2. Ensure answer is verifiable from standard
3. Provide helpful progressive hints
4. Test that the puzzle is solvable
5. Balance rewards appropriately

---

## Examples

See `game-content-examples/` in this documentation folder for complete working examples of each content type.
