// Feather Icons Safe Loader - Prevents toSvg() Crashes
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
