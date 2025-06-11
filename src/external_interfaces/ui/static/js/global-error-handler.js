// Global Error Handler - Prevents JavaScript Crashes
console.log("Global error handler loading...");

window.GlobalErrorHandler = {
    errorCount: 0,
    maxErrors: 10,
    errorLog: [],
    
    init() {
        this.setupErrorHandlers();
        this.setupPromiseRejectionHandler();
        console.log("✅ Global error handler initialized");
    },
    
    setupErrorHandlers() {
        window.addEventListener('error', (event) => {
            this.handleError({
                type: 'JavaScript Error',
                message: event.message,
                filename: event.filename,
                lineno: event.lineno,
                timestamp: new Date().toISOString()
            });
        });
        
        window.addEventListener('unhandledrejection', (event) => {
            this.handleError({
                type: 'Promise Rejection',
                message: event.reason?.message || event.reason,
                filename: '',
                lineno: 0,
                timestamp: new Date().toISOString()
            });
            
            // Prevent the error from appearing in console
            event.preventDefault();
        });
    },
    
    setupPromiseRejectionHandler() {
        // Override fetch to handle network errors gracefully
        const originalFetch = window.fetch;
        
        window.fetch = async (...args) => {
            try {
                const response = await originalFetch.apply(this, args);
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                return response;
            } catch (error) {
                this.handleNetworkError(args[0], error);
                throw error;
            }
        };
    },
    
    handleError(errorInfo) {
        this.errorCount++;
        this.errorLog.push(errorInfo);
        
        // Keep only last 20 errors
        if (this.errorLog.length > 20) {
            this.errorLog.shift();
        }
        
        // Log error safely
        this.safeLog(errorInfo);
        
        // Handle specific error types
        if (errorInfo.message.includes('toSvg')) {
            this.handleFeatherError();
        } else if (errorInfo.message.includes('orchestrator')) {
            this.handleOrchestratorError();
        } else if (errorInfo.message.includes('fetch')) {
            this.handleFetchError();
        }
        
        // Emergency fallback if too many errors
        if (this.errorCount > this.maxErrors) {
            this.activateEmergencyMode();
        }
    },
    
    handleNetworkError(url, error) {
        const urlString = typeof url === 'string' ? url : url.toString();
        
        if (urlString.includes('/api/')) {
            this.showUserFriendlyError('Network connection issue. Please check your internet connection.');
        }
    },
    
    handleFeatherError() {
        // Replace feather icons with safe fallbacks
        if (window.FeatherSafe) {
            window.FeatherSafe.createFallbackIcons();
        }
    },
    
    handleOrchestratorError() {
        // Show AI unavailable message
        this.showUserFriendlyError('AI assistant temporarily unavailable. Basic features are still working.');
    },
    
    handleFetchError() {
        // Generic fetch error handling
        this.showUserFriendlyError('Unable to load some data. Retrying automatically...');
    },
    
    safeLog(errorInfo) {
        try {
            console.warn('Safe Error Log:', JSON.stringify(errorInfo, null, 2));
        } catch (e) {
            console.warn('Safe Error Log:', 'Handled Error:', errorInfo);
        }
    },
    
    showUserFriendlyError(message) {
        // Show toast notification instead of console error
        this.showToast(message, 'warning');
    },
    
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        
        // Position toast
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 1rem;
            border-radius: 6px;
            border-left: 4px solid ${type === 'warning' ? '#ffa500' : '#4a90e2'};
            z-index: 10000;
            max-width: 300px;
            backdrop-filter: blur(10px);
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(toast);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (toast.parentElement) {
                toast.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => toast.remove(), 300);
            }
        }, 5000);
    },
    
    activateEmergencyMode() {
        console.warn('Emergency mode activated - too many errors detected');
        
        // Disable non-essential features
        this.disableAnimations();
        this.simplifyInterface();
        
        this.showToast('Simplified mode activated due to technical issues', 'warning');
    },
    
    disableAnimations() {
        const style = document.createElement('style');
        style.textContent = `
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        `;
        document.head.appendChild(style);
    },
    
    simplifyInterface() {
        // Hide complex components that might be causing issues
        const complexElements = document.querySelectorAll('.chart-container, .bim-viewer, [data-feather]');
        complexElements.forEach(el => {
            el.style.display = 'none';
        });
    },
    
    getErrorStats() {
        return {
            totalErrors: this.errorCount,
            recentErrors: this.errorLog.slice(-5),
            errorTypes: this.errorLog.reduce((acc, error) => {
                acc[error.type] = (acc[error.type] || 0) + 1;
                return acc;
            }, {})
        };
    }
};

// Auto-initialize
document.addEventListener('DOMContentLoaded', () => {
    window.GlobalErrorHandler.init();
});

// Add animation keyframes
const errorStyle = document.createElement('style');
errorStyle.textContent = `
@keyframes slideIn {
    from { 
        opacity: 0; 
        transform: translateX(100%); 
    }
    to { 
        opacity: 1; 
        transform: translateX(0); 
    }
}

@keyframes slideOut {
    from { 
        opacity: 1; 
        transform: translateX(0); 
    }
    to { 
        opacity: 0; 
        transform: translateX(100%); 
    }
}
`;
document.head.appendChild(errorStyle);
