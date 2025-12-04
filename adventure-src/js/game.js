/**
 * game.js - Main game engine for the C++ Standard Adventure Game
 *
 * Coordinates all modules and handles command processing.
 */

class AdventureGame {
    constructor(terminalElement, contentPanel) {
        this.terminal = new Terminal(terminalElement);
        this.contentPanel = contentPanel;
        this.world = new World();
        this.player = new Player();

        // NPCs and other data
        this.npcs = [];
        this.items = [];
        this.quests = [];
        this.puzzles = [];

        // Command registry
        this.commands = this.buildCommandRegistry();

        // Bind terminal callbacks
        this.terminal.onCommand = (cmd) => this.handleCommand(cmd);
        this.terminal.onWikilinkClick = (target) => this.handleWikilinkClick(target);
    }

    /**
     * Handle wikilink click - navigate to target section
     */
    handleWikilinkClick(target) {
        // Echo the command in terminal and execute goto
        this.terminal.print(`> goto ${target}`);
        this.cmdGoto([target]);
    }

    /**
     * Initialize the game
     */
    async init() {
        this.terminal.print('Loading C++ Standard Adventure...');

        try {
            // Load world data
            await this.world.load();

            // Load additional game data
            await Promise.all([
                this.loadNPCs(),
                this.loadItems(),
                this.loadQuests(),
                this.loadPuzzles(),
            ]);

            // Load or create player save
            const hasSave = this.player.load();

            // Validate player location exists
            if (!this.world.getSection(this.player.currentLocation)) {
                this.player.state.currentLocation = 'intro';
                this.player.save();
            }

            this.terminal.clear();
            this.terminal.print('Welcome to the C++ Standard Adventure!');
            this.terminal.print('Explore the C++ standard as an interactive world.');
            this.terminal.print('');

            if (hasSave) {
                this.terminal.print(`Welcome back, ${this.player.state.name}!`);
                this.terminal.print(`Level ${this.player.level} ${this.player.title}`);
            } else {
                this.terminal.print('Type "help" for a list of commands.');
            }

            this.terminal.print('');

            // Show current location
            await this.showLocation();

            // Update UI
            this.updateStatusBar();

            this.terminal.focus();
        } catch (error) {
            this.terminal.print(`Error loading game: ${error.message}`);
            console.error('Game init error:', error);
        }
    }

    /**
     * Load NPC data
     */
    async loadNPCs() {
        try {
            const response = await fetch('/data/game/npcs.json');
            if (response.ok) {
                this.npcs = await response.json();
            }
        } catch (error) {
            console.warn('Failed to load NPCs:', error);
        }
    }

    /**
     * Load item data
     */
    async loadItems() {
        try {
            const response = await fetch('/data/game/items.json');
            if (response.ok) {
                this.items = await response.json();
            }
        } catch (error) {
            console.warn('Failed to load items:', error);
        }
    }

    /**
     * Load quest data
     */
    async loadQuests() {
        try {
            const response = await fetch('/data/game/quests.json');
            if (response.ok) {
                this.quests = await response.json();
            }
        } catch (error) {
            console.warn('Failed to load quests:', error);
        }
    }

    /**
     * Load puzzle data
     */
    async loadPuzzles() {
        try {
            const response = await fetch('/data/game/puzzles.json');
            if (response.ok) {
                this.puzzles = await response.json();
            }
        } catch (error) {
            console.warn('Failed to load puzzles:', error);
        }
    }

    /**
     * Build the command registry
     */
    buildCommandRegistry() {
        return {
            // Navigation
            'look': () => this.cmdLook(),
            'l': () => this.cmdLook(),
            'go': (args) => this.cmdGo(args),
            'n': () => this.cmdGo(['north']),
            's': () => this.cmdGo(['south']),
            'e': () => this.cmdGo(['east']),
            'w': () => this.cmdGo(['west']),
            'north': () => this.cmdGo(['north']),
            'south': () => this.cmdGo(['south']),
            'east': () => this.cmdGo(['east']),
            'west': () => this.cmdGo(['west']),
            'enter': (args) => this.cmdEnter(args),
            'exit': () => this.cmdExit(),
            'leave': () => this.cmdExit(),
            'warp': (args) => this.cmdWarp(args),
            'goto': (args) => this.cmdGoto(args),
            'g': (args) => this.cmdGoto(args),
            'search': (args) => this.cmdSearch(args),
            'find': (args) => this.cmdSearch(args),
            'map': () => this.cmdMap(),
            'where': () => this.cmdWhere(),
            'whereami': () => this.cmdWhere(),

            // Time travel
            'timeshift': (args) => this.cmdTimeshift(args),
            'era': () => this.cmdEra(),

            // Interaction
            'talk': (args) => this.cmdTalk(args),
            'ask': (args) => this.cmdAsk(args),

            // Items
            'inventory': () => this.cmdInventory(),
            'inv': () => this.cmdInventory(),
            'i': () => this.cmdInventory(),
            'examine': (args) => this.cmdExamine(args),
            'take': (args) => this.cmdTake(args),
            'get': (args) => this.cmdTake(args),

            // Player
            'stats': () => this.cmdStats(),
            'status': () => this.cmdStats(),

            // System
            'help': () => this.cmdHelp(),
            'h': () => this.cmdHelp(),
            '?': () => this.cmdHelp(),
            'clear': () => this.terminal.clear(),
            'cls': () => this.terminal.clear(),
            'save': () => this.cmdSave(),
            'reset': (args) => this.cmdReset(args),
        };
    }

    /**
     * Handle a command input
     */
    async handleCommand(input) {
        const parts = input.trim().split(/\s+/);
        const cmd = parts[0].toLowerCase();
        const args = parts.slice(1);

        if (this.commands[cmd]) {
            await this.commands[cmd](args);
        } else {
            this.terminal.print(`Unknown command: ${cmd}`);
            this.terminal.print('Type "help" for a list of commands.');
        }

        // Auto-save after each command
        this.player.save();
        this.updateStatusBar();
    }

    /**
     * Update the status bar in the header
     */
    updateStatusBar() {
        const eraBadge = document.getElementById('era-badge');
        const levelBadge = document.getElementById('level-badge');

        if (eraBadge) {
            eraBadge.textContent = this.world.getEraName(this.player.currentEra);
        }
        if (levelBadge) {
            levelBadge.textContent = `Level ${this.player.level}`;
        }
    }

    /**
     * Show current location
     * @param {boolean} scrollToTop - Whether to scroll content panel to top (default true)
     */
    async showLocation(scrollToTop = true) {
        const section = this.world.getSection(this.player.currentLocation);
        if (!section) {
            this.terminal.print('Error: Location not found.');
            return;
        }

        const eraName = this.world.getEraName(this.player.currentEra);
        const realm = this.world.getRealm(section.realm);

        // Location header
        this.terminal.print('');
        this.terminal.printLocation(eraName, section.displayName, section.stableName);
        this.terminal.printSeparator('═');

        // Realm info (for top-level sections)
        if (section.stableName === section.realm && realm) {
            this.terminal.print(realm.description);
            this.terminal.print('');
        }

        // Section description
        this.terminal.print(section.description);

        // Exits
        const exits = this.world.getExitDescriptions(section.stableName, this.player.currentEra);
        if (exits.length > 0) {
            this.terminal.print('');
            this.terminal.print(`Exits: ${exits.join(', ')}`);
        }

        // NPCs here
        const npcsHere = this.getNPCsAtLocation(section.stableName);
        if (npcsHere.length > 0) {
            this.terminal.print('');
            const npcNames = npcsHere.map(n => n.name).join(', ');
            this.terminal.print(`You see: ${npcNames}`);
        }

        // Items here
        const itemsHere = this.getItemsAtLocation(section.stableName);
        if (itemsHere.length > 0) {
            this.terminal.print('');
            const itemNames = itemsHere.map(i => `${i.name} (${i.rarity})`).join(', ');
            this.terminal.print(`Items: ${itemNames}`);
        }

        // Load content into side panel
        await this.loadContentPanel(section, scrollToTop);
    }

    /**
     * Get NPCs at a location
     */
    getNPCsAtLocation(stableName) {
        return this.npcs.filter(npc => {
            if (npc.locations.includes('*')) return true;
            return npc.locations.includes(stableName);
        });
    }

    /**
     * Get items at a location (not yet collected)
     */
    getItemsAtLocation(stableName) {
        return this.items.filter(item => {
            if (this.player.hasItem(item.id)) return false;
            return item.sourceSection === stableName;
        });
    }

    /**
     * Load content into the side panel
     * @param {object} section - Section data
     * @param {boolean} scrollToTop - Whether to scroll to top after loading (default true)
     */
    async loadContentPanel(section, scrollToTop = true) {
        if (!this.contentPanel) return;

        const titleEl = document.getElementById('content-title');
        if (titleEl) {
            titleEl.textContent = `${section.displayName} [[${section.stableName}]]`;
        }

        // Fetch markdown content
        const chapter = section.chapter;
        const era = this.player.currentEra;
        const url = `/${era}/${chapter}.md`;

        try {
            const response = await fetch(url);
            if (!response.ok) {
                this.contentPanel.innerHTML = '<p>Content not available in this era.</p>';
                return;
            }

            const markdown = await response.text();
            const sectionContent = this.extractSectionContent(markdown, section.stableName);

            // Render markdown
            this.contentPanel.innerHTML = this.renderMarkdown(sectionContent || 'Section content not found.');

            // Apply syntax highlighting to code blocks
            if (typeof Prism !== 'undefined') {
                Prism.highlightAllUnder(this.contentPanel);
            }

            // Bind click handlers for wikilinks
            this.bindWikilinks();

            // Scroll to top if requested
            if (scrollToTop) {
                this.contentPanel.scrollTop = 0;
            }
        } catch (error) {
            this.contentPanel.innerHTML = `<p>Error loading content: ${error.message}</p>`;
        }
    }

    /**
     * Extract section content from markdown
     */
    extractSectionContent(markdown, stableName) {
        // Find the section by anchor
        const anchorIndex = markdown.indexOf(`<a id="${stableName}"`);

        // If anchor not found, this might be a top-level/file section
        // In that case, return the entire file content
        if (anchorIndex === -1) {
            // Check if this is a file-level section (no dots, or the file starts with content for this section)
            // Return the whole file for file-level sections
            return markdown;
        }

        // Find the start of the heading line
        const lineStart = markdown.lastIndexOf('\n', anchorIndex) + 1;

        // Find the heading level
        const headingMatch = markdown.substring(lineStart, anchorIndex + 50).match(/^(#{1,6})/);
        const headingLevel = headingMatch ? headingMatch[1].length : 2;

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

    /**
     * Simple markdown to HTML renderer
     */
    renderMarkdown(markdown) {
        // Pre-process: Convert [[stable.name]] wikilinks to placeholders
        // We use a placeholder that marked.js won't interpret as a link
        const wikilinks = [];
        const processedMarkdown = markdown.replace(
            /\[\[([^\]]+)\]\]/g,
            (match, target) => {
                const index = wikilinks.length;
                wikilinks.push(target);
                return `%%WIKILINK_${index}%%`;
            }
        );

        let html;
        // Use marked.js if available, otherwise basic conversion
        if (typeof marked !== 'undefined') {
            // Configure marked for GFM
            marked.setOptions({
                gfm: true,
                breaks: false,
                pedantic: false,
            });
            html = marked.parse(processedMarkdown);
        } else {
            // Basic fallback
            html = processedMarkdown
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/^### (.+)$/gm, '<h3>$1</h3>')
                .replace(/^## (.+)$/gm, '<h2>$1</h2>')
                .replace(/^# (.+)$/gm, '<h1>$1</h1>')
                .replace(/`([^`]+)`/g, '<code>$1</code>')
                .replace(/\n\n/g, '</p><p>')
                .replace(/^/, '<p>')
                .replace(/$/, '</p>');
        }

        // Post-process: Replace wikilink placeholders with actual HTML links
        html = html.replace(/%%WIKILINK_(\d+)%%/g, (match, index) => {
            const target = wikilinks[parseInt(index)];
            return `<a href="#" class="wikilink" data-target="${target}">[${target}]</a>`;
        });

        return html;
    }

    /**
     * Bind click handlers for wikilinks in the content panel
     */
    bindWikilinks() {
        if (!this.contentPanel) return;

        const wikilinks = this.contentPanel.querySelectorAll('.wikilink');
        wikilinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = link.dataset.target;
                if (target) {
                    // Execute goto command and echo it in terminal
                    this.terminal.print(`> goto ${target}`);
                    this.cmdGoto([target]);
                }
            });
        });
    }

    // --- Command implementations ---

    cmdLook() {
        this.showLocation();
    }

    cmdGo(args) {
        if (args.length === 0) {
            this.terminal.print('Go where? (north, south, east, west)');
            return;
        }

        const direction = args[0].toLowerCase();
        const validDirections = ['north', 'south', 'east', 'west', 'n', 's', 'e', 'w'];

        if (!validDirections.includes(direction)) {
            this.terminal.print(`Invalid direction: ${direction}`);
            return;
        }

        // Normalize short directions
        const dirMap = { n: 'north', s: 'south', e: 'east', w: 'west' };
        const fullDirection = dirMap[direction] || direction;

        const result = this.world.navigate(
            this.player.currentLocation,
            fullDirection,
            this.player.currentEra
        );

        if (result.success) {
            this.terminal.print(`You travel ${fullDirection}...`);
            const isNew = this.player.moveTo(result.target);
            if (isNew) {
                this.terminal.print('(New area discovered! +10 XP)');
            }
            this.showLocation();
        } else {
            this.terminal.print(result.message);
        }
    }

    cmdEnter(args) {
        if (args.length === 0) {
            const section = this.world.getSection(this.player.currentLocation);
            const children = section?.children || [];
            if (children.length === 0) {
                this.terminal.print('There is nothing to enter here.');
            } else {
                this.terminal.print('Enter what? Available:');
                children.slice(0, 10).forEach(c => {
                    const childSection = this.world.getSection(c);
                    this.terminal.print(`  - ${childSection?.displayName || c}`);
                });
                if (children.length > 10) {
                    this.terminal.print(`  ... and ${children.length - 10} more`);
                }
            }
            return;
        }

        const target = args.join(' ');
        const result = this.world.enter(
            this.player.currentLocation,
            target,
            this.player.currentEra
        );

        if (result.success) {
            this.terminal.print('You enter...');
            const isNew = this.player.moveTo(result.target);
            if (isNew) {
                this.terminal.print('(New area discovered! +10 XP)');
            }
            this.showLocation();
        } else {
            this.terminal.print(result.message);
        }
    }

    cmdExit() {
        const result = this.world.exit(
            this.player.currentLocation,
            this.player.currentEra
        );

        if (result.success) {
            this.terminal.print('You exit to the parent area...');
            this.player.moveTo(result.target);
            this.showLocation();
        } else {
            this.terminal.print(result.message);
        }
    }

    cmdWarp(args) {
        if (args.length === 0) {
            this.terminal.print('Warp where? Usage: warp <location>');
            this.terminal.print(`You have visited ${this.player.state.sectionsVisited.length} locations.`);
            return;
        }

        const target = args.join(' ');
        const result = this.world.warp(
            target,
            this.player.currentEra,
            this.player.getVisitedSections()
        );

        if (result.success) {
            this.terminal.print('You warp through space...');
            this.player.moveTo(result.target);
            this.showLocation();
        } else {
            this.terminal.print(result.message);
        }
    }

    cmdGoto(args) {
        if (args.length === 0) {
            this.terminal.print('Goto where? Usage: goto <stable.name>');
            this.terminal.print('Example: goto class.copy, goto expr.prim.lambda');
            return;
        }

        const target = args.join('.');  // Allow "goto class copy" or "goto class.copy"
        const section = this.world.getSection(target);

        if (!section) {
            // Try partial match
            const allSections = Object.keys(this.world.sections);
            const matches = allSections.filter(s =>
                s.includes(target) ||
                this.world.sections[s].displayName.toLowerCase().includes(target.toLowerCase())
            );

            if (matches.length === 0) {
                this.terminal.print(`Section "${target}" not found.`);
                this.terminal.print('Use "search <term>" to find sections.');
                return;
            }

            if (matches.length === 1) {
                // Single match - go there
                const match = matches[0];
                if (!this.world.isAvailableInEra(match, this.player.currentEra)) {
                    this.terminal.print(`${match} doesn't exist in ${this.world.getEraName(this.player.currentEra)}.`);
                    return;
                }
                this.terminal.print(`Going to ${match}...`);
                this.player.moveTo(match);
                this.showLocation();
                return;
            }

            // Multiple matches - show list
            this.terminal.print(`Multiple matches for "${target}":`);
            matches.slice(0, 10).forEach(m => {
                const s = this.world.getSection(m);
                this.terminal.print(`  ${m} - ${s?.title || ''}`);
            });
            if (matches.length > 10) {
                this.terminal.print(`  ... and ${matches.length - 10} more`);
            }
            return;
        }

        // Exact match
        if (!this.world.isAvailableInEra(target, this.player.currentEra)) {
            this.terminal.print(`${target} doesn't exist in ${this.world.getEraName(this.player.currentEra)}.`);
            return;
        }

        this.player.moveTo(target);
        this.showLocation();
    }

    cmdSearch(args) {
        if (args.length === 0) {
            this.terminal.print('Search for what? Usage: search <term>');
            return;
        }

        const term = args.join(' ').toLowerCase();
        const allSections = Object.keys(this.world.sections);

        // Search in stable names and titles
        const matches = allSections.filter(s => {
            const section = this.world.sections[s];
            return s.toLowerCase().includes(term) ||
                   section.title?.toLowerCase().includes(term) ||
                   section.displayName?.toLowerCase().includes(term);
        });

        // Filter by current era
        const available = matches.filter(m =>
            this.world.isAvailableInEra(m, this.player.currentEra)
        );

        if (available.length === 0) {
            this.terminal.print(`No sections found matching "${term}" in ${this.world.getEraName(this.player.currentEra)}.`);
            return;
        }

        this.terminal.print(`Found ${available.length} sections matching "${term}":`);
        this.terminal.print('');

        available.slice(0, 20).forEach(m => {
            const s = this.world.getSection(m);
            this.terminal.print(`  [[${m}]] - ${s?.title || s?.displayName || ''}`);
        });

        if (available.length > 20) {
            this.terminal.print(`  ... and ${available.length - 20} more`);
        }

        this.terminal.print('');
        this.terminal.print('Use "goto <stable.name>" to jump to a section.');
    }

    cmdMap() {
        const currentSection = this.world.getSection(this.player.currentLocation);
        const realm = this.world.getRealm(currentSection?.realm);

        if (!realm) {
            this.terminal.print('Unable to display map.');
            return;
        }

        this.terminal.print('');
        this.terminal.print(`Map of ${realm.name}`);
        this.terminal.printSeparator();
        this.terminal.print(realm.description);
        this.terminal.print('');

        // Show top-level sections in this realm
        const sections = realm.sections
            .filter(s => this.world.isAvailableInEra(s, this.player.currentEra))
            .slice(0, 15);

        sections.forEach(s => {
            const section = this.world.getSection(s);
            const visited = this.player.hasVisited(s) ? '✓' : ' ';
            const current = s === this.player.currentLocation ? '→' : ' ';
            this.terminal.print(`${current}[${visited}] ${section?.displayName || s}`);
        });

        if (realm.sections.length > 15) {
            this.terminal.print(`... and ${realm.sections.length - 15} more areas`);
        }
    }

    cmdWhere() {
        const section = this.world.getSection(this.player.currentLocation);
        if (!section) {
            this.terminal.print('Location unknown.');
            return;
        }

        // Build path from root
        const path = [section.displayName];
        let current = section.parent;
        while (current) {
            const parentSection = this.world.getSection(current);
            if (parentSection) {
                path.unshift(parentSection.displayName);
                current = parentSection.parent;
            } else {
                break;
            }
        }

        this.terminal.print('');
        this.terminal.print(`Location: ${path.join(' > ')}`);
        this.terminal.print(`Stable name: [[${section.stableName}]]`);
        this.terminal.print(`Era: ${this.world.getEraName(this.player.currentEra)}`);
        this.terminal.print(`Realm: ${this.world.getRealm(section.realm)?.name || section.realm}`);
    }

    cmdTimeshift(args) {
        if (args.length === 0) {
            this.terminal.print('Timeshift to which era?');
            this.terminal.print('Available: cpp11, cpp14, cpp17, cpp20, cpp23, cpp26');
            return;
        }

        const eraMap = {
            'cpp11': 'n3337', 'c++11': 'n3337', 'n3337': 'n3337',
            'cpp14': 'n4140', 'c++14': 'n4140', 'n4140': 'n4140',
            'cpp17': 'n4659', 'c++17': 'n4659', 'n4659': 'n4659',
            'cpp20': 'n4861', 'c++20': 'n4861', 'n4861': 'n4861',
            'cpp23': 'n4950', 'c++23': 'n4950', 'n4950': 'n4950',
            'cpp26': 'trunk', 'c++26': 'trunk', 'trunk': 'trunk',
        };

        const input = args[0].toLowerCase();
        const eraTag = eraMap[input];

        if (!eraTag) {
            this.terminal.print(`Unknown era: ${args[0]}`);
            this.terminal.print('Available: cpp11, cpp14, cpp17, cpp20, cpp23, cpp26');
            return;
        }

        if (eraTag === this.player.currentEra) {
            this.terminal.print(`You are already in ${this.world.getEraName(eraTag)}.`);
            return;
        }

        // Check if current location exists in target era
        if (!this.world.isAvailableInEra(this.player.currentLocation, eraTag)) {
            const section = this.world.getSection(this.player.currentLocation);
            this.terminal.print(`${section?.displayName || this.player.currentLocation} doesn't exist in ${this.world.getEraName(eraTag)}.`);
            this.terminal.print('You would be displaced to a nearby location.');
            // Could implement displacement logic here
            return;
        }

        this.terminal.print('');
        this.terminal.print('*The world ripples as you shift through time...*');
        this.terminal.print('');

        const isFirst = this.player.setEra(eraTag);
        if (isFirst) {
            this.terminal.print('(First time travel! +50 XP)');
            this.terminal.print('You have unlocked the Chrono Compass.');
        }

        // Don't scroll to top on timeshift - preserve scroll position
        this.showLocation(false);
    }

    cmdEra() {
        this.terminal.print('');
        this.terminal.print(`Current era: ${this.world.getEraName(this.player.currentEra)}`);
        this.terminal.print('');
        this.terminal.print('Available eras:');

        const eras = this.world.getAllEras();
        for (const [tag, name] of Object.entries(eras)) {
            const current = tag === this.player.currentEra ? '→' : ' ';
            this.terminal.print(`${current} ${name} (${tag})`);
        }
    }

    cmdTalk(args) {
        const npcsHere = this.getNPCsAtLocation(this.player.currentLocation);

        if (npcsHere.length === 0) {
            this.terminal.print('There is no one here to talk to.');
            return;
        }

        let targetNPC = null;

        if (args.length === 0) {
            if (npcsHere.length === 1) {
                targetNPC = npcsHere[0];
            } else {
                this.terminal.print('Talk to whom?');
                npcsHere.forEach(npc => this.terminal.print(`  - ${npc.name}`));
                return;
            }
        } else {
            const npcName = args.join(' ').toLowerCase();
            targetNPC = npcsHere.find(npc =>
                npc.name.toLowerCase().includes(npcName) ||
                npc.id.toLowerCase().includes(npcName)
            );

            if (!targetNPC) {
                this.terminal.print(`Cannot find "${args.join(' ')}" here.`);
                return;
            }
        }

        // Get greeting based on era
        const dialogue = targetNPC.dialogue || {};
        let greeting = dialogue.greeting;
        if (typeof greeting === 'object') {
            greeting = greeting[this.player.currentEra] || greeting.default || 'Hello.';
        }

        this.terminal.print('');
        this.terminal.print(`${targetNPC.name}: "${greeting}"`);

        // Show available topics
        const topics = Object.keys(dialogue.topics || {});
        if (topics.length > 0) {
            this.terminal.print('');
            this.terminal.print(`Ask about: ${topics.join(', ')}`);
        }

        // Record interaction
        this.player.talkToNPC(targetNPC.id);
    }

    cmdAsk(args) {
        if (args.length < 2 || args[0].toLowerCase() !== 'about') {
            this.terminal.print('Usage: ask about <topic>');
            return;
        }

        const topic = args.slice(1).join(' ').toLowerCase();
        const npcsHere = this.getNPCsAtLocation(this.player.currentLocation);

        for (const npc of npcsHere) {
            const topics = npc.dialogue?.topics || {};
            for (const [topicKey, response] of Object.entries(topics)) {
                if (topicKey.toLowerCase().includes(topic) || topic.includes(topicKey.toLowerCase())) {
                    this.terminal.print('');
                    this.terminal.print(`${npc.name}: "${response}"`);
                    return;
                }
            }
        }

        this.terminal.print(`No one here knows about "${topic}".`);
    }

    cmdInventory() {
        this.terminal.print('');
        this.terminal.print(`Inventory (${this.player.inventory.length} items):`);
        this.terminal.printSeparator();

        if (this.player.inventory.length === 0) {
            this.terminal.print('Your inventory is empty.');
            return;
        }

        // Group by category
        const categories = {};
        for (const itemId of this.player.inventory) {
            const item = this.items.find(i => i.id === itemId);
            if (item) {
                const cat = item.category || 'misc';
                if (!categories[cat]) categories[cat] = [];
                categories[cat].push(item);
            }
        }

        for (const [category, items] of Object.entries(categories)) {
            this.terminal.print(`${category}:`);
            items.forEach(item => {
                this.terminal.print(`  - ${item.name} (${item.rarity})`);
            });
        }
    }

    cmdExamine(args) {
        if (args.length === 0) {
            this.terminal.print('Examine what?');
            return;
        }

        const itemName = args.join(' ').toLowerCase();

        // Check inventory first
        for (const itemId of this.player.inventory) {
            const item = this.items.find(i => i.id === itemId);
            if (item && (item.name.toLowerCase().includes(itemName) || item.id.includes(itemName))) {
                this.terminal.print('');
                this.terminal.print(`${item.name} (${item.rarity})`);
                this.terminal.printSeparator();
                this.terminal.print(item.description);
                if (item.lore) {
                    this.terminal.print('');
                    this.terminal.print(item.lore);
                }
                return;
            }
        }

        // Check items in location
        const itemsHere = this.getItemsAtLocation(this.player.currentLocation);
        for (const item of itemsHere) {
            if (item.name.toLowerCase().includes(itemName) || item.id.includes(itemName)) {
                this.terminal.print('');
                this.terminal.print(`${item.name} (${item.rarity})`);
                this.terminal.printSeparator();
                this.terminal.print(item.description);
                this.terminal.print('');
                this.terminal.print('Use "take" to pick it up.');
                return;
            }
        }

        this.terminal.print(`Cannot find "${args.join(' ')}" to examine.`);
    }

    cmdTake(args) {
        if (args.length === 0) {
            this.terminal.print('Take what?');
            return;
        }

        const itemName = args.join(' ').toLowerCase();
        const itemsHere = this.getItemsAtLocation(this.player.currentLocation);

        for (const item of itemsHere) {
            if (item.name.toLowerCase().includes(itemName) || item.id.includes(itemName)) {
                this.player.addItem(item.id);

                this.terminal.print(`You pick up the ${item.name}.`);

                // Apply effects
                if (item.effects?.statBoost) {
                    for (const [stat, amount] of Object.entries(item.effects.statBoost)) {
                        this.player.boostStat(stat, amount);
                        this.terminal.print(`+${amount} ${stat}`);
                    }
                }

                return;
            }
        }

        this.terminal.print(`Cannot find "${args.join(' ')}" to take.`);
    }

    cmdStats() {
        this.terminal.print('');
        this.terminal.print(`${this.player.state.name} - Level ${this.player.level} ${this.player.title}`);
        this.terminal.printSeparator();
        this.terminal.print(`XP: ${this.player.experience}/${this.player.experienceToNext}`);
        this.terminal.print('');
        this.terminal.print('Stats:');

        for (const [stat, value] of Object.entries(this.player.stats)) {
            const bar = '█'.repeat(Math.floor(value / 5)) + '░'.repeat(20 - Math.floor(value / 5));
            this.terminal.print(`  ${stat}: ${bar} ${value}`);
        }

        this.terminal.print('');
        this.terminal.print(`Sections visited: ${this.player.state.sectionsVisited.length}`);
        this.terminal.print(`Time travels: ${this.player.state.timeTravelsPerformed}`);
    }

    cmdHelp() {
        this.terminal.print(`
NAVIGATION
  look (l)           - View current location
  go <direction>     - Move north/south/east/west (or n/s/e/w)
  enter <area>       - Enter a sub-section
  exit               - Return to parent section
  goto (g) <name>    - Jump to any [[stable.name]]
  search <term>      - Find sections by name or title
  warp <location>    - Fast travel to visited location
  map                - Show current realm overview
  where              - Show location in hierarchy

TIME TRAVEL
  timeshift <era>    - Travel to era (cpp11/14/17/20/23/26)
  era                - Show current era and list available

INTERACTION
  talk [npc]         - Talk to an NPC
  ask about <topic>  - Ask NPC about a topic

ITEMS
  inventory (i)      - View your items
  examine <item>     - Look at an item
  take <item>        - Pick up an item

PLAYER
  stats              - View character stats

SYSTEM
  help (h, ?)        - Show this help
  clear              - Clear terminal
  save               - Force save game
  reset              - Reset game to initial state (requires confirmation)
`);
    }

    cmdSave() {
        this.player.save();
        this.terminal.print('Game saved.');
    }

    cmdReset(args) {
        if (args.length === 0 || args[0].toLowerCase() !== 'confirm') {
            this.terminal.print('');
            this.terminal.print('⚠ WARNING: This will completely reset your game!');
            this.terminal.print('');
            this.terminal.print('You will lose:');
            this.terminal.print('  - All visited locations');
            this.terminal.print('  - All collected items');
            this.terminal.print('  - All experience and level progress');
            this.terminal.print('  - NPC interaction history');
            this.terminal.print('  - Quest progress');
            this.terminal.print('');
            this.terminal.print('Type "reset confirm" to confirm the reset.');
            return;
        }

        // User confirmed - perform reset
        this.terminal.print('');
        this.terminal.print('Resetting game...');
        this.terminal.print('*The world fades and reforms around you...*');

        // Clear all game-related localStorage
        this.player.reset();
        localStorage.removeItem('adventure-terminal-width');

        // Reload the page to get a completely fresh state
        setTimeout(() => {
            window.location.reload();
        }, 1000);
    }
}

// Initialize game when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const terminalEl = document.getElementById('adventure-terminal');
    const contentEl = document.getElementById('adventure-content');

    if (terminalEl) {
        window.game = new AdventureGame(terminalEl, contentEl);
        window.game.init();
    }

    // Initialize resizable divider
    initResizableDivider();
});

/**
 * Initialize the resizable divider between terminal and content panels
 */
function initResizableDivider() {
    const divider = document.getElementById('resize-divider');
    const terminalContainer = document.querySelector('.adventure-terminal-container');
    const contentContainer = document.querySelector('.adventure-content-container');
    const main = document.querySelector('.adventure-main');

    if (!divider || !terminalContainer || !contentContainer || !main) {
        return;
    }

    let isDragging = false;
    let startX = 0;
    let startTerminalWidth = 0;

    // Load saved width from localStorage
    const savedWidth = localStorage.getItem('adventure-terminal-width');
    if (savedWidth) {
        const width = parseFloat(savedWidth);
        if (width > 0 && width < 100) {
            terminalContainer.style.width = `${width}%`;
            contentContainer.style.width = `${100 - width}%`;
        }
    } else {
        // Default 50/50 split
        terminalContainer.style.width = '50%';
        contentContainer.style.width = '50%';
    }

    divider.addEventListener('mousedown', (e) => {
        isDragging = true;
        startX = e.clientX;
        startTerminalWidth = terminalContainer.getBoundingClientRect().width;

        divider.classList.add('dragging');
        document.body.classList.add('resizing');

        e.preventDefault();
    });

    document.addEventListener('mousemove', (e) => {
        if (!isDragging) return;

        const mainRect = main.getBoundingClientRect();
        const deltaX = e.clientX - startX;
        const newTerminalWidth = startTerminalWidth + deltaX;

        // Calculate percentage (accounting for divider width)
        const dividerWidth = divider.getBoundingClientRect().width;
        const availableWidth = mainRect.width - dividerWidth;
        let terminalPercent = (newTerminalWidth / availableWidth) * 100;

        // Clamp between 20% and 80%
        terminalPercent = Math.max(20, Math.min(80, terminalPercent));

        terminalContainer.style.width = `${terminalPercent}%`;
        contentContainer.style.width = `${100 - terminalPercent}%`;
    });

    document.addEventListener('mouseup', () => {
        if (!isDragging) return;

        isDragging = false;
        divider.classList.remove('dragging');
        document.body.classList.remove('resizing');

        // Save the width to localStorage
        const terminalPercent = (terminalContainer.getBoundingClientRect().width /
            (main.getBoundingClientRect().width - divider.getBoundingClientRect().width)) * 100;
        localStorage.setItem('adventure-terminal-width', terminalPercent.toString());
    });

    // Handle touch events for mobile
    divider.addEventListener('touchstart', (e) => {
        if (e.touches.length === 1) {
            isDragging = true;
            startX = e.touches[0].clientX;
            startTerminalWidth = terminalContainer.getBoundingClientRect().width;

            divider.classList.add('dragging');
            document.body.classList.add('resizing');

            e.preventDefault();
        }
    });

    document.addEventListener('touchmove', (e) => {
        if (!isDragging || e.touches.length !== 1) return;

        const mainRect = main.getBoundingClientRect();
        const deltaX = e.touches[0].clientX - startX;
        const newTerminalWidth = startTerminalWidth + deltaX;

        const dividerWidth = divider.getBoundingClientRect().width;
        const availableWidth = mainRect.width - dividerWidth;
        let terminalPercent = (newTerminalWidth / availableWidth) * 100;

        terminalPercent = Math.max(20, Math.min(80, terminalPercent));

        terminalContainer.style.width = `${terminalPercent}%`;
        contentContainer.style.width = `${100 - terminalPercent}%`;
    });

    document.addEventListener('touchend', () => {
        if (!isDragging) return;

        isDragging = false;
        divider.classList.remove('dragging');
        document.body.classList.remove('resizing');

        const terminalPercent = (terminalContainer.getBoundingClientRect().width /
            (main.getBoundingClientRect().width - divider.getBoundingClientRect().width)) * 100;
        localStorage.setItem('adventure-terminal-width', terminalPercent.toString());
    });
}
