/**
 * terminal.js - Terminal UI component for the C++ Standard Adventure Game
 *
 * Provides a text-based terminal interface with:
 * - Command input with history (up/down arrows)
 * - Scrolling output area
 * - Command callback handling
 */

class Terminal {
    constructor(container) {
        this.container = container;
        this.history = [];
        this.historyIndex = -1;
        this.onCommand = null;
        this.onWikilinkClick = null;  // Callback for wikilink clicks

        this.render();
        this.bindEvents();
    }

    /**
     * Escape HTML special characters to prevent XSS and display issues
     * @param {string} text - Text to escape
     * @returns {string} Escaped text safe for innerHTML
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Convert [[stable.name]] wikilinks to clickable HTML
     * @param {string} text - Text potentially containing wikilinks
     * @returns {string} HTML with wikilinks converted to anchor tags
     */
    processWikilinks(text) {
        // First escape HTML, then convert wikilinks
        const escaped = this.escapeHtml(text);
        return escaped.replace(
            /\[\[([^\]]+)\]\]/g,
            '<a href="#" class="wikilink" data-target="$1">[$1]</a>'
        );
    }

    /**
     * Bind click handlers for wikilinks in a container element
     * @param {HTMLElement} container - Container to search for wikilinks
     */
    bindWikilinksIn(container) {
        const wikilinks = container.querySelectorAll('.wikilink');
        wikilinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = link.dataset.target;
                if (target && this.onWikilinkClick) {
                    this.onWikilinkClick(target);
                }
            });
        });
    }

    render() {
        this.container.innerHTML = `
            <div class="terminal-output" id="terminal-output"></div>
            <div class="terminal-input-line">
                <span class="terminal-prompt">&gt;</span>
                <input type="text" class="terminal-input" id="terminal-input"
                       placeholder="Type a command..." autocomplete="off" spellcheck="false">
            </div>
        `;

        this.output = this.container.querySelector('#terminal-output');
        this.input = this.container.querySelector('#terminal-input');
    }

    bindEvents() {
        this.input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                const cmd = this.input.value.trim();
                if (cmd) {
                    this.history.push(cmd);
                    this.historyIndex = this.history.length;
                    this.print(`> ${cmd}`, 'command');
                    this.input.value = '';
                    if (this.onCommand) {
                        this.onCommand(cmd);
                    }
                }
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                if (this.historyIndex > 0) {
                    this.historyIndex--;
                    this.input.value = this.history[this.historyIndex];
                    // Move cursor to end
                    setTimeout(() => {
                        this.input.selectionStart = this.input.selectionEnd = this.input.value.length;
                    }, 0);
                }
            } else if (e.key === 'ArrowDown') {
                e.preventDefault();
                if (this.historyIndex < this.history.length - 1) {
                    this.historyIndex++;
                    this.input.value = this.history[this.historyIndex];
                } else {
                    this.historyIndex = this.history.length;
                    this.input.value = '';
                }
            }
        });

        // Focus input on container click
        this.container.addEventListener('click', (e) => {
            // Don't steal focus if user is selecting text
            if (window.getSelection().toString() === '') {
                this.input.focus();
            }
        });
    }

    /**
     * Print a line to the terminal output
     * Automatically converts [[stable.name]] to clickable links
     * @param {string} text - Text to print
     * @param {string} className - Optional CSS class for styling
     */
    print(text, className = '') {
        const line = document.createElement('div');
        line.className = `terminal-line ${className}`.trim();

        // Check if text contains wikilinks
        if (text.includes('[[')) {
            line.innerHTML = this.processWikilinks(text);
            this.output.appendChild(line);
            this.bindWikilinksIn(line);
        } else {
            line.textContent = text;
            this.output.appendChild(line);
        }
        this.scrollToBottom();
    }

    /**
     * Print multiple lines at once
     * @param {string[]} lines - Array of lines to print
     * @param {string} className - Optional CSS class for styling
     */
    printLines(lines, className = '') {
        lines.forEach(line => this.print(line, className));
    }

    /**
     * Print HTML content to the terminal
     * @param {string} html - HTML string to render
     */
    printHTML(html) {
        const line = document.createElement('div');
        line.className = 'terminal-line';
        line.innerHTML = html;
        this.output.appendChild(line);
        this.scrollToBottom();
    }

    /**
     * Print markdown content to the terminal
     * Uses marked.js for rendering and Prism.js for syntax highlighting
     * @param {string} text - Markdown text to render
     */
    printMarkdown(text) {
        // Fallback to plain text if marked isn't available
        if (typeof marked === 'undefined') {
            return this.print(text);
        }

        // Process wikilinks before markdown (use placeholder to preserve them)
        // Use a format that won't be interpreted as markdown emphasis
        const wikilinks = [];
        const withPlaceholders = text.replace(/\[\[([^\]]+)\]\]/g, (match, target) => {
            wikilinks.push(target);
            return `WIKILINK_PLACEHOLDER_${wikilinks.length - 1}_END`;
        });

        // Render markdown
        let html = marked.parse(withPlaceholders);

        // Restore wikilinks
        html = html.replace(/WIKILINK_PLACEHOLDER_(\d+)_END/g, (match, index) => {
            const target = wikilinks[parseInt(index)];
            return `<a href="#" class="wikilink" data-target="${target}">[${target}]</a>`;
        });

        const line = document.createElement('div');
        line.className = 'terminal-line terminal-markdown';
        line.innerHTML = html;
        this.output.appendChild(line);
        this.bindWikilinksIn(line);

        // Syntax highlighting for code blocks
        if (typeof Prism !== 'undefined') {
            Prism.highlightAllUnder(line);
        }

        // Add Compiler Explorer links to C++ code blocks
        this.addCompilerExplorerLinks(line);

        this.scrollToBottom();
    }

    /**
     * Encode string to base64 with proper UTF-8 handling
     * @param {string} str - String to encode
     * @returns {string} Base64 encoded string
     */
    b64UTFEncode(str) {
        return btoa(encodeURIComponent(str).replace(/%([0-9A-F]{2})/g, function(match, v) {
            return String.fromCharCode(parseInt(v, 16));
        }));
    }

    /**
     * Generate a Compiler Explorer link for code
     * @param {string} code - C++ code to open in CE
     * @returns {string} Compiler Explorer URL
     */
    generateCompilerExplorerLink(code) {
        const clientState = {
            sessions: [{
                id: 1,
                language: 'c++',
                source: code,
                compilers: [{
                    id: 'clang_trunk',
                    options: '-std=c++26'
                }]
            }]
        };

        const encoded = this.b64UTFEncode(JSON.stringify(clientState));
        return `https://compiler-explorer.com/clientstate/${encoded}`;
    }

    /**
     * Add "Try in Compiler Explorer" links to C++ code blocks
     * @param {HTMLElement} container - Container to search for code blocks
     */
    addCompilerExplorerLinks(container) {
        const codeBlocks = container.querySelectorAll('pre code.language-cpp, pre code.language-c\\+\\+');
        codeBlocks.forEach(codeBlock => {
            const code = codeBlock.textContent;
            const pre = codeBlock.parentElement;

            // Create link container
            const linkDiv = document.createElement('div');
            linkDiv.className = 'ce-link-container';

            const link = document.createElement('a');
            link.href = this.generateCompilerExplorerLink(code);
            link.target = '_blank';
            link.rel = 'noopener noreferrer';
            link.className = 'ce-link';
            link.textContent = '▶ Try in Compiler Explorer';

            linkDiv.appendChild(link);
            pre.parentElement.insertBefore(linkDiv, pre.nextSibling);
        });
    }

    /**
     * Print a horizontal separator
     */
    printSeparator(char = '─', length = 50) {
        this.print(char.repeat(length), 'separator');
    }

    /**
     * Print styled text (era indicator, location name, etc.)
     * @param {string} era - Era name (e.g., "C++23")
     * @param {string} location - Location display name
     * @param {string} stableName - Stable name (e.g., "class.copy")
     */
    printLocation(era, location, stableName) {
        // Escape location to handle titles with < > characters (like `<initializer_list>`)
        const safeLocation = this.escapeHtml(location);
        // Make the stable name a clickable wikilink
        const line = document.createElement('div');
        line.className = 'terminal-line';
        line.innerHTML = `<span class="era-tag">[${era}]</span> <span class="location-name">${safeLocation}</span> <span class="stable-name"><a href="#" class="wikilink" data-target="${stableName}">[${stableName}]</a></span>`;
        this.output.appendChild(line);
        this.bindWikilinksIn(line);
        this.scrollToBottom();
    }

    /**
     * Clear the terminal output
     */
    clear() {
        this.output.innerHTML = '';
    }

    /**
     * Scroll output to bottom
     */
    scrollToBottom() {
        this.output.scrollTop = this.output.scrollHeight;
    }

    /**
     * Focus the input field
     */
    focus() {
        this.input.focus();
    }

    /**
     * Disable input (e.g., during async operations)
     */
    disable() {
        this.input.disabled = true;
    }

    /**
     * Enable input
     */
    enable() {
        this.input.disabled = false;
        this.focus();
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Terminal;
}
