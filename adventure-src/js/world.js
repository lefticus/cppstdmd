/**
 * world.js - World map and navigation for the C++ Standard Adventure Game
 *
 * Handles:
 * - Loading and storing world map data
 * - Section lookups and navigation
 * - Era availability checks
 * - Realm information
 */

class World {
    constructor() {
        this.worldMap = null;
        this.sections = {};
        this.realms = {};
        this.eras = {};
        this.stableNameAliases = {};  // Maps stable names to their aliases
        this.loaded = false;
    }

    /**
     * Load world map data from JSON file
     * @returns {Promise<void>}
     */
    async load() {
        try {
            const response = await fetch('/data/game/world-map.json');
            if (!response.ok) {
                throw new Error(`Failed to load world map: ${response.status}`);
            }
            this.worldMap = await response.json();
            this.sections = this.worldMap.sections || {};
            this.realms = this.worldMap.realms || {};
            this.eras = this.worldMap.eras || {};
            this.stableNameAliases = this.worldMap.stableNameAliases || {};
            this.loaded = true;
        } catch (error) {
            console.error('Failed to load world map:', error);
            throw error;
        }
    }

    /**
     * Get a section by stable name
     * @param {string} stableName - The section's stable name
     * @returns {object|null} Section data or null if not found
     */
    getSection(stableName) {
        return this.sections[stableName] || null;
    }

    /**
     * Get a realm by key
     * @param {string} realmKey - The realm key (first part of stable name)
     * @returns {object|null} Realm data or null if not found
     */
    getRealm(realmKey) {
        return this.realms[realmKey] || null;
    }

    /**
     * Get the realm for a section
     * @param {string} stableName - The section's stable name
     * @returns {object|null} Realm data
     */
    getRealmForSection(stableName) {
        const section = this.getSection(stableName);
        if (!section) return null;
        return this.getRealm(section.realm);
    }

    /**
     * Check if a section exists in a specific era
     * @param {string} stableName - The section's stable name
     * @param {string} era - Era tag (e.g., "n4950")
     * @returns {boolean}
     */
    isAvailableInEra(stableName, era) {
        const section = this.getSection(stableName);
        if (!section) return false;
        return section.availableIn.includes(era);
    }

    /**
     * Get available exits from a section
     * @param {string} stableName - The section's stable name
     * @returns {object} Exits object with directions and targets
     */
    getExits(stableName) {
        const section = this.getSection(stableName);
        if (!section) return { directions: [], children: [], parent: null };

        const exits = {
            directions: [],
            children: section.children || [],
            parent: section.parent,
        };

        const connections = section.connections || {};
        for (const [direction, target] of Object.entries(connections)) {
            if (target) {
                const targetSection = this.getSection(target);
                if (targetSection) {
                    exits.directions.push({
                        direction,
                        target,
                        displayName: targetSection.displayName,
                    });
                }
            }
        }

        return exits;
    }

    /**
     * Get formatted exits string for display
     * @param {string} stableName - The section's stable name
     * @param {string} currentEra - Current era for availability filtering
     * @returns {string[]} Array of exit descriptions
     */
    getExitDescriptions(stableName, currentEra) {
        const exits = this.getExits(stableName);
        const descriptions = [];

        // Cardinal directions
        for (const exit of exits.directions) {
            if (this.isAvailableInEra(exit.target, currentEra)) {
                descriptions.push(`${exit.direction} to ${exit.displayName}`);
            }
        }

        // Children (enter)
        const availableChildren = exits.children.filter(
            child => this.isAvailableInEra(child, currentEra)
        );
        if (availableChildren.length > 0) {
            const childNames = availableChildren
                .map(c => this.getSection(c)?.displayName || c)
                .slice(0, 5); // Limit to 5
            if (availableChildren.length > 5) {
                childNames.push(`... and ${availableChildren.length - 5} more`);
            }
            descriptions.push(`enter: ${childNames.join(', ')}`);
        }

        // Parent (exit)
        if (exits.parent && this.isAvailableInEra(exits.parent, currentEra)) {
            const parentSection = this.getSection(exits.parent);
            if (parentSection) {
                descriptions.push(`exit to ${parentSection.displayName}`);
            }
        }

        return descriptions;
    }

    /**
     * Navigate in a direction from current section
     * @param {string} currentSection - Current section stable name
     * @param {string} direction - Direction to move (north/south/east/west)
     * @param {string} currentEra - Current era
     * @returns {object} Result with success, target, or error message
     */
    navigate(currentSection, direction, currentEra) {
        const section = this.getSection(currentSection);
        if (!section) {
            return { success: false, message: 'Current location not found.' };
        }

        const connections = section.connections || {};
        const target = connections[direction];

        if (!target) {
            return { success: false, message: `You cannot go ${direction} from here.` };
        }

        if (!this.isAvailableInEra(target, currentEra)) {
            const targetSection = this.getSection(target);
            const eraName = this.eras[currentEra] || currentEra;
            return {
                success: false,
                message: `${targetSection?.displayName || target} doesn't exist in ${eraName}.`,
            };
        }

        return { success: true, target };
    }

    /**
     * Enter a child section
     * @param {string} currentSection - Current section stable name
     * @param {string} childName - Child section name or partial match
     * @param {string} currentEra - Current era
     * @returns {object} Result with success, target, or error message
     */
    enter(currentSection, childName, currentEra) {
        const section = this.getSection(currentSection);
        if (!section) {
            return { success: false, message: 'Current location not found.' };
        }

        const children = section.children || [];
        if (children.length === 0) {
            return { success: false, message: 'There is nothing to enter here.' };
        }

        // Find matching child (exact or partial)
        const childLower = childName.toLowerCase();
        let target = children.find(c => c.toLowerCase() === childLower);

        if (!target) {
            // Try partial match on display name
            target = children.find(c => {
                const childSection = this.getSection(c);
                return childSection?.displayName.toLowerCase().includes(childLower);
            });
        }

        if (!target) {
            // Try partial match on stable name
            target = children.find(c => c.toLowerCase().includes(childLower));
        }

        if (!target) {
            return { success: false, message: `Cannot find "${childName}" to enter.` };
        }

        if (!this.isAvailableInEra(target, currentEra)) {
            const eraName = this.eras[currentEra] || currentEra;
            return {
                success: false,
                message: `That area doesn't exist in ${eraName}.`,
            };
        }

        return { success: true, target };
    }

    /**
     * Exit to parent section
     * @param {string} currentSection - Current section stable name
     * @param {string} currentEra - Current era
     * @returns {object} Result with success, target, or error message
     */
    exit(currentSection, currentEra) {
        const section = this.getSection(currentSection);
        if (!section) {
            return { success: false, message: 'Current location not found.' };
        }

        const parent = section.parent;
        if (!parent) {
            return { success: false, message: 'There is nowhere to exit to from here.' };
        }

        if (!this.isAvailableInEra(parent, currentEra)) {
            const eraName = this.eras[currentEra] || currentEra;
            return {
                success: false,
                message: `The parent area doesn't exist in ${eraName}.`,
            };
        }

        return { success: true, target: parent };
    }

    /**
     * Warp directly to a section (fast travel)
     * @param {string} targetName - Target stable name or partial match
     * @param {string} currentEra - Current era
     * @param {Set<string>} visitedSections - Set of visited section names
     * @returns {object} Result with success, target, or error message
     */
    warp(targetName, currentEra, visitedSections) {
        const targetLower = targetName.toLowerCase();

        // Exact match first
        if (this.sections[targetName]) {
            if (!visitedSections.has(targetName)) {
                return { success: false, message: `You haven't discovered ${targetName} yet.` };
            }
            if (!this.isAvailableInEra(targetName, currentEra)) {
                const eraName = this.eras[currentEra] || currentEra;
                return { success: false, message: `That area doesn't exist in ${eraName}.` };
            }
            return { success: true, target: targetName };
        }

        // Partial match on visited sections
        const matches = Array.from(visitedSections).filter(name => {
            const section = this.getSection(name);
            return (
                name.toLowerCase().includes(targetLower) ||
                section?.displayName.toLowerCase().includes(targetLower)
            );
        });

        if (matches.length === 0) {
            return { success: false, message: `Cannot find "${targetName}" in visited locations.` };
        }

        if (matches.length > 1) {
            const names = matches.slice(0, 5).map(m => this.getSection(m)?.displayName || m);
            return {
                success: false,
                message: `Multiple matches: ${names.join(', ')}. Be more specific.`,
            };
        }

        const target = matches[0];
        if (!this.isAvailableInEra(target, currentEra)) {
            const eraName = this.eras[currentEra] || currentEra;
            return { success: false, message: `That area doesn't exist in ${eraName}.` };
        }

        return { success: true, target };
    }

    /**
     * Get list of all realm names for map display
     * @returns {string[]} Array of realm keys
     */
    getRealmList() {
        return Object.keys(this.realms);
    }

    /**
     * Get sections in a realm
     * @param {string} realmKey - Realm key
     * @returns {string[]} Array of section stable names
     */
    getSectionsInRealm(realmKey) {
        const realm = this.getRealm(realmKey);
        return realm?.sections || [];
    }

    /**
     * Get era display name
     * @param {string} eraTag - Era tag (e.g., "n4950")
     * @returns {string} Display name (e.g., "C++23")
     */
    getEraName(eraTag) {
        return this.eras[eraTag] || eraTag;
    }

    /**
     * Get all available eras
     * @returns {object} Map of era tags to names
     */
    getAllEras() {
        return { ...this.eras };
    }

    /**
     * Get aliases for a stable name
     * @param {string} stableName - The section's stable name
     * @returns {string[]} Array of alias names (may be empty)
     */
    getAliases(stableName) {
        return this.stableNameAliases[stableName] || [];
    }

    /**
     * Find an equivalent stable name that exists in the target era
     * @param {string} stableName - The section's stable name
     * @param {string} targetEra - The era to check
     * @returns {string|null} An alias that exists in the era, or null
     */
    findAliasForEra(stableName, targetEra) {
        // First check if the name itself exists in the era
        if (this.isAvailableInEra(stableName, targetEra)) {
            return stableName;
        }

        // Check aliases
        const aliases = this.getAliases(stableName);
        for (const alias of aliases) {
            const aliasSection = this.getSection(alias);
            if (aliasSection && aliasSection.availableIn.includes(targetEra)) {
                return alias;
            }
        }

        return null;
    }

    /**
     * Timeshift to a different era, finding the equivalent section
     * @param {string} currentSection - Current section stable name
     * @param {string} targetEra - Era to shift to
     * @returns {object} Result with success, target, aliased, and message
     */
    timeshift(currentSection, targetEra) {
        // Check if direct navigation works
        if (this.isAvailableInEra(currentSection, targetEra)) {
            return {
                success: true,
                target: currentSection,
                aliased: false,
            };
        }

        // Try to find an alias that exists in the target era
        const alias = this.findAliasForEra(currentSection, targetEra);
        if (alias) {
            const aliasSection = this.getSection(alias);
            const currentSectionData = this.getSection(currentSection);
            return {
                success: true,
                target: alias,
                aliased: true,
                message: `Section "${currentSectionData?.title || currentSection}" was renamed to "${aliasSection?.title || alias}" in ${this.getEraName(targetEra)}.`,
            };
        }

        // No equivalent found
        const eraName = this.getEraName(targetEra);
        const section = this.getSection(currentSection);
        return {
            success: false,
            message: `"${section?.displayName || currentSection}" doesn't exist in ${eraName} and has no known equivalent.`,
        };
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = World;
}
