// Modal Stack Management - Proper Z-index Hierarchy
console.log("Modal stack management loading...");

window.ModalStackManager = {
    modalStack: [],
    baseZIndex: 1040,
    
    init() {
        this.setupModalInterception();
        this.fixExistingModals();
        console.log("✅ Modal stack manager active");
    },
    
    setupModalInterception() {
        // Intercept Bootstrap modal events
        document.addEventListener('show.bs.modal', (e) => {
            this.onModalShow(e.target);
        });
        
        document.addEventListener('hide.bs.modal', (e) => {
            this.onModalHide(e.target);
        });
        
        // Intercept custom modal operations
        document.addEventListener('click', (e) => {
            if (e.target.matches('.modal-trigger, [data-modal]')) {
                const modalId = e.target.dataset.modal || e.target.getAttribute('href')?.substring(1);
                if (modalId) {
                    const modal = document.getElementById(modalId);
                    if (modal) {
                        this.showModal(modal);
                    }
                }
            } else if (e.target.matches('.modal-close, .modal-dismiss')) {
                const modal = e.target.closest('.modal');
                if (modal) {
                    this.hideModal(modal);
                }
            }
        });
        
        // Handle Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.modalStack.length > 0) {
                const topModal = this.modalStack[this.modalStack.length - 1];
                this.hideModal(topModal.element);
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
        // Ensure proper structure
        if (!modal.querySelector('.modal-dialog')) {
            const content = modal.innerHTML;
            modal.innerHTML = `
                <div class="modal-dialog">
                    <div class="modal-content">
                        ${content}
                    </div>
                </div>
            `;
        }
        
        // Add backdrop if missing
        if (!modal.querySelector('.modal-backdrop')) {
            const backdrop = document.createElement('div');
            backdrop.className = 'modal-backdrop';
            backdrop.onclick = () => this.hideModal(modal);
            modal.appendChild(backdrop);
        }
        
        // Add close button if missing
        if (!modal.querySelector('.modal-close')) {
            const closeBtn = document.createElement('button');
            closeBtn.className = 'modal-close';
            closeBtn.innerHTML = '×';
            closeBtn.onclick = () => this.hideModal(modal);
            
            const modalContent = modal.querySelector('.modal-content');
            if (modalContent) {
                modalContent.insertBefore(closeBtn, modalContent.firstChild);
            }
        }
    },
    
    onModalShow(modal) {
        this.showModal(modal);
    },
    
    onModalHide(modal) {
        this.hideModal(modal);
    },
    
    showModal(modal) {
        if (!modal) return;
        
        this.prepareModal(modal);
        
        const zIndex = this.baseZIndex + (this.modalStack.length * 10);
        const backdropZIndex = zIndex - 5;
        
        // Set z-indexes
        modal.style.zIndex = zIndex;
        
        const backdrop = modal.querySelector('.modal-backdrop');
        if (backdrop) {
            backdrop.style.zIndex = backdropZIndex;
        }
        
        // Add to stack
        const modalData = {
            element: modal,
            zIndex: zIndex,
            timestamp: Date.now()
        };
        
        this.modalStack.push(modalData);
        
        // Show modal
        modal.classList.add('show');
        modal.style.display = 'block';
        
        // Disable body scroll
        document.body.style.overflow = 'hidden';
        
        // Focus management
        const firstFocusable = modal.querySelector('button, input, select, textarea, [tabindex]:not([tabindex="-1"])');
        if (firstFocusable) {
            firstFocusable.focus();
        }
    },
    
    hideModal(modal) {
        if (!modal) return;
        
        // Remove from stack
        const index = this.modalStack.findIndex(item => item.element === modal);
        if (index >= 0) {
            this.modalStack.splice(index, 1);
        }
        
        // Hide modal
        modal.classList.remove('show');
        modal.style.display = 'none';
        
        // Re-enable body scroll if no modals
        if (this.modalStack.length === 0) {
            document.body.style.overflow = '';
        }
        
        // Focus management - return to previous modal or body
        if (this.modalStack.length > 0) {
            const topModal = this.modalStack[this.modalStack.length - 1];
            topModal.element.focus();
        } else {
            document.body.focus();
        }
    },
    
    hideAllModals() {
        while (this.modalStack.length > 0) {
            const modal = this.modalStack[this.modalStack.length - 1];
            this.hideModal(modal.element);
        }
    },
    
    getActiveModals() {
        return this.modalStack.map(item => ({
            id: item.element.id,
            zIndex: item.zIndex,
            timestamp: item.timestamp
        }));
    }
};

// Auto-initialize
document.addEventListener('DOMContentLoaded', () => {
    window.ModalStackManager.init();
});

// Global modal controls
window.showModal = (modalId) => {
    const modal = document.getElementById(modalId);
    if (modal && window.ModalStackManager) {
        window.ModalStackManager.showModal(modal);
    }
};

window.hideModal = (modalId) => {
    const modal = typeof modalId === 'string' ? document.getElementById(modalId) : modalId;
    if (modal && window.ModalStackManager) {
        window.ModalStackManager.hideModal(modal);
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
    display: none;
    align-items: center;
    justify-content: center;
    z-index: 1050;
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
    z-index: 1040;
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
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    position: relative;
    padding: 2rem;
    color: #fff;
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
}

.modal-close:hover {
    background: rgba(255, 255, 255, 0.1);
}
`;
document.head.appendChild(modalStyle);
