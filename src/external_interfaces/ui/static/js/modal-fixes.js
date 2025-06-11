// Modal Interaction Fixes
console.log("Modal fixes loading...");

window.ModalFixes = {
    init() {
        this.setupGlobalModalHandlers();
        this.fixExistingModals();
        console.log("✅ Modal fixes initialized");
    },
    
    setupGlobalModalHandlers() {
        // Global escape key handler
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeAllModals();
            }
        });
        
        // Global backdrop click handler
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal-backdrop')) {
                this.closeAllModals();
            }
        });
    },
    
    fixExistingModals() {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            this.addCloseButton(modal);
            this.fixModalZIndex(modal);
        });
    },
    
    addCloseButton(modal) {
        if (modal.querySelector('.modal-close-btn')) return;
        
        const closeBtn = document.createElement('button');
        closeBtn.className = 'modal-close-btn';
        closeBtn.innerHTML = '&times;';
        closeBtn.style.cssText = `
            position: absolute;
            top: 15px;
            right: 20px;
            background: rgba(255, 255, 255, 0.2);
            border: none;
            color: #fff;
            font-size: 24px;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            cursor: pointer;
            z-index: 10001;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
        `;
        
        closeBtn.addEventListener('click', () => {
            this.closeModal(modal);
        });
        
        closeBtn.addEventListener('mouseenter', () => {
            closeBtn.style.background = 'rgba(255, 255, 255, 0.3)';
        });
        
        closeBtn.addEventListener('mouseleave', () => {
            closeBtn.style.background = 'rgba(255, 255, 255, 0.2)';
        });
        
        const modalContent = modal.querySelector('.modal-content') || modal;
        modalContent.appendChild(closeBtn);
    },
    
    fixModalZIndex(modal) {
        modal.style.zIndex = '10000';
        
        const backdrop = modal.querySelector('.modal-backdrop');
        if (backdrop) {
            backdrop.style.zIndex = '9999';
        }
    },
    
    closeModal(modal) {
        modal.style.display = 'none';
        modal.classList.remove('show');
        
        const backdrop = document.querySelector('.modal-backdrop');
        if (backdrop) {
            backdrop.remove();
        }
        
        document.body.classList.remove('modal-open');
        document.body.style.overflow = '';
    },
    
    closeAllModals() {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            this.closeModal(modal);
        });
    },
    
    openModal(modalId) {
        const modal = document.getElementById(modalId);
        if (!modal) return;
        
        this.addCloseButton(modal);
        this.fixModalZIndex(modal);
        
        modal.style.display = 'block';
        modal.classList.add('show');
        
        document.body.classList.add('modal-open');
        document.body.style.overflow = 'hidden';
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        window.ModalFixes.init();
    }, 1000);
});

// Export for global use
window.openModal = (modalId) => window.ModalFixes.openModal(modalId);
window.closeModal = (modalId) => {
    const modal = document.getElementById(modalId);
    if (modal) window.ModalFixes.closeModal(modal);
};
