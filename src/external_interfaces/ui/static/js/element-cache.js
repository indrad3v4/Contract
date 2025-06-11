// Element Cache - Stores DOM References for Fast Access
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
