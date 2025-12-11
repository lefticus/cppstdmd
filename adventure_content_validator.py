#!/usr/bin/env python3
"""Validate adventure game content for completeness and consistency.

This module provides validation for quest, NPC, item, and puzzle content
to ensure all quests are completable before the game data is generated.
"""

from __future__ import annotations


class ContentValidator:
    """Validates quest, NPC, item, and puzzle consistency."""

    def __init__(
        self,
        quests: list[dict],
        npcs: list[dict],
        items: list[dict],
        puzzles: list[dict],
        world_map: dict,
    ):
        """Initialize validator with game content.

        Args:
            quests: List of quest dictionaries
            npcs: List of NPC dictionaries
            items: List of item dictionaries
            puzzles: List of puzzle dictionaries
            world_map: World map with sections dict (includes availableIn per section)
        """
        self.quests = {q["id"]: q for q in quests}
        self.npcs = {n["id"]: n for n in npcs}
        self.items = {i["id"]: i for i in items}
        self.puzzles = {p["id"]: p for p in puzzles}
        self.world_map_sections = world_map.get("sections", {})
        self.sections = set(self.world_map_sections.keys())
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def validate_all(self) -> bool:
        """Run all validations.

        Returns:
            True if no errors (warnings are OK), False if any errors found.
        """
        for quest in self.quests.values():
            self._validate_quest(quest)
        self._check_circular_prerequisites()
        return len(self.errors) == 0

    def _validate_quest(self, quest: dict) -> None:
        """Validate a single quest for completeness."""
        qid = quest["id"]

        # Check giver NPC exists
        giver = quest.get("giver")
        if giver:
            if giver not in self.npcs:
                self.errors.append(f"Quest '{qid}': giver NPC '{giver}' not found")

        # Check giver location exists
        loc = quest.get("giverLocation")
        if loc:
            if loc not in self.sections:
                self.errors.append(f"Quest '{qid}': giverLocation '{loc}' not found")

        # Check giver NPC is actually at the giver location
        if giver and loc and giver in self.npcs and loc in self.sections:
            npc_locations = self.npcs[giver].get("locations", [])
            if loc not in npc_locations:
                self.errors.append(
                    f"Quest '{qid}': giver NPC '{giver}' is not at giverLocation '{loc}' "
                    f"(NPC locations: {', '.join(npc_locations) or 'none'})"
                )

        # Check giver NPC has this quest in their quest list
        if giver and giver in self.npcs:
            npc_quests = self.npcs[giver].get("quests", [])
            if qid not in npc_quests:
                self.errors.append(
                    f"Quest '{qid}': giver NPC '{giver}' doesn't have this quest in their quests list"
                )

        # Check prerequisites exist
        for prereq in quest.get("prerequisites", []):
            if prereq not in self.quests:
                self.errors.append(
                    f"Quest '{qid}': prerequisite quest '{prereq}' not found"
                )

        # Check each step
        for i, step in enumerate(quest.get("steps", [])):
            self._validate_step(qid, i, step)

        # Check reward items exist
        for item_id in quest.get("rewards", {}).get("items", []):
            if item_id not in self.items:
                self.errors.append(f"Quest '{qid}': reward item '{item_id}' not found")

    def _validate_step(self, quest_id: str, step_idx: int, step: dict) -> None:
        """Validate a quest step's target and rewards."""
        target = step.get("target", {})
        prefix = f"Quest '{quest_id}' step {step_idx + 1}"

        # Check section exists
        if section := target.get("section"):
            if section not in self.sections:
                self.errors.append(f"{prefix}: section '{section}' not found")
            elif era := target.get("era"):
                # Check that section is available in the specified era
                section_data = self.world_map_sections[section]
                available_in = section_data.get("availableIn", [])
                if era not in available_in:
                    self.errors.append(
                        f"{prefix}: section '{section}' not available in era '{era}' "
                        f"(available in: {', '.join(available_in) or 'none'})"
                    )

        # Check NPC exists
        if npc := target.get("npc"):
            if npc not in self.npcs:
                self.errors.append(f"{prefix}: NPC '{npc}' not found")
            elif topic := target.get("topic"):
                # Check NPC has the required topic
                npc_data = self.npcs[npc]
                npc_topics = npc_data.get("dialogue", {}).get("topics", {})
                if topic not in npc_topics:
                    self.warnings.append(
                        f"{prefix}: NPC '{npc}' missing topic '{topic}'"
                    )

        # Check puzzle exists
        if puzzle := target.get("puzzle"):
            if puzzle not in self.puzzles:
                self.errors.append(f"{prefix}: puzzle '{puzzle}' not found")

        # Check onComplete item exists
        if item := step.get("onComplete", {}).get("item"):
            if item not in self.items:
                self.errors.append(f"{prefix}: onComplete item '{item}' not found")

    def _check_circular_prerequisites(self) -> None:
        """Detect circular prerequisite chains between quests."""

        def find_cycle(
            quest_id: str, visited: set[str], path: list[str]
        ) -> list[str] | None:
            if quest_id in path:
                # Found a cycle - return the cycle portion
                return path[path.index(quest_id) :] + [quest_id]
            if quest_id in visited or quest_id not in self.quests:
                return None

            visited.add(quest_id)
            path.append(quest_id)

            for prereq in self.quests[quest_id].get("prerequisites", []):
                if cycle := find_cycle(prereq, visited, path):
                    return cycle

            path.pop()
            return None

        visited: set[str] = set()
        for quest_id in self.quests:
            if cycle := find_cycle(quest_id, visited, []):
                self.errors.append(f"Circular prerequisites: {' -> '.join(cycle)}")
                break  # One cycle error is enough to fail


def validate_content(
    quests: list[dict],
    npcs: list[dict],
    items: list[dict],
    puzzles: list[dict],
    world_map: dict,
) -> tuple[bool, list[str], list[str]]:
    """Convenience function to validate all content.

    Args:
        quests: List of quest dictionaries
        npcs: List of NPC dictionaries
        items: List of item dictionaries
        puzzles: List of puzzle dictionaries
        world_map: World map with sections dict (includes availableIn per section)

    Returns:
        Tuple of (success, errors, warnings)
    """
    validator = ContentValidator(
        quests=quests,
        npcs=npcs,
        items=items,
        puzzles=puzzles,
        world_map=world_map,
    )
    success = validator.validate_all()
    return success, validator.errors, validator.warnings
