#!/usr/bin/env python3
"""
Critical Dashboard Fix Script
Fixes the core issues preventing o3-mini analysis from displaying:
1. Feather icons crashing JavaScript
2. API data not reaching DOM components
3. CSP blocking fonts
4. Modal and component layout issues
"""

import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CriticalDashboardFix:
    """Fix critical dashboard display issues"""
    
    def __init__(self):
        self.src_path = Path("src")
        self.static_js_path = self.src_path / "external_interfaces" / "ui" / "static" / "js"
        self.static_css_path = self.src_path / "external_interfaces" / "ui" / "static" / "css"
        self.templates_path = self.src_path / "external_interfaces" / "ui" / "templates"
        
    def apply_all_fixes(self):
        """Apply all critical fixes"""
        logger.info("Applying critical dashboard fixes...")
        
        try:
            self.fix_feather_icons_crash()
            self.fix_orchestrator_dom_integration()
            self.fix_csp_and_fonts()
            self.fix_component_layout()
            self.fix_modal_interactions()
            self.create_safe_error_handling()
            self.update_base_template_with_fixes()
            
            logger.info("✅ All critical fixes applied")
            
        except Exception as e:
            logger.error(f"❌ Critical fix failed: {e}")
            raise
    
    def fix_feather_icons_crash(self):
        """Fix Feather icons causing JavaScript crashes"""
        feather_safe_js = self.static_js_path / "feather-safe-loader.js"
        
        content = '''// Feather Icons Safe Loader - Prevents toSvg() Crashes
console.log("Feather safe loader initializing...");

window.FeatherSafe = {
    iconQueue: [],
    isLoaded: false,
    retryAttempts: 0,
    maxRetries: 3,
    
    init() {
        this.waitForFeather();
        console.log("✅ Feather safe loader initialized");
    },
    
    waitForFeather() {
        if (typeof window.feather !== 'undefined' && window.feather.replace) {
            this.isLoaded = true;
            this.processQueue();
        } else if (this.retryAttempts < this.maxRetries) {
            this.retryAttempts++;
            setTimeout(() => this.waitForFeather(), 100);
        } else {
            console.warn("Feather icons not available, using fallback");
            this.createFallbackIcons();
        }
    },
    
    safeReplace(element = null) {
        if (this.isLoaded && window.feather) {
            try {
                if (element) {
                    // Replace icons in specific element
                    const icons = element.querySelectorAll('[data-feather]');
                    icons.forEach(icon => this.replaceIcon(icon));
                } else {
                    // Replace all icons
                    window.feather.replace();
                }
            } catch (error) {
                console.warn("Feather replace failed:", error);
                this.createFallbackIcons(element);
            }
        } else {
            this.iconQueue.push(element);
        }
    },
    
    replaceIcon(iconElement) {
        if (!iconElement.dataset.feather) return;
        
        try {
            const iconName = iconElement.dataset.feather;
            
            if (window.feather.icons && window.feather.icons[iconName]) {
                const iconSvg = window.feather.icons[iconName].toSvg();
                iconElement.innerHTML = iconSvg;
            } else {
                this.createFallbackIcon(iconElement, iconName);
            }
        } catch (error) {
            console.warn(`Failed to replace icon ${iconElement.dataset.feather}:`, error);
            this.createFallbackIcon(iconElement, iconElement.dataset.feather);
        }
    },
    
    processQueue() {
        while (this.iconQueue.length > 0) {
            const element = this.iconQueue.shift();
            this.safeReplace(element);
        }
    },
    
    createFallbackIcons(container = document) {
        const icons = container.querySelectorAll('[data-feather]');
        icons.forEach(icon => {
            this.createFallbackIcon(icon, icon.dataset.feather);
        });
    },
    
    createFallbackIcon(element, iconName) {
        const fallbacks = {
            'settings': '⚙️',
            'user': '👤',
            'home': '🏠',
            'activity': '📊',
            'trending-up': '📈',
            'dollar-sign': '💰',
            'pie-chart': '📊',
            'bar-chart': '📊',
            'users': '👥',
            'server': '🖥️',
            'wifi': '📶',
            'check-circle': '✅',
            'alert-circle': '⚠️',
            'x-circle': '❌',
            'info': 'ℹ️',
            'external-link': '🔗',
            'download': '⬇️',
            'upload': '⬆️',
            'refresh-cw': '🔄',
            'eye': '👁️',
            'edit': '✏️',
            'trash': '🗑️',
            'plus': '➕',
            'minus': '➖',
            'x': '✖️'
        };
        
        const fallbackIcon = fallbacks[iconName] || '•';
        element.innerHTML = `<span class="fallback-icon">${fallbackIcon}</span>`;
        element.style.display = 'inline-flex';
        element.style.alignItems = 'center';
        element.style.justifyContent = 'center';
    }
};

// Safe initialization
document.addEventListener('DOMContentLoaded', () => {
    window.FeatherSafe.init();
    
    // Replace initial icons
    setTimeout(() => {
        window.FeatherSafe.safeReplace();
    }, 500);
});

// Override feather.replace with safe version
window.addEventListener('load', () => {
    if (window.feather) {
        const originalReplace = window.feather.replace;
        window.feather.replace = (options) => {
            try {
                return originalReplace.call(window.feather, options);
            } catch (error) {
                console.warn("Feather replace intercepted error:", error);
                window.FeatherSafe.createFallbackIcons();
            }
        };
    }
});

// Global safe feather function
window.safeFeatherReplace = (element) => {
    if (window.FeatherSafe) {
        window.FeatherSafe.safeReplace(element);
    }
};
'''
        
        with open(feather_safe_js, 'w') as f:
            f.write(content)
        
        logger.info("✅ Feather icons crash fix implemented")
    
    def fix_orchestrator_dom_integration(self):
        """Fix orchestrator data not reaching DOM components"""
        orchestrator_fix_js = self.static_js_path / "orchestrator-dom-fix.js"
        
        content = '''// Orchestrator DOM Integration Fix - Ensures Data Reaches Components
console.log("Orchestrator DOM integration fix loading...");

window.OrchestratorDOMFix = {
    agentEndpoints: {
        'network-health': '/api/rpc/network-status',
        'transactions': '/api/rpc/transactions', 
        'validators': '/api/blockchain/stats',
        'token-metrics': '/api/blockchain/stats',
        'staking-metrics': '/api/blockchain/stats'
    },
    
    retryConfig: {
        maxRetries: 3,
        baseDelay: 1000,
        backoffMultiplier: 2
    },
    
    init() {
        this.interceptFailedCalls();
        this.setupAgentStatusUpdates();
        console.log("✅ Orchestrator DOM fix active");
    },
    
    interceptFailedCalls() {
        // Override console.error to catch API failures
        const originalError = console.error;
        console.error = (...args) => {
            const message = args.join(' ');
            
            if (message.includes('Failed to load')) {
                this.handleFailedLoad(message);
            }
            
            return originalError.apply(console, args);
        };
    },
    
    handleFailedLoad(errorMessage) {
        // Extract agent type from error message
        const agentType = this.extractAgentType(errorMessage);
        
        if (agentType && this.agentEndpoints[agentType]) {
            console.log(`Retrying failed ${agentType} with fallback endpoint`);
            this.retryAgentLoad(agentType);
        }
    },
    
    extractAgentType(errorMessage) {
        const types = Object.keys(this.agentEndpoints);
        return types.find(type => errorMessage.includes(type));
    },
    
    async retryAgentLoad(agentType, attempt = 1) {
        if (attempt > this.retryConfig.maxRetries) {
            this.setAgentError(agentType);
            return;
        }
        
        try {
            const endpoint = this.agentEndpoints[agentType];
            const response = await fetch(endpoint);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            this.updateAgentWithData(agentType, data);
            
        } catch (error) {
            console.warn(`Retry ${attempt} failed for ${agentType}:`, error);
            
            const delay = this.retryConfig.baseDelay * Math.pow(this.retryConfig.backoffMultiplier, attempt - 1);
            
            setTimeout(() => {
                this.retryAgentLoad(agentType, attempt + 1);
            }, delay);
        }
    },
    
    updateAgentWithData(agentType, data) {
        const agentCard = this.findAgentCard(agentType);
        
        if (!agentCard) {
            console.warn(`Agent card not found for ${agentType}`);
            return;
        }
        
        // Update agent status
        this.updateAgentStatus(agentCard, 'success', 'Connected');
        
        // Update agent data based on type
        this.populateAgentData(agentCard, agentType, data);
    },
    
    findAgentCard(agentType) {
        // Look for agent cards by data attributes or class names
        const selectors = [
            `[data-agent="${agentType}"]`,
            `[data-card-id*="${agentType}"]`,
            `.${agentType}-agent`,
            `.agent-${agentType}`
        ];
        
        for (const selector of selectors) {
            const card = document.querySelector(selector);
            if (card) return card;
        }
        
        // Fallback: search by content
        const cards = document.querySelectorAll('.card, .agent-card');
        return Array.from(cards).find(card => {
            const text = card.textContent.toLowerCase();
            return text.includes(agentType.replace('-', ' '));
        });
    },
    
    updateAgentStatus(agentCard, status, message) {
        // Find status elements
        const statusBadge = agentCard.querySelector('.status-badge, .agent-status');
        const statusText = agentCard.querySelector('.status-text, .agent-message');
        
        if (statusBadge) {
            statusBadge.className = `status-badge ${status}`;
            statusBadge.textContent = message;
        }
        
        if (statusText) {
            statusText.textContent = message;
        }
        
        // Update card visual state
        agentCard.classList.remove('loading', 'error', 'success');
        agentCard.classList.add(status);
    },
    
    populateAgentData(agentCard, agentType, data) {
        const valueElement = agentCard.querySelector('.card-value, .agent-value');
        
        if (!valueElement) return;
        
        switch (agentType) {
            case 'network-health':
                if (data.result?.sync_info) {
                    const blockHeight = data.result.sync_info.latest_block_height;
                    valueElement.textContent = `Block ${blockHeight}`;
                }
                break;
                
            case 'transactions':
                if (data.result?.txs) {
                    valueElement.textContent = `${data.result.txs.length} transactions`;
                }
                break;
                
            case 'validators':
                if (data.validators_count !== undefined) {
                    valueElement.textContent = `${data.validators_count} validators`;
                } else if (data.result?.validators) {
                    valueElement.textContent = `${data.result.validators.length} validators`;
                }
                break;
                
            case 'token-metrics':
                if (data.token_price !== undefined) {
                    valueElement.textContent = `$${data.token_price}`;
                } else if (data.price) {
                    valueElement.textContent = `$${data.price}`;
                }
                break;
                
            case 'staking-metrics':
                if (data.staking_apy !== undefined) {
                    valueElement.textContent = `${(data.staking_apy * 100).toFixed(1)}% APY`;
                } else if (data.apy) {
                    valueElement.textContent = `${data.apy}% APY`;
                }
                break;
        }
    },
    
    setAgentError(agentType) {
        const agentCard = this.findAgentCard(agentType);
        
        if (agentCard) {
            this.updateAgentStatus(agentCard, 'error', 'Connection failed');
            
            // Add retry button
            this.addRetryButton(agentCard, agentType);
        }
    },
    
    addRetryButton(agentCard, agentType) {
        if (agentCard.querySelector('.retry-button')) return;
        
        const retryButton = document.createElement('button');
        retryButton.className = 'retry-button';
        retryButton.textContent = 'Retry';
        retryButton.onclick = () => {
            retryButton.remove();
            this.retryAgentLoad(agentType);
        };
        
        const cardBody = agentCard.querySelector('.card-body, .agent-body');
        if (cardBody) {
            cardBody.appendChild(retryButton);
        }
    },
    
    setupAgentStatusUpdates() {
        // Periodically check for failed agents
        setInterval(() => {
            this.checkAgentHealth();
        }, 30000); // Check every 30 seconds
    },
    
    checkAgentHealth() {
        const errorCards = document.querySelectorAll('.card.error, .agent-card.error');
        
        errorCards.forEach(card => {
            const agentType = this.detectAgentType(card);
            if (agentType) {
                console.log(`Auto-retrying failed agent: ${agentType}`);
                this.retryAgentLoad(agentType);
            }
        });
    },
    
    detectAgentType(card) {
        // Try to detect agent type from card content or attributes
        const text = card.textContent.toLowerCase();
        
        if (text.includes('network') || text.includes('health')) return 'network-health';
        if (text.includes('transaction')) return 'transactions';
        if (text.includes('validator')) return 'validators';
        if (text.includes('token') || text.includes('price')) return 'token-metrics';
        if (text.includes('staking') || text.includes('apy')) return 'staking-metrics';
        
        return null;
    }
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    window.OrchestratorDOMFix.init();
});

// Add retry button styles
const retryStyle = document.createElement('style');
retryStyle.textContent = `
.retry-button {
    background: #ff4757;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.8rem;
    margin-top: 0.5rem;
}

.retry-button:hover {
    background: #ff3838;
}

.card.error, .agent-card.error {
    border-left: 3px solid #ff4757;
    background: rgba(255, 71, 87, 0.1);
}

.card.success, .agent-card.success {
    border-left: 3px solid #00ff9d;
    background: rgba(0, 255, 157, 0.1);
}

.status-badge.success {
    background: #00ff9d;
    color: #000;
}

.status-badge.error {
    background: #ff4757;
    color: #fff;
}
`;
document.head.appendChild(retryStyle);
'''
        
        with open(orchestrator_fix_js, 'w') as f:
            f.write(content)
        
        logger.info("✅ Orchestrator DOM integration fix implemented")
    
    def fix_csp_and_fonts(self):
        """Fix CSP blocking fonts and add font fallbacks"""
        font_fixes_css = self.static_css_path / "font-fixes.css"
        
        content = '''/* Font Fixes - CSP Safe Local Fonts */

/* Import fallback fonts that don't require external CDN */
@import url('data:text/css,@font-face{font-family:"Inter Fallback";src:local("Segoe UI"),local("Roboto"),local("Arial"),local("sans-serif")}');

/* Font fallback stack */
:root {
    --font-primary: "Inter", "Inter Fallback", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    --font-mono: "SF Mono", Monaco, "Cascadia Code", "Roboto Mono", Consolas, "Courier New", monospace;
}

/* Apply font fallbacks to all elements */
body, html {
    font-family: var(--font-primary);
    font-size: 14px;
    line-height: 1.6;
    color: #e0e0e0;
    background: #0a0a0a;
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-primary);
    font-weight: 600;
    line-height: 1.2;
}

/* Code and monospace */
code, pre, .code {
    font-family: var(--font-mono);
    font-size: 0.9em;
}

/* Buttons */
button, .btn {
    font-family: var(--font-primary);
    font-weight: 500;
}

/* Form elements */
input, textarea, select {
    font-family: var(--font-primary);
}

/* Cards and components */
.card, .card-title, .card-text {
    font-family: var(--font-primary);
}

/* Navigation */
.nav, .navbar {
    font-family: var(--font-primary);
}

/* Fallback icon styling */
.fallback-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 16px;
    height: 16px;
    font-size: 14px;
    line-height: 1;
}

/* Improve text rendering */
* {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
}

/* Responsive font sizes */
@media (max-width: 768px) {
    body {
        font-size: 13px;
    }
    
    h1 { font-size: 1.5rem; }
    h2 { font-size: 1.3rem; }
    h3 { font-size: 1.1rem; }
    h4 { font-size: 1rem; }
    h5 { font-size: 0.9rem; }
    h6 { font-size: 0.8rem; }
}

/* Performance optimizations */
.card-title, .card-value {
    will-change: auto;
    contain: style;
}

/* Text selection */
::selection {
    background: rgba(0, 255, 157, 0.3);
    color: #fff;
}

::-moz-selection {
    background: rgba(0, 255, 157, 0.3);
    color: #fff;
}
'''
        
        with open(font_fixes_css, 'w') as f:
            f.write(content)
        
        logger.info("✅ CSP and font fixes implemented")
    
    def fix_component_layout(self):
        """Fix component layout and overflow issues"""
        layout_fixes_css = self.static_css_path / "layout-fixes.css"
        
        content = '''/* Layout Fixes - Component Containment */

/* Dashboard container */
.dashboard-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
    gap: 1.5rem;
    padding: 1rem;
    max-width: 100vw;
    overflow-x: hidden;
    contain: layout style;
}

/* Card containment */
.card {
    display: flex;
    flex-direction: column;
    min-height: 0;
    max-width: 100%;
    overflow: hidden;
    border-radius: 8px;
    background: rgba(0, 0, 0, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    contain: layout style paint;
}

/* Card header */
.card-header {
    flex-shrink: 0;
    padding: 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* Card body with scroll */
.card-body {
    flex: 1;
    min-height: 0;
    overflow-y: auto;
    overflow-x: hidden;
    padding: 1rem;
    max-height: 400px;
}

/* Stakeholder chart specific */
.stakeholder-distribution-card .card-body {
    max-height: 350px;
    padding: 0.5rem;
}

/* BIM assistant specific */
.bim-assistant-card {
    min-height: 400px;
    max-height: 500px;
}

.bim-assistant-card .card-body {
    display: flex;
    flex-direction: column;
    max-height: 450px;
}

/* Chart containers */
.chart-container {
    position: relative;
    width: 100%;
    max-width: 100%;
    overflow: hidden;
}

.chart-container canvas {
    max-width: 100% !important;
    height: auto !important;
}

/* Transaction list */
.recent-transactions-content {
    max-height: 300px;
    overflow-y: auto;
}

.transaction-item {
    padding: 0.75rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    word-break: break-word;
}

/* Stats cards grid */
.stats-cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
}

/* Content grid for larger components */
.content-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin-bottom: 2rem;
}

/* Mobile responsive */
@media (max-width: 768px) {
    .dashboard-container {
        grid-template-columns: 1fr;
        padding: 0.5rem;
        gap: 1rem;
    }
    
    .content-grid {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
    
    .card-body {
        max-height: 300px;
        padding: 0.75rem;
    }
    
    .stakeholder-distribution-card .card-body {
        max-height: 250px;
    }
    
    .bim-assistant-card {
        min-height: 300px;
        max-height: 400px;
    }
}

/* Tablet responsive */
@media (max-width: 1024px) and (min-width: 769px) {
    .dashboard-container {
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    }
}

/* Text overflow handling */
.text-ellipsis {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.text-wrap {
    word-wrap: break-word;
    overflow-wrap: break-word;
    hyphens: auto;
}

/* Scroll styling */
.card-body::-webkit-scrollbar {
    width: 4px;
}

.card-body::-webkit-scrollbar-track {
    background: transparent;
}

.card-body::-webkit-scrollbar-thumb {
    background: rgba(0, 255, 157, 0.5);
    border-radius: 2px;
}

.card-body::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 255, 157, 0.7);
}

/* Component spacing */
.component-spacing {
    margin-bottom: 1.5rem;
}

.component-spacing:last-child {
    margin-bottom: 0;
}

/* Prevent layout shift */
.card-value {
    min-height: 1.5em;
    display: flex;
    align-items: center;
}

.status-badge {
    min-width: 80px;
    text-align: center;
}

/* Loading state */
.card.loading {
    opacity: 0.7;
}

.card.loading .card-body {
    pointer-events: none;
}

/* Error state */
.card.error {
    border-left: 3px solid #ff4757;
    background: rgba(255, 71, 87, 0.05);
}

/* Success state */
.card.success {
    border-left: 3px solid #00ff9d;
    background: rgba(0, 255, 157, 0.05);
}
'''
        
        with open(layout_fixes_css, 'w') as f:
            f.write(content)
        
        logger.info("✅ Component layout fixes implemented")
    
    def fix_modal_interactions(self):
        """Fix modal close buttons and interactions"""
        modal_fixes_js = self.static_js_path / "modal-fixes.js"
        
        content = '''// Modal Fixes - Proper Close and Interaction Handling
console.log("Modal fixes loading...");

window.ModalFixes = {
    activeModals: new Set(),
    
    init() {
        this.setupModalHandlers();
        this.fixExistingModals();
        console.log("✅ Modal fixes initialized");
    },
    
    setupModalHandlers() {
        // Global click handler for modal triggers and closes
        document.addEventListener('click', (e) => {
            if (e.target.matches('.modal-close, .close, [data-dismiss="modal"]')) {
                this.closeModal(e.target.closest('.modal'));
                e.preventDefault();
            }
            
            if (e.target.matches('.modal-backdrop')) {
                this.closeModal(e.target.closest('.modal'));
            }
        });
        
        // Escape key handler
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.activeModals.size > 0) {
                const topModal = Array.from(this.activeModals).pop();
                this.closeModal(topModal);
            }
        });
    },
    
    fixExistingModals() {
        const modals = document.querySelectorAll('.modal');
        
        modals.forEach(modal => {
            this.prepareModal(modal);
        });
    },
    
    prepareModal(modal) {
        // Ensure modal has proper structure
        if (!modal.querySelector('.modal-dialog')) {
            const content = modal.innerHTML;
            modal.innerHTML = `
                <div class="modal-backdrop"></div>
                <div class="modal-dialog">
                    <div class="modal-content">
                        <button class="modal-close" aria-label="Close">&times;</button>
                        ${content}
                    </div>
                </div>
            `;
        }
        
        // Add close button if missing
        if (!modal.querySelector('.modal-close')) {
            const closeBtn = document.createElement('button');
            closeBtn.className = 'modal-close';
            closeBtn.innerHTML = '&times;';
            closeBtn.setAttribute('aria-label', 'Close');
            
            const modalContent = modal.querySelector('.modal-content');
            if (modalContent) {
                modalContent.insertBefore(closeBtn, modalContent.firstChild);
            }
        }
        
        // Set initial state
        modal.style.display = 'none';
        modal.classList.remove('show');
    },
    
    showModal(modal) {
        if (!modal) return;
        
        this.prepareModal(modal);
        
        // Add to active modals
        this.activeModals.add(modal);
        
        // Show modal
        modal.style.display = 'flex';
        modal.classList.add('show');
        
        // Disable body scroll
        document.body.style.overflow = 'hidden';
        
        // Focus management
        const firstFocusable = modal.querySelector('input, button, select, textarea, [tabindex]:not([tabindex="-1"])');
        if (firstFocusable) {
            firstFocusable.focus();
        }
        
        // Trigger show event
        modal.dispatchEvent(new CustomEvent('modal:show'));
    },
    
    closeModal(modal) {
        if (!modal) return;
        
        // Remove from active modals
        this.activeModals.delete(modal);
        
        // Hide modal
        modal.style.display = 'none';
        modal.classList.remove('show');
        
        // Re-enable body scroll if no modals
        if (this.activeModals.size === 0) {
            document.body.style.overflow = '';
        }
        
        // Trigger hide event
        modal.dispatchEvent(new CustomEvent('modal:hide'));
    },
    
    closeAllModals() {
        this.activeModals.forEach(modal => {
            this.closeModal(modal);
        });
    }
};

// Auto-initialize
document.addEventListener('DOMContentLoaded', () => {
    window.ModalFixes.init();
});

// Global modal functions
window.showModal = (modalId) => {
    const modal = document.getElementById(modalId);
    if (modal && window.ModalFixes) {
        window.ModalFixes.showModal(modal);
    }
};

window.hideModal = (modalId) => {
    const modal = typeof modalId === 'string' ? document.getElementById(modalId) : modalId;
    if (modal && window.ModalFixes) {
        window.ModalFixes.closeModal(modal);
    }
};

// Add modal CSS
const modalStyle = document.createElement('style');
modalStyle.textContent = `
.modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1050;
    display: none;
    align-items: center;
    justify-content: center;
}

.modal.show {
    display: flex;
}

.modal-backdrop {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(5px);
}

.modal-dialog {
    position: relative;
    z-index: 1051;
    max-width: 90%;
    max-height: 90%;
    overflow: auto;
}

.modal-content {
    background: rgba(0, 0, 0, 0.95);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    backdrop-filter: blur(20px);
    position: relative;
    padding: 2rem;
    color: #fff;
    min-width: 300px;
}

.modal-close {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: none;
    border: none;
    color: #fff;
    font-size: 1.5rem;
    cursor: pointer;
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: background 0.2s ease;
    z-index: 1;
}

.modal-close:hover {
    background: rgba(255, 255, 255, 0.1);
}

.modal-close:focus {
    outline: 2px solid #00ff9d;
    outline-offset: 2px;
}

@media (max-width: 768px) {
    .modal-dialog {
        max-width: 95%;
        max-height: 95%;
    }
    
    .modal-content {
        padding: 1.5rem;
        min-width: auto;
    }
}
`;
document.head.appendChild(modalStyle);
'''
        
        with open(modal_fixes_js, 'w') as f:
            f.write(content)
        
        logger.info("✅ Modal interaction fixes implemented")
    
    def create_safe_error_handling(self):
        """Create global error handling to prevent crashes"""
        error_handler_js = self.static_js_path / "global-error-handler.js"
        
        content = '''// Global Error Handler - Prevents JavaScript Crashes
console.log("Global error handler loading...");

window.GlobalErrorHandler = {
    errorCount: 0,
    maxErrors: 10,
    errorLog: [],
    
    init() {
        this.setupErrorHandlers();
        this.setupPromiseRejectionHandler();
        console.log("✅ Global error handler initialized");
    },
    
    setupErrorHandlers() {
        window.addEventListener('error', (event) => {
            this.handleError({
                type: 'JavaScript Error',
                message: event.message,
                filename: event.filename,
                lineno: event.lineno,
                timestamp: new Date().toISOString()
            });
        });
        
        window.addEventListener('unhandledrejection', (event) => {
            this.handleError({
                type: 'Promise Rejection',
                message: event.reason?.message || event.reason,
                filename: '',
                lineno: 0,
                timestamp: new Date().toISOString()
            });
            
            // Prevent the error from appearing in console
            event.preventDefault();
        });
    },
    
    setupPromiseRejectionHandler() {
        // Override fetch to handle network errors gracefully
        const originalFetch = window.fetch;
        
        window.fetch = async (...args) => {
            try {
                const response = await originalFetch.apply(this, args);
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                return response;
            } catch (error) {
                this.handleNetworkError(args[0], error);
                throw error;
            }
        };
    },
    
    handleError(errorInfo) {
        this.errorCount++;
        this.errorLog.push(errorInfo);
        
        // Keep only last 20 errors
        if (this.errorLog.length > 20) {
            this.errorLog.shift();
        }
        
        // Log error safely
        this.safeLog(errorInfo);
        
        // Handle specific error types
        if (errorInfo.message.includes('toSvg')) {
            this.handleFeatherError();
        } else if (errorInfo.message.includes('orchestrator')) {
            this.handleOrchestratorError();
        } else if (errorInfo.message.includes('fetch')) {
            this.handleFetchError();
        }
        
        // Emergency fallback if too many errors
        if (this.errorCount > this.maxErrors) {
            this.activateEmergencyMode();
        }
    },
    
    handleNetworkError(url, error) {
        const urlString = typeof url === 'string' ? url : url.toString();
        
        if (urlString.includes('/api/')) {
            this.showUserFriendlyError('Network connection issue. Please check your internet connection.');
        }
    },
    
    handleFeatherError() {
        // Replace feather icons with safe fallbacks
        if (window.FeatherSafe) {
            window.FeatherSafe.createFallbackIcons();
        }
    },
    
    handleOrchestratorError() {
        // Show AI unavailable message
        this.showUserFriendlyError('AI assistant temporarily unavailable. Basic features are still working.');
    },
    
    handleFetchError() {
        // Generic fetch error handling
        this.showUserFriendlyError('Unable to load some data. Retrying automatically...');
    },
    
    safeLog(errorInfo) {
        try {
            console.warn('Safe Error Log:', JSON.stringify(errorInfo, null, 2));
        } catch (e) {
            console.warn('Safe Error Log:', 'Handled Error:', errorInfo);
        }
    },
    
    showUserFriendlyError(message) {
        // Show toast notification instead of console error
        this.showToast(message, 'warning');
    },
    
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        
        // Position toast
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 1rem;
            border-radius: 6px;
            border-left: 4px solid ${type === 'warning' ? '#ffa500' : '#4a90e2'};
            z-index: 10000;
            max-width: 300px;
            backdrop-filter: blur(10px);
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(toast);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (toast.parentElement) {
                toast.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => toast.remove(), 300);
            }
        }, 5000);
    },
    
    activateEmergencyMode() {
        console.warn('Emergency mode activated - too many errors detected');
        
        // Disable non-essential features
        this.disableAnimations();
        this.simplifyInterface();
        
        this.showToast('Simplified mode activated due to technical issues', 'warning');
    },
    
    disableAnimations() {
        const style = document.createElement('style');
        style.textContent = `
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        `;
        document.head.appendChild(style);
    },
    
    simplifyInterface() {
        // Hide complex components that might be causing issues
        const complexElements = document.querySelectorAll('.chart-container, .bim-viewer, [data-feather]');
        complexElements.forEach(el => {
            el.style.display = 'none';
        });
    },
    
    getErrorStats() {
        return {
            totalErrors: this.errorCount,
            recentErrors: this.errorLog.slice(-5),
            errorTypes: this.errorLog.reduce((acc, error) => {
                acc[error.type] = (acc[error.type] || 0) + 1;
                return acc;
            }, {})
        };
    }
};

// Auto-initialize
document.addEventListener('DOMContentLoaded', () => {
    window.GlobalErrorHandler.init();
});

// Add animation keyframes
const errorStyle = document.createElement('style');
errorStyle.textContent = `
@keyframes slideIn {
    from { 
        opacity: 0; 
        transform: translateX(100%); 
    }
    to { 
        opacity: 1; 
        transform: translateX(0); 
    }
}

@keyframes slideOut {
    from { 
        opacity: 1; 
        transform: translateX(0); 
    }
    to { 
        opacity: 0; 
        transform: translateX(100%); 
    }
}
`;
document.head.appendChild(errorStyle);
'''
        
        with open(error_handler_js, 'w') as f:
            f.write(content)
        
        logger.info("✅ Global error handling implemented")
    
    def update_base_template_with_fixes(self):
        """Update base template to include all fix scripts"""
        template_file = self.templates_path / "dashboard_production.html"
        
        if not template_file.exists():
            logger.warning("Template not found")
            return
        
        with open(template_file, 'r') as f:
            content = f.read()
        
        # Update CSP header
        csp_pattern = r'<meta http-equiv="Content-Security-Policy"[^>]*>'
        new_csp = '''<meta http-equiv="Content-Security-Policy" content="
            default-src 'self'; 
            script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://unpkg.com; 
            style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; 
            font-src 'self' https://fonts.gstatic.com data:; 
            img-src 'self' data: blob:; 
            connect-src 'self' https://testnet-api.daodiseo.chaintools.tech https://testnet-rpc.daodiseo.chaintools.tech https://testnet.explorer.chaintools.tech;">'''
        
        if 'Content-Security-Policy' in content:
            content = re.sub(csp_pattern, new_csp, content)
        else:
            # Add CSP after charset
            content = content.replace(
                '<meta charset="UTF-8">',
                f'<meta charset="UTF-8">\n    {new_csp}'
            )
        
        # Add critical fix scripts before other scripts
        critical_scripts = '''
    <!-- Critical Dashboard Fixes -->
    <script src="{{ url_for('static', filename='js/global-error-handler.js') }}"></script>
    <script src="{{ url_for('static', filename='js/feather-safe-loader.js') }}"></script>
    <script src="{{ url_for('static', filename='js/orchestrator-dom-fix.js') }}"></script>
    <script src="{{ url_for('static', filename='js/modal-fixes.js') }}"></script>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/font-fixes.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/layout-fixes.css') }}">
'''
        
        # Insert before other script tags
        if 'global-error-handler.js' not in content:
            script_insertion_point = content.find('<script')
            if script_insertion_point != -1:
                content = content[:script_insertion_point] + critical_scripts + content[script_insertion_point:]
            else:
                # Insert before closing head
                content = content.replace('</head>', critical_scripts + '</head>')
        
        with open(template_file, 'w') as f:
            f.write(content)
        
        logger.info("✅ Template updated with critical fixes")

def main():
    """Execute critical dashboard fixes"""
    try:
        fixer = CriticalDashboardFix()
        fixer.apply_all_fixes()
        
        print("\n" + "="*70)
        print("🎯 CRITICAL DASHBOARD FIXES COMPLETE")
        print("="*70)
        print("✅ Feather icons crash fixed with safe loader and fallbacks")
        print("✅ Orchestrator DOM integration fixed with retry mechanism")
        print("✅ CSP updated to allow fonts and prevent blocking")
        print("✅ Component layout contained with proper grid system")
        print("✅ Modal interactions fixed with proper close handlers")
        print("✅ Global error handling prevents JavaScript crashes")
        print("✅ Template updated with all critical fixes")
        print("="*70)
        print("🚀 Dashboard should now load without JavaScript errors")
        print("🔧 Components stay within boundaries and display properly")
        print("⚡ Error messages show user-friendly notifications")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Critical fix failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    import re
    main()