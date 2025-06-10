
// Global Error Handler
class GlobalErrorHandler {
    constructor() {
        this.errorQueue = [];
        this.maxErrors = 50;
        this.notificationTimeout = 5000;
        this.setupGlobalHandlers();
    }
    
    setupGlobalHandlers() {
        // Catch JavaScript errors
        window.addEventListener('error', (event) => {
            this.handleError({
                type: 'javascript',
                message: event.message,
                filename: event.filename,
                lineno: event.lineno,
                colno: event.colno,
                stack: event.error ? event.error.stack : null
            });
        });
        
        // Catch unhandled promise rejections
        window.addEventListener('unhandledrejection', (event) => {
            this.handleError({
                type: 'promise',
                message: event.reason.message || event.reason,
                stack: event.reason.stack
            });
        });
        
        // Catch fetch errors
        const originalFetch = window.fetch;
        window.fetch = async (...args) => {
            try {
                const response = await originalFetch(...args);
                if (!response.ok) {
                    this.handleError({
                        type: 'network',
                        message: `HTTP ${response.status}: ${response.statusText}`,
                        url: args[0]
                    });
                }
                return response;
            } catch (error) {
                this.handleError({
                    type: 'network',
                    message: error.message,
                    url: args[0]
                });
                throw error;
            }
        };
    }
    
    handleError(errorInfo) {
        const timestamp = new Date().toISOString();
        const error = { ...errorInfo, timestamp };
        
        // Add to queue
        this.errorQueue.push(error);
        if (this.errorQueue.length > this.maxErrors) {
            this.errorQueue.shift();
        }
        
        // Log to console
        console.error('Global Error:', error);
        
        // Show user notification for critical errors
        if (this.isCriticalError(error)) {
            this.showErrorNotification(error);
        }
        
        // Send to analytics (if available)
        this.sendErrorAnalytics(error);
    }
    
    isCriticalError(error) {
        const criticalPatterns = [
            /network/i,
            /fetch/i,
            /api/i,
            /blockchain/i,
            /wallet/i
        ];
        
        return criticalPatterns.some(pattern => 
            pattern.test(error.message) || pattern.test(error.type)
        );
    }
    
    showErrorNotification(error) {
        const notification = document.createElement('div');
        notification.className = 'error-notification';
        notification.innerHTML = `
            <div class="error-content">
                <div class="error-icon">⚠️</div>
                <div class="error-text">
                    <strong>Connection Issue</strong>
                    <p>Some features may not work properly. Please check your connection.</p>
                </div>
                <button class="error-close" onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, this.notificationTimeout);
    }
    
    sendErrorAnalytics(error) {
        // Send error data to analytics service
        // Implementation depends on analytics provider
        console.log('Error Analytics:', error);
    }
    
    getErrorReport() {
        return {
            errors: this.errorQueue,
            summary: this.generateErrorSummary()
        };
    }
    
    generateErrorSummary() {
        const types = {};
        this.errorQueue.forEach(error => {
            types[error.type] = (types[error.type] || 0) + 1;
        });
        
        return {
            total: this.errorQueue.length,
            byType: types,
            lastError: this.errorQueue[this.errorQueue.length - 1]
        };
    }
}

window.errorHandler = new GlobalErrorHandler();
