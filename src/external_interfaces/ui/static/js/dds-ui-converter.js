/**
 * DAODISEO UI Converter - Systematic Status Indicator Replacement
 * Converts inconsistent dot indicators and status language to unified design system
 */

class DDSUIConverter {
    constructor() {
        this.statusMappings = {
            'verified': 'dds-status-verified',
            'tokenized': 'dds-status-tokenized',
            'pending': 'dds-status-pending',
            'active': 'dds-status-active',
            'inactive': 'dds-status-inactive',
            'connected': 'dds-status-active',
            'disconnected': 'dds-status-inactive',
            'online': 'dds-status-active',
            'offline': 'dds-status-inactive'
        };
        
        this.init();
    }

    init() {
        // Convert all existing status indicators on page load
        document.addEventListener('DOMContentLoaded', () => {
            this.convertAllStatusIndicators();
            this.convertAllButtons();
            this.convertAllCards();
            this.setupMutationObserver();
        });
    }

    // Convert legacy dot indicators to new status system
    convertAllStatusIndicators() {
        // Find all elements with old status classes
        const oldStatusSelectors = [
            '.status-dot',
            '.status-indicator',
            '.badge',
            '.text-success',
            '.text-warning',
            '.text-danger',
            '.text-info'
        ];

        oldStatusSelectors.forEach(selector => {
            document.querySelectorAll(selector).forEach(element => {
                this.convertStatusElement(element);
            });
        });

        // Convert specific status text
        this.convertStatusText();
    }

    convertStatusElement(element) {
        const classList = element.classList;
        const textContent = element.textContent.toLowerCase().trim();
        
        // Determine status type from classes or content
        let statusType = this.determineStatusType(element);
        
        if (statusType) {
            // Create new status element
            const newStatus = document.createElement('div');
            newStatus.className = `dds-status ${this.statusMappings[statusType]}`;
            
            // Add status dot
            const dot = document.createElement('div');
            dot.className = 'dds-status-dot';
            newStatus.appendChild(dot);
            
            // Add status text
            const text = document.createElement('span');
            text.textContent = this.getStatusText(statusType);
            newStatus.appendChild(text);
            
            // Replace old element
            element.parentNode.replaceChild(newStatus, element);
        }
    }

    determineStatusType(element) {
        const classList = Array.from(element.classList);
        const textContent = element.textContent.toLowerCase().trim();
        
        // Check text content first
        if (textContent.includes('verified') || textContent.includes('active')) return 'verified';
        if (textContent.includes('tokenized')) return 'tokenized';
        if (textContent.includes('pending')) return 'pending';
        if (textContent.includes('connected') || textContent.includes('online')) return 'active';
        if (textContent.includes('disconnected') || textContent.includes('offline')) return 'inactive';
        
        // Check classes
        if (classList.includes('text-success') || classList.includes('status-connected')) return 'verified';
        if (classList.includes('text-info')) return 'tokenized';
        if (classList.includes('text-warning')) return 'pending';
        if (classList.includes('text-danger')) return 'inactive';
        if (classList.includes('active')) return 'active';
        
        return null;
    }

    getStatusText(statusType) {
        const statusTexts = {
            'verified': 'Verified',
            'tokenized': 'Tokenized',
            'pending': 'Pending',
            'active': 'Active',
            'inactive': 'Inactive'
        };
        
        return statusTexts[statusType] || statusType;
    }

    convertStatusText() {
        // Find and replace inconsistent status language
        const walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_TEXT,
            null,
            false
        );

        const textNodes = [];
        let node;
        while (node = walker.nextNode()) {
            textNodes.push(node);
        }

        textNodes.forEach(textNode => {
            let text = textNode.textContent;
            
            // Replace inconsistent terminology
            text = text.replace(/\b(Verified|VERIFIED)\b/g, 'Verified');
            text = text.replace(/\b(Tokenized|TOKENIZED)\b/g, 'Tokenized');
            text = text.replace(/\b(Active|ACTIVE|Online|ONLINE)\b/g, 'Active');
            text = text.replace(/\b(Inactive|INACTIVE|Offline|OFFLINE)\b/g, 'Inactive');
            text = text.replace(/\b(Pending|PENDING)\b/g, 'Pending');
            
            if (text !== textNode.textContent) {
                textNode.textContent = text;
            }
        });
    }

    // Convert all buttons to unified design system
    convertAllButtons() {
        document.querySelectorAll('button, .btn').forEach(button => {
            this.convertButton(button);
        });
    }

    convertButton(button) {
        const classList = Array.from(button.classList);
        
        // Remove old Bootstrap classes
        button.classList.remove('btn-primary', 'btn-secondary', 'btn-success', 'btn-warning', 'btn-danger', 'btn-info');
        
        // Add DDS button classes
        if (!button.classList.contains('dds-btn')) {
            button.classList.add('dds-btn');
            
            // Determine button type
            if (classList.includes('btn-primary') || button.type === 'submit') {
                button.classList.add('dds-btn-primary');
            } else if (classList.includes('btn-outline-primary')) {
                button.classList.add('dds-btn-outline');
            } else {
                button.classList.add('dds-btn-secondary');
            }
            
            // Handle button sizes
            if (classList.includes('btn-sm')) {
                button.classList.add('dds-btn-sm');
            } else if (classList.includes('btn-lg')) {
                button.classList.add('dds-btn-lg');
            }
        }
    }

    // Convert all cards to unified design system
    convertAllCards() {
        document.querySelectorAll('.card').forEach(card => {
            this.convertCard(card);
        });
    }

    convertCard(card) {
        if (!card.classList.contains('dds-card')) {
            card.classList.add('dds-card');
            
            // Convert card headers
            const header = card.querySelector('.card-header');
            if (header && !header.classList.contains('dds-card-header')) {
                header.classList.add('dds-card-header');
            }
            
            // Convert card bodies
            const body = card.querySelector('.card-body');
            if (body && !body.classList.contains('dds-card-body')) {
                body.classList.add('dds-card-body');
            }
            
            // Convert card titles
            const title = card.querySelector('.card-title, h5, h6');
            if (title && !title.classList.contains('dds-card-title')) {
                title.classList.add('dds-card-title');
            }
        }
    }

    // Setup mutation observer to convert dynamically added elements
    setupMutationObserver() {
        const observer = new MutationObserver(mutations => {
            mutations.forEach(mutation => {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        this.convertDynamicElement(node);
                    }
                });
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    convertDynamicElement(element) {
        // Convert buttons
        if (element.matches('button, .btn')) {
            this.convertButton(element);
        }
        
        // Convert cards
        if (element.matches('.card')) {
            this.convertCard(element);
        }
        
        // Convert status indicators
        if (element.matches('.status-dot, .status-indicator, .badge')) {
            this.convertStatusElement(element);
        }
        
        // Convert child elements
        element.querySelectorAll('button, .btn').forEach(btn => this.convertButton(btn));
        element.querySelectorAll('.card').forEach(card => this.convertCard(card));
        element.querySelectorAll('.status-dot, .status-indicator, .badge').forEach(status => this.convertStatusElement(status));
    }

    // Utility method to update validator status indicators
    updateValidatorStatus(validatorElement, status) {
        const statusElement = validatorElement.querySelector('.dds-status');
        if (statusElement) {
            // Remove all status classes
            Object.values(this.statusMappings).forEach(className => {
                statusElement.classList.remove(className);
            });
            
            // Add new status class
            if (this.statusMappings[status]) {
                statusElement.classList.add(this.statusMappings[status]);
                
                // Update status text
                const textElement = statusElement.querySelector('span');
                if (textElement) {
                    textElement.textContent = this.getStatusText(status);
                }
            }
        }
    }

    // Utility method to create new status indicator
    createStatusIndicator(status, text = null) {
        const statusElement = document.createElement('div');
        statusElement.className = `dds-status ${this.statusMappings[status]}`;
        
        const dot = document.createElement('div');
        dot.className = 'dds-status-dot';
        statusElement.appendChild(dot);
        
        const textSpan = document.createElement('span');
        textSpan.textContent = text || this.getStatusText(status);
        statusElement.appendChild(textSpan);
        
        return statusElement;
    }
}

// Initialize the UI converter
window.ddsUIConverter = new DDSUIConverter();

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DDSUIConverter;
}