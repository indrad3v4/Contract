// Throttled Fetch Queue - Prevents API Overload
console.log("Throttled fetch queue loading...");

window.FetchQueueManager = {
    queue: [],
    activeRequests: 0,
    maxConcurrent: 2,
    requestDelay: 300, // ms between requests
    lastRequestTime: 0,
    
    init() {
        this.interceptFetch();
        this.startQueueProcessor();
        console.log("✅ Fetch queue manager active");
    },
    
    interceptFetch() {
        const originalFetch = window.fetch;
        
        window.fetch = (...args) => {
            return this.queuedFetch(originalFetch, ...args);
        };
    },
    
    queuedFetch(originalFetch, ...args) {
        return new Promise((resolve, reject) => {
            const request = {
                id: Date.now() + Math.random(),
                originalFetch,
                args,
                resolve,
                reject,
                timestamp: Date.now(),
                priority: this.getRequestPriority(args[0])
            };
            
            this.queue.push(request);
            this.queue.sort((a, b) => b.priority - a.priority);
            
            this.processQueue();
        });
    },
    
    getRequestPriority(url) {
        if (typeof url === 'string') {
            if (url.includes('/orchestrator/')) return 100; // AI requests
            if (url.includes('/blockchain/stats')) return 80; // Stats
            if (url.includes('/rpc/')) return 60; // RPC calls
            if (url.includes('/bim-agent/')) return 40; // BIM
        }
        return 50; // Default priority
    },
    
    processQueue() {
        if (this.activeRequests >= this.maxConcurrent || this.queue.length === 0) {
            return;
        }
        
        const now = Date.now();
        const timeSinceLastRequest = now - this.lastRequestTime;
        
        if (timeSinceLastRequest < this.requestDelay) {
            setTimeout(() => this.processQueue(), this.requestDelay - timeSinceLastRequest);
            return;
        }
        
        const request = this.queue.shift();
        this.executeRequest(request);
    },
    
    async executeRequest(request) {
        this.activeRequests++;
        this.lastRequestTime = Date.now();
        
        try {
            const response = await request.originalFetch(...request.args);
            request.resolve(response);
            
            // Log successful request
            this.logRequest(request, 'success');
            
        } catch (error) {
            request.reject(error);
            
            // Log failed request
            this.logRequest(request, 'error', error);
            
        } finally {
            this.activeRequests--;
            
            // Process next request after delay
            setTimeout(() => this.processQueue(), this.requestDelay);
        }
    },
    
    logRequest(request, status, error = null) {
        const url = typeof request.args[0] === 'string' ? request.args[0] : 'unknown';
        const duration = Date.now() - request.timestamp;
        
        if (window.PerformanceMonitor) {
            window.PerformanceMonitor.recordRequest(url, status, duration);
        }
        
        if (status === 'error') {
            console.warn(`Fetch failed for ${url}:`, error);
        }
    },
    
    startQueueProcessor() {
        // Periodic queue processing
        setInterval(() => {
            this.processQueue();
        }, 100);
    },
    
    // Priority fetch for critical requests
    priorityFetch(...args) {
        const originalFetch = window.fetch.__original || fetch;
        
        return new Promise((resolve, reject) => {
            const request = {
                id: Date.now() + Math.random(),
                originalFetch,
                args,
                resolve,
                reject,
                timestamp: Date.now(),
                priority: 1000 // Highest priority
            };
            
            this.queue.unshift(request); // Add to front
            this.processQueue();
        });
    },
    
    // Batch fetch for multiple requests
    batchFetch(requests) {
        const promises = requests.map(request => {
            if (Array.isArray(request)) {
                return this.queuedFetch(window.fetch.__original || fetch, ...request);
            } else {
                return this.queuedFetch(window.fetch.__original || fetch, request);
            }
        });
        
        return Promise.all(promises);
    },
    
    // Cancel requests by URL pattern
    cancelRequests(urlPattern) {
        this.queue = this.queue.filter(request => {
            const url = typeof request.args[0] === 'string' ? request.args[0] : '';
            
            if (url.includes(urlPattern)) {
                request.reject(new Error('Request cancelled'));
                return false;
            }
            
            return true;
        });
    },
    
    // Get queue status
    getStatus() {
        return {
            queueLength: this.queue.length,
            activeRequests: this.activeRequests,
            maxConcurrent: this.maxConcurrent,
            requestDelay: this.requestDelay
        };
    },
    
    // Adjust throttling parameters
    setThrottling(maxConcurrent, requestDelay) {
        this.maxConcurrent = maxConcurrent;
        this.requestDelay = requestDelay;
    },
    
    // Clear queue
    clearQueue() {
        this.queue.forEach(request => {
            request.reject(new Error('Queue cleared'));
        });
        this.queue = [];
    }
};

// Store original fetch for priority requests
if (!window.fetch.__original) {
    window.fetch.__original = window.fetch;
}

// Auto-initialize
document.addEventListener('DOMContentLoaded', () => {
    window.FetchQueueManager.init();
});

// Global helpers
window.priorityFetch = (...args) => {
    if (window.FetchQueueManager) {
        return window.FetchQueueManager.priorityFetch(...args);
    }
    return fetch(...args);
};

window.batchFetch = (requests) => {
    if (window.FetchQueueManager) {
        return window.FetchQueueManager.batchFetch(requests);
    }
    return Promise.all(requests.map(req => fetch(req)));
};

// Expose queue management
window.getFetchQueueStatus = () => {
    return window.FetchQueueManager?.getStatus() || { error: 'Queue manager not initialized' };
};
