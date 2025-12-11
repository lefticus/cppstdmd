/**
 * player.js - Player state management for the C++ Standard Adventure Game
 *
 * Handles:
 * - Player state (location, era, stats, inventory)
 * - Experience and leveling
 * - Visited sections tracking
 * - Save/load to localStorage
 */

class Player {
    constructor() {
        this.state = this.getDefaultState();
        this.saveKey = 'cppevo_adventure_save';
    }

    /**
     * Get default player state
     * @returns {object} Default state object
     */
    getDefaultState() {
        return {
            version: '1.0.0',
            timestamp: Date.now(),

            // Identity
            name: 'Traveler',
            title: 'Novice Programmer',

            // Progression
            level: 1,
            experience: 0,
            experienceToNext: 100,

            // Stats (0-100 scale)
            stats: {
                fundamentals: 10,
                library: 10,
                metaprogramming: 10,
                modernCpp: 10,
            },

            // Current state
            currentLocation: 'intro',
            currentEra: 'n4950',

            // Collections
            inventory: [],
            badges: [],
            certificates: [],

            // Tracking
            sectionsVisited: [],
            sectionsCompleted: [],
            timeTravelsPerformed: 0,
            puzzlesSolved: 0,
            npcsSpokenTo: [],

            // Quests
            activeQuests: [],
            completedQuests: [],
            questProgress: {},

            // Settings
            settings: {
                animationSpeed: 'normal', // 'slow', 'normal', 'fast', 'off'
            },
        };
    }

    /**
     * Level titles by level range
     */
    static LEVEL_TITLES = {
        1: 'Novice Programmer',
        6: 'Apprentice Developer',
        11: 'Junior Engineer',
        16: 'Journeyman Coder',
        21: 'Senior Developer',
        31: 'Expert Engineer',
        41: 'Master Architect',
        46: 'Standard Scholar',
    };

    /**
     * Get title for a level
     * @param {number} level
     * @returns {string}
     */
    static getTitleForLevel(level) {
        let title = 'Novice Programmer';
        for (const [minLevel, levelTitle] of Object.entries(Player.LEVEL_TITLES)) {
            if (level >= parseInt(minLevel)) {
                title = levelTitle;
            }
        }
        return title;
    }

    /**
     * Calculate XP needed for next level
     * @param {number} level
     * @returns {number}
     */
    static getXPForLevel(level) {
        return Math.floor(100 * Math.pow(1.2, level - 1));
    }

    /**
     * Load player state from localStorage
     * @returns {boolean} True if save was found and loaded
     */
    load() {
        try {
            const saved = localStorage.getItem(this.saveKey);
            if (!saved) {
                return false;
            }

            const data = JSON.parse(saved);

            // Merge with defaults to handle new fields
            this.state = { ...this.getDefaultState(), ...data };

            // Convert arrays to Sets for visited tracking (if needed by caller)
            return true;
        } catch (error) {
            console.error('Failed to load save:', error);
            return false;
        }
    }

    /**
     * Save player state to localStorage
     */
    save() {
        try {
            this.state.timestamp = Date.now();
            localStorage.setItem(this.saveKey, JSON.stringify(this.state));
        } catch (error) {
            console.error('Failed to save:', error);
        }
    }

    /**
     * Reset player to default state
     */
    reset() {
        this.state = this.getDefaultState();
        localStorage.removeItem(this.saveKey);
    }

    // --- Location ---

    /**
     * Get current location
     * @returns {string} Stable name of current location
     */
    get currentLocation() {
        return this.state.currentLocation;
    }

    /**
     * Get current era
     * @returns {string} Era tag (e.g., "n4950")
     */
    get currentEra() {
        return this.state.currentEra;
    }

    /**
     * Move to a new location
     * @param {string} stableName - Destination stable name
     * @returns {boolean} True if this is a new location
     */
    moveTo(stableName) {
        this.state.currentLocation = stableName;

        const isNew = !this.state.sectionsVisited.includes(stableName);
        if (isNew) {
            this.state.sectionsVisited.push(stableName);
            this.gainExperience(10); // XP for visiting new section
        }

        this.save();
        return isNew;
    }

    /**
     * Check if a section has been visited
     * @param {string} stableName
     * @returns {boolean}
     */
    hasVisited(stableName) {
        return this.state.sectionsVisited.includes(stableName);
    }

    /**
     * Get set of visited sections
     * @returns {Set<string>}
     */
    getVisitedSections() {
        return new Set(this.state.sectionsVisited);
    }

    // --- Era ---

    /**
     * Change current era
     * @param {string} eraTag - Era tag to switch to
     * @returns {boolean} True if this is the first time travel
     */
    setEra(eraTag) {
        const isFirst = this.state.timeTravelsPerformed === 0;
        this.state.currentEra = eraTag;
        this.state.timeTravelsPerformed++;

        if (isFirst) {
            this.gainExperience(50); // Bonus for first time travel
        }

        this.save();
        return isFirst;
    }

    // --- Experience & Leveling ---

    /**
     * Get current level
     * @returns {number}
     */
    get level() {
        return this.state.level;
    }

    /**
     * Get current experience
     * @returns {number}
     */
    get experience() {
        return this.state.experience;
    }

    /**
     * Get experience needed for next level
     * @returns {number}
     */
    get experienceToNext() {
        return this.state.experienceToNext;
    }

    /**
     * Get current title
     * @returns {string}
     */
    get title() {
        return this.state.title;
    }

    /**
     * Gain experience points
     * @param {number} amount - XP to gain
     * @returns {object} Result with leveledUp flag and new level/title if applicable
     */
    gainExperience(amount) {
        this.state.experience += amount;
        const result = { leveledUp: false, amount };

        // Check for level up
        while (this.state.experience >= this.state.experienceToNext && this.state.level < 50) {
            this.state.experience -= this.state.experienceToNext;
            this.state.level++;
            this.state.experienceToNext = Player.getXPForLevel(this.state.level);

            const newTitle = Player.getTitleForLevel(this.state.level);
            if (newTitle !== this.state.title) {
                this.state.title = newTitle;
                result.newTitle = newTitle;
            }

            result.leveledUp = true;
            result.newLevel = this.state.level;
        }

        this.save();
        return result;
    }

    // --- Stats ---

    /**
     * Get all stats
     * @returns {object}
     */
    get stats() {
        return { ...this.state.stats };
    }

    /**
     * Get a specific stat
     * @param {string} statName
     * @returns {number}
     */
    getStat(statName) {
        return this.state.stats[statName] || 0;
    }

    /**
     * Boost a stat
     * @param {string} statName
     * @param {number} amount
     */
    boostStat(statName, amount) {
        if (this.state.stats[statName] !== undefined) {
            this.state.stats[statName] = Math.min(100, this.state.stats[statName] + amount);
            this.save();
        }
    }

    // --- Inventory ---

    /**
     * Get inventory
     * @returns {string[]} Array of item IDs
     */
    get inventory() {
        return [...this.state.inventory];
    }

    /**
     * Check if player has an item
     * @param {string} itemId
     * @returns {boolean}
     */
    hasItem(itemId) {
        return this.state.inventory.includes(itemId);
    }

    /**
     * Add item to inventory
     * @param {string} itemId
     * @returns {boolean} True if item was added (not duplicate)
     */
    addItem(itemId) {
        if (!this.state.inventory.includes(itemId)) {
            this.state.inventory.push(itemId);
            this.gainExperience(15); // XP for collecting item
            this.save();
            return true;
        }
        return false;
    }

    // --- NPCs ---

    /**
     * Record speaking to an NPC
     * @param {string} npcId
     * @returns {boolean} True if this is the first conversation
     */
    talkToNPC(npcId) {
        const isFirst = !this.state.npcsSpokenTo.includes(npcId);
        if (isFirst) {
            this.state.npcsSpokenTo.push(npcId);
            this.gainExperience(10); // XP for first NPC conversation
            this.save();
        }
        return isFirst;
    }

    /**
     * Check if player has talked to an NPC
     * @param {string} npcId
     * @returns {boolean}
     */
    hasSpokenTo(npcId) {
        return this.state.npcsSpokenTo.includes(npcId);
    }

    // --- Topics ---

    /**
     * Learn a topic from an NPC (for XP rewards)
     * @param {string} npcId
     * @param {string} topicKey
     * @returns {boolean} True if this is the first time learning this topic
     */
    learnTopic(npcId, topicKey) {
        const key = `${npcId}_${topicKey}`;
        if (!this.state.topicsLearned) {
            this.state.topicsLearned = [];
        }
        if (!this.state.topicsLearned.includes(key)) {
            this.state.topicsLearned.push(key);
            this.save();
            return true;
        }
        return false;
    }

    /**
     * Check if player has learned a topic from an NPC
     * @param {string} npcId
     * @param {string} topicKey
     * @returns {boolean}
     */
    hasLearnedTopic(npcId, topicKey) {
        const key = `${npcId}_${topicKey}`;
        return this.state.topicsLearned?.includes(key) ?? false;
    }

    // --- Quests ---

    /**
     * Get active quests
     * @returns {string[]}
     */
    get activeQuests() {
        return [...this.state.activeQuests];
    }

    /**
     * Start a quest
     * @param {string} questId
     * @returns {boolean} True if quest was started
     */
    startQuest(questId) {
        if (!this.state.activeQuests.includes(questId) &&
            !this.state.completedQuests.includes(questId)) {
            this.state.activeQuests.push(questId);
            this.state.questProgress[questId] = { currentStep: 0, completed: [] };
            this.save();
            return true;
        }
        return false;
    }

    /**
     * Complete a quest
     * @param {string} questId
     */
    completeQuest(questId) {
        const idx = this.state.activeQuests.indexOf(questId);
        if (idx !== -1) {
            this.state.activeQuests.splice(idx, 1);
            this.state.completedQuests.push(questId);
            this.save();
        }
    }

    /**
     * Reset a quest (remove from active/completed, clear progress)
     * Used for testing quests
     * @param {string} questId
     * @returns {boolean} True if quest was reset
     */
    resetQuest(questId) {
        let found = false;

        // Remove from active quests
        const activeIdx = this.state.activeQuests.indexOf(questId);
        if (activeIdx !== -1) {
            this.state.activeQuests.splice(activeIdx, 1);
            found = true;
        }

        // Remove from completed quests
        const completedIdx = this.state.completedQuests.indexOf(questId);
        if (completedIdx !== -1) {
            this.state.completedQuests.splice(completedIdx, 1);
            found = true;
        }

        // Clear quest progress
        if (this.state.questProgress[questId]) {
            delete this.state.questProgress[questId];
            found = true;
        }

        if (found) {
            this.save();
        }
        return found;
    }

    // --- Settings ---

    /**
     * Get a setting value
     * @param {string} key
     * @returns {*}
     */
    getSetting(key) {
        return this.state.settings?.[key];
    }

    /**
     * Set a setting value
     * @param {string} key
     * @param {*} value
     */
    setSetting(key, value) {
        if (!this.state.settings) {
            this.state.settings = {};
        }
        this.state.settings[key] = value;
        this.save();
    }

    /**
     * Get animation duration in ms based on speed setting
     * @returns {number}
     */
    getAnimationDuration() {
        const speed = this.getSetting('animationSpeed') || 'normal';
        const durations = {
            'slow': 2000,
            'normal': 1200,
            'fast': 500,
            'off': 0,
        };
        return durations[speed] ?? 1200;
    }

    // --- Export ---

    /**
     * Export save data as JSON string
     * @returns {string}
     */
    exportSave() {
        return JSON.stringify(this.state, null, 2);
    }

    /**
     * Import save data from JSON string
     * @param {string} jsonString
     * @returns {boolean} True if import succeeded
     */
    importSave(jsonString) {
        try {
            const data = JSON.parse(jsonString);
            this.state = { ...this.getDefaultState(), ...data };
            this.save();
            return true;
        } catch (error) {
            console.error('Failed to import save:', error);
            return false;
        }
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Player;
}
