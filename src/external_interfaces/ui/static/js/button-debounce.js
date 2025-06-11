// Button Click Debouncing - Prevents Multiple Rapid Clicks
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
