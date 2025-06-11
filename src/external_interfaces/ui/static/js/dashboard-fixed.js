// DAODISEO Dashboard - Fixed Rate Limiting and Error Handling
class DashboardManager {
    constructor() {
        this.isInitialized = false;
        this.loadingComponents = new Set();
        this.errorComponents = new Set();
        this.retryTimeouts = new Map();
    }

    async initialize() {
        if (this.isInitialized) return;
        
        console.log('Initializing DAODISEO Dashboard with enhanced error handling...');
        
        // Wait for data manager
        await this.waitForDataManager();
        
        // Initialize components with staggered loading
        await this.staggeredComponentLoad();
        
        this.isInitialized = true;
        console.log('Dashboard initialization complete');
    }

    async waitForDataManager() {
        return new Promise(resolve => {
            const checkManager = () => {
                if (window.dataManager && window.chartLoader) {
                    resolve();
                } else {
                    setTimeout(checkManager, 100);
                }
            };
            checkManager();
        });
    }

    async staggeredComponentLoad() {
        const components = [
            { id: 'network-status', endpoint: '/api/rpc/network-status', handler: this.updateNetworkStatus.bind(this) },
            { id: 'token-metrics', endpoint: '/api/orchestrator/token-metrics', handler: this.updateTokenMetrics.bind(this) },
            { id: 'staking-metrics', endpoint: '/api/orchestrator/staking-metrics', handler: this.updateStakingMetrics.bind(this) }
        ];

        for (let i = 0; i < components.length; i++) {
            const component = components[i];
            setTimeout(() => {
                this.loadComponent(component);
            }, i * 3000); // 3 second delay between components
        }
    }

    async loadComponent(component) {
        const { id, endpoint, handler } = component;
        
        if (this.loadingComponents.has(id)) return;
        
        this.loadingComponents.add(id);
        this.showLoadingState(id);

        try {
            const data = await window.dataManager.getData(endpoint);
            
            if (data && data.success) {
                this.errorComponents.delete(id);
                await handler(data);
                this.showSuccessState(id);
            } else {
                throw new Error('Invalid response data');
            }
        } catch (error) {
            this.handleComponentError(id, endpoint, handler, error);
        } finally {
            this.loadingComponents.delete(id);
        }
    }

    handleComponentError(id, endpoint, handler, error) {
        this.errorComponents.add(id);
        console.error(`Component ${id} error:`, error);
        
        if (error.status === 429) {
            this.showRateLimitError(id, 'Rate limited - will retry automatically');
            this.scheduleRetry(id, endpoint, handler, 30000);
        } else {
            this.showGenericError(id, `Failed to load ${id} data`);
            this.scheduleRetry(id, endpoint, handler, 10000);
        }
    }

    scheduleRetry(id, endpoint, handler, delay) {
        if (this.retryTimeouts.has(id)) {
            clearTimeout(this.retryTimeouts.get(id));
        }
        
        const timeout = setTimeout(() => {
            this.loadComponent({ id, endpoint, handler });
            this.retryTimeouts.delete(id);
        }, delay);
        
        this.retryTimeouts.set(id, timeout);
    }

    showLoadingState(id) {
        const element = document.querySelector(`[data-component="${id}"]`);
        if (element) {
            element.innerHTML = `
                <div class="loading-state">
                    <div class="spinner"></div>
                    <div class="loading-text">Loading ${id}...</div>
                </div>
            `;
        }
    }

    showSuccessState(id) {
        const element = document.querySelector(`[data-component="${id}"]`);
        if (element) {
            element.classList.remove('error-state', 'loading-state');
            element.classList.add('success-state');
        }
    }

    showRateLimitError(id, message) {
        const element = document.querySelector(`[data-component="${id}"]`);
        if (element) {
            element.innerHTML = `
                <div class="error-state rate-limit">
                    <div class="error-icon">⏱️</div>
                    <div class="error-message">${message}</div>
                    <div class="retry-info">Retrying in 30 seconds...</div>
                </div>
            `;
        }
    }

    showGenericError(id, message) {
        const element = document.querySelector(`[data-component="${id}"]`);
        if (element) {
            element.innerHTML = `
                <div class="error-state generic">
                    <div class="error-icon">⚠️</div>
                    <div class="error-message">${message}</div>
                    <button class="retry-btn" onclick="dashboardManager.retryComponent('${id}')">
                        Retry
                    </button>
                </div>
            `;
        }
    }

    async updateNetworkStatus(data) {
        const networkData = data.data || data;
        const element = document.querySelector('[data-component="network-status"]');
        if (element) {
            element.innerHTML = `
                <div class="network-status-content">
                    <div class="status-item">
                        <span class="label">Block Height:</span>
                        <span class="value">${networkData.block_height || 'N/A'}</span>
                    </div>
                    <div class="status-item">
                        <span class="label">Network:</span>
                        <span class="value">${networkData.network || 'ithaca-1'}</span>
                    </div>
                    <div class="status-item">
                        <span class="label">Status:</span>
                        <span class="value success">Healthy</span>
                    </div>
                </div>
            `;
        }
    }

    async updateTokenMetrics(data) {
        const tokenData = data.data || data;
        const element = document.querySelector('[data-component="token-metrics"]');
        if (element) {
            element.innerHTML = `
                <div class="token-metrics-content">
                    <div class="metric-item">
                        <span class="label">Token Price:</span>
                        <span class="value">$${tokenData.token_price || '0.00'}</span>
                    </div>
                    <div class="metric-item">
                        <span class="label">Market Cap:</span>
                        <span class="value">$${tokenData.market_cap || '0'}</span>
                    </div>
                    <div class="metric-item">
                        <span class="label">24h Volume:</span>
                        <span class="value">$${tokenData.volume_24h || '0'}</span>
                    </div>
                </div>
            `;
        }
    }

    async updateStakingMetrics(data) {
        const stakingData = data.data || data;
        const element = document.querySelector('[data-component="staking-metrics"]');
        if (element) {
            element.innerHTML = `
                <div class="staking-metrics-content">
                    <div class="metric-item">
                        <span class="label">Staking APY:</span>
                        <span class="value">${stakingData.staking_apy || '0'}%</span>
                    </div>
                    <div class="metric-item">
                        <span class="label">Daily Rewards:</span>
                        <span class="value">${stakingData.daily_rewards || '0'} ODIS</span>
                    </div>
                    <div class="metric-item">
                        <span class="label">Validators:</span>
                        <span class="value">${stakingData.validator_count || '0'}</span>
                    </div>
                </div>
            `;
        }
    }

    retryComponent(id) {
        // Find and retry the specific component
        const componentConfig = {
            'network-status': { endpoint: '/api/rpc/network-status', handler: this.updateNetworkStatus.bind(this) },
            'token-metrics': { endpoint: '/api/orchestrator/token-metrics', handler: this.updateTokenMetrics.bind(this) },
            'staking-metrics': { endpoint: '/api/orchestrator/staking-metrics', handler: this.updateStakingMetrics.bind(this) }
        };

        const config = componentConfig[id];
        if (config) {
            this.loadComponent({ id, ...config });
        }
    }
}

// Global dashboard manager
window.dashboardManager = new DashboardManager();

// Enhanced CSS for error states
const dashboardStyles = `
<style>
.loading-state, .error-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 120px;
    padding: 20px;
    text-align: center;
}

.spinner {
    width: 30px;
    height: 30px;
    border: 3px solid rgba(255, 255, 255, 0.1);
    border-left: 3px solid #007bff;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 12px;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.loading-text {
    color: rgba(255, 255, 255, 0.7);
    font-size: 14px;
}

.error-state {
    background: rgba(255, 107, 107, 0.1);
    border: 1px dashed rgba(255, 107, 107, 0.3);
    border-radius: 8px;
}

.error-state.rate-limit {
    background: rgba(255, 165, 0, 0.1);
    border-color: rgba(255, 165, 0, 0.3);
}

.error-icon {
    font-size: 24px;
    margin-bottom: 8px;
}

.error-message {
    color: #ff6b6b;
    font-size: 14px;
    margin-bottom: 12px;
}

.retry-info {
    color: rgba(255, 255, 255, 0.6);
    font-size: 12px;
}

.retry-btn {
    padding: 6px 12px;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 12px;
}

.retry-btn:hover {
    background: #0056b3;
}

.success-state {
    border: 1px solid rgba(40, 167, 69, 0.3);
    background: rgba(40, 167, 69, 0.05);
}

.metric-item, .status-item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
    padding: 4px 0;
}

.label {
    color: rgba(255, 255, 255, 0.7);
    font-size: 14px;
}

.value {
    color: #ffffff;
    font-weight: 500;
    font-size: 14px;
}

.value.success {
    color: #28a745;
}
</style>
`;

// Inject styles
document.head.insertAdjacentHTML('beforeend', dashboardStyles);

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        window.dashboardManager.initialize();
    }, 1000);
});

console.log('DAODISEO Dashboard Manager loaded with enhanced error handling');