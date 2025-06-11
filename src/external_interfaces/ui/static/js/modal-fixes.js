// Modal Fixes - Proper Close and Interaction Handling
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
