/**
 * parser.js - ISHML-based natural language parser for C++ Standard Adventure
 *
 * Uses the ISHML library (https://github.com/bikibird/ishml) to parse player commands.
 * Builds a custom lexicon from world-map.json section names and game vocabulary.
 */

class AdventureParser {
    constructor() {
        this.lexicon = null;
        this.grammar = null;
        this.parser = null;
        this.sectionNames = new Set();
    }

    /**
     * Initialize the parser with world data
     * @param {Object} worldData - world-map.json data with sections
     */
    init(worldData) {
        if (typeof ishml === 'undefined') {
            console.warn('[Parser] ISHML not loaded, falling back to simple parsing');
            return false;
        }

        this.buildLexicon(worldData);
        this.buildGrammar();
        this.parser = ishml.Parser({ lexicon: this.lexicon, grammar: this.grammar });

        console.log(`[Parser] Initialized with ${this.sectionNames.size} section names`);
        return true;
    }

    /**
     * Build the lexicon from game vocabulary and world data
     */
    buildLexicon(worldData) {
        this.lexicon = ishml.Lexicon();

        // Navigation verbs
        this.lexicon
            .register('go', 'move', 'walk', 'travel')
            .as({ key: 'go', type: 'verb', category: 'navigation' });

        this.lexicon
            .register('goto', 'g', 'jump', 'teleport')
            .as({ key: 'goto', type: 'verb', category: 'navigation' });

        this.lexicon
            .register('enter', 'in', 'into')
            .as({ key: 'enter', type: 'verb', category: 'navigation' });

        this.lexicon
            .register('exit', 'out', 'leave', 'back')
            .as({ key: 'exit', type: 'verb', category: 'navigation' });

        this.lexicon
            .register('warp')
            .as({ key: 'warp', type: 'verb', category: 'navigation' });

        this.lexicon
            .register('look', 'l', 'view')
            .as({ key: 'look', type: 'verb', category: 'observation' });

        this.lexicon
            .register('examine', 'x', 'inspect')
            .as({ key: 'examine', type: 'verb', category: 'observation' });

        this.lexicon
            .register('search', 'find', 'locate')
            .as({ key: 'search', type: 'verb', category: 'observation' });

        this.lexicon
            .register('map', 'overview')
            .as({ key: 'map', type: 'verb', category: 'observation' });

        this.lexicon
            .register('where', 'whereami', 'location')
            .as({ key: 'where', type: 'verb', category: 'observation' });

        // Time travel verbs
        this.lexicon
            .register('timeshift', 'timewarp', 'era', 'time')
            .as({ key: 'timeshift', type: 'verb', category: 'timetravel' });

        // Interaction verbs
        this.lexicon
            .register('talk', 'speak', 'chat')
            .as({ key: 'talk', type: 'verb', category: 'interaction' });

        this.lexicon
            .register('ask')
            .as({ key: 'ask', type: 'verb', category: 'interaction' });

        // Item verbs
        this.lexicon
            .register('take', 'get', 'grab', 'pick')
            .as({ key: 'take', type: 'verb', category: 'items' });

        this.lexicon
            .register('inventory', 'inv', 'i', 'items')
            .as({ key: 'inventory', type: 'verb', category: 'items' });

        // Player verbs
        this.lexicon
            .register('stats', 'status', 'character', 'me')
            .as({ key: 'stats', type: 'verb', category: 'player' });

        // System verbs
        this.lexicon
            .register('help', 'h', '?', 'commands')
            .as({ key: 'help', type: 'verb', category: 'system' });

        this.lexicon
            .register('clear', 'cls')
            .as({ key: 'clear', type: 'verb', category: 'system' });

        this.lexicon
            .register('save')
            .as({ key: 'save', type: 'verb', category: 'system' });

        this.lexicon
            .register('reset')
            .as({ key: 'reset', type: 'verb', category: 'system' });

        this.lexicon
            .register('speed', 'animation')
            .as({ key: 'speed', type: 'verb', category: 'system' });

        // Directions
        this.lexicon
            .register('north', 'n')
            .as({ key: 'north', type: 'direction' });

        this.lexicon
            .register('south', 's')
            .as({ key: 'south', type: 'direction' });

        this.lexicon
            .register('east', 'e')
            .as({ key: 'east', type: 'direction' });

        this.lexicon
            .register('west', 'w')
            .as({ key: 'west', type: 'direction' });

        // Eras
        this.lexicon
            .register('cpp11', 'c++11', 'n3337')
            .as({ key: 'n3337', type: 'era', displayName: 'C++11' });

        this.lexicon
            .register('cpp14', 'c++14', 'n4140')
            .as({ key: 'n4140', type: 'era', displayName: 'C++14' });

        this.lexicon
            .register('cpp17', 'c++17', 'n4659')
            .as({ key: 'n4659', type: 'era', displayName: 'C++17' });

        this.lexicon
            .register('cpp20', 'c++20', 'n4861')
            .as({ key: 'n4861', type: 'era', displayName: 'C++20' });

        this.lexicon
            .register('cpp23', 'c++23', 'n4950')
            .as({ key: 'n4950', type: 'era', displayName: 'C++23' });

        this.lexicon
            .register('cpp26', 'c++26', 'trunk')
            .as({ key: 'trunk', type: 'era', displayName: 'C++26' });

        // Prepositions and articles (to be ignored in parsing)
        this.lexicon
            .register('to', 'at', 'the', 'a', 'an', 'about', 'with', 'up')
            .as({ type: 'filler' });

        // Register section names from world data
        if (worldData && worldData.sections) {
            for (const [stableName, section] of Object.entries(worldData.sections)) {
                this.sectionNames.add(stableName);

                // Register the stable name as a section
                this.lexicon.register(stableName).as({
                    key: stableName,
                    type: 'section',
                    displayName: section.displayName || stableName,
                    chapter: section.chapter
                });

                // Also register display name if different
                if (section.displayName && section.displayName !== stableName) {
                    const normalizedDisplay = section.displayName.toLowerCase().replace(/[^a-z0-9]/g, '');
                    if (normalizedDisplay.length > 2) {
                        this.lexicon.register(normalizedDisplay).as({
                            key: stableName,
                            type: 'section',
                            displayName: section.displayName,
                            chapter: section.chapter
                        });
                    }
                }
            }
        }
    }

    /**
     * Build the grammar rules
     */
    buildGrammar() {
        this.grammar = ishml.Rule();

        // Command structure: verb [target]
        this.grammar.snip('verb').snip('filler').snip('target');

        // Verb must be a verb
        this.grammar.verb.configure({
            filter: (def) => def.type === 'verb',
            minimum: 1,
            maximum: 1
        });

        // Filler words are optional
        this.grammar.filler.configure({
            filter: (def) => def.type === 'filler',
            minimum: 0,
            maximum: Infinity
        });

        // Target can be direction, era, section, or any remaining text
        this.grammar.target.configure({
            filter: (def) => ['direction', 'era', 'section'].includes(def.type),
            minimum: 0,
            maximum: Infinity
        });
    }

    /**
     * Parse a command string
     * @param {string} input - Raw command input
     * @returns {Object} Parsed command { verb, args, raw, success }
     */
    parse(input) {
        const trimmed = input.trim().toLowerCase();

        // If no parser available, fall back to simple split
        if (!this.parser) {
            return this.simpleParse(trimmed);
        }

        // Try ISHML parsing
        const result = this.parser.analyze(trimmed);

        // Debug logging
        console.log('[Parser] Input:', trimmed);
        console.log('[Parser] ISHML result:', {
            success: result.success,
            interpretations: result.interpretations?.length || 0,
            remainder: result.remainder,
            gist: result.interpretations?.[0]?.gist
        });

        // Check if we got any interpretations (even partial matches)
        if (result.interpretations && result.interpretations.length > 0) {
            const interp = result.interpretations[0];
            const gist = interp.gist;

            // Extract verb - gist.verb can be an object or array depending on ISHML config
            const verbData = Array.isArray(gist.verb) ? gist.verb[0] : gist.verb;
            const verbDef = verbData?.definition;
            const verb = verbDef?.key || null;

            // If ISHML matched but didn't find a verb, fall back to simple parsing
            if (!verb) {
                return this.simpleParse(trimmed);
            }

            // Extract target(s) - same handling for array vs object
            const targetData = Array.isArray(gist.target) ? gist.target : (gist.target ? [gist.target] : []);
            const targets = targetData.map(t => t.definition?.key || t.lexeme);

            // For partial matches, extract remaining text after verb and filler
            // by removing matched tokens from the input
            let args = targets;
            if (targets.length === 0) {
                // No recognized targets - extract remainder from original input
                // Remove the verb and any filler words we matched
                const fillerData = Array.isArray(gist.filler) ? gist.filler : (gist.filler ? [gist.filler] : []);
                const matchedWords = new Set([verbData?.lexeme, ...fillerData.map(f => f.lexeme)].filter(Boolean));

                // Get words that weren't matched as verb or filler
                const inputWords = trimmed.split(/\s+/);
                const remainingWords = inputWords.filter(w => !matchedWords.has(w));

                if (remainingWords.length > 0) {
                    args = [remainingWords.join(' ')];
                }
            }

            return {
                success: true,
                verb: verb,
                args: args,
                raw: input,
                verbDef: verbDef,
                interpretations: result.interpretations.length,
                partial: !result.success  // Flag if this was a partial match
            };
        }

        // ISHML didn't match anything - fall back to simple parsing
        return this.simpleParse(trimmed);
    }

    /**
     * Simple fallback parser (original behavior)
     * @param {string} input - Trimmed lowercase input
     * @returns {Object} Parsed command
     */
    simpleParse(input) {
        const parts = input.split(/\s+/);
        const cmd = parts[0];
        const args = parts.slice(1);

        // Always return the command as verb - the game will handle unknown commands
        // This is the simplest fallback that matches the original behavior
        return {
            success: true,
            verb: cmd,
            args: args,
            raw: input,
            fallback: true
        };
    }

    /**
     * Get suggestions for partial input (for autocomplete)
     * @param {string} partial - Partial input
     * @returns {Array} Suggestions
     */
    getSuggestions(partial) {
        if (!this.lexicon) return [];

        const trimmed = partial.trim().toLowerCase();
        const suggestions = [];

        // Search lexicon for matches
        const entries = this.lexicon.search(trimmed);
        for (const entry of entries) {
            suggestions.push({
                text: entry.key,
                type: entry.type,
                displayName: entry.displayName
            });
        }

        // Also do prefix matching on section names
        if (this.sectionNames.size > 0) {
            for (const name of this.sectionNames) {
                if (name.startsWith(trimmed) && !suggestions.find(s => s.text === name)) {
                    suggestions.push({
                        text: name,
                        type: 'section'
                    });
                }
            }
        }

        return suggestions.slice(0, 10);
    }
}

// Export for use in game.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AdventureParser;
}
