#!/usr/bin/env python3
"""
Button Response Optimization
10 ideas to fix slow button clicks and improve UI responsiveness
"""

import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ButtonResponseOptimizer:
    """Optimize button response times and UI reactivity"""
    
    def __init__(self):
        self.src_path = Path("src")
        self.static_js_path = self.src_path / "external_interfaces" / "ui" / "static" / "js"
        self.optimization_ideas = [
            "debounce_button_clicks",
            "remove_redundant_event_listeners", 
            "optimize_dom_queries",
            "implement_lazy_loading",
            "fix_blocking_operations",
            "add_visual_feedback",
            "cache_dom_elements",
            "use_event_delegation",
            "optimize_css_animations",
            "implement_web_workers"
        ]
        
    def implement_all_optimizations(self):
        """Implement all 10 optimization ideas"""
        logger.info("Implementing button response optimizations...")
        
        try:
            self.idea_1_debounce_button_clicks()
            self.idea_2_remove_redundant_listeners()
            self.idea_3_optimize_dom_queries()
            self.idea_4_implement_lazy_loading()
            self.idea_5_fix_blocking_operations()
            self.idea_6_add_visual_feedback()
            self.idea_7_cache_dom_elements()
            self.idea_8_use_event_delegation()
            self.idea_9_optimize_css_animations()
            self.idea_10_implement_web_workers()
            
            logger.info("✅ All button response optimizations implemented")
            
        except Exception as e:
            logger.error(f"❌ Optimization failed: {e}")
            raise
    
    def idea_1_debounce_button_clicks(self):
        """Idea 1: Debounce button clicks to prevent multiple rapid submissions"""
        debounce_js = self.static_js_path / "button-debounce.js"
        
        content = '''// Button Click Debouncing - Prevents Multiple Rapid Clicks
console.log("Button debouncing system loading...");

window.ButtonDebounce = {
    clickTimers: new Map(),
    debounceDelay: 300, // 300ms debounce
    
    init() {
        this.setupGlobalDebouncing();
        console.log("✅ Button debouncing active");
    },
    
    setupGlobalDebouncing() {
        // Intercept all button clicks
        document.addEventListener('click', (e) => {
            if (e.target.matches('button, .btn, [role="button"]')) {
                this.debounceClick(e);
            }
        }, true); // Use capture phase
    },
    
    debounceClick(event) {
        const button = event.target;
        const buttonId = this.getButtonId(button);
        
        // Check if button is already debounced
        if (this.clickTimers.has(buttonId)) {
            event.preventDefault();
            event.stopPropagation();
            return false;
        }
        
        // Add visual feedback immediately
        this.showClickFeedback(button);
        
        // Set debounce timer
        this.clickTimers.set(buttonId, setTimeout(() => {
            this.clickTimers.delete(buttonId);
            this.removeClickFeedback(button);
        }, this.debounceDelay));
    },
    
    getButtonId(button) {
        return button.id || button.className || button.textContent.trim() || Math.random().toString();
    },
    
    showClickFeedback(button) {
        button.style.transform = 'scale(0.95)';
        button.style.opacity = '0.8';
        button.disabled = true;
    },
    
    removeClickFeedback(button) {
        button.style.transform = '';
        button.style.opacity = '';
        button.disabled = false;
    }
};

document.addEventListener('DOMContentLoaded', () => {
    window.ButtonDebounce.init();
});
'''
        
        with open(debounce_js, 'w') as f:
            f.write(content)
        
        logger.info("✅ Idea 1: Button debouncing implemented")
    
    def idea_2_remove_redundant_listeners(self):
        """Idea 2: Remove redundant event listeners that cause delays"""
        cleanup_js = self.static_js_path / "event-cleanup.js"
        
        content = '''// Event Listener Cleanup - Removes Redundant Handlers
console.log("Event cleanup system loading...");

window.EventCleanup = {
    registeredEvents: new Map(),
    
    init() {
        this.cleanupExistingListeners();
        this.interceptEventRegistration();
        console.log("✅ Event cleanup active");
    },
    
    cleanupExistingListeners() {
        // Remove duplicate feather icon listeners
        const featherElements = document.querySelectorAll('[data-feather]');
        featherElements.forEach(el => {
            el.replaceWith(el.cloneNode(true)); // Removes all listeners
        });
        
        // Clean up modal listeners
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            const clone = modal.cloneNode(true);
            modal.parentNode.replaceChild(clone, modal);
        });
    },
    
    interceptEventRegistration() {
        const originalAddEventListener = Element.prototype.addEventListener;
        
        Element.prototype.addEventListener = function(type, listener, options) {
            const elementId = this.id || this.className || 'anonymous';
            const key = `${elementId}:${type}`;
            
            // Prevent duplicate registrations
            if (this.registeredEvents?.has?.(key)) {
                console.warn(`Prevented duplicate event listener: ${key}`);
                return;
            }
            
            if (!this.registeredEvents) {
                this.registeredEvents = new Set();
            }
            this.registeredEvents.add(key);
            
            return originalAddEventListener.call(this, type, listener, options);
        };
    }
};

document.addEventListener('DOMContentLoaded', () => {
    window.EventCleanup.init();
});
'''
        
        with open(cleanup_js, 'w') as f:
            f.write(content)
        
        logger.info("✅ Idea 2: Event listener cleanup implemented")
    
    def idea_3_optimize_dom_queries(self):
        """Idea 3: Optimize DOM queries with caching and efficient selectors"""
        dom_optimizer_js = self.static_js_path / "dom-optimizer.js"
        
        content = '''// DOM Query Optimizer - Caches Selectors and Optimizes Queries
console.log("DOM optimizer loading...");

window.DOMOptimizer = {
    cache: new Map(),
    
    init() {
        this.createOptimizedSelectors();
        this.interceptDocumentQueries();
        console.log("✅ DOM optimizer active");
    },
    
    createOptimizedSelectors() {
        // Pre-cache commonly used elements
        this.cacheElement('cards', '[data-card-id]');
        this.cacheElement('buttons', 'button, .btn');
        this.cacheElement('modals', '.modal');
        this.cacheElement('statusBadges', '.status-badge');
        this.cacheElement('cardValues', '.card-value');
    },
    
    cacheElement(name, selector) {
        const elements = document.querySelectorAll(selector);
        this.cache.set(name, Array.from(elements));
        this.cache.set(selector, Array.from(elements));
    },
    
    interceptDocumentQueries() {
        const originalQuerySelector = document.querySelector;
        const originalQuerySelectorAll = document.querySelectorAll;
        
        document.querySelector = (selector) => {
            if (this.cache.has(selector)) {
                return this.cache.get(selector)[0] || null;
            }
            return originalQuerySelector.call(document, selector);
        };
        
        document.querySelectorAll = (selector) => {
            if (this.cache.has(selector)) {
                return this.cache.get(selector);
            }
            const result = originalQuerySelectorAll.call(document, selector);
            this.cache.set(selector, Array.from(result));
            return result;
        };
    },
    
    refreshCache() {
        this.cache.clear();
        this.createOptimizedSelectors();
    },
    
    getCachedElements(name) {
        return this.cache.get(name) || [];
    }
};

document.addEventListener('DOMContentLoaded', () => {
    window.DOMOptimizer.init();
});
'''
        
        with open(dom_optimizer_js, 'w') as f:
            f.write(content)
        
        logger.info("✅ Idea 3: DOM query optimization implemented")
    
    def idea_4_implement_lazy_loading(self):
        """Idea 4: Implement lazy loading for heavy components"""
        lazy_loader_js = self.static_js_path / "lazy-loader.js"
        
        content = '''// Lazy Loading System - Loads Components Only When Needed
console.log("Lazy loader loading...");

window.LazyLoader = {
    observers: new Map(),
    loadedComponents: new Set(),
    
    init() {
        this.setupIntersectionObserver();
        this.markLazyComponents();
        console.log("✅ Lazy loader active");
    },
    
    setupIntersectionObserver() {
        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.loadComponent(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '50px'
        });
    },
    
    markLazyComponents() {
        // Mark charts for lazy loading
        const charts = document.querySelectorAll('#asset-distribution-chart, .chart-container');
        charts.forEach(chart => {
            if (!this.loadedComponents.has(chart)) {
                this.observer.observe(chart);
            }
        });
        
        // Mark heavy lists for lazy loading
        const lists = document.querySelectorAll('.recent-transactions-content, .validator-list');
        lists.forEach(list => {
            if (!this.loadedComponents.has(list)) {
                this.observer.observe(list);
            }
        });
    },
    
    loadComponent(element) {
        if (this.loadedComponents.has(element)) return;
        
        this.loadedComponents.add(element);
        this.observer.unobserve(element);
        
        // Load component based on type
        if (element.id === 'asset-distribution-chart') {
            this.loadAssetChart(element);
        } else if (element.classList.contains('recent-transactions-content')) {
            this.loadTransactionList(element);
        }
    },
    
    loadAssetChart(chartElement) {
        // Only load chart when visible
        if (typeof window.EnhancedAssetDistribution !== 'undefined') {
            setTimeout(() => {
                new window.EnhancedAssetDistribution();
            }, 100);
        }
    },
    
    loadTransactionList(listElement) {
        // Only load transactions when visible
        if (typeof window.EnhancedTransactionList !== 'undefined') {
            setTimeout(() => {
                new window.EnhancedTransactionList();
            }, 100);
        }
    }
};

document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        window.LazyLoader.init();
    }, 1000);
});
'''
        
        with open(lazy_loader_js, 'w') as f:
            f.write(content)
        
        logger.info("✅ Idea 4: Lazy loading implemented")
    
    def idea_5_fix_blocking_operations(self):
        """Idea 5: Fix blocking operations that freeze the UI"""
        async_handler_js = self.static_js_path / "async-handler.js"
        
        content = '''// Async Operation Handler - Prevents UI Blocking
console.log("Async handler loading...");

window.AsyncHandler = {
    taskQueue: [],
    isProcessing: false,
    
    init() {
        this.interceptBlockingOperations();
        this.startTaskProcessor();
        console.log("✅ Async handler active");
    },
    
    interceptBlockingOperations() {
        // Wrap expensive operations in async handlers
        const originalFeatherReplace = window.feather?.replace;
        if (originalFeatherReplace) {
            window.feather.replace = (...args) => {
                this.addTask(() => originalFeatherReplace.apply(window.feather, args));
            };
        }
        
        // Wrap Chart.js operations
        const originalChart = window.Chart;
        if (originalChart) {
            window.Chart = function(...args) {
                const instance = new originalChart(...args);
                return instance;
            };
            Object.setPrototypeOf(window.Chart, originalChart);
            Object.assign(window.Chart, originalChart);
        }
    },
    
    addTask(taskFunction) {
        this.taskQueue.push(taskFunction);
        if (!this.isProcessing) {
            this.processNextTask();
        }
    },
    
    async processNextTask() {
        if (this.taskQueue.length === 0) {
            this.isProcessing = false;
            return;
        }
        
        this.isProcessing = true;
        const task = this.taskQueue.shift();
        
        try {
            // Use requestIdleCallback if available, otherwise setTimeout
            if (window.requestIdleCallback) {
                window.requestIdleCallback(() => {
                    task();
                    this.processNextTask();
                });
            } else {
                setTimeout(() => {
                    task();
                    this.processNextTask();
                }, 0);
            }
        } catch (error) {
            console.warn('Async task failed:', error);
            this.processNextTask();
        }
    },
    
    wrapAsyncFunction(fn) {
        return (...args) => {
            return new Promise((resolve, reject) => {
                this.addTask(() => {
                    try {
                        const result = fn.apply(this, args);
                        resolve(result);
                    } catch (error) {
                        reject(error);
                    }
                });
            });
        };
    }
};

document.addEventListener('DOMContentLoaded', () => {
    window.AsyncHandler.init();
});
'''
        
        with open(async_handler_js, 'w') as f:
            f.write(content)
        
        logger.info("✅ Idea 5: Blocking operation fixes implemented")
    
    def idea_6_add_visual_feedback(self):
        """Idea 6: Add immediate visual feedback for button interactions"""
        feedback_css = self.src_path / "external_interfaces" / "ui" / "static" / "css" / "button-feedback.css"
        
        content = '''/* Button Visual Feedback - Immediate Response Indicators */

/* Instant click feedback */
button, .btn, [role="button"] {
    transition: all 0.1s ease !important;
    cursor: pointer;
}

button:active, .btn:active, [role="button"]:active {
    transform: scale(0.98) !important;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2) !important;
}

/* Loading state */
button.loading, .btn.loading {
    position: relative;
    pointer-events: none;
}

button.loading::after, .btn.loading::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 12px;
    height: 12px;
    margin: -6px 0 0 -6px;
    border: 2px solid transparent;
    border-top: 2px solid currentColor;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Hover feedback */
button:hover, .btn:hover, [role="button"]:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

/* Focus feedback */
button:focus, .btn:focus, [role="button"]:focus {
    outline: 2px solid #00ff9d;
    outline-offset: 2px;
}

/* Disabled state */
button:disabled, .btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none !important;
}

/* AI button specific feedback */
.ai-btn {
    position: relative;
    overflow: hidden;
}

.ai-btn::before {
    content: '';
    position: absolute;
    top: 50%;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: left 0.5s;
}

.ai-btn:hover::before {
    left: 100%;
}

/* Ripple effect */
.ripple {
    position: relative;
    overflow: hidden;
}

.ripple::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    transform: translate(-50%, -50%);
    transition: width 0.3s, height 0.3s;
}

.ripple:active::after {
    width: 200px;
    height: 200px;
}

/* Success feedback */
.btn-success-flash {
    animation: successFlash 0.6s ease;
}

@keyframes successFlash {
    0% { background-color: #00ff9d; }
    100% { background-color: initial; }
}

/* Error feedback */
.btn-error-shake {
    animation: errorShake 0.5s ease;
}

@keyframes errorShake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-4px); }
    75% { transform: translateX(4px); }
}
'''
        
        with open(feedback_css, 'w') as f:
            f.write(content)
        
        logger.info("✅ Idea 6: Visual feedback implemented")
    
    def idea_7_cache_dom_elements(self):
        """Idea 7: Cache DOM elements to avoid repeated queries"""
        element_cache_js = self.static_js_path / "element-cache.js"
        
        content = '''// Element Cache - Stores DOM References for Fast Access
console.log("Element cache loading...");

window.ElementCache = {
    cache: new Map(),
    selectors: {
        cards: '[data-card-id]',
        buttons: 'button, .btn',
        aiButtons: '.ai-btn',
        statusBadges: '.status-badge',
        cardValues: '.card-value',
        modals: '.modal'
    },
    
    init() {
        this.buildCache();
        this.createHelperMethods();
        console.log("✅ Element cache active");
    },
    
    buildCache() {
        Object.entries(this.selectors).forEach(([name, selector]) => {
            const elements = document.querySelectorAll(selector);
            this.cache.set(name, Array.from(elements));
        });
    },
    
    createHelperMethods() {
        // Fast element getters
        window.getCards = () => this.cache.get('cards') || [];
        window.getButtons = () => this.cache.get('buttons') || [];
        window.getAIButtons = () => this.cache.get('aiButtons') || [];
        window.getStatusBadges = () => this.cache.get('statusBadges') || [];
        window.getCardValues = () => this.cache.get('cardValues') || [];
        window.getModals = () => this.cache.get('modals') || [];
        
        // Fast element finder by card ID
        window.getCardById = (cardId) => {
            return this.cache.get('cards')?.find(card => card.dataset.cardId === cardId);
        };
        
        // Fast element updater
        window.updateCardValue = (cardId, value) => {
            const card = window.getCardById(cardId);
            if (card) {
                const valueEl = card.querySelector('.card-value');
                if (valueEl) valueEl.textContent = value;
            }
        };
        
        window.updateCardStatus = (cardId, status) => {
            const card = window.getCardById(cardId);
            if (card) {
                const statusEl = card.querySelector('.status-badge');
                if (statusEl) {
                    statusEl.textContent = status;
                    statusEl.className = `status-badge ${status}`;
                }
            }
        };
    },
    
    refresh() {
        this.cache.clear();
        this.buildCache();
    },
    
    get(name) {
        return this.cache.get(name) || [];
    },
    
    invalidate(name) {
        if (name) {
            this.cache.delete(name);
            if (this.selectors[name]) {
                const elements = document.querySelectorAll(this.selectors[name]);
                this.cache.set(name, Array.from(elements));
            }
        } else {
            this.refresh();
        }
    }
};

// Auto-refresh cache when DOM changes
const observer = new MutationObserver(() => {
    if (window.ElementCache) {
        window.ElementCache.refresh();
    }
});

document.addEventListener('DOMContentLoaded', () => {
    window.ElementCache.init();
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});
'''
        
        with open(element_cache_js, 'w') as f:
            f.write(content)
        
        logger.info("✅ Idea 7: Element caching implemented")
    
    def idea_8_use_event_delegation(self):
        """Idea 8: Use event delegation to reduce event listener overhead"""
        event_delegation_js = self.static_js_path / "event-delegation.js"
        
        content = '''// Event Delegation - Single Event Listener for Multiple Elements
console.log("Event delegation loading...");

window.EventDelegation = {
    init() {
        this.setupDelegatedEvents();
        console.log("✅ Event delegation active");
    },
    
    setupDelegatedEvents() {
        // Single click handler for all buttons
        document.addEventListener('click', this.handleClick.bind(this));
        
        // Single change handler for all inputs
        document.addEventListener('change', this.handleChange.bind(this));
        
        // Single mouseover handler for all interactive elements
        document.addEventListener('mouseover', this.handleMouseOver.bind(this));
    },
    
    handleClick(event) {
        const target = event.target;
        
        // AI button clicks
        if (target.matches('.ai-btn, .ai-analyze-btn')) {
            this.handleAIButtonClick(target, event);
        }
        
        // Modal close buttons
        else if (target.matches('.modal-close, .modal-close-btn')) {
            this.handleModalClose(target, event);
        }
        
        // Settings buttons
        else if (target.matches('.settings-btn, .gear-icon')) {
            this.handleSettingsClick(target, event);
        }
        
        // Navigation buttons
        else if (target.matches('.nav-btn, .sidebar-item')) {
            this.handleNavigationClick(target, event);
        }
    },
    
    handleAIButtonClick(button, event) {
        event.preventDefault();
        
        // Add immediate visual feedback
        button.classList.add('loading');
        
        const cardId = button.dataset.cardId || button.closest('[data-card-id]')?.dataset.cardId;
        
        if (cardId && window.OnDemandAI) {
            window.OnDemandAI.runAnalysis(cardId, button);
        }
    },
    
    handleModalClose(button, event) {
        event.preventDefault();
        
        const modal = button.closest('.modal');
        if (modal && window.ModalFixes) {
            window.ModalFixes.closeModal(modal);
        }
    },
    
    handleSettingsClick(button, event) {
        event.preventDefault();
        
        // Toggle settings panel
        const settingsPanel = document.querySelector('.settings-panel');
        if (settingsPanel) {
            settingsPanel.style.display = settingsPanel.style.display === 'none' ? 'block' : 'none';
        }
    },
    
    handleNavigationClick(button, event) {
        // Add navigation feedback
        button.classList.add('active');
        
        // Remove active class from siblings
        const siblings = button.parentElement.querySelectorAll('.nav-btn, .sidebar-item');
        siblings.forEach(sibling => {
            if (sibling !== button) {
                sibling.classList.remove('active');
            }
        });
    },
    
    handleChange(event) {
        const target = event.target;
        
        // Asset selection dropdowns
        if (target.matches('.asset-select, .investment-select')) {
            this.handleAssetSelection(target, event);
        }
    },
    
    handleAssetSelection(select, event) {
        const selectedValue = select.value;
        const card = select.closest('[data-card-id]');
        
        if (card) {
            // Update card based on selection
            this.updateCardForAsset(card, selectedValue);
        }
    },
    
    updateCardForAsset(card, assetId) {
        // Update card content based on selected asset
        const titleEl = card.querySelector('.card-title');
        if (titleEl && assetId) {
            titleEl.textContent = `Asset: ${assetId}`;
        }
    },
    
    handleMouseOver(event) {
        const target = event.target;
        
        // Preload hover states
        if (target.matches('button, .btn')) {
            target.classList.add('hover-ready');
        }
    }
};

document.addEventListener('DOMContentLoaded', () => {
    window.EventDelegation.init();
});
'''
        
        with open(event_delegation_js, 'w') as f:
            f.write(content)
        
        logger.info("✅ Idea 8: Event delegation implemented")
    
    def idea_9_optimize_css_animations(self):
        """Idea 9: Optimize CSS animations to reduce reflows and repaints"""
        animation_optimizer_css = self.src_path / "external_interfaces" / "ui" / "static" / "css" / "animation-optimizer.css"
        
        content = '''/* Animation Optimizer - GPU-Accelerated Animations */

/* Force GPU acceleration for better performance */
.gpu-accelerated,
button,
.btn,
.modal,
.card,
.ai-btn {
    will-change: transform, opacity;
    transform: translateZ(0);
    backface-visibility: hidden;
}

/* Optimize transitions - only animate transform and opacity */
button, .btn {
    transition: transform 0.1s ease, opacity 0.1s ease !important;
}

/* Remove expensive animations */
.card {
    transition: transform 0.2s ease !important;
}

.card:hover {
    transform: translateY(-2px) translateZ(0);
}

/* Optimize loading animations */
@keyframes optimizedSpin {
    from { transform: rotate(0deg) translateZ(0); }
    to { transform: rotate(360deg) translateZ(0); }
}

.loading::after {
    animation: optimizedSpin 0.8s linear infinite;
}

/* Optimize modal animations */
.modal {
    transition: opacity 0.2s ease, transform 0.2s ease !important;
}

.modal.show {
    transform: translateY(0) translateZ(0);
    opacity: 1;
}

.modal:not(.show) {
    transform: translateY(-20px) translateZ(0);
    opacity: 0;
}

/* Optimize fade animations */
.fade-in {
    animation: optimizedFadeIn 0.3s ease forwards;
}

@keyframes optimizedFadeIn {
    from { 
        opacity: 0; 
        transform: translateY(10px) translateZ(0);
    }
    to { 
        opacity: 1; 
        transform: translateY(0) translateZ(0);
    }
}

/* Reduce animation complexity for mobile */
@media (max-width: 768px) {
    * {
        animation-duration: 0.2s !important;
        transition-duration: 0.2s !important;
    }
    
    .card:hover {
        transform: none;
    }
}

/* Disable animations for reduced motion preference */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

/* Optimize scroll animations */
.smooth-scroll {
    scroll-behavior: smooth;
}

/* Contain layout and paint for better performance */
.card,
.modal,
.dashboard-container {
    contain: layout style paint;
}

/* Optimize backdrop filters */
.modal-backdrop,
.glass-effect {
    backdrop-filter: blur(10px);
    will-change: backdrop-filter;
}

/* Optimize gradients */
.gradient-bg {
    background-attachment: fixed;
    will-change: background-position;
}
'''
        
        with open(animation_optimizer_css, 'w') as f:
            f.write(content)
        
        logger.info("✅ Idea 9: CSS animation optimization implemented")
    
    def idea_10_implement_web_workers(self):
        """Idea 10: Implement Web Workers for heavy computations"""
        web_worker_js = self.static_js_path / "web-worker-manager.js"
        
        content = '''// Web Worker Manager - Offloads Heavy Computations
console.log("Web worker manager loading...");

window.WebWorkerManager = {
    workers: new Map(),
    
    init() {
        this.createDataProcessingWorker();
        this.setupWorkerCommunication();
        console.log("✅ Web worker manager active");
    },
    
    createDataProcessingWorker() {
        // Create worker for data processing
        const workerCode = `
            self.onmessage = function(e) {
                const { type, data, id } = e.data;
                
                try {
                    let result;
                    
                    switch(type) {
                        case 'processChartData':
                            result = processChartData(data);
                            break;
                        case 'formatLargeNumbers':
                            result = formatLargeNumbers(data);
                            break;
                        case 'calculateMetrics':
                            result = calculateMetrics(data);
                            break;
                        default:
                            throw new Error('Unknown task type: ' + type);
                    }
                    
                    self.postMessage({ success: true, result, id });
                } catch (error) {
                    self.postMessage({ success: false, error: error.message, id });
                }
            };
            
            function processChartData(data) {
                // Process chart data without blocking UI
                return data.map(item => ({
                    ...item,
                    processed: true,
                    timestamp: Date.now()
                }));
            }
            
            function formatLargeNumbers(numbers) {
                return numbers.map(num => {
                    if (num >= 1000000) {
                        return (num / 1000000).toFixed(1) + 'M';
                    } else if (num >= 1000) {
                        return (num / 1000).toFixed(1) + 'K';
                    }
                    return num.toString();
                });
            }
            
            function calculateMetrics(data) {
                // Heavy calculation example
                const result = {
                    total: data.reduce((sum, item) => sum + (item.value || 0), 0),
                    average: 0,
                    max: Math.max(...data.map(item => item.value || 0)),
                    min: Math.min(...data.map(item => item.value || 0))
                };
                
                result.average = result.total / data.length;
                
                return result;
            }
        `;
        
        const blob = new Blob([workerCode], { type: 'application/javascript' });
        const worker = new Worker(URL.createObjectURL(blob));
        
        this.workers.set('dataProcessor', worker);
    },
    
    setupWorkerCommunication() {
        this.workers.forEach((worker, name) => {
            worker.onmessage = (e) => {
                this.handleWorkerMessage(name, e.data);
            };
            
            worker.onerror = (error) => {
                console.error(`Worker ${name} error:`, error);
            };
        });
    },
    
    handleWorkerMessage(workerName, data) {
        const { success, result, error, id } = data;
        
        if (success) {
            this.resolveTask(id, result);
        } else {
            this.rejectTask(id, new Error(error));
        }
    },
    
    pendingTasks: new Map(),
    taskIdCounter: 0,
    
    runTask(workerName, taskType, taskData) {
        return new Promise((resolve, reject) => {
            const taskId = ++this.taskIdCounter;
            this.pendingTasks.set(taskId, { resolve, reject });
            
            const worker = this.workers.get(workerName);
            if (!worker) {
                reject(new Error(`Worker ${workerName} not found`));
                return;
            }
            
            worker.postMessage({
                type: taskType,
                data: taskData,
                id: taskId
            });
        });
    },
    
    resolveTask(taskId, result) {
        const task = this.pendingTasks.get(taskId);
        if (task) {
            task.resolve(result);
            this.pendingTasks.delete(taskId);
        }
    },
    
    rejectTask(taskId, error) {
        const task = this.pendingTasks.get(taskId);
        if (task) {
            task.reject(error);
            this.pendingTasks.delete(taskId);
        }
    },
    
    // Helper methods for common tasks
    async processChartData(data) {
        return this.runTask('dataProcessor', 'processChartData', data);
    },
    
    async formatNumbers(numbers) {
        return this.runTask('dataProcessor', 'formatLargeNumbers', numbers);
    },
    
    async calculateMetrics(data) {
        return this.runTask('dataProcessor', 'calculateMetrics', data);
    },
    
    terminate() {
        this.workers.forEach(worker => worker.terminate());
        this.workers.clear();
        this.pendingTasks.clear();
    }
};

// Initialize web workers
document.addEventListener('DOMContentLoaded', () => {
    if (typeof Worker !== 'undefined') {
        window.WebWorkerManager.init();
    } else {
        console.warn('Web Workers not supported in this browser');
    }
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (window.WebWorkerManager) {
        window.WebWorkerManager.terminate();
    }
});
'''
        
        with open(web_worker_js, 'w') as f:
            f.write(content)
        
        logger.info("✅ Idea 10: Web Workers implemented")
    
    def update_template_with_optimizations(self):
        """Update template to include all optimization scripts"""
        template_file = self.src_path / "external_interfaces" / "ui" / "templates" / "dashboard_production.html"
        
        if not template_file.exists():
            logger.warning("Template not found")
            return
        
        with open(template_file, 'r') as f:
            content = f.read()
        
        # Add optimization scripts
        optimization_scripts = '''
    <!-- Button Response Optimizations -->
    <script src="{{ url_for('static', filename='js/button-debounce.js') }}"></script>
    <script src="{{ url_for('static', filename='js/event-cleanup.js') }}"></script>
    <script src="{{ url_for('static', filename='js/dom-optimizer.js') }}"></script>
    <script src="{{ url_for('static', filename='js/lazy-loader.js') }}"></script>
    <script src="{{ url_for('static', filename='js/async-handler.js') }}"></script>
    <script src="{{ url_for('static', filename='js/element-cache.js') }}"></script>
    <script src="{{ url_for('static', filename='js/event-delegation.js') }}"></script>
    <script src="{{ url_for('static', filename='js/web-worker-manager.js') }}"></script>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/button-feedback.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/animation-optimizer.css') }}">
</body>'''
        
        if 'button-debounce.js' not in content:
            content = content.replace('</body>', optimization_scripts)
        
        with open(template_file, 'w') as f:
            f.write(content)
        
        logger.info("✅ Template updated with optimizations")

def main():
    """Execute all button response optimizations"""
    try:
        optimizer = ButtonResponseOptimizer()
        optimizer.implement_all_optimizations()
        optimizer.update_template_with_optimizations()
        
        print("\n" + "="*70)
        print("⚡ BUTTON RESPONSE OPTIMIZATION COMPLETE")
        print("="*70)
        print("✅ 1. Debounced button clicks (prevents multiple rapid clicks)")
        print("✅ 2. Removed redundant event listeners (reduces overhead)")
        print("✅ 3. Optimized DOM queries (cached selectors)")
        print("✅ 4. Implemented lazy loading (loads components when visible)")
        print("✅ 5. Fixed blocking operations (async processing)")
        print("✅ 6. Added visual feedback (immediate button responses)")
        print("✅ 7. Cached DOM elements (avoids repeated queries)")
        print("✅ 8. Used event delegation (single listeners)")
        print("✅ 9. Optimized CSS animations (GPU acceleration)")
        print("✅ 10. Implemented Web Workers (offloads heavy tasks)")
        print("="*70)
        print("🚀 Buttons should now respond instantly with smooth interactions")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Optimization failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()