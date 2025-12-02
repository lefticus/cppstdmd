# RPG Systems Design

## Character Progression

### Player State

```javascript
const Player = {
    // Identity
    name: "Traveler",           // Customizable
    title: "Novice Programmer", // Changes with level

    // Progression
    level: 1,                   // 1-50
    experience: 0,
    experienceToNext: 100,      // Scales with level

    // Core stats (0-100 scale)
    stats: {
        fundamentals: 10,       // Core language knowledge (basic, lex, expr)
        library: 10,            // Standard library mastery (containers, algorithms)
        metaprogramming: 10,    // Template/constexpr skills (temp, concepts)
        modernCpp: 10           // C++11+ feature knowledge
    },

    // Current state
    currentLocation: "intro",
    currentEra: "n4950",

    // Collections
    inventory: [],
    badges: [],
    certificates: [],

    // Tracking
    sectionsVisited: new Set(),
    sectionsCompleted: new Set(),    // Read fully
    timeTravelsPerformed: 0,
    puzzlesSolved: 0,
    npcsSpokenTo: new Set()
};
```

### Level Progression

| Level Range | Title | Unlocks |
|-------------|-------|---------|
| 1-5 | Novice Programmer | Basic navigation, `look` command |
| 6-10 | Apprentice Developer | Chrono Compass (time travel) |
| 11-15 | Junior Engineer | Fast travel (`warp`) to visited locations |
| 16-20 | Journeyman Coder | Access to advanced sections |
| 21-30 | Senior Developer | Hidden area hints |
| 31-40 | Expert Engineer | All puzzles unlocked |
| 41-45 | Master Architect | Bonus dialogue options |
| 46-50 | Standard Scholar | Secret areas, all content |

### Experience Sources

| Action | XP Reward | Notes |
|--------|-----------|-------|
| Visit new section | 10 | First time only |
| Read section content | 20 | Mark as "completed" |
| Complete quest step | 25-100 | Varies by quest |
| Solve puzzle | 50-200 | Varies by difficulty |
| Discover hidden area | 100 | Rare locations |
| First time travel | 50 | One-time bonus |
| Collect item | 15 | Per unique item |
| Talk to NPC | 10 | First conversation |

### Stat Effects

Stats unlock dialogue options, hints, and some puzzle shortcuts:

```javascript
function getStatBasedHint(player, puzzle) {
    if (puzzle.category === "templates" && player.stats.metaprogramming >= 50) {
        return "Your template mastery reveals: " + puzzle.expertHint;
    }
    return puzzle.basicHint;
}
```

---

## Knowledge Inventory

### Item Categories

| Category | Icon | Description | Example Items |
|----------|------|-------------|---------------|
| Language Scrolls | 📜 | Core language feature knowledge | "RAII Scroll", "Move Semantics Codex" |
| Library Tomes | 📕 | Standard library documentation | "Container Compendium", "Algorithm Atlas" |
| Pattern Crystals | 💎 | Design patterns and idioms | "CRTP Crystal", "Pimpl Stone" |
| Temporal Fragments | ⏳ | Era-specific knowledge | "C++11 Lambda Shard", "Concepts Fragment" |
| Puzzle Keys | 🔑 | Items needed to solve puzzles | "Iterator Category Key" |
| Certificates | 🏆 | Major milestone completions | "Template Master Certificate" |

### Item Structure

```javascript
const Item = {
    id: "copy_elision_scroll",
    name: "Copy Elision Scroll",
    category: "language_scroll",
    rarity: "uncommon",          // common, uncommon, rare, legendary
    description: "Ancient wisdom about how compilers can eliminate copies.",

    // Where to find it
    sourceSection: "class.copy.elision",
    sourceEra: null,             // null = all eras, or specific era

    // Effects when collected
    effects: {
        statBoost: { fundamentals: 2 },
        unlocks: ["class.copy.elision.hidden"],  // Hidden subsection
        questProgress: ["optimization_quest"]
    },

    // Lore text shown on examine
    lore: `"In ancient times, every copy was a burden. Then the wise
    compilers learned to see through unnecessary duplications..."`,

    // Can be used for something?
    usable: false,
    useEffect: null
};
```

### Rarity Distribution

| Rarity | Drop Rate | Stat Boost | Color |
|--------|-----------|------------|-------|
| Common | 60% | +1 | White |
| Uncommon | 25% | +2 | Green |
| Rare | 12% | +3-5 | Blue |
| Legendary | 3% | +5-10 | Purple |

### Inventory Commands

```
> inventory
Inventory (12/50 items):

📜 Language Scrolls (4):
  - RAII Scroll (uncommon)
  - Move Semantics Codex (rare)
  - Copy Elision Scroll (uncommon)
  - Value Categories Tome (common)

💎 Pattern Crystals (2):
  - CRTP Crystal (rare)
  - Pimpl Stone (uncommon)

⏳ Temporal Fragments (3):
  - C++11 Lambda Shard
  - C++14 Generic Lambda Piece
  - C++20 Concepts Fragment

🏆 Certificates (1):
  - Basics Certificate

> examine "Move Semantics Codex"
Move Semantics Codex (rare)
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Found in: class.copy.move
Era: C++11+

"The revolution that changed everything. No longer must we
copy when we can simply... move."

Effects: +5 modernCpp
Unlocks: Move semantics quest line
```

---

## NPC Design

### NPC Types

#### 1. Compiler Spirits (Guides)

Represent different C++ compilers, provide implementation-specific hints.

| NPC | Location | Specialty |
|-----|----------|-----------|
| GCC Ghost | Throughout | GNU extensions, optimization hints |
| Clang Specter | Throughout | Diagnostics, modern features |
| MSVC Wraith | Throughout | Windows-specific, ABI details |

```javascript
const GCCGhost = {
    id: "gcc_ghost",
    name: "GCC Ghost",
    type: "compiler_spirit",
    locations: ["*"],  // Appears anywhere
    appearance: "A translucent figure wearing GNU horns",

    dialogue: {
        greeting: {
            default: "Greetings, traveler. I am the spirit of GCC.",
            "n3337": "Ah, C++11! I remember implementing this...",
            "n4950": "C++23 brings many optimizations I'm proud of."
        },
        topics: {
            "optimization": "Did you know -O3 enables vectorization?",
            "extensions": "I offer many extensions beyond the standard...",
            "warnings": "-Wall -Wextra -Werror is the path to enlightenment."
        }
    }
};
```

#### 2. Concept Personifications (Teachers)

Abstract concepts given form, found in their relevant sections.

| NPC | Location | Teaching Focus |
|-----|----------|----------------|
| RAII Guardian | `mem.res`, `class.dtor` | Resource management |
| Iterator Wanderer | `iterators.*` | Iterator patterns |
| Constexpr Oracle | `dcl.constexpr`, `expr.const` | Compile-time computation |
| Move Master | `class.copy.move` | Move semantics |
| Template Sage | `temp.*` | Template metaprogramming |
| Concept Keeper | `concepts.*` | Concepts and constraints |
| Range Ranger | `ranges.*` | Ranges library |

```javascript
const RAIIGuardian = {
    id: "raii_guardian",
    name: "RAII Guardian",
    type: "concept_personification",
    locations: ["mem.res", "class.dtor", "class.ctor"],
    appearance: "An armored figure holding a smart pointer as a shield",

    dialogue: {
        greeting: {
            "n3337": "Welcome! In these times, unique_ptr and shared_ptr are our finest tools.",
            "n4950": "Greetings! We now have pmr allocators and fancy pointers too."
        },
        topics: {
            "raii": "Resource Acquisition Is Initialization. Never forget: acquire in constructor, release in destructor.",
            "smart_pointers": "unique_ptr for exclusive ownership, shared_ptr for shared, weak_ptr to break cycles.",
            "leaks": "Memory leaks are the enemy. RAII is your shield against them."
        },
        quest_intro: "The memory leaks have grown bold. Will you help contain them?"
    },

    quests: ["memory_guardian_quest"],
    trades: ["smart_pointer_scroll"]  // Can give this item
};
```

#### 3. Historical Figures (Lore NPCs)

Provide background and history (appear in intro areas or special events).

| NPC | Appears In | Role |
|-----|------------|------|
| Bjarne the Founder | `intro`, special events | C++ history, design philosophy |
| Alexander the Librarian | `library`, `containers` | STL history |
| Herb the Modernizer | `class.copy.move`, `temp` | Modern C++ advocate |

#### 4. Bug Creatures (Challenges)

Represent common programming errors, must be "defeated" by solving puzzles.

| Creature | Location | Challenge Type |
|----------|----------|----------------|
| Dangling Pointer Phantom | `basic.life` | Lifetime puzzle |
| Race Condition Wraith | `thread` | Synchronization puzzle |
| Undefined Behavior Beast | Various | UB identification quiz |
| Memory Leak Slime | `mem` | Resource management puzzle |

### NPC Interaction Commands

```
> talk raii guardian
RAII Guardian: "Welcome, traveler! I am the guardian of resources."

> ask about smart pointers
RAII Guardian: "unique_ptr for exclusive ownership, shared_ptr
for shared, weak_ptr to break cycles. These are our weapons
against the Memory Leak Slime."

> ask about quest
RAII Guardian: "The Memory Leak Slime has infested the Utility
Workshop. Defeat it by properly managing these resources..."
[Quest Started: Memory Guardian]
```

---

## Quest System

### Quest Structure

```javascript
const Quest = {
    id: "concepts_journey",
    title: "The Concept Revolution",
    description: "Witness the birth of Concepts and trace their evolution.",
    type: "time_travel",           // exploration, learning, time_travel, puzzle, collection
    difficulty: "medium",          // easy, medium, hard, legendary
    minLevel: 10,                  // Required player level
    prerequisites: ["basic_exploration"],  // Required completed quests

    giver: "concept_keeper",       // NPC who gives the quest
    giverLocation: "concepts",

    steps: [
        {
            id: 1,
            instruction: "Visit the Concept Cathedral in C++17 era",
            type: "visit",
            target: { section: "concepts", era: "n4659" },
            completion: "discover_missing",  // Section doesn't exist
            onComplete: {
                dialogue: "The cathedral does not exist in this era...",
                xp: 25
            }
        },
        {
            id: 2,
            instruction: "Shift to C++20 to witness the cathedral's creation",
            type: "visit",
            target: { section: "concepts", era: "n4861" },
            completion: "visit",
            onComplete: {
                dialogue: "Magnificent! The Concept Cathedral stands tall!",
                xp: 50
            }
        },
        {
            id: 3,
            instruction: "Read about the 'same_as' concept",
            type: "read",
            target: { section: "concepts.lang", era: "n4861" },
            completion: "read_content",
            onComplete: {
                dialogue: "You understand how same_as constrains types.",
                xp: 50,
                item: "same_as_crystal"
            }
        },
        {
            id: 4,
            instruction: "Solve the constraint satisfaction puzzle",
            type: "puzzle",
            target: { puzzle: "constraint_puzzle" },
            onComplete: {
                dialogue: "You have mastered basic constraint logic!",
                xp: 100
            }
        }
    ],

    rewards: {
        experience: 500,
        items: ["concepts_certificate"],
        title: "Concept Explorer",
        unlocks: ["concepts.callable"],  // Hidden section
        statBoost: { metaprogramming: 5 }
    }
};
```

### Quest Types

#### 1. Exploration Quests
Visit a set of related sections.

```javascript
{
    type: "exploration",
    title: "Tour of Container Harbor",
    steps: [
        { instruction: "Visit the Vector Vessel", target: { section: "vector" } },
        { instruction: "Visit the Map Mansion", target: { section: "map" } },
        { instruction: "Visit the Deque Dock", target: { section: "deque" } }
    ]
}
```

#### 2. Learning Quests
Read and understand specific content.

```javascript
{
    type: "learning",
    title: "Understanding Move Semantics",
    steps: [
        { instruction: "Read about rvalue references", target: { section: "dcl.ref" } },
        { instruction: "Read about move constructors", target: { section: "class.copy.move" } },
        { instruction: "Answer the move semantics quiz", target: { puzzle: "move_quiz" } }
    ]
}
```

#### 3. Time Travel Quests
Compare sections across eras.

```javascript
{
    type: "time_travel",
    title: "Lambda Through the Ages",
    steps: [
        { target: { section: "expr.prim.lambda", era: "n3337" } },
        { target: { section: "expr.prim.lambda", era: "n4140" } },
        { target: { section: "expr.prim.lambda", era: "n4861" } }
    ]
}
```

#### 4. Collection Quests
Gather specific items.

```javascript
{
    type: "collection",
    title: "Iterator Category Collection",
    items_required: [
        "input_iterator_scroll",
        "output_iterator_scroll",
        "forward_iterator_scroll",
        "bidirectional_iterator_scroll",
        "random_access_iterator_scroll",
        "contiguous_iterator_scroll"
    ]
}
```

#### 5. Puzzle Quests
Solve a series of related puzzles.

```javascript
{
    type: "puzzle",
    title: "Template Deduction Trials",
    puzzles: [
        "template_argument_deduction_1",
        "template_argument_deduction_2",
        "class_template_argument_deduction"
    ]
}
```

### Quest Journal Commands

```
> journal
Quest Journal
━━━━━━━━━━━━━

Active Quests (2):
  ★ The Concept Revolution [2/4 steps]
    "Shift to C++20 to witness the cathedral's creation"

  ○ Tour of Container Harbor [1/3 steps]
    "Visit the Map Mansion"

Available Quests (3):
  - Lambda Through the Ages (requires: level 10)
  - Template Deduction Trials (requires: Template Tundra visited)
  - Memory Guardian (talk to RAII Guardian)

Completed Quests (5):
  ✓ Welcome to the Standard
  ✓ Basic Exploration
  ...

> quest details "The Concept Revolution"
[Shows full quest info and progress]
```

---

## Puzzle System

### Puzzle Types

#### 1. Code Completion
Fill in missing parts based on the standard.

```javascript
const CodeCompletionPuzzle = {
    id: "vector_push_back",
    type: "code_completion",
    location: "vector.modifiers",
    difficulty: "easy",

    question: "Complete this vector operation:",
    code: `
std::vector<int> v = {1, 2, 3};
v._______(4);  // Add 4 to the end
`,
    answer: "push_back",
    alternateAnswers: ["emplace_back"],
    hint: "Read [[vector.modifiers]] for the answer",

    rewards: { xp: 30 }
};
```

#### 2. Matching/Categorization
Match concepts to their properties.

```javascript
const MatchingPuzzle = {
    id: "iterator_categories",
    type: "matching",
    location: "iterators.general",
    difficulty: "medium",

    question: "Match each iterator category with its key capability:",
    pairs: [
        ["Input Iterator", "Single-pass read"],
        ["Forward Iterator", "Multi-pass"],
        ["Bidirectional Iterator", "Move backwards"],
        ["Random Access Iterator", "O(1) arbitrary access"],
        ["Contiguous Iterator", "Elements stored contiguously"]
    ],
    hint: "Read [[iterator.requirements]] for help",

    rewards: { xp: 50, item: "iterator_mastery_scroll" }
};
```

#### 3. Timeline/Ordering
Arrange features by when they were introduced.

```javascript
const TimelinePuzzle = {
    id: "feature_timeline",
    type: "timeline",
    location: "intro",
    difficulty: "hard",

    question: "Order these features by when they were added to C++:",
    items: [
        { name: "Lambdas", era: "n3337" },
        { name: "Concepts", era: "n4861" },
        { name: "Structured bindings", era: "n4659" },
        { name: "Generic lambdas", era: "n4140" },
        { name: "Ranges", era: "n4861" }
    ],
    // Correct order: Lambdas, Generic lambdas, Structured bindings, Concepts/Ranges

    rewards: { xp: 100, title: "Temporal Scholar" }
};
```

#### 4. True/False Quiz
Answer questions about the standard.

```javascript
const QuizPuzzle = {
    id: "move_semantics_quiz",
    type: "quiz",
    location: "class.copy.move",
    difficulty: "medium",

    questions: [
        {
            q: "A moved-from object is in a valid but unspecified state.",
            a: true,
            explanation: "The standard guarantees validity but not specific values."
        },
        {
            q: "std::move actually moves the object.",
            a: false,
            explanation: "std::move only casts to rvalue reference; actual move happens in the constructor/assignment."
        },
        {
            q: "Move constructors should be noexcept when possible.",
            a: true,
            explanation: "Many standard library operations require noexcept moves for efficiency."
        }
    ],

    passingScore: 2,  // Out of 3
    rewards: { xp: 75 }
};
```

#### 5. Bug Hunt
Find the undefined behavior or error.

```javascript
const BugHuntPuzzle = {
    id: "dangling_reference",
    type: "bug_hunt",
    location: "basic.life",
    difficulty: "hard",

    question: "Find the undefined behavior in this code:",
    code: `
std::string& get_greeting() {
    std::string s = "Hello";
    return s;  // Line to identify
}

int main() {
    std::string& ref = get_greeting();
    std::cout << ref;
}
`,
    answer: {
        line: 3,
        issue: "Returning reference to local variable",
        explanation: "The string 's' is destroyed when the function returns, leaving a dangling reference."
    },

    rewards: { xp: 100, badge: "Bug Hunter" }
};
```

### Puzzle Interface

```
> look puzzle
A mystical puzzle stone glows before you...

Iterator Category Challenge
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Match each iterator category with its key capability:

  1. Input Iterator        A. Elements stored contiguously
  2. Forward Iterator      B. O(1) arbitrary access
  3. Bidirectional         C. Single-pass read
  4. Random Access         D. Multi-pass
  5. Contiguous            E. Move backwards

> solve 1C 2D 3E 4B 5A
Correct! You have mastered iterator categories.
+50 XP
Received: Iterator Mastery Scroll

> hint
The RAII Guardian whispers: "Read [[iterator.requirements]]
for the detailed requirements of each category."
```

---

## Unlockable Areas

### Gate Types

| Gate Type | Requirement | Example |
|-----------|-------------|---------|
| Level Gate | Minimum player level | "Requires Level 20" |
| Knowledge Gate | Specific inventory item | "Requires SFINAE Scroll" |
| Quest Gate | Completed prerequisite quest | "Complete 'Template Basics'" |
| Era Gate | Specific C++ version | "Only accessible in C++20+" |
| Puzzle Gate | Solve guardian puzzle | "Answer the riddle" |

### Hidden Areas

| Area | Requirement | Reward |
|------|-------------|--------|
| Template Metaprogramming Depths | Level 20 + SFINAE Scroll | Legendary items |
| Undefined Behavior Abyss | Complete "Safety Quest" | UB compendium |
| Implementation-Defined Maze | 5 timeshifts in one session | Compiler secrets |
| The Standards Committee Chamber | All certificates | Easter eggs, lore |
| Allocator Catacombs | Talk to all compiler spirits | Memory optimization secrets |

```javascript
const HiddenArea = {
    id: "template_depths",
    name: "Template Metaprogramming Depths",
    parent: "temp.deduct",
    requirements: {
        level: 20,
        items: ["sfinae_scroll"],
        quests: ["template_basics"]
    },
    description: "The deepest mysteries of template instantiation...",
    exclusiveItems: ["expression_sfinae_crystal", "detection_idiom_tome"],
    exclusiveNPC: "template_ancient"
};
```
