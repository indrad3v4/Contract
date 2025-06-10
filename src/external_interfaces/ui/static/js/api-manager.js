
// Enhanced API Error Handling
class APIManager {
    constructor() {
        this.retryCount = 3;
        this.baseTimeout = 5000;
    }
    
    async fetchWithRetry(url, options = {}, retries = this.retryCount) {
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), this.baseTimeout);
            
            const response = await fetch(url, {
                ...options,
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            return await response.json();
        } catch (error) {
            console.warn(`API call failed for ${url}:`, error.message);
            
            if (retries > 0 && !error.name === 'AbortError') {
                console.log(`Retrying API call... (${this.retryCount - retries + 1}/${this.retryCount})`);
                await new Promise(resolve => setTimeout(resolve, 1000 * (this.retryCount - retries + 1)));
                return this.fetchWithRetry(url, options, retries - 1);
            }
            
            // Return structured error response instead of empty object
            return {
                error: true,
                message: error.message,
                url: url,
                timestamp: new Date().toISOString()
            };
        }
    }
    
    async loadBlockchainData() {
        const endpoints = [
            '/api/blockchain/stats',
            '/api/blockchain/token-price',
            '/api/blockchain/stakeholder-distribution'
        ];
        
        const results = {};
        
        for (const endpoint of endpoints) {
            results[endpoint] = await this.fetchWithRetry(endpoint);
        }
        
        return results;
    }
}

window.apiManager = new APIManager();
