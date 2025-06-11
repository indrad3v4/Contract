// Global Error Handler - Prevents Dashboard Crashes
console.log("Global error handler loading...");

window.GlobalErrorHandler = {
    errorCount: 0,
    maxErrors: 10,
    
    init() {
        this.setupGlobalErrorHandling();
        this.setupConsoleOverrides();
        console.log("✅ Global error handler initialized");
    },
    
    setupGlobalErrorHandling() {
        // Catch unhandled JavaScript errors
        window.addEventListener('error', (event) => {
            this.handleError('JavaScript Error', event.error, event.filename, event.lineno);
            event.preventDefault(); // Prevent default browser error handling
        });
        
        // Catch unhandled promise rejections
        window.addEventListener('unhandledrejection', (event) => {
            this.handleError('Promise Rejection', event.reason);
            event.preventDefault();
        });
    },
    
    setupConsoleOverrides() {
        const originalError = console.error;
        console.error = (...args) => {
            this.logSafeError(...args);
            originalError.apply(console, args);
        };
    },
    
    handleError(type, error, filename = '', lineno = 0) {
        this.errorCount++;
        
        if (this.errorCount > this.maxErrors) {
            console.warn("Too many errors, suppressing further error handling");
            return;
        }
        
        const errorInfo = {
            type,
            message: error?.message || error?.toString() || 'Unknown error',
            filename,
            lineno,
            timestamp: new Date().toISOString()
        };
        
        // Log safely
        this.logSafeError('Handled Error:', errorInfo);
        
        // Show user-friendly notification for critical errors
        if (this.isCriticalError(errorInfo.message)) {
            this.showErrorNotification(errorInfo.message);
        }
    },
    
    logSafeError(...args) {
        try {
            // Safe logging that won't crash
            const message = args.map(arg => 
                typeof arg === 'object' ? JSON.stringify(arg, null, 2) : String(arg)
            ).join(' ');
            
            console.warn('Safe Error Log:', message);
        } catch (e) {
            // Even logging failed, just continue
        }
    },
    
    isCriticalError(message) {
        const criticalPatterns = [
            'feather',
            'toSvg',
            'undefined is not an object',
            'Cannot read properties of undefined',
            'fetch'
        ];
        
        return criticalPatterns.some(pattern => 
            message.toLowerCase().includes(pattern.toLowerCase())
        );
    },
    
    showErrorNotification(message) {
        // Only show if not already showing
        if (document.querySelector('.error-notification')) return;
        
        const notification = document.createElement('div');
        notification.className = 'error-notification';
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            background: rgba(255, 71, 87, 0.9);
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            max-width: 300px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
        `;
        
        notification.innerHTML = `
            <div style="display: flex; align-items: center; gap: 8px;">
                <span>⚠️</span>
                <div>
                    <div style="font-weight: 600; margin-bottom: 4px;">Dashboard Notice</div>
                    <div style="font-size: 0.9rem;">Some features may be temporarily unavailable. Retrying...</div>
                </div>
                <button onclick="this.parentElement.parentElement.remove()" style="background: none; border: none; color: white; font-size: 18px; cursor: pointer; padding: 0; margin-left: 8px;">&times;</button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    },
    
    // Safe function wrapper
    safeExecute(fn, context = null, ...args) {
        try {
            return fn.apply(context, args);
        } catch (error) {
            this.handleError('Safe Execute', error);
            return null;
        }
    },
    
    // Safe async function wrapper
    async safeExecuteAsync(fn, context = null, ...args) {
        try {
            return await fn.apply(context, args);
        } catch (error) {
            this.handleError('Safe Execute Async', error);
            return null;
        }
    }
};

// Initialize immediately
window.GlobalErrorHandler.init();

// Export safe execution methods globally
window.safeExecute = (fn, ...args) => window.GlobalErrorHandler.safeExecute(fn, null, ...args);
window.safeExecuteAsync = (fn, ...args) => window.GlobalErrorHandler.safeExecuteAsync(fn, null, ...args);
