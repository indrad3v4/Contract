/**
 * Blockchain Metrics Module
 * Fetches real ODIS token data and network statistics from authentic blockchain endpoints
 */

const BlockchainMetrics = {
    // Update intervals in milliseconds
    intervals: {
        tokenPrice: 30000,    // 30 seconds
        networkStats: 15000,  // 15 seconds  
        realEstate: 60000     // 1 minute
    },
    
    // Store interval IDs for cleanup
    intervalIds: {},
    
    // Initialize the metrics system
    init() {
        this.fetchAllMetrics();
        this.startAutoRefresh();
    },
    
    // Fetch all metrics once
    async fetchAllMetrics() {
        await Promise.all([
            this.fetchTokenPrice(),
            this.fetchNetworkStats(),
            this.fetchRealEstateMetrics()
        ]);
    },
    
    // Start automatic refresh intervals
    startAutoRefresh() {
        this.intervalIds.tokenPrice = setInterval(() => {
            this.fetchTokenPrice();
        }, this.intervals.tokenPrice);
        
        this.intervalIds.networkStats = setInterval(() => {
            this.fetchNetworkStats();
        }, this.intervals.networkStats);
        
        this.intervalIds.realEstate = setInterval(() => {
            this.fetchRealEstateMetrics();
        }, this.intervals.realEstate);
    },
    
    // Stop all auto-refresh intervals
    stopAutoRefresh() {
        Object.values(this.intervalIds).forEach(id => clearInterval(id));
        this.intervalIds = {};
    },
    
    // Fetch ODIS token price from blockchain
    async fetchTokenPrice() {
        try {
            const response = await fetch('/api/blockchain/token-price');
            if (!response.ok) throw new Error('Token price fetch failed');
            
            const result = await response.json();
            if (result.success) {
                this.updateTokenPriceUI(result.data);
            } else {
                this.showTokenPriceError(result.error);
            }
        } catch (error) {
            console.error('Error fetching token price:', error);
            this.showTokenPriceError('Unable to fetch current token price');
        }
    },
    
    // Fetch network statistics from blockchain
    async fetchNetworkStats() {
        try {
            const response = await fetch('/api/blockchain/network-stats');
            if (!response.ok) throw new Error('Network stats fetch failed');
            
            const result = await response.json();
            if (result.success) {
                this.updateNetworkStatsUI(result.data);
            } else {
                this.showNetworkStatsError(result.error);
            }
        } catch (error) {
            console.error('Error fetching network stats:', error);
            this.showNetworkStatsError('Unable to fetch network statistics');
        }
    },
    
    // Fetch real estate metrics from blockchain
    async fetchRealEstateMetrics() {
        try {
            const response = await fetch('/api/blockchain/real-estate-metrics');
            if (!response.ok) throw new Error('Real estate metrics fetch failed');
            
            const result = await response.json();
            if (result.success) {
                this.updateRealEstateUI(result.data);
            } else {
                this.showRealEstateError(result.error);
            }
        } catch (error) {
            console.error('Error fetching real estate metrics:', error);
            this.showRealEstateError('Unable to fetch property data');
        }
    },
    
    // Update token price UI with authentic data
    updateTokenPriceUI(data) {
        const priceElement = document.getElementById('odis-price');
        const changeElement = document.getElementById('price-change');
        
        if (priceElement) {
            priceElement.textContent = `$${data.current_price}`;
            priceElement.classList.remove('error');
        }
        
        if (changeElement && data.price_change_24h !== undefined) {
            const change = data.price_change_24h;
            const isPositive = change >= 0;
            
            changeElement.textContent = `${isPositive ? '+' : ''}${change}%`;
            changeElement.className = `metric-change ${isPositive ? 'positive' : 'negative'}`;
        }
    },
    
    // Update network statistics UI
    updateNetworkStatsUI(data) {
        const blockHeightElement = document.getElementById('block-height');
        const validatorCountElement = document.getElementById('validator-count');
        
        if (blockHeightElement) {
            blockHeightElement.textContent = data.latest_block_height.toLocaleString();
            blockHeightElement.classList.remove('error');
        }
        
        if (validatorCountElement) {
            validatorCountElement.textContent = data.active_validators;
            validatorCountElement.classList.remove('error');
        }
    },
    
    // Update real estate metrics UI
    updateRealEstateUI(data) {
        const propertiesElement = document.getElementById('total-properties');
        const valueElement = document.getElementById('total-value');
        
        if (propertiesElement) {
            propertiesElement.textContent = data.total_properties_tokenized;
            propertiesElement.classList.remove('error');
        }
        
        if (valueElement) {
            const valueInK = data.total_value_locked_usd >= 1000 ? 
                `$${(data.total_value_locked_usd / 1000).toFixed(1)}K` : 
                `$${data.total_value_locked_usd.toFixed(0)}`;
            valueElement.textContent = valueInK;
            valueElement.classList.remove('error');
        }
    },
    
    // Show token price error
    showTokenPriceError(message) {
        const priceElement = document.getElementById('odis-price');
        const changeElement = document.getElementById('price-change');
        
        if (priceElement) {
            priceElement.textContent = 'Error';
            priceElement.classList.add('error');
            priceElement.title = message;
        }
        
        if (changeElement) {
            changeElement.textContent = '...';
            changeElement.className = 'metric-change';
        }
    },
    
    // Show network stats error
    showNetworkStatsError(message) {
        const blockHeightElement = document.getElementById('block-height');
        const validatorCountElement = document.getElementById('validator-count');
        
        [blockHeightElement, validatorCountElement].forEach(element => {
            if (element) {
                element.textContent = 'Error';
                element.classList.add('error');
                element.title = message;
            }
        });
    },
    
    // Show real estate error
    showRealEstateError(message) {
        const propertiesElement = document.getElementById('total-properties');
        const valueElement = document.getElementById('total-value');
        
        [propertiesElement, valueElement].forEach(element => {
            if (element) {
                element.textContent = 'Error';
                element.classList.add('error');
                element.title = message;
            }
        });
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    BlockchainMetrics.init();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    BlockchainMetrics.stopAutoRefresh();
});