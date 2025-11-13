// C++ Standard Evolution Viewer - Navigation & Enhancement

(function() {
    'use strict';

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    function init() {
        // Add keyboard shortcuts
        addKeyboardShortcuts();

        // Add smooth scrolling
        addSmoothScrolling();

        // Add copy-to-clipboard for section names
        addCopyButtons();

        // Enhance external links
        enhanceExternalLinks();

        // Add theme toggle (optional)
        // addThemeToggle();
    }

    /**
     * Add keyboard shortcuts for navigation
     */
    function addKeyboardShortcuts() {
        document.addEventListener('keydown', function(e) {
            // Ignore if user is typing in an input field
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
                return;
            }

            // 'h' - Go home
            if (e.key === 'h' || e.key === 'H') {
                const homeLink = document.querySelector('a[href*="index.html"]');
                if (homeLink) {
                    window.location.href = homeLink.href;
                }
            }

            // '/' - Focus search (if available)
            if (e.key === '/') {
                e.preventDefault();
                const searchInput = document.getElementById('search-input');
                if (searchInput) {
                    searchInput.focus();
                }
            }

            // 'Escape' - Clear search
            if (e.key === 'Escape') {
                const searchInput = document.getElementById('search-input');
                if (searchInput && searchInput === document.activeElement) {
                    searchInput.value = '';
                    searchInput.dispatchEvent(new Event('input'));
                    searchInput.blur();
                }
            }
        });
    }

    /**
     * Add smooth scrolling to anchor links
     */
    function addSmoothScrolling() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    /**
     * Add copy-to-clipboard buttons for section names
     */
    function addCopyButtons() {
        // Find all section headers with stable names (format: [name])
        const headers = document.querySelectorAll('h1, h2, h3');

        headers.forEach(header => {
            const text = header.textContent.trim();
            // Check if it's a stable name (starts with [ and ends with ])
            if (text.startsWith('[') && text.endsWith(']')) {
                const copyBtn = document.createElement('button');
                copyBtn.className = 'copy-btn';
                copyBtn.innerHTML = '<i class="fa-solid fa-copy"></i>';
                copyBtn.title = 'Copy stable name to clipboard';
                copyBtn.style.cssText = `
                    margin-left: 0.5rem;
                    padding: 0.25rem 0.5rem;
                    border: 1px solid #dee2e6;
                    background: white;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 0.9rem;
                    transition: all 0.2s ease;
                `;

                copyBtn.addEventListener('click', function() {
                    copyToClipboard(text);
                    copyBtn.innerHTML = '<i class="fa-solid fa-check"></i>';
                    copyBtn.style.backgroundColor = '#28a745';
                    copyBtn.style.color = 'white';
                    copyBtn.style.borderColor = '#28a745';

                    setTimeout(() => {
                        copyBtn.innerHTML = '<i class="fa-solid fa-copy"></i>';
                        copyBtn.style.backgroundColor = 'white';
                        copyBtn.style.color = '';
                        copyBtn.style.borderColor = '#dee2e6';
                    }, 2000);
                });

                copyBtn.addEventListener('mouseenter', function() {
                    if (copyBtn.innerHTML === '<i class="fa-solid fa-copy"></i>') {
                        copyBtn.style.backgroundColor = '#f8f9fa';
                    }
                });

                copyBtn.addEventListener('mouseleave', function() {
                    if (copyBtn.innerHTML === '<i class="fa-solid fa-copy"></i>') {
                        copyBtn.style.backgroundColor = 'white';
                    }
                });

                header.appendChild(copyBtn);
            }
        });
    }

    /**
     * Copy text to clipboard
     */
    function copyToClipboard(text) {
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text).catch(err => {
                console.error('Failed to copy:', err);
                fallbackCopy(text);
            });
        } else {
            fallbackCopy(text);
        }
    }

    /**
     * Fallback copy method for older browsers
     */
    function fallbackCopy(text) {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        try {
            document.execCommand('copy');
        } catch (err) {
            console.error('Fallback copy failed:', err);
        }
        document.body.removeChild(textarea);
    }

    /**
     * Enhance external links
     */
    function enhanceExternalLinks() {
        document.querySelectorAll('a[target="_blank"]').forEach(link => {
            // Add visual indicator for external links
            if (!link.querySelector('.external-indicator')) {
                const indicator = document.createElement('span');
                indicator.className = 'external-indicator';
                indicator.innerHTML = ' ↗';
                indicator.style.fontSize = '0.85em';
                indicator.style.opacity = '0.7';
                link.appendChild(indicator);
            }
        });
    }

    /**
     * Add theme toggle (dark mode) - Optional
     */
    function addThemeToggle() {
        // Check if user has a theme preference
        const currentTheme = localStorage.getItem('theme') || 'light';

        // Create toggle button
        const toggleBtn = document.createElement('button');
        toggleBtn.id = 'theme-toggle';
        toggleBtn.innerHTML = currentTheme === 'dark' ? '<i class="fa-solid fa-sun"></i>' : '<i class="fa-solid fa-moon"></i>';
        toggleBtn.title = 'Toggle dark mode';
        toggleBtn.style.cssText = `
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            padding: 0.75rem;
            border: none;
            background: white;
            border-radius: 50%;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            cursor: pointer;
            font-size: 1.5rem;
            z-index: 1000;
            transition: all 0.3s ease;
        `;

        toggleBtn.addEventListener('click', function() {
            const newTheme = document.body.classList.contains('dark-theme') ? 'light' : 'dark';
            document.body.classList.toggle('dark-theme');
            toggleBtn.innerHTML = newTheme === 'dark' ? '<i class="fa-solid fa-sun"></i>' : '<i class="fa-solid fa-moon"></i>';
            localStorage.setItem('theme', newTheme);
        });

        toggleBtn.addEventListener('mouseenter', function() {
            toggleBtn.style.transform = 'scale(1.1)';
        });

        toggleBtn.addEventListener('mouseleave', function() {
            toggleBtn.style.transform = 'scale(1)';
        });

        document.body.appendChild(toggleBtn);

        // Apply saved theme
        if (currentTheme === 'dark') {
            document.body.classList.add('dark-theme');
        }
    }

    /**
     * Show loading indicator for large diffs
     */
    function showLoadingIndicator() {
        // Check if we're on a diff page with large content
        const diffContainer = document.querySelector('.d2h-wrapper');
        if (diffContainer) {
            const observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    if (mutation.addedNodes.length > 0) {
                        // Content loaded, hide loading indicator
                        const loader = document.querySelector('.loading-indicator');
                        if (loader) {
                            loader.remove();
                        }
                    }
                });
            });

            observer.observe(diffContainer, {
                childList: true,
                subtree: true
            });

            // Add loading indicator
            const loader = document.createElement('div');
            loader.className = 'loading-indicator';
            loader.innerHTML = '<div class="spinner"></div><p>Loading diff...</p>';
            loader.style.cssText = `
                text-align: center;
                padding: 3rem;
                color: #6c757d;
            `;

            diffContainer.insertBefore(loader, diffContainer.firstChild);
        }
    }

    // Log keyboard shortcuts hint
    console.log('%cKeyboard Shortcuts:', 'font-weight: bold; font-size: 14px');
    console.log('  h - Go to home page');
    console.log('  / - Focus search (on overview pages)');
    console.log('  Esc - Clear search');

})();
