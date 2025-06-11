// Safe Feather Icons Handler - Prevents Dashboard Crashes
console.log("Safe feather icons handler loading...");

window.SafeFeather = {
    initialized: false,
    
    init() {
        if (this.initialized) return;
        
        // Wait for feather to be available
        if (typeof feather === 'undefined') {
            setTimeout(() => this.init(), 100);
            return;
        }
        
        this.initialized = true;
        console.log("✅ Safe feather icons initialized");
    },
    
    replace(selector = null) {
        if (typeof feather === 'undefined') {
            console.warn("Feather icons not loaded, skipping replace");
            return;
        }
        
        try {
            if (selector) {
                const elements = document.querySelectorAll(selector);
                elements.forEach(el => {
                    if (el && el.hasAttribute('data-feather')) {
                        const iconName = el.getAttribute('data-feather');
                        if (this.isValidIcon(iconName)) {
                            feather.replace(el);
                        } else {
                            console.warn(`Invalid feather icon: ${iconName}`);
                            this.setFallbackIcon(el);
                        }
                    }
                });
            } else {
                // Replace all with safety check
                const featherElements = document.querySelectorAll('[data-feather]');
                featherElements.forEach(el => {
                    const iconName = el.getAttribute('data-feather');
                    if (!this.isValidIcon(iconName)) {
                        console.warn(`Invalid feather icon: ${iconName}`);
                        this.setFallbackIcon(el);
                    }
                });
                
                feather.replace();
            }
            
        } catch (error) {
            console.warn('Feather replace error:', error);
            // Continue without crashing
        }
    },
    
    isValidIcon(iconName) {
        const validIcons = [
            'activity', 'alert-circle', 'alert-triangle', 'arrow-down-left', 'arrow-up-right',
            'bar-chart-2', 'check-circle', 'credit-card', 'database', 'dollar-sign',
            'eye', 'home', 'info', 'lock', 'pie-chart', 'settings', 'trending-up',
            'unlock', 'upload', 'users', 'wallet', 'wifi'
        ];
        
        return validIcons.includes(iconName);
    },
    
    setFallbackIcon(element) {
        element.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>';
    }
};

// Override global feather.replace with safe version
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        window.SafeFeather.init();
        
        // Override feather.replace globally
        if (typeof feather !== 'undefined') {
            const originalReplace = feather.replace;
            feather.replace = function(target) {
                try {
                    return originalReplace.call(this, target);
                } catch (error) {
                    console.warn('Feather replace intercepted error:', error);
                    window.SafeFeather.replace();
                }
            };
        }
    }, 500);
});
