# C++ Standard Adventure Game - Design Documentation

This folder contains the complete design documentation for adding a text-based adventure game to the cppevo website (cppstdmd.com).

## Overview

The adventure game transforms the C++ standard documentation into an explorable world where players:
- Navigate sections as physical locations in themed "realms"
- Collect knowledge items and level up their character
- Complete quests that teach C++ concepts
- Time-travel between C++ eras (C++11 → C++26) to witness language evolution
- Interact with NPCs that provide hints and lore
- Solve puzzles based on the standard's content

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Integration | Both standalone page + embeddable widget | Maximum accessibility |
| Content Display | Split-screen (terminal + markdown panel) | See content while playing |
| Complexity | Full RPG elements | Deep engagement with the standard |
| Time Travel | Core mechanic | Leverages existing diff infrastructure |
| Tech Stack | Vanilla JavaScript | Matches existing codebase |

## Documents

1. **[Game World Design](01-game-world.md)**
   - World structure (Realms, Zones, Rooms)
   - Navigation model and commands
   - Time travel mechanics
   - Location theming

2. **[RPG Systems](02-rpg-systems.md)**
   - Character progression
   - Knowledge inventory
   - NPC design and dialogue
   - Quest system
   - Puzzle types

3. **[Technical Architecture](03-technical-architecture.md)**
   - File structure
   - Data generation pipeline
   - Client-side architecture
   - State management
   - Content loading

4. **[Implementation Phases](04-implementation-phases.md)**
   - 10-phase roadmap
   - Task breakdowns
   - Dependencies
   - Success criteria

## Quick Start for Implementation

1. Read all design docs in order
2. Start with Phase 1 (Terminal & Navigation Foundation)
3. Each phase builds on the previous
4. Core playable game after Phase 3
5. Full feature set after Phase 10

## User Requirements (from planning session)

- **Integration**: Both standalone `/adventure/` page AND embeddable widget
- **Content Display**: Split screen - game terminal on left, rendered markdown on right
- **Quest System**: Full RPG elements - character progression, inventory, unlockable areas, NPCs, puzzles
- **Time Travel**: Core feature - players can travel between C++11/14/17/20/23/26
