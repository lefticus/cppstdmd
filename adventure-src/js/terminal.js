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

        this.render();
        this.bindEvents();
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
     * @param {string} text - Text to print
     * @param {string} className - Optional CSS class for styling
     */
    print(text, className = '') {
        const line = document.createElement('div');
        line.className = `terminal-line ${className}`.trim();
        line.textContent = text;
        this.output.appendChild(line);
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
        this.printHTML(`<span class="era-tag">[${era}]</span> <span class="location-name">${location}</span> <span class="stable-name">[[${stableName}]]</span>`);
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
