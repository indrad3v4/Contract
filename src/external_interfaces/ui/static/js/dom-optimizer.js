// DOM Query Optimizer - Caches Selectors and Optimizes Queries
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
