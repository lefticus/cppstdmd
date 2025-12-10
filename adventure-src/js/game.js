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

        // ISHML-based parser (initialized after world loads)
        this.parser = new AdventureParser();

        // Diff animator for timewarp animations
        this.diffAnimator = new DiffAnimator(contentPanel);

        // Era order for keyboard navigation (chronological order)
        this.eraOrder = ['n3337', 'n4140', 'n4659', 'n4861', 'n4950', 'trunk'];

        // Era to version slug mapping (maps current era to the "previous → current" diff slug)
        this.eraToSlug = {
            'n4140': 'cpp11-to-cpp14',  // C++14: link to C++11→C++14
            'n4659': 'cpp14-to-cpp17',  // C++17: link to C++14→C++17
            'n4861': 'cpp17-to-cpp20',  // C++20: link to C++17→C++20
            'n4950': 'cpp20-to-cpp23',  // C++23: link to C++20→C++23
            'trunk': 'cpp23-to-trunk',  // Trunk: link to C++23→Trunk
            'n3337': 'cpp11-to-cpp14',  // C++11: link to C++11→C++14 (no prior, so use first)
        };

        // Era to external standard URL base mapping
        this.eraToStandardUrl = {
            'trunk': 'https://eel.is/c++draft/',           // Latest working draft
            'n4950': 'https://timsong-cpp.github.io/cppwp/n4950/',  // C++23
            'n4861': 'https://timsong-cpp.github.io/cppwp/n4861/',  // C++20
            'n4659': 'https://timsong-cpp.github.io/cppwp/n4659/',  // C++17
            'n4140': 'https://timsong-cpp.github.io/cppwp/n4140/',  // C++14
            'n3337': 'https://timsong-cpp.github.io/cppwp/n3337/',  // C++11
        };

        // NPCs and other data
        this.npcs = [];
        this.items = [];
        this.quests = [];
        this.puzzles = [];
        this.episodeCorrelations = {};

        // Quest state
        this.pendingQuest = null;  // Quest currently being offered

        // Puzzle state
        this.activePuzzle = null;  // Puzzle currently being solved
        this.puzzleHintsUsed = 0;  // Hints used on current puzzle

        // Command registry (maps verb keys to handlers)
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

            // Initialize ISHML parser with world data
            this.parser.init(this.world.worldData);

            // Load additional game data
            await Promise.all([
                this.loadNPCs(),
                this.loadItems(),
                this.loadQuests(),
                this.loadPuzzles(),
                this.loadEpisodeCorrelations(),
            ]);

            // Load or create player save
            const hasSave = this.player.load();

            // Apply animation speed setting from saved preferences
            this.updateAnimationClass();

            // Validate player location exists
            if (!this.world.getSection(this.player.currentLocation)) {
                this.player.state.currentLocation = 'intro';
                this.player.save();
            }

            // Handle URL parameters for deep linking (e.g., from diff pages)
            const urlParams = new URLSearchParams(window.location.search);
            const sectionParam = urlParams.get('section');
            const eraParam = urlParams.get('era');

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

            // Execute deep link commands (if coming from a diff page)
            // cmdTimeshift handles era validation and mapping (cpp11, c++11, n3337, etc.)
            if (eraParam) {
                this.terminal.print(`> timeshift ${eraParam}`);
                this.cmdTimeshift([eraParam]);
            }

            if (sectionParam && this.world.getSection(sectionParam)) {
                this.terminal.print(`> goto ${sectionParam}`);
                this.cmdGoto([sectionParam]);
            } else {
                // Show current location if no deep link
                await this.showLocation();
            }

            // Update UI
            this.updateStatusBar();

            // Bind keyboard shortcuts for era navigation
            this.bindKeyboardShortcuts();

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
     * Load episode correlations data (C++ Weekly episodes related to sections)
     */
    async loadEpisodeCorrelations() {
        try {
            const response = await fetch('/data/game/episode-correlations.json');
            if (response.ok) {
                this.episodeCorrelations = await response.json();
            }
        } catch (error) {
            console.warn('Failed to load episode correlations:', error);
        }
    }

    /**
     * Get C++ Weekly episodes related to a section
     * @param {string} stableName - The section's stable name
     * @returns {Array} Array of episode objects with title, youtube_url, etc.
     */
    getEpisodesForSection(stableName) {
        return this.episodeCorrelations[stableName] || [];
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

            // Settings
            'speed': (args) => this.cmdSpeed(args),
            'animation': (args) => this.cmdSpeed(args),

            // Quests
            'quests': () => this.cmdQuests(),
            'quest': () => this.cmdQuests(),
            'journal': () => this.cmdQuests(),
            'accept': () => this.cmdAcceptQuest(),
            'decline': () => this.cmdDeclineQuest(),

            // Puzzles
            'solve': (args) => this.cmdSolve(args),
            'puzzle': () => this.cmdPuzzle(),
            'answer': (args) => this.cmdAnswer(args),
            'hint': () => this.cmdHint(),

            // Debug (undocumented)
            'iddqd': () => this.cmdGodMode(),
        };
    }

    /**
     * Handle a command input
     */
    async handleCommand(input) {
        // Use ISHML parser to interpret the command
        const parsed = this.parser.parse(input);

        if (!parsed.verb) {
            this.terminal.print(`I don't understand "${input}".`);
            this.terminal.print('Type "help" for a list of commands.');
            return;
        }

        const verb = parsed.verb;
        const args = parsed.args;

        // Special handling for direction shortcuts when used as standalone commands
        if (['north', 'south', 'east', 'west'].includes(verb) && args.length === 0) {
            await this.cmdGo([verb]);
        } else if (verb === 'ask') {
            // Pass raw input to cmdAsk so it can extract the topic correctly
            // (ISHML may transform topic names like "navigation" to section keys)
            await this.cmdAsk(args, input);
        } else if (this.commands[verb]) {
            await this.commands[verb](args);
        } else {
            // Fallback: maybe it's a section name for goto
            if (this.world.getSection(input.trim())) {
                await this.cmdGoto([input.trim()]);
            } else {
                this.terminal.print(`Unknown command: ${verb}`);
                this.terminal.print('Type "help" for a list of commands.');
            }
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

        // Also update the back link
        this.updateBackLink();
    }

    /**
     * Update the "Back to cppevo" link to point to the current section's diff page
     */
    updateBackLink() {
        const backLink = document.getElementById('back-to-cppevo');
        const era = this.player.currentEra;
        const location = this.player.currentLocation;
        const slug = this.eraToSlug[era];

        if (backLink) {
            if (slug && location) {
                // Sanitize stable name for URL (same logic as Python sanitize_filename)
                const safeName = location.replace(/[<>:"/\\|?*]/g, '_');
                backLink.href = `/diffs/${slug}/${safeName}.html`;
                backLink.textContent = `View in cppevo`;
            } else {
                backLink.href = '/';
                backLink.textContent = 'Back to cppevo';
            }
        }

        // Update the "View Standard" link to point to the external standard site
        this.updateStandardLink();

        // Update the "View Markdown" link to point to the GitHub repo
        this.updateMarkdownLink();
    }

    /**
     * Update the "View Standard" link to point to the external standard website
     * (eel.is for trunk, timsong-cpp for archived versions)
     */
    updateStandardLink() {
        const standardLink = document.getElementById('view-standard');
        if (!standardLink) return;

        const era = this.player.currentEra;
        const location = this.player.currentLocation;
        const baseUrl = this.eraToStandardUrl[era];

        if (baseUrl && location) {
            standardLink.href = `${baseUrl}${location}`;
        } else if (baseUrl) {
            standardLink.href = baseUrl;
        } else {
            standardLink.href = 'https://eel.is/c++draft/';
        }
    }

    /**
     * Update the "View Markdown" link to point to the GitHub repo at the correct SHA
     */
    updateMarkdownLink() {
        const markdownLink = document.getElementById('view-markdown');
        if (!markdownLink) return;

        const era = this.player.currentEra;
        const location = this.player.currentLocation;
        const section = this.world.getSection(location);
        const sha = this.world.cppstdmdSha || 'main';

        // Map era tags to directory names (trunk is special)
        const eraDir = era === 'trunk' ? 'trunk' : era;

        if (section && section.chapter && location) {
            // Link to specific file and anchor
            markdownLink.href = `https://github.com/lefticus/cppstdmd/blob/${sha}/${eraDir}/${section.chapter}.md#${location}`;
        } else if (era) {
            // Just link to the version directory
            markdownLink.href = `https://github.com/lefticus/cppstdmd/blob/${sha}/${eraDir}`;
        } else {
            markdownLink.href = 'https://github.com/lefticus/cppstdmd';
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
            this.terminal.printMarkdown(realm.description);
            this.terminal.print('');
        }

        // Section description
        this.terminal.printMarkdown(section.description);

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
            for (const npc of npcsHere) {
                // Check if NPC has available quests
                let hasQuest = false;
                if (npc.quests && npc.quests.length > 0) {
                    for (const questId of npc.quests) {
                        const quest = this.quests.find(q => q.id === questId);
                        if (quest && this.canOfferQuest(quest)) {
                            hasQuest = true;
                            break;
                        }
                    }
                }
                if (hasQuest) {
                    this.terminal.print(`You see: ${npc.name} (has a quest for you!)`);
                } else {
                    this.terminal.print(`You see: ${npc.name}`);
                }
            }
        }

        // Items here
        const itemsHere = this.getItemsAtLocation(section.stableName);
        if (itemsHere.length > 0) {
            this.terminal.print('');
            const itemNames = itemsHere.map(i => `${i.name} (${i.rarity})`).join(', ');
            this.terminal.print(`Items: ${itemNames}`);
        }

        // Related C++ Weekly episodes
        const episodes = this.getEpisodesForSection(section.stableName);
        if (episodes.length > 0) {
            this.terminal.print('');
            this.terminal.print('📺 Related C++ Weekly:');
            // Show top 3 episodes (already sorted by confidence)
            for (const ep of episodes.slice(0, 3)) {
                const epNum = ep.episode || '?';
                const title = ep.title || `Episode ${epNum}`;
                const url = ep.youtube_url || '#';
                // Create clickable link in the terminal
                this.terminal.printHTML(
                    `  • <a href="${url}" target="_blank" rel="noopener noreferrer" class="episode-link">Ep ${epNum}: ${title}</a>`
                );
            }
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
            titleEl.textContent = `${section.displayName} [${section.stableName}]`;
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
        // Check quest progress for reading the current location
        this.checkQuestProgress({
            section: this.player.currentLocation,
            read: true
        });
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

        // Allow "goto class copy" or "goto class.copy" or "goto [class.copy]"
        let target = args.join('.');
        // Strip brackets if present (e.g., "[class.copy]" -> "class.copy")
        target = target.replace(/^\[+|\]+$/g, '');
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
                this.checkQuestProgress({ section: match });
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

        // Check quest progress
        this.checkQuestProgress({ section: target });
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
        this.terminal.printMarkdown(realm.description);
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

    /**
     * Bind keyboard shortcuts for era navigation
     */
    bindKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Only handle shortcuts when not typing in terminal input
            if (document.activeElement === this.terminal.input) return;

            if (e.key === '[') {
                e.preventDefault();
                this.warpBackward();
            } else if (e.key === ']') {
                e.preventDefault();
                this.warpForward();
            }
        });
    }

    /**
     * Warp to the previous era (keyboard shortcut: [)
     */
    warpBackward() {
        const currentIndex = this.eraOrder.indexOf(this.player.currentEra);
        if (currentIndex > 0) {
            const targetEra = this.eraOrder[currentIndex - 1];
            this.terminal.print(`> timeshift ${this.world.getEraName(targetEra)}`);
            this.doTimeshift(targetEra);
        } else {
            this.terminal.print('You are already in the earliest era (C++11).');
        }
    }

    /**
     * Warp to the next era (keyboard shortcut: ])
     */
    warpForward() {
        const currentIndex = this.eraOrder.indexOf(this.player.currentEra);
        if (currentIndex < this.eraOrder.length - 1) {
            const targetEra = this.eraOrder[currentIndex + 1];
            this.terminal.print(`> timeshift ${this.world.getEraName(targetEra)}`);
            this.doTimeshift(targetEra);
        } else {
            this.terminal.print('You are already in the latest era (C++26).');
        }
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

        this.doTimeshift(eraTag);
    }

    /**
     * Perform the actual timeshift with animation
     * @param {string} eraTag - Target era tag (e.g., 'n4950')
     */
    async doTimeshift(eraTag) {
        const oldEra = this.player.currentEra;

        if (eraTag === oldEra) {
            this.terminal.print(`You are already in ${this.world.getEraName(eraTag)}.`);
            return;
        }

        // Check if current location exists in target era
        if (!this.world.isAvailableInEra(this.player.currentLocation, eraTag)) {
            const section = this.world.getSection(this.player.currentLocation);
            this.terminal.print(`${section?.displayName || this.player.currentLocation} doesn't exist in ${this.world.getEraName(eraTag)}.`);
            this.terminal.print('You would be displaced to a nearby location.');
            return;
        }

        const section = this.world.getSection(this.player.currentLocation);

        this.terminal.print('');
        this.terminal.print('*The world ripples as you shift through time...*');

        // Update player era
        const isFirst = this.player.setEra(eraTag);

        // Update content panel title
        const titleEl = document.getElementById('content-title');
        if (titleEl) {
            titleEl.textContent = `${section.displayName} [${section.stableName}]`;
        }

        // Get the new rendered HTML for the target era
        const newHtml = await this.getRenderedSectionHtml(section, eraTag);

        // Animate the transition using morphdom
        let hasChanges = false;
        if (newHtml && this.diffAnimator) {
            const duration = this.player.getAnimationDuration();
            const result = await this.diffAnimator.animateTransition(newHtml, duration);
            hasChanges = result.hasChanges;

            // Apply syntax highlighting and wikilink bindings after morph
            if (typeof Prism !== 'undefined') {
                Prism.highlightAllUnder(this.contentPanel);
            }
            this.bindWikilinks();
        } else {
            // Fallback: just load the content normally
            await this.loadContentPanel(section, false);
        }

        if (hasChanges) {
            this.terminal.print('*Changes shimmer into view...*');
        } else {
            this.terminal.print('*This section appears unchanged across time.*');
        }

        this.terminal.print('');

        if (isFirst) {
            this.terminal.print('(First time travel! +50 XP)');
            this.terminal.print('You have unlocked the Chrono Compass.');
        }

        // Update terminal with location info and status bar
        this.printLocationHeader(section);
        this.updateStatusBar();

        // Check quest progress for era change
        this.checkQuestProgress({ era: eraTag, section: this.player.currentLocation });
    }

    /**
     * Print location header to terminal (without loading content panel)
     */
    printLocationHeader(section) {
        const eraName = this.world.getEraName(this.player.currentEra);
        const realm = this.world.getRealm(section.realm);

        this.terminal.print('');
        this.terminal.printLocation(eraName, section.displayName, section.stableName);
        this.terminal.printSeparator('═');

        if (section.stableName === section.realm && realm) {
            this.terminal.printMarkdown(realm.description);
            this.terminal.print('');
        }

        this.terminal.printMarkdown(section.description);

        const exits = this.world.getExitDescriptions(section.stableName, this.player.currentEra);
        if (exits.length > 0) {
            this.terminal.print('');
            this.terminal.print(`Exits: ${exits.join(', ')}`);
        }

        const npcsHere = this.getNPCsAtLocation(section.stableName);
        if (npcsHere.length > 0) {
            this.terminal.print('');
            for (const npc of npcsHere) {
                // Check if NPC has available quests
                let hasQuest = false;
                if (npc.quests && npc.quests.length > 0) {
                    for (const questId of npc.quests) {
                        const quest = this.quests.find(q => q.id === questId);
                        if (quest && this.canOfferQuest(quest)) {
                            hasQuest = true;
                            break;
                        }
                    }
                }
                if (hasQuest) {
                    this.terminal.print(`You see: ${npc.name} (has a quest for you!)`);
                } else {
                    this.terminal.print(`You see: ${npc.name}`);
                }
            }
        }

        const itemsHere = this.getItemsAtLocation(section.stableName);
        if (itemsHere.length > 0) {
            this.terminal.print('');
            const itemNames = itemsHere.map(i => `${i.name} (${i.rarity})`).join(', ');
            this.terminal.print(`Items: ${itemNames}`);
        }
    }

    /**
     * Get rendered HTML for a section in a specific era (without updating DOM)
     */
    async getRenderedSectionHtml(section, era) {
        if (!section) return null;

        const chapter = section.chapter;
        const url = `/${era}/${chapter}.md`;

        try {
            const response = await fetch(url);
            if (!response.ok) return null;

            const markdown = await response.text();
            const sectionContent = this.extractSectionContent(markdown, section.stableName);

            return this.renderMarkdown(sectionContent || 'Section content not found.');
        } catch (error) {
            return null;
        }
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
        this.terminal.print(`${targetNPC.name}:`);
        this.terminal.printMarkdown(greeting);

        // Show available topics (filtered by era restrictions)
        const allTopics = dialogue.topics || {};
        const availableTopics = Object.entries(allTopics)
            .filter(([key, data]) => {
                // If topic has era restriction, check if current era matches
                if (typeof data === 'object' && !Array.isArray(data) && data.requiresEra) {
                    return data.requiresEra === this.player.currentEra;
                }
                return true;
            })
            .map(([key]) => key);

        if (availableTopics.length > 0) {
            this.terminal.print('');
            this.terminal.print(`Ask about: ${availableTopics.join(', ')}`);
        }

        // Record interaction
        this.player.talkToNPC(targetNPC.id);

        // Check if NPC has quests to offer
        if (targetNPC.quests && targetNPC.quests.length > 0) {
            for (const questId of targetNPC.quests) {
                const quest = this.quests.find(q => q.id === questId);
                if (quest && this.canOfferQuest(quest)) {
                    this.offerQuest(quest, targetNPC);
                    break;  // Only offer one quest at a time
                }
            }
        }
    }

    cmdAsk(args, rawInput) {
        // For "ask about <topic>", we need the raw topic text, not the
        // ISHML-transformed args (which may convert "navigation" to a section key)
        let topic;

        if (rawInput) {
            // Extract topic from raw input: "ask about <topic>" or "ask <topic>"
            const match = rawInput.toLowerCase().match(/^ask\s+(?:about\s+)?(.+)$/);
            if (match) {
                topic = match[1].trim();
            }
        }

        // Fallback to args if raw input parsing failed
        if (!topic) {
            if (args.length === 0) {
                this.terminal.print('Usage: ask about <topic>');
                return;
            } else if (args[0].toLowerCase() === 'about') {
                // "ask about <topic>" - skip "about"
                if (args.length < 2) {
                    this.terminal.print('Usage: ask about <topic>');
                    return;
                }
                topic = args.slice(1).join(' ').toLowerCase();
            } else {
                // Parser already stripped "about", args is just the topic
                topic = args.join(' ').toLowerCase();
            }
        }
        const npcsHere = this.getNPCsAtLocation(this.player.currentLocation);

        for (const npc of npcsHere) {
            const topics = npc.dialogue?.topics || {};
            for (const [topicKey, topicData] of Object.entries(topics)) {
                if (topicKey.toLowerCase().includes(topic) || topic.includes(topicKey.toLowerCase())) {
                    // Handle era-specific topic responses (like greetings)
                    let response;
                    if (typeof topicData === 'object' && !Array.isArray(topicData)) {
                        // Era-specific responses: { "trunk": "...", "n4950": "...", "default": "..." }
                        // Also supports "requiresEra" to restrict topic availability
                        if (topicData.requiresEra && topicData.requiresEra !== this.player.currentEra) {
                            // Topic not available in this era
                            continue;
                        }
                        response = topicData[this.player.currentEra] || topicData.default || topicData.response;
                    } else {
                        // Simple string response
                        response = topicData;
                    }

                    if (!response) continue;

                    this.terminal.print('');
                    this.terminal.print(`${npc.name}:`);
                    this.terminal.printMarkdown(response);

                    // Check quest progress for asking about a topic
                    this.checkQuestProgress({
                        section: this.player.currentLocation,
                        era: this.player.currentEra,
                        npc: npc.id,
                        topic: topicKey
                    });
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
                this.terminal.printMarkdown(item.description);
                if (item.lore) {
                    this.terminal.print('');
                    this.terminal.printMarkdown(item.lore);
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
                this.terminal.printMarkdown(item.description);
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
  [ / ]              - Warp to previous/next era (keyboard shortcuts)

INTERACTION
  talk [npc]         - Talk to an NPC
  ask about <topic>  - Ask NPC about a topic

QUESTS
  quests             - View active and completed quests
  accept             - Accept an offered quest
  decline            - Decline an offered quest

PUZZLES (in quests)
  solve              - Start solving a puzzle
  puzzle             - Show current puzzle
  answer <response>  - Submit your answer
  hint               - Get a hint for the puzzle

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

    cmdSpeed(args) {
        const validSpeeds = ['slow', 'normal', 'fast', 'off'];
        const currentSpeed = this.player.getSetting('animationSpeed') || 'normal';

        if (args.length === 0) {
            this.terminal.print('');
            this.terminal.print(`Current animation speed: ${currentSpeed}`);
            this.terminal.print('');
            this.terminal.print('Available speeds:');
            this.terminal.print('  slow   - 2 seconds (detailed view of changes)');
            this.terminal.print('  normal - 1.2 seconds (default)');
            this.terminal.print('  fast   - 0.5 seconds (quick transitions)');
            this.terminal.print('  off    - instant (no animation)');
            this.terminal.print('');
            this.terminal.print('Usage: speed <slow|normal|fast|off>');
            return;
        }

        const speed = args[0].toLowerCase();
        if (!validSpeeds.includes(speed)) {
            this.terminal.print(`Unknown speed: ${speed}`);
            this.terminal.print('Valid options: slow, normal, fast, off');
            return;
        }

        this.player.setSetting('animationSpeed', speed);
        this.updateAnimationClass();
        this.terminal.print(`Animation speed set to: ${speed}`);
    }

    /**
     * God mode - max level for testing (undocumented)
     */
    cmdGodMode() {
        this.player.state.level = 99;
        this.player.state.experience = 999999;
        this.player.save();
        this.terminal.print('');
        this.terminal.print('*Reality bends to your will*');
        this.terminal.print('Level set to 99. All restrictions lifted.');
        this.terminal.print('');
        this.updateStatusBar();
    }

    // --- Quest System ---

    /**
     * Check if a quest can be offered to the player
     */
    canOfferQuest(quest) {
        // Already active or completed
        if (this.player.state.activeQuests.includes(quest.id)) return false;
        if (this.player.state.completedQuests.includes(quest.id)) return false;

        // Check level requirement
        if (quest.minLevel && this.player.level < quest.minLevel) return false;

        // Check prerequisites
        if (quest.prerequisites) {
            for (const prereq of quest.prerequisites) {
                if (!this.player.state.completedQuests.includes(prereq)) {
                    return false;
                }
            }
        }

        return true;
    }

    /**
     * Offer a quest to the player
     */
    offerQuest(quest, npc) {
        this.pendingQuest = quest;

        this.terminal.print('');
        this.terminal.printSeparator('─');
        this.terminal.print(`📜 Quest Available: ${quest.title}`);
        this.terminal.print(`   Difficulty: ${quest.difficulty || 'unknown'}`);
        if (quest.minLevel) {
            this.terminal.print(`   Required Level: ${quest.minLevel}`);
        }
        this.terminal.print('');
        this.terminal.printMarkdown(quest.description);
        this.terminal.print('');
        this.terminal.print('Type "accept" to begin this quest, or "decline" to refuse.');
        this.terminal.printSeparator('─');
    }

    /**
     * Accept the pending quest
     */
    cmdAcceptQuest() {
        if (!this.pendingQuest) {
            this.terminal.print('No quest has been offered.');
            return;
        }

        const quest = this.pendingQuest;
        this.player.startQuest(quest.id);
        this.pendingQuest = null;

        this.terminal.print('');
        this.terminal.print(`Quest accepted: ${quest.title}`);
        this.showCurrentObjective(quest);
    }

    /**
     * Decline the pending quest
     */
    cmdDeclineQuest() {
        if (!this.pendingQuest) {
            this.terminal.print('No quest has been offered.');
            return;
        }

        const questTitle = this.pendingQuest.title;
        this.pendingQuest = null;
        this.terminal.print(`Quest "${questTitle}" declined.`);
    }

    /**
     * Show quest journal / active quests
     */
    cmdQuests() {
        const active = this.player.state.activeQuests;
        const completed = this.player.state.completedQuests;

        this.terminal.print('');
        this.terminal.print('═══ Quest Journal ═══');

        if (active.length === 0 && completed.length === 0) {
            this.terminal.print('');
            this.terminal.print('You have no quests.');
            this.terminal.print('Talk to NPCs to discover quests.');
            return;
        }

        if (active.length > 0) {
            this.terminal.print('');
            this.terminal.print('Active Quests:');
            for (const questId of active) {
                const quest = this.quests.find(q => q.id === questId);
                if (!quest) continue;

                const progress = this.player.state.questProgress[questId];
                const currentStep = progress?.currentStep || 0;
                const totalSteps = quest.steps?.length || 0;

                this.terminal.print('');
                this.terminal.print(`  📜 ${quest.title} [${currentStep}/${totalSteps}]`);

                // Show current objective
                if (quest.steps && quest.steps[currentStep]) {
                    const step = quest.steps[currentStep];
                    this.terminal.printMarkdown(`     → ${step.instruction}`);
                }
            }
        }

        if (completed.length > 0) {
            this.terminal.print('');
            this.terminal.print(`Completed Quests: ${completed.length}`);
            for (const questId of completed.slice(0, 5)) {
                const quest = this.quests.find(q => q.id === questId);
                if (quest) {
                    this.terminal.print(`  ✓ ${quest.title}`);
                }
            }
            if (completed.length > 5) {
                this.terminal.print(`  ... and ${completed.length - 5} more`);
            }
        }
    }

    // ═══════════════════════════════════════════════════════════════════════
    // Puzzle Commands
    // ═══════════════════════════════════════════════════════════════════════

    /**
     * Get the puzzle for the current quest step (if any)
     */
    getCurrentPuzzle() {
        // Check if current quest step requires a puzzle
        for (const questId of this.player.state.activeQuests) {
            const quest = this.quests.find(q => q.id === questId);
            const progress = this.player.state.questProgress[questId];
            if (!quest || !progress || !quest.steps) continue;

            const step = quest.steps[progress.currentStep];
            if (step?.target?.puzzle) {
                const puzzle = this.puzzles.find(p => p.id === step.target.puzzle);
                if (puzzle) {
                    return { puzzle, quest, step };
                } else {
                    // Puzzle referenced but doesn't exist - error!
                    return { error: `Puzzle "${step.target.puzzle}" not found! This is a content error.`, puzzleId: step.target.puzzle };
                }
            }
        }
        return null;
    }

    /**
     * Show puzzle status or start puzzle
     */
    cmdPuzzle() {
        if (this.activePuzzle) {
            // Show current puzzle state
            this.showPuzzle(this.activePuzzle);
            return;
        }

        const puzzleInfo = this.getCurrentPuzzle();
        if (!puzzleInfo) {
            this.terminal.print('No puzzle is currently available.');
            this.terminal.print('Complete quest steps to unlock puzzles.');
            return;
        }

        if (puzzleInfo.error) {
            this.terminal.print(`ERROR: ${puzzleInfo.error}`);
            return;
        }

        // Start the puzzle
        this.activePuzzle = puzzleInfo.puzzle;
        this.puzzleHintsUsed = 0;
        this.showPuzzle(puzzleInfo.puzzle);
    }

    /**
     * Start solving a puzzle
     */
    cmdSolve(args) {
        // If no args, show current puzzle or available puzzle
        if (args.length === 0) {
            this.cmdPuzzle();
            return;
        }

        // Could support "solve puzzle" as alias
        const puzzleName = args.join(' ').toLowerCase();
        if (puzzleName === 'puzzle') {
            this.cmdPuzzle();
            return;
        }

        this.terminal.print(`Unknown puzzle: ${puzzleName}`);
        this.terminal.print('Use "puzzle" to see available puzzles.');
    }

    /**
     * Display a puzzle
     */
    showPuzzle(puzzle) {
        this.terminal.print('');
        this.terminal.print(`═══ ${puzzle.type === 'quiz' ? 'Quiz' : 'Puzzle'}: ${puzzle.id} ═══`);
        this.terminal.print(`Difficulty: ${puzzle.difficulty}`);
        this.terminal.print('');
        this.terminal.printMarkdown(puzzle.question);
        this.terminal.print('');

        if (puzzle.type === 'quiz') {
            this.terminal.print('Answer with T (True) or F (False) for each question.');
            this.terminal.print('Format: answer TFTF or answer T F T F');
        } else if (puzzle.type === 'matching') {
            this.terminal.print('Match items from the left to the right.');
            // Show shuffled options for matching
            const rights = puzzle.pairs.map(p => p[1]);
            this.terminal.print('');
            puzzle.pairs.forEach((pair, i) => {
                this.terminal.print(`  ${i + 1}. ${pair[0]}`);
            });
            this.terminal.print('');
            this.terminal.print('Options (in random order):');
            const shuffled = [...rights].sort(() => Math.random() - 0.5);
            shuffled.forEach((opt, i) => {
                this.terminal.print(`  ${String.fromCharCode(65 + i)}. ${opt}`);
            });
            this.terminal.print('');
            this.terminal.print('Answer with letters matching each number: answer 1A 2B 3C...');
        }

        this.terminal.print('');
        this.terminal.print('Commands: answer <your answer>, hint, puzzle (redisplay)');
    }

    /**
     * Submit an answer to the current puzzle
     */
    cmdAnswer(args) {
        if (!this.activePuzzle) {
            this.terminal.print('No puzzle is currently active.');
            this.terminal.print('Use "puzzle" or "solve" to start a puzzle.');
            return;
        }

        if (args.length === 0) {
            this.terminal.print('Usage: answer <your answer>');
            return;
        }

        const puzzle = this.activePuzzle;
        const answer = args.join(' ').toUpperCase().replace(/\s+/g, '');

        if (puzzle.type === 'quiz') {
            // Check quiz answers (T/F format)
            const expected = puzzle.answers.join('').toUpperCase();
            if (answer === expected) {
                this.puzzleSolved(puzzle);
            } else {
                this.terminal.print('');
                this.terminal.print('❌ Incorrect! Try again.');
                const correct = answer.split('').filter((c, i) => c === expected[i]).length;
                this.terminal.print(`You got ${correct}/${expected.length} correct.`);
                this.terminal.print('Use "hint" for help, or "puzzle" to see the questions again.');
            }
        } else if (puzzle.type === 'matching') {
            // For matching, we'd need more complex handling
            this.terminal.print('Matching puzzle answers are not yet implemented.');
        }
    }

    /**
     * Request a hint for the current puzzle
     */
    cmdHint() {
        if (!this.activePuzzle) {
            this.terminal.print('No puzzle is currently active.');
            return;
        }

        const puzzle = this.activePuzzle;
        const hints = puzzle.hints || [];

        if (hints.length === 0) {
            this.terminal.print('No hints available for this puzzle.');
            return;
        }

        if (this.puzzleHintsUsed >= hints.length) {
            this.terminal.print('You\'ve used all available hints!');
            return;
        }

        const hint = hints[this.puzzleHintsUsed];
        this.puzzleHintsUsed++;

        this.terminal.print('');
        this.terminal.print(`═══ Hint ${this.puzzleHintsUsed}/${hints.length} ═══`);
        this.terminal.printMarkdown(hint);
    }

    /**
     * Handle puzzle completion
     */
    puzzleSolved(puzzle) {
        this.terminal.print('');
        this.terminal.print('✓ Correct! Puzzle solved!');
        this.terminal.print('');

        // Show explanation
        if (puzzle.explanation) {
            this.terminal.print('═══ Explanation ═══');
            this.terminal.printMarkdown(puzzle.explanation);
        }

        // Grant rewards
        if (puzzle.rewards) {
            this.terminal.print('');
            this.terminal.print('Rewards:');
            if (puzzle.rewards.xp) {
                const result = this.player.gainExperience(puzzle.rewards.xp);
                this.terminal.print(`  +${puzzle.rewards.xp} XP`);
                if (result.leveledUp) {
                    this.terminal.print(`  Level up! You are now level ${result.newLevel}!`);
                }
            }
            if (puzzle.rewards.item) {
                const item = this.items.find(i => i.id === puzzle.rewards.item);
                if (item) {
                    this.player.addItem(item.id);
                    this.terminal.print(`  Received: ${item.name}`);
                }
            }
        }

        // Track solved puzzle
        if (!this.player.state.solvedPuzzles) {
            this.player.state.solvedPuzzles = [];
        }
        if (!this.player.state.solvedPuzzles.includes(puzzle.id)) {
            this.player.state.solvedPuzzles.push(puzzle.id);
        }

        // Clear active puzzle
        this.activePuzzle = null;
        this.puzzleHintsUsed = 0;

        // Check quest progress for solving this puzzle
        // Include section and era context so quest steps with multiple conditions can match
        console.log('puzzleSolved: checking progress for puzzle.id =', puzzle.id);
        this.checkQuestProgress({
            puzzle: puzzle.id,
            section: this.player.currentLocation,
            era: this.player.currentEra
        });

        this.player.save();
        this.updateStatusBar();
    }

    /**
     * Show the current objective for a quest
     */
    showCurrentObjective(quest) {
        const progress = this.player.state.questProgress[quest.id];
        const currentStep = progress?.currentStep || 0;

        if (quest.steps && quest.steps[currentStep]) {
            const step = quest.steps[currentStep];
            this.terminal.print('');
            this.terminal.print('Current objective:');
            this.terminal.printMarkdown(`  → ${step.instruction}`);
        }
    }

    /**
     * Check if any quest steps were completed by an action
     * @param {object} action - The action performed (section, era, npc, topic)
     */
    checkQuestProgress(action) {
        for (const questId of this.player.state.activeQuests) {
            const quest = this.quests.find(q => q.id === questId);
            const progress = this.player.state.questProgress[questId];
            if (!quest || !progress || !quest.steps) continue;

            const step = quest.steps[progress.currentStep];
            if (!step?.target) continue;

            console.log('checkQuestProgress: step.target =', JSON.stringify(step.target), 'action =', JSON.stringify(action));
            const completed = this.stepCompleted(step.target, action);
            console.log('checkQuestProgress: stepCompleted returned', completed);
            if (completed) {
                this.advanceQuest(quest, progress);
            }
        }
    }

    /**
     * Check if a step's target requirements are met
     */
    stepCompleted(target, action) {
        // All specified target conditions must match
        if (target.section && action.section !== target.section) return false;
        if (target.era && action.era !== target.era) return false;
        if (target.npc && action.npc !== target.npc) return false;
        if (target.topic && !action.topic?.toLowerCase().includes(target.topic.toLowerCase())) return false;
        if (target.puzzle && action.puzzle !== target.puzzle) return false;
        if (target.read && !action.read) return false;

        // At least one condition must be present and matched
        return target.section || target.era || target.npc || target.topic || target.puzzle || target.read;
    }

    /**
     * Advance a quest to the next step
     */
    advanceQuest(quest, progress) {
        const completedStep = quest.steps[progress.currentStep];
        progress.completed.push(progress.currentStep);
        progress.currentStep++;

        const isQuestComplete = progress.currentStep >= quest.steps.length;

        this.terminal.print('');
        this.terminal.printSeparator('─');
        if (isQuestComplete) {
            this.terminal.print(`✓ Quest complete!`);
        } else {
            this.terminal.print(`✓ Quest step completed!`);
        }

        // Show step completion rewards
        if (completedStep.onComplete) {
            if (completedStep.onComplete.dialogue) {
                this.terminal.print('');
                this.terminal.printMarkdown(completedStep.onComplete.dialogue);
            }
            if (completedStep.onComplete.xp) {
                const result = this.player.gainExperience(completedStep.onComplete.xp);
                this.terminal.print(`  +${completedStep.onComplete.xp} XP`);
                if (result.leveledUp) {
                    this.terminal.print(`  Level up! You are now level ${result.newLevel}!`);
                }
            }
            if (completedStep.onComplete.item) {
                const item = this.items.find(i => i.id === completedStep.onComplete.item);
                if (item) {
                    this.player.addItem(item.id);
                    this.terminal.print(`  Received: ${item.name}`);
                }
            }
        }

        // Check if quest is complete
        if (isQuestComplete) {
            this.completeQuest(quest);
        } else {
            this.showCurrentObjective(quest);
        }

        this.terminal.printSeparator('─');
        this.player.save();
        this.updateStatusBar();
    }

    /**
     * Complete a quest and grant final rewards
     */
    completeQuest(quest) {
        this.player.completeQuest(quest.id);

        this.terminal.print('');
        this.terminal.print(`🎉 Quest Complete: ${quest.title}!`);

        if (quest.rewards) {
            if (quest.rewards.experience) {
                const result = this.player.gainExperience(quest.rewards.experience);
                this.terminal.print(`  +${quest.rewards.experience} XP`);
                if (result.leveledUp) {
                    this.terminal.print(`  Level up! You are now level ${result.newLevel}!`);
                }
            }
            if (quest.rewards.items) {
                for (const itemId of quest.rewards.items) {
                    const item = this.items.find(i => i.id === itemId);
                    if (item) {
                        this.player.addItem(itemId);
                        this.terminal.print(`  Received: ${item.name}`);
                    }
                }
            }
            if (quest.rewards.title) {
                this.terminal.print(`  Title earned: "${quest.rewards.title}"`);
            }
        }
    }

    /**
     * Update body class to match animation speed setting
     */
    updateAnimationClass() {
        const speed = this.player.getSetting('animationSpeed') || 'normal';
        document.body.classList.remove('animation-slow', 'animation-normal', 'animation-fast', 'animation-off');
        document.body.classList.add(`animation-${speed}`);
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
