// Event Delegation - Single Event Listener for Multiple Elements
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
