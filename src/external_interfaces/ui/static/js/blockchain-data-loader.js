
// Blockchain Data Loading with Graceful Degradation
class BlockchainDataLoader {
    constructor() {
        this.cache = new Map();
        this.cacheTimeout = 30000; // 30 seconds
        this.loadingStates = new Set();
    }
    
    async loadData(endpoint, fallbackData = null) {
        const cacheKey = endpoint;
        const now = Date.now();
        
        // Check cache first
        if (this.cache.has(cacheKey)) {
            const cached = this.cache.get(cacheKey);
            if (now - cached.timestamp < this.cacheTimeout) {
                return cached.data;
            }
        }
        
        // Prevent duplicate loading
        if (this.loadingStates.has(endpoint)) {
            return this.waitForLoad(endpoint);
        }
        
        this.loadingStates.add(endpoint);
        this.showLoadingState(endpoint);
        
        try {
            const data = await window.apiManager.fetchWithRetry(endpoint);
            
            if (data.error) {
                throw new Error(data.message);
            }
            
            // Cache successful response
            this.cache.set(cacheKey, {
                data: data,
                timestamp: now
            });
            
            this.hideLoadingState(endpoint);
            this.loadingStates.delete(endpoint);
            
            return data;
            
        } catch (error) {
            console.warn(`Failed to load ${endpoint}:`, error);
            this.showErrorState(endpoint, error.message);
            this.loadingStates.delete(endpoint);
            
            // Return fallback data if available
            if (fallbackData) {
                return fallbackData;
            }
            
            return {
                error: true,
                message: error.message,
                endpoint: endpoint
            };
        }
    }
    
    showLoadingState(endpoint) {
        const elements = document.querySelectorAll(`[data-endpoint="${endpoint}"]`);
        elements.forEach(el => {
            el.classList.add('loading');
            el.innerHTML = '<div class="loading-spinner"></div><span>Loading...</span>';
        });
    }
    
    hideLoadingState(endpoint) {
        const elements = document.querySelectorAll(`[data-endpoint="${endpoint}"]`);
        elements.forEach(el => {
            el.classList.remove('loading', 'error');
        });
    }
    
    showErrorState(endpoint, message) {
        const elements = document.querySelectorAll(`[data-endpoint="${endpoint}"]`);
        elements.forEach(el => {
            el.classList.add('error');
            el.innerHTML = `
                <div class="error-icon">⚠️</div>
                <span class="error-message">${message}</span>
                <button class="retry-btn" onclick="retryLoad('${endpoint}')">Retry</button>
            `;
        });
    }
    
    async waitForLoad(endpoint) {
        return new Promise((resolve) => {
            const checkLoading = () => {
                if (!this.loadingStates.has(endpoint)) {
                    const cached = this.cache.get(endpoint);
                    resolve(cached ? cached.data : null);
                } else {
                    setTimeout(checkLoading, 100);
                }
            };
            checkLoading();
        });
    }
}

window.blockchainDataLoader = new BlockchainDataLoader();

// Global retry function
function retryLoad(endpoint) {
    window.blockchainDataLoader.cache.delete(endpoint);
    window.blockchainDataLoader.loadData(endpoint);
}
