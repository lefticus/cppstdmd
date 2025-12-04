/**
 * diff.js - Diff animation for C++ Standard Adventure Game timewarp feature
 *
 * Provides smooth animated transitions when traveling between C++ eras.
 * Uses morphdom to diff rendered HTML and animate changes in place.
 */

class DiffAnimator {
    constructor(contentPanel) {
        this.contentPanel = contentPanel;
    }

    /**
     * Animate transition from current rendered content to new rendered content
     * Uses morphdom to efficiently diff and update the DOM with animations
     *
     * @param {string} newHtml - New rendered HTML content
     * @param {number} duration - Animation duration in ms (0 = instant, no animation)
     * @returns {Promise<{hasChanges: boolean}>} Result object
     */
    async animateTransition(newHtml, duration = 1200) {
        // If duration is 0, just swap content instantly
        if (duration === 0) {
            this.contentPanel.innerHTML = newHtml;
            return { hasChanges: true };
        }

        const animationDuration = duration;
        if (typeof morphdom === 'undefined') {
            console.warn('morphdom library not loaded, falling back to direct replacement');
            this.contentPanel.innerHTML = newHtml;
            return { hasChanges: true };
        }

        // Track if any changes occurred
        let hasChanges = false;
        const nodesToRemove = [];

        // Create a wrapper div for the new content
        const wrapper = document.createElement('div');
        wrapper.innerHTML = newHtml;

        // Use morphdom to diff and update the DOM
        morphdom(this.contentPanel, wrapper, {
            childrenOnly: true,

            // Called before a node is removed
            onBeforeNodeDiscarded: (node) => {
                if (node.nodeType === Node.ELEMENT_NODE) {
                    hasChanges = true;
                    // Add animation class and delay removal
                    node.classList.add('morph-removing');
                    nodesToRemove.push(node);
                    return false; // Don't remove yet
                }
                return true;
            },

            // Called when a new node is added
            onNodeAdded: (node) => {
                if (node.nodeType === Node.ELEMENT_NODE) {
                    hasChanges = true;
                    node.classList.add('morph-added');
                    // Remove the class after animation completes
                    setTimeout(() => {
                        node.classList.remove('morph-added');
                    }, animationDuration);
                }
                return node;
            },

            // Called when an element is updated (content changed)
            onElUpdated: (el) => {
                if (el.nodeType === Node.ELEMENT_NODE) {
                    hasChanges = true;
                    el.classList.add('morph-changed');
                    setTimeout(() => {
                        el.classList.remove('morph-changed');
                    }, animationDuration);
                }
            },

            // Called before element is updated - can skip updates
            onBeforeElUpdated: (fromEl, toEl) => {
                // Always update
                return true;
            }
        });

        // Wait for animations to play, then remove the discarded nodes
        if (nodesToRemove.length > 0) {
            await new Promise(resolve => setTimeout(resolve, animationDuration));
            nodesToRemove.forEach(node => {
                if (node.parentNode) {
                    node.parentNode.removeChild(node);
                }
            });
        }

        // Small delay to let added/changed animations complete
        if (hasChanges) {
            await new Promise(resolve => setTimeout(resolve, 100));
        }

        return { hasChanges };
    }

    /**
     * Simple check if two HTML strings are meaningfully different
     * (ignoring whitespace differences)
     */
    htmlDiffers(html1, html2) {
        const normalize = (html) => html.replace(/\s+/g, ' ').trim();
        return normalize(html1) !== normalize(html2);
    }
}
