/**
 * Content Enhancement System - Replacing Generic Text with User-Friendly Content
 * Addresses loading states, unclear labeling, and data presentation issues
 */

class ContentEnhancer {
    constructor() {
        this.contentMappings = {
            // Technical terms to user-friendly explanations
            'APY': 'Annual Percentage Yield - yearly returns on your staked tokens',
            'Market Cap': 'Total value of all ODIS tokens in circulation',
            'Volume': 'Total amount of ODIS traded in the last 24 hours',
            'Staking': 'Lock your tokens to earn rewards and secure the network',
            'Validator': 'Network operator that processes transactions and earns rewards',
            'Delegation': 'Assign your tokens to a validator to earn staking rewards',
            'Governance': 'Vote on network proposals and protocol changes',
            'Liquidity': 'How easily tokens can be bought or sold without affecting price'
        };

        this.loadingMessages = [
            'Fetching latest blockchain data...',
            'Connecting to Odiseo network...',
            'Updating validator information...',
            'Loading real-time market data...',
            'Synchronizing with testnet...'
        ];

        this.init();
    }

    init() {
        document.addEventListener('DOMContentLoaded', () => {
            this.enhanceAllContent();
            this.setupContentObserver();
            this.formatFinancialData();
            this.addContextualHelp();
        });
    }

    enhanceAllContent() {
        // Replace generic "Loading..." with contextual messages
        this.replaceLoadingStates();
        
        // Add explanations to technical terms
        this.addTermExplanations();
        
        // Improve button labels and CTAs
        this.enhanceButtonLabels();
        
        // Format large numbers properly
        this.formatNumericData();
        
        // Add status explanations
        this.enhanceStatusIndicators();
    }

    replaceLoadingStates() {
        document.querySelectorAll('[data-loading]').forEach(element => {
            const context = element.dataset.loading || 'default';
            const message = this.getContextualLoadingMessage(context);
            
            element.innerHTML = `
                <div class="loading-state">
                    <div class="loading-spinner"></div>
                    <span>${message}</span>
                </div>
            `;
        });

        // Replace generic "Loading..." text
        const walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_TEXT,
            null,
            false
        );

        const textNodes = [];
        let node;
        while (node = walker.nextNode()) {
            if (node.textContent.trim() === 'Loading...') {
                textNodes.push(node);
            }
        }

        textNodes.forEach(textNode => {
            const context = this.determineLoadingContext(textNode);
            textNode.textContent = this.getContextualLoadingMessage(context);
        });
    }

    getContextualLoadingMessage(context) {
        const messages = {
            'blockchain': 'Fetching latest blockchain data...',
            'validators': 'Loading validator information...',
            'market': 'Updating market prices...',
            'portfolio': 'Calculating your portfolio value...',
            'transactions': 'Loading transaction history...',
            'charts': 'Generating price charts...',
            'default': 'Loading real-time data...'
        };

        return messages[context] || messages.default;
    }

    determineLoadingContext(textNode) {
        const parentElement = textNode.parentElement;
        if (!parentElement) return 'default';

        const className = parentElement.className.toLowerCase();
        const id = parentElement.id.toLowerCase();

        if (className.includes('validator') || id.includes('validator')) return 'validators';
        if (className.includes('market') || className.includes('price')) return 'market';
        if (className.includes('portfolio') || className.includes('balance')) return 'portfolio';
        if (className.includes('transaction') || className.includes('history')) return 'transactions';
        if (className.includes('chart') || className.includes('graph')) return 'charts';
        if (className.includes('blockchain') || className.includes('network')) return 'blockchain';

        return 'default';
    }

    addTermExplanations() {
        Object.keys(this.contentMappings).forEach(term => {
            const regex = new RegExp(`\\b${term}\\b`, 'gi');
            this.addTooltipsToText(regex, term, this.contentMappings[term]);
        });
    }

    addTooltipsToText(regex, term, explanation) {
        const walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_TEXT,
            null,
            false
        );

        const textNodes = [];
        let node;
        while (node = walker.nextNode()) {
            if (regex.test(node.textContent)) {
                textNodes.push(node);
            }
        }

        textNodes.forEach(textNode => {
            if (textNode.parentElement.closest('.tooltip-enhanced')) return;

            const newContent = textNode.textContent.replace(regex, match => {
                return `<span class="term-with-tooltip" data-tooltip="${explanation}">${match}</span>`;
            });

            if (newContent !== textNode.textContent) {
                const wrapper = document.createElement('span');
                wrapper.innerHTML = newContent;
                wrapper.className = 'tooltip-enhanced';
                textNode.parentNode.replaceChild(wrapper, textNode);
            }
        });
    }

    enhanceButtonLabels() {
        const buttonEnhancements = {
            'Details': 'View Full Details',
            'Delegate': 'Stake Your Tokens',
            'Withdraw': 'Withdraw Rewards',
            'Vote': 'Cast Your Vote',
            'Claim': 'Claim Rewards',
            'Connect': 'Connect Wallet',
            'Buy': 'Buy ODIS Tokens'
        };

        document.querySelectorAll('button, .btn, a[role="button"]').forEach(button => {
            const text = button.textContent.trim();
            if (buttonEnhancements[text]) {
                button.innerHTML = `
                    ${button.innerHTML.includes('<i') ? button.querySelector('i').outerHTML : ''}
                    <span>${buttonEnhancements[text]}</span>
                `;
                button.setAttribute('aria-label', `${buttonEnhancements[text]} - ${this.getButtonContext(button)}`);
            }
        });
    }

    getButtonContext(button) {
        const contexts = {
            'delegate': 'Choose a validator to earn staking rewards',
            'withdraw': 'Transfer your earned rewards to your wallet',
            'vote': 'Participate in network governance decisions',
            'claim': 'Collect your accumulated staking rewards',
            'connect': 'Link your Keplr wallet to access features',
            'buy': 'Purchase ODIS tokens from the exchange'
        };

        const buttonText = button.textContent.toLowerCase();
        for (const [key, context] of Object.entries(contexts)) {
            if (buttonText.includes(key)) {
                return context;
            }
        }
        
        return 'Interact with this feature';
    }

    formatNumericData() {
        // Find and format large numbers
        document.querySelectorAll('.metric-value, .currency-value, .large-number').forEach(element => {
            const text = element.textContent.trim();
            const number = this.extractNumber(text);
            
            if (number !== null) {
                const formatted = this.formatNumber(number);
                const currency = text.includes('$') ? '$' : '';
                const percentage = text.includes('%') ? '%' : '';
                
                element.innerHTML = `
                    ${currency}${formatted}${percentage}
                    ${number >= 1000000 ? '<span class="metric-explanation">Million</span>' : ''}
                    ${number >= 1000000000 ? '<span class="metric-explanation">Billion</span>' : ''}
                `;
            }
        });
    }

    extractNumber(text) {
        const match = text.match(/[\d,]+\.?\d*/);
        if (match) {
            return parseFloat(match[0].replace(/,/g, ''));
        }
        return null;
    }

    formatNumber(number) {
        if (number >= 1000000000) {
            return (number / 1000000000).toFixed(2) + 'B';
        } else if (number >= 1000000) {
            return (number / 1000000).toFixed(2) + 'M';
        } else if (number >= 1000) {
            return (number / 1000).toFixed(1) + 'K';
        }
        return number.toLocaleString();
    }

    enhanceStatusIndicators() {
        const statusExplanations = {
            'VERIFIED': 'This validator has been verified by the network',
            'ACTIVE': 'Currently processing transactions and earning rewards',
            'PENDING': 'Waiting for network confirmation',
            'TOKENIZED': 'Successfully converted to blockchain tokens',
            'ONLINE': 'Validator is online and accepting delegations',
            'OFFLINE': 'Validator is temporarily unavailable'
        };

        document.querySelectorAll('.status-indicator, .badge, [class*="status"]').forEach(element => {
            const statusText = element.textContent.trim().toUpperCase();
            if (statusExplanations[statusText]) {
                element.setAttribute('title', statusExplanations[statusText]);
                element.classList.add('status-with-explanation');
            }
        });
    }

    addContextualHelp() {
        // Add help icons to complex sections
        const helpSections = [
            { selector: '.validators-section', text: 'Validators secure the network and process transactions. Delegate to them to earn rewards.' },
            { selector: '.staking-section', text: 'Staking locks your tokens to help secure the network in exchange for rewards.' },
            { selector: '.governance-section', text: 'Vote on proposals to shape the future of the Odiseo network.' },
            { selector: '.portfolio-section', text: 'Track your token holdings, staking rewards, and transaction history.' }
        ];

        helpSections.forEach(section => {
            const element = document.querySelector(section.selector);
            if (element) {
                this.addHelpIcon(element, section.text);
            }
        });
    }

    addHelpIcon(element, helpText) {
        const helpIcon = document.createElement('div');
        helpIcon.className = 'help-icon';
        helpIcon.innerHTML = `
            <i data-feather="help-circle"></i>
            <div class="help-tooltip">${helpText}</div>
        `;
        
        const header = element.querySelector('.card-header, .section-header, h1, h2, h3');
        if (header) {
            header.style.position = 'relative';
            header.appendChild(helpIcon);
        }
    }

    setupContentObserver() {
        const observer = new MutationObserver(mutations => {
            mutations.forEach(mutation => {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        this.enhanceNewContent(node);
                    }
                });
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    enhanceNewContent(element) {
        // Apply enhancements to dynamically added content
        if (element.textContent && element.textContent.includes('Loading...')) {
            this.replaceLoadingStates();
        }
        
        // Format any new numeric data
        element.querySelectorAll?.('.metric-value, .currency-value').forEach(el => {
            this.formatNumericData();
        });
        
        // Add tooltips to new terms
        Object.keys(this.contentMappings).forEach(term => {
            const regex = new RegExp(`\\b${term}\\b`, 'gi');
            this.addTooltipsToText(regex, term, this.contentMappings[term]);
        });
    }

    // Utility method to update content contextually
    updateLoadingContent(selector, context) {
        const elements = document.querySelectorAll(selector);
        elements.forEach(element => {
            const message = this.getContextualLoadingMessage(context);
            element.innerHTML = `
                <div class="loading-state">
                    <div class="loading-spinner"></div>
                    <span>${message}</span>
                </div>
            `;
        });
    }

    // Method to add explanations for specific financial metrics
    addFinancialExplanations() {
        const financialTerms = {
            'TVL': 'Total Value Locked - amount of assets staked in the protocol',
            'MCap': 'Market Capitalization - total value of all tokens',
            'FDV': 'Fully Diluted Valuation - market cap if all tokens were in circulation',
            'P/E Ratio': 'Price to Earnings ratio - valuation metric',
            'ROI': 'Return on Investment - percentage gain or loss',
            'Yield': 'Annual percentage return on your investment'
        };

        Object.entries(financialTerms).forEach(([term, explanation]) => {
            document.querySelectorAll(`[data-metric="${term}"], .metric-${term.toLowerCase()}`).forEach(element => {
                if (!element.querySelector('.metric-explanation')) {
                    const explanationEl = document.createElement('div');
                    explanationEl.className = 'metric-explanation';
                    explanationEl.textContent = explanation;
                    element.appendChild(explanationEl);
                }
            });
        });
    }
}

// Initialize content enhancer
window.contentEnhancer = new ContentEnhancer();

// Add CSS for enhanced tooltips and help
const enhancementCSS = `
.term-with-tooltip {
    position: relative;
    border-bottom: 1px dotted var(--dds-accent-cyan);
    cursor: help;
}

.term-with-tooltip::after {
    content: attr(data-tooltip);
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    background: var(--dds-primary-dark);
    color: var(--dds-white);
    padding: var(--dds-space-2) var(--dds-space-3);
    border-radius: var(--dds-radius-md);
    font-size: var(--dds-font-size-xs);
    white-space: nowrap;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s ease;
    z-index: var(--dds-z-tooltip);
    border: 1px solid var(--dds-accent-cyan);
    max-width: 250px;
    white-space: normal;
}

.term-with-tooltip:hover::after {
    opacity: 1;
}

.help-icon {
    position: absolute;
    top: 0;
    right: 0;
    cursor: pointer;
    color: rgba(255, 255, 255, 0.6);
    transition: color 0.3s ease;
}

.help-icon:hover {
    color: var(--dds-accent-cyan);
}

.help-icon i {
    width: 16px;
    height: 16px;
}

.help-tooltip {
    position: absolute;
    top: 100%;
    right: 0;
    background: var(--dds-primary-dark);
    color: var(--dds-white);
    padding: var(--dds-space-3);
    border-radius: var(--dds-radius-md);
    font-size: var(--dds-font-size-sm);
    max-width: 200px;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s ease;
    z-index: var(--dds-z-tooltip);
    border: 1px solid var(--dds-accent-cyan);
}

.help-icon:hover .help-tooltip {
    opacity: 1;
}

.status-with-explanation {
    cursor: help;
}
`;

const style = document.createElement('style');
style.textContent = enhancementCSS;
document.head.appendChild(style);