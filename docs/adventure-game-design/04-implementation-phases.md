# Implementation Phases

This document breaks down the adventure game implementation into 10 phases, each building on the previous. The game becomes playable after Phase 3.

---

## Phase Overview

| Phase | Name | Core Deliverable | Dependencies |
|-------|------|------------------|--------------|
| 1 | Terminal Foundation | Working terminal UI with navigation | None |
| 2 | Content Integration | Markdown displayed in side panel | Phase 1 |
| 3 | Time Travel | Era switching works | Phase 2 |
| 4 | Player System | Levels, stats, saving | Phase 1 |
| 5 | Inventory | Collectible items | Phase 4 |
| 6 | NPCs | Interactive characters | Phase 2 |
| 7 | Quest System | Trackable objectives | Phase 4, 5 |
| 8 | Puzzles | Interactive challenges | Phase 2 |
| 9 | Widget | Embeddable on all pages | Phase 3 |
| 10 | Polish | Accessibility, mobile, tutorial | All |

---

## Phase 1: Terminal & Navigation Foundation

**Goal**: Create a working terminal interface with basic world navigation.

### Tasks

- [ ] **1.1 Create template structure**
  - Create `templates/adventure.html` with split-screen layout
  - Add basic CSS in `build/site/css/adventure.css`
  - Add Font Awesome and base fonts

- [ ] **1.2 Implement Terminal UI** (`terminal.js`)
  - Render terminal with output area and input field
  - Handle Enter key for command submission
  - Implement command history (up/down arrows)
  - Auto-scroll output
  - Focus management

- [ ] **1.3 Generate world map data**
  - Add `generate_adventure_data()` to `generate_html_site.py`
  - Extract sections from markdown files
  - Build `world-map.json` with navigation graph
  - Generate realm themes and display names

- [ ] **1.4 Implement World module** (`world.js`)
  - Load `world-map.json`
  - `getSection(stableName)` - get section data
  - `getExits(section)` - list available directions
  - `getChildren(section)` - list enterable subsections

- [ ] **1.5 Implement core commands**
  - `look` - show current location description
  - `go <direction>` - move north/south/east/west
  - `enter <zone>` - enter child section
  - `exit` - return to parent
  - `where` - show current location
  - `help` - list commands

- [ ] **1.6 Wire up game engine** (`game.js`)
  - Initialize modules
  - Command routing
  - Basic game loop

### Deliverables

- `/adventure/index.html` - playable terminal
- `build/site/data/game/world-map.json` - generated navigation data
- Basic navigation working

### Verification

```
> look
You are in the Introduction [[intro]]
Exits: south to Lexical Conventions

> go south
You travel south...
You are in Lexical Conventions [[lex]]

> where
Introduction > Lexical Conventions [[lex]]
```

---

## Phase 2: Content Integration

**Goal**: Display actual C++ standard markdown in the content panel.

### Tasks

- [ ] **2.1 Implement MarkdownLoader** (`markdown-loader.js`)
  - Fetch markdown files from version directories
  - Extract section content by stable name anchor
  - Cache loaded content
  - Handle missing sections gracefully

- [ ] **2.2 Add marked.js for rendering**
  - Include from CDN
  - Configure for GitHub-flavored markdown
  - Handle code blocks

- [ ] **2.3 Add Prism.js for syntax highlighting**
  - Include from CDN with C++ language support
  - Style code blocks appropriately
  - Handle inline code

- [ ] **2.4 Create ContentPanel component**
  - Render markdown in right panel
  - Update title with section name
  - Show loading state
  - Handle errors (section not found)

- [ ] **2.5 Integrate with `look` command**
  - Load section content on `look`
  - Display in content panel
  - Show stable name and era indicator

- [ ] **2.6 Add `look content` variant**
  - `look` - show location description
  - `look content` - show full markdown

### Deliverables

- Working markdown display
- Syntax-highlighted code blocks
- Section content visible in split view

### Verification

```
> look
[C++23] Class Citadel [[class]]
[Content panel shows rendered class.md section]

> look content
[Full markdown of [[class]] section displayed]
```

---

## Phase 3: Time Travel

**Goal**: Players can switch between C++ eras and see different content.

### Tasks

- [ ] **3.1 Implement TimeTravel module** (`time-travel.js`)
  - `shift(era)` - change current era
  - `getEraName(tag)` - "C++23" from "n4950"
  - `getAvailableEras()` - list all eras
  - Validate era transitions

- [ ] **3.2 Update world navigation for eras**
  - Check `availableIn` before allowing movement
  - Show "doesn't exist in this era" for missing sections
  - Track sections that appear/disappear

- [ ] **3.3 Update MarkdownLoader for eras**
  - Load from era-specific directory
  - Handle missing sections per era

- [ ] **3.4 Add era indicator to UI**
  - Show current era in header badge
  - Update on timeshift

- [ ] **3.5 Implement `timeshift` command**
  - Parse era aliases (cpp11, cpp14, cpp17, cpp20, cpp23, cpp26)
  - Show transition effect message
  - Reload current section content

- [ ] **3.6 Add visual transition effect**
  - Brief animation/message on era change
  - Update terminal color scheme subtly per era (optional)

### Deliverables

- Working time travel between all eras
- Era-specific content display
- Missing section handling

### Verification

```
> timeshift cpp11
*The world ripples as you shift through time...*
[C++11] You are in Class Citadel [[class]]

> go concepts
That area doesn't exist in C++11.
It will be built in C++20.

> timeshift cpp20
> go concepts
You travel to Concept Cathedral...
[C++20] Concept Cathedral [[concepts]]
```

---

## Phase 4: Player System

**Goal**: Character progression with levels, stats, and persistent saves.

### Tasks

- [ ] **4.1 Implement SaveSystem** (`save-system.js`)
  - Save to localStorage
  - Load with version migration
  - Default state generation
  - Export/import JSON files

- [ ] **4.2 Implement Player module** (`player.js`)
  - Player state management
  - `moveTo(section)` - update location
  - `gainExperience(amount)` - add XP
  - `levelUp()` - check and apply level up
  - `getStat(name)` - get stat value

- [ ] **4.3 Experience and leveling**
  - XP for visiting new sections
  - XP for reading content
  - Level thresholds
  - Title changes per level range

- [ ] **4.4 Stats system**
  - 4 core stats: fundamentals, library, metaprogramming, modernCpp
  - Stat boosts from items
  - Stat checks for hints

- [ ] **4.5 Implement player commands**
  - `stats` - show current stats
  - `save` - force save
  - `load` - reload from save (with confirmation)

- [ ] **4.6 Add player status to UI**
  - Level badge in header
  - Update on level up
  - Optional: XP progress bar

- [ ] **4.7 Auto-save**
  - Save after each command
  - Load on page open

### Deliverables

- Persistent player state
- Working level system
- Stats display

### Verification

```
> stats
Traveler - Level 3 (Novice Programmer)
XP: 245/300

Stats:
  Fundamentals: 12
  Library: 10
  Metaprogramming: 10
  Modern C++: 15

Sections visited: 15
Sections completed: 8

[Refresh page, state persists]
```

---

## Phase 5: Inventory & Items

**Goal**: Collectible knowledge items with effects.

### Tasks

- [ ] **5.1 Generate items data**
  - Add `generate_items()` to `generate_html_site.py`
  - Create items from notable sections
  - Assign rarities
  - Define stat effects

- [ ] **5.2 Implement Inventory module** (`inventory.js`)
  - Add/remove items
  - Check for item
  - Get items by category
  - Apply item effects

- [ ] **5.3 Implement item commands**
  - `inventory` - list items by category
  - `examine <item>` - show item details
  - `take <item>` - pick up item at location

- [ ] **5.4 Item collection triggers**
  - Items appear at specific sections
  - Collected on first visit or explicit `take`
  - One-time collection

- [ ] **5.5 Item effects**
  - Stat boosts on collection
  - Unlock hidden sections (for Phase 7 gates)

- [ ] **5.6 Display item notifications**
  - "You found: [Item Name]" on collection
  - Rarity color coding

### Deliverables

- `items.json` generated data
- Working inventory system
- Item collection working

### Verification

```
> look
...
Items here: Copy Elision Scroll (uncommon)

> take scroll
You pick up the Copy Elision Scroll.
+2 Fundamentals

> inventory
Inventory (3/50):
📜 Language Scrolls:
  - Copy Elision Scroll (uncommon)
  - RAII Scroll (common)
💎 Pattern Crystals:
  - CRTP Crystal (rare)

> examine "Copy Elision Scroll"
Copy Elision Scroll (uncommon)
Found in: class.copy.elision
"Ancient wisdom about compiler copy elimination..."
```

---

## Phase 6: NPCs

**Goal**: Interactive characters that provide hints and lore.

### Tasks

- [ ] **6.1 Generate NPC data**
  - Add `generate_npcs()` to `generate_html_site.py`
  - Create compiler spirits
  - Create concept personifications
  - Assign to locations

- [ ] **6.2 Implement NPC module** (`npcs.js`)
  - Load NPC data
  - `getNPC(id)` - get NPC by ID
  - `getNPCsAt(section)` - get NPCs at location
  - `getDialogue(npc, topic, era)` - get era-specific dialogue

- [ ] **6.3 Era-specific dialogue**
  - Different greetings per era
  - Different topic responses per era
  - Track NPC interactions

- [ ] **6.4 Implement NPC commands**
  - `talk <npc>` - start conversation
  - `ask about <topic>` - ask current NPC about topic
  - `topics` - list available topics

- [ ] **6.5 Display NPCs in location**
  - Show NPCs on `look`
  - Show NPC dialogue in terminal

- [ ] **6.6 NPC knowledge trades**
  - Some NPCs give items
  - Track given items

### Deliverables

- `npcs.json` generated data
- Working NPC conversations
- Era-specific dialogue

### Verification

```
> look
...
You see: RAII Guardian (NPC)

> talk raii guardian
RAII Guardian: "Welcome to the Memory Depths! I am the
guardian of resources."

> ask about smart pointers
RAII Guardian: "unique_ptr for exclusive ownership,
shared_ptr for shared, weak_ptr to break cycles."

> timeshift cpp03
> talk raii guardian
RAII Guardian: "In these ancient times, we must manually
manage resources. auto_ptr is... problematic."
```

---

## Phase 7: Quest System

**Goal**: Trackable objectives with rewards.

### Tasks

- [ ] **7.1 Generate quest data**
  - Add `generate_quests()` to `generate_html_site.py`
  - Create exploration quests per realm
  - Create time travel quests
  - Create collection quests

- [ ] **7.2 Implement Quest module** (`quests.js`)
  - Load quest data
  - `getAvailableQuests(player)` - quests player can start
  - `getActiveQuests()` - currently active
  - `checkProgress(quest, action)` - update progress
  - `completeQuest(quest)` - apply rewards

- [ ] **7.3 Quest triggers**
  - Start quest from NPC dialogue
  - Auto-track progress on actions
  - Complete step on matching action

- [ ] **7.4 Quest rewards**
  - Experience points
  - Items
  - Titles
  - Section unlocks

- [ ] **7.5 Implement quest commands**
  - `journal` - list active/available quests
  - `quest <name>` - show quest details
  - `abandon <quest>` - drop active quest

- [ ] **7.6 Quest notifications**
  - "Quest Started: [Name]"
  - "Quest Progress: [Step]"
  - "Quest Complete! [Rewards]"

### Deliverables

- `quests.json` generated data
- Working quest tracking
- Reward system

### Verification

```
> journal
Active Quests:
  ★ Tour of Container Harbor [1/3]
    "Visit the Map Mansion"

Available Quests:
  - Lambda Through the Ages (Level 10+)
  - Template Basics (visit Template Tundra)

> go map
You travel to Map Mansion...
Quest Progress: Tour of Container Harbor [2/3]

[After completing all steps]
Quest Complete: Tour of Container Harbor!
+100 XP
Received: Container Explorer Badge
```

---

## Phase 8: Puzzles

**Goal**: Interactive challenges based on standard content.

### Tasks

- [ ] **8.1 Generate puzzle data**
  - Add `generate_puzzles()` to `generate_html_site.py`
  - Create matching puzzles
  - Create timeline puzzles
  - Create quiz puzzles
  - Create code completion puzzles

- [ ] **8.2 Implement Puzzle module** (`puzzles.js`)
  - Load puzzle data
  - `getPuzzleAt(section)` - get puzzle for location
  - `checkAnswer(puzzle, answer)` - validate
  - `getHint(puzzle)` - provide hint

- [ ] **8.3 Puzzle presentation**
  - Display puzzle question in terminal
  - Show options for matching/quiz
  - Handle free-form input for code completion

- [ ] **8.4 Implement puzzle commands**
  - `puzzle` - start puzzle at current location
  - `solve <answer>` - submit answer
  - `hint` - get hint (may cost stat points)

- [ ] **8.5 Puzzle rewards**
  - XP for correct answers
  - Items for some puzzles
  - Badges for puzzle completion streaks

- [ ] **8.6 Error handling**
  - "Try again" for wrong answers
  - Track attempts
  - Progressive hints

### Deliverables

- `puzzles.json` generated data
- Working puzzle system
- Multiple puzzle types

### Verification

```
> puzzle
Iterator Category Challenge
Match each category with its capability:
  1. Input Iterator       A. O(1) access
  2. Forward Iterator     B. Single-pass
  3. Random Access        C. Multi-pass

> solve 1B 2C 3A
Correct! +50 XP
You understand iterator categories better.
+2 Library

> hint
Read [[iterator.requirements]] for help.
```

---

## Phase 9: Widget Integration

**Goal**: Embeddable game widget on all site pages.

### Tasks

- [ ] **9.1 Create widget toggle button**
  - Add to `navigation.js`
  - Fixed position bottom-right
  - Scroll icon
  - Toggle panel visibility

- [ ] **9.2 Create widget panel**
  - Collapsible panel with terminal
  - Smaller than full page
  - Link to open full version

- [ ] **9.3 Widget terminal**
  - Reuse Terminal class
  - Smaller font size
  - Limited height with scroll

- [ ] **9.4 State synchronization**
  - Widget and standalone share localStorage
  - Same player progress
  - Context-aware: could auto-go to current page's section

- [ ] **9.5 Add to existing pages**
  - Update `_footer.html` or add to all templates
  - Only load scripts when widget is opened (lazy load)

- [ ] **9.6 Responsive widget**
  - Hide on very small screens
  - Adjust size on tablet

### Deliverables

- Floating widget button on all pages
- Working mini-terminal
- State sync with full page

### Verification

- Open diff page
- Click scroll button
- Widget opens with working terminal
- Progress syncs with /adventure/ page

---

## Phase 10: Polish

**Goal**: Accessibility, mobile support, tutorial, and final touches.

### Tasks

- [ ] **10.1 Keyboard navigation**
  - Vim-style navigation (h/j/k/l optional)
  - Tab through interactive elements
  - Escape to close panels

- [ ] **10.2 Accessibility**
  - ARIA labels on all interactive elements
  - Screen reader announcements for game events
  - High contrast mode support
  - Skip links

- [ ] **10.3 Mobile responsive**
  - Stack terminal and content vertically
  - Touch-friendly input
  - Larger buttons
  - Swipe gestures (optional)

- [ ] **10.4 Tutorial/onboarding**
  - First-run tutorial quest
  - Guided introduction to commands
  - Progressive disclosure of features

- [ ] **10.5 Achievement display**
  - Badges page/command
  - Achievement notifications
  - Progress tracking

- [ ] **10.6 Settings**
  - Font size adjustment
  - Auto-save toggle
  - Hint visibility toggle
  - Reset game option

- [ ] **10.7 Error handling**
  - Graceful degradation if data fails to load
  - Helpful error messages
  - Recovery suggestions

- [ ] **10.8 Performance**
  - Lazy load game scripts
  - Debounce save operations
  - Optimize markdown parsing

### Deliverables

- Fully accessible game
- Mobile-playable
- Tutorial for new players
- Settings management

---

## Success Criteria

The adventure game is complete when:

1. **Navigation**: Players can navigate between sections using text commands
2. **Content**: `look` displays rendered markdown of current section
3. **Time Travel**: Time travel shows different content per C++ era
4. **Persistence**: Progress persists across sessions (localStorage)
5. **Quests**: At least 10 quests spanning different quest types work
6. **NPCs**: NPCs provide contextual help at key sections
7. **Puzzles**: At least 5 puzzles of different types work
8. **Widget**: Widget accessible from any page on the site
9. **Mobile**: Game playable on mobile devices
10. **Accessibility**: Passes basic accessibility audit

---

## Estimated Effort

| Phase | Estimated Hours | Complexity |
|-------|-----------------|------------|
| 1 | 8-12 | Medium |
| 2 | 4-6 | Low |
| 3 | 4-6 | Medium |
| 4 | 6-8 | Medium |
| 5 | 4-6 | Low |
| 6 | 4-6 | Medium |
| 7 | 6-8 | Medium |
| 8 | 6-8 | Medium |
| 9 | 4-6 | Low |
| 10 | 8-12 | Medium |

**Total: 54-78 hours** (depending on polish level)

---

## Risk Factors

| Risk | Mitigation |
|------|------------|
| Markdown parsing complexity | Test with diverse sections early |
| Large JSON files slow loading | Lazy load, split data files |
| Mobile performance | Progressive enhancement, optimize |
| Browser compatibility | Test early, polyfill if needed |
| Content changes break game | Version data, graceful fallbacks |
