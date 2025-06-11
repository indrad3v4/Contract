// Event Listener Cleanup - Removes Redundant Handlers
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
