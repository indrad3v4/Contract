/**
 * DAODISEO AI Brain Orchestrator
 * Global state management and cross-route synchronization
 * Matches the system architecture with AI Brain as central orchestrator
 */

class DaodiseoOrchestrator {
    constructor() {
        this.initialized = false;
        this.eventListeners = new Map();
        this.stateCache = new Map();
        this.syncInterval = null;
        
        // Central AI Core state
        this.aiCore = {
            predictiveInsights: [],
            optimizationRecommendations: [],
            riskAssessment: {},
            neuralConnections: []
        };
        
        // Shared state across all routes
        this.sharedState = {
            wallet: {
                connected: false,
                address: null,
                balance: 0,
                provider: null
            },
            assets: {
                verified: [],
                pending: [],
                totalValue: 0,
                lastUpdate: null
            },
            contracts: {
                active: [],
                pending: [],
                completed: [],
                lastUpdate: null
            },
            transactions: {
                recent: [],
                status: {},
                lastUpdate: null
            },
            blockchain: {
                validators: [],
                networkStats: {},
                tokenPrice: 0,
                stakingInfo: {},
                lastUpdate: null
            }
        };
        
        this.init();
    }
    
    init() {
        if (this.initialized) return;
        
        // Load persistent state from sessionStorage
        this.loadPersistedState();
        
        // Set up cross-route communication
        this.setupCrossRouteSync();
        
        // Start periodic data synchronization
        this.startPeriodicSync();
        
        // Set up event listeners
        this.setupEventListeners();
        
        this.initialized = true;
        this.emit('orchestrator:initialized', this.sharedState);
    }
    
    // Load state from sessionStorage for persistence across navigation
    loadPersistedState() {
        try {
            const persistedWallet = sessionStorage.getItem('daodiseo_wallet_state');
            if (persistedWallet) {
                this.sharedState.wallet = { ...this.sharedState.wallet, ...JSON.parse(persistedWallet) };
            }
            
            const persistedAssets = sessionStorage.getItem('daodiseo_assets_state');
            if (persistedAssets) {
                this.sharedState.assets = { ...this.sharedState.assets, ...JSON.parse(persistedAssets) };
            }
            
            const persistedContracts = sessionStorage.getItem('daodiseo_contracts_state');
            if (persistedContracts) {
                this.sharedState.contracts = { ...this.sharedState.contracts, ...JSON.parse(persistedContracts) };
            }
            
            const persistedTransactions = sessionStorage.getItem('daodiseo_transactions_state');
            if (persistedTransactions) {
                this.sharedState.transactions = { ...this.sharedState.transactions, ...JSON.parse(persistedTransactions) };
            }
        } catch (error) {
            console.warn('Failed to load persisted state:', error);
        }
    }
    
    // Persist critical state to sessionStorage
    persistState(stateKey = null) {
        try {
            if (stateKey) {
                sessionStorage.setItem(`daodiseo_${stateKey}_state`, JSON.stringify(this.sharedState[stateKey]));
            } else {
                // Persist all state
                Object.keys(this.sharedState).forEach(key => {
                    sessionStorage.setItem(`daodiseo_${key}_state`, JSON.stringify(this.sharedState[key]));
                });
            }
        } catch (error) {
            console.warn('Failed to persist state:', error);
        }
    }
    
    // Update shared state and notify all listeners
    updateState(stateKey, newData) {
        const oldState = { ...this.sharedState[stateKey] };
        this.sharedState[stateKey] = { ...oldState, ...newData, lastUpdate: Date.now() };
        
        // Persist updated state
        this.persistState(stateKey);
        
        // Emit change event
        this.emit(`state:${stateKey}:updated`, this.sharedState[stateKey], oldState);
        this.emit('state:updated', { key: stateKey, data: this.sharedState[stateKey] });
        
        // Update AI insights based on state changes
        this.updateAIInsights(stateKey, this.sharedState[stateKey]);
    }
    
    // Get current state
    getState(stateKey = null) {
        return stateKey ? this.sharedState[stateKey] : this.sharedState;
    }
    
    // Event system for cross-component communication
    on(event, callback) {
        if (!this.eventListeners.has(event)) {
            this.eventListeners.set(event, []);
        }
        this.eventListeners.get(event).push(callback);
    }
    
    off(event, callback) {
        if (this.eventListeners.has(event)) {
            const listeners = this.eventListeners.get(event);
            const index = listeners.indexOf(callback);
            if (index > -1) {
                listeners.splice(index, 1);
            }
        }
    }
    
    emit(event, ...args) {
        if (this.eventListeners.has(event)) {
            this.eventListeners.get(event).forEach(callback => {
                try {
                    callback(...args);
                } catch (error) {
                    console.error(`Error in event listener for ${event}:`, error);
                }
            });
        }
    }
    
    // Cross-route synchronization
    setupCrossRouteSync() {
        // Listen for storage events from other tabs/windows
        window.addEventListener('storage', (e) => {
            if (e.key && e.key.startsWith('daodiseo_') && e.newValue) {
                try {
                    const stateKey = e.key.replace('daodiseo_', '').replace('_state', '');
                    const newData = JSON.parse(e.newValue);
                    this.sharedState[stateKey] = newData;
                    this.emit(`state:${stateKey}:synced`, newData);
                } catch (error) {
                    console.warn('Failed to sync cross-route state:', error);
                }
            }
        });
        
        // Listen for browser navigation
        window.addEventListener('beforeunload', () => {
            this.persistState();
        });
        
        // Page visibility API for background sync
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                this.refreshAllData();
            }
        });
    }
    
    // Periodic data synchronization
    startPeriodicSync() {
        // Sync every 10 seconds for real-time data
        this.syncInterval = setInterval(() => {
            this.refreshCriticalData();
        }, 10000);
        
        // Initial data load
        this.refreshAllData();
    }
    
    stopPeriodicSync() {
        if (this.syncInterval) {
            clearInterval(this.syncInterval);
            this.syncInterval = null;
        }
    }
    
    // Refresh all data from APIs
    async refreshAllData() {
        const promises = [
            this.refreshBlockchainData(),
            this.refreshAssetsData(),
            this.refreshContractsData(),
            this.refreshTransactionsData()
        ];
        
        try {
            await Promise.allSettled(promises);
            this.emit('data:refresh:complete');
        } catch (error) {
            console.error('Failed to refresh all data:', error);
            this.emit('data:refresh:error', error);
        }
    }
    
    // Refresh only critical real-time data
    async refreshCriticalData() {
        try {
            await Promise.allSettled([
                this.refreshTokenPrice(),
                this.refreshWalletBalance(),
                this.refreshNetworkStats()
            ]);
        } catch (error) {
            console.warn('Failed to refresh critical data:', error);
        }
    }
    
    // Individual data refresh methods
    async refreshBlockchainData() {
        try {
            const response = await fetch('/api/blockchain/stats');
            if (response.ok) {
                const data = await response.json();
                this.updateState('blockchain', {
                    validators: data.validators || [],
                    networkStats: data.network_stats || {},
                    tokenPrice: data.token_price || 0,
                    stakingInfo: data.staking_info || {}
                });
            }
        } catch (error) {
            console.warn('Failed to refresh blockchain data:', error);
        }
    }
    
    async refreshAssetsData() {
        try {
            const response = await fetch('/api/assets/summary');
            if (response.ok) {
                const data = await response.json();
                this.updateState('assets', {
                    verified: data.verified || [],
                    pending: data.pending || [],
                    totalValue: data.total_value || 0
                });
            }
        } catch (error) {
            console.warn('Failed to refresh assets data:', error);
        }
    }
    
    async refreshContractsData() {
        try {
            const response = await fetch('/api/contracts/summary');
            if (response.ok) {
                const data = await response.json();
                this.updateState('contracts', {
                    active: data.active || [],
                    pending: data.pending || [],
                    completed: data.completed || []
                });
            }
        } catch (error) {
            console.warn('Failed to refresh contracts data:', error);
        }
    }
    
    async refreshTransactionsData() {
        try {
            const response = await fetch('/api/transactions/recent');
            if (response.ok) {
                const data = await response.json();
                this.updateState('transactions', {
                    recent: data.transactions || [],
                    status: data.status || {}
                });
            }
        } catch (error) {
            console.warn('Failed to refresh transactions data:', error);
        }
    }
    
    async refreshTokenPrice() {
        try {
            const response = await fetch('/api/blockchain/token-price');
            if (response.ok) {
                const data = await response.json();
                this.updateState('blockchain', { tokenPrice: data.price || 0 });
            }
        } catch (error) {
            console.warn('Failed to refresh token price:', error);
        }
    }
    
    async refreshWalletBalance() {
        if (this.sharedState.wallet.connected && this.sharedState.wallet.address) {
            try {
                const response = await fetch(`/api/account/${this.sharedState.wallet.address}/balance`);
                if (response.ok) {
                    const data = await response.json();
                    this.updateState('wallet', { balance: data.balance || 0 });
                }
            } catch (error) {
                console.warn('Failed to refresh wallet balance:', error);
            }
        }
    }
    
    async refreshNetworkStats() {
        try {
            const response = await fetch('/api/blockchain/network-stats');
            if (response.ok) {
                const data = await response.json();
                this.updateState('blockchain', { networkStats: data });
            }
        } catch (error) {
            console.warn('Failed to refresh network stats:', error);
        }
    }
    
    // AI insights and recommendations
    updateAIInsights(stateKey, stateData) {
        // Generate AI insights based on state changes
        switch (stateKey) {
            case 'assets':
                this.generateAssetInsights(stateData);
                break;
            case 'contracts':
                this.generateContractInsights(stateData);
                break;
            case 'transactions':
                this.generateTransactionInsights(stateData);
                break;
            case 'blockchain':
                this.generateBlockchainInsights(stateData);
                break;
        }
    }
    
    generateAssetInsights(assetsData) {
        const insights = [];
        
        if (assetsData.pending && assetsData.pending.length > 0) {
            insights.push({
                type: 'asset_pending',
                priority: 'medium',
                message: `${assetsData.pending.length} assets pending verification`,
                action: 'Review pending assets',
                route: '/upload'
            });
        }
        
        if (assetsData.totalValue > 1000000) {
            insights.push({
                type: 'portfolio_milestone',
                priority: 'high',
                message: 'Portfolio exceeds $1M threshold',
                action: 'Consider diversification strategies',
                route: '/dashboard'
            });
        }
        
        this.aiCore.predictiveInsights = this.aiCore.predictiveInsights
            .filter(insight => insight.type !== 'asset_pending' && insight.type !== 'portfolio_milestone')
            .concat(insights);
            
        this.emit('ai:insights:updated', this.aiCore.predictiveInsights);
    }
    
    generateContractInsights(contractsData) {
        const insights = [];
        
        if (contractsData.pending && contractsData.pending.length > 0) {
            insights.push({
                type: 'contract_action_required',
                priority: 'high',
                message: `${contractsData.pending.length} contracts require signature`,
                action: 'Sign pending contracts',
                route: '/contracts'
            });
        }
        
        this.aiCore.predictiveInsights = this.aiCore.predictiveInsights
            .filter(insight => insight.type !== 'contract_action_required')
            .concat(insights);
            
        this.emit('ai:insights:updated', this.aiCore.predictiveInsights);
    }
    
    generateTransactionInsights(transactionsData) {
        const insights = [];
        
        if (transactionsData.recent && transactionsData.recent.length > 10) {
            insights.push({
                type: 'high_activity',
                priority: 'medium',
                message: 'High transaction activity detected',
                action: 'Monitor gas fees and timing',
                route: '/dashboard'
            });
        }
        
        this.aiCore.predictiveInsights = this.aiCore.predictiveInsights
            .filter(insight => insight.type !== 'high_activity')
            .concat(insights);
            
        this.emit('ai:insights:updated', this.aiCore.predictiveInsights);
    }
    
    generateBlockchainInsights(blockchainData) {
        const insights = [];
        
        if (blockchainData.stakingInfo && blockchainData.stakingInfo.apy > 10) {
            insights.push({
                type: 'staking_opportunity',
                priority: 'medium',
                message: `High staking APY: ${blockchainData.stakingInfo.apy}%`,
                action: 'Consider increasing stake',
                route: '/dashboard'
            });
        }
        
        this.aiCore.predictiveInsights = this.aiCore.predictiveInsights
            .filter(insight => insight.type !== 'staking_opportunity')
            .concat(insights);
            
        this.emit('ai:insights:updated', this.aiCore.predictiveInsights);
    }
    
    // Wallet connection management
    async connectWallet(address, provider = 'keplr') {
        this.updateState('wallet', {
            connected: true,
            address: address,
            provider: provider
        });
        
        // Refresh wallet-specific data
        await this.refreshWalletBalance();
        
        this.emit('wallet:connected', this.sharedState.wallet);
    }
    
    disconnectWallet() {
        this.updateState('wallet', {
            connected: false,
            address: null,
            balance: 0,
            provider: null
        });
        
        this.emit('wallet:disconnected');
    }
    
    // Route-specific state helpers
    getDashboardData() {
        return {
            portfolio: {
                totalReserves: this.sharedState.assets.totalValue,
                verifiedAssets: this.sharedState.assets.verified.length,
                activeContracts: this.sharedState.contracts.active.length,
                dailyRewards: this.calculateDailyRewards()
            },
            tokenData: this.sharedState.blockchain,
            recentTransactions: this.sharedState.transactions.recent.slice(0, 5),
            aiInsights: this.aiCore.predictiveInsights
        };
    }
    
    getViewerData() {
        return {
            assets: this.sharedState.assets,
            selectedAsset: sessionStorage.getItem('selected_asset'),
            viewerSettings: JSON.parse(sessionStorage.getItem('viewer_settings') || '{}')
        };
    }
    
    getUploadData() {
        return {
            uploadProgress: JSON.parse(sessionStorage.getItem('upload_progress') || '{}'),
            pendingAssets: this.sharedState.assets.pending
        };
    }
    
    getContractsData() {
        return {
            contracts: this.sharedState.contracts,
            wallet: this.sharedState.wallet,
            recentTransactions: this.sharedState.transactions.recent
        };
    }
    
    // Utility methods
    calculateDailyRewards() {
        const { stakingInfo, tokenPrice } = this.sharedState.blockchain;
        const { balance } = this.sharedState.wallet;
        
        if (stakingInfo.apy && balance && tokenPrice) {
            return (balance * (stakingInfo.apy / 100) / 365).toFixed(3);
        }
        return '0.000';
    }
    
    // Setup event listeners for UI updates
    setupEventListeners() {
        // Listen for wallet connection events
        this.on('wallet:connected', (walletData) => {
            this.updateWalletUI(walletData);
        });
        
        this.on('wallet:disconnected', () => {
            this.updateWalletUI({ connected: false });
        });
        
        // Listen for AI insights updates
        this.on('ai:insights:updated', (insights) => {
            this.updateAIInsightsUI(insights);
        });
        
        // Listen for state updates
        this.on('state:updated', ({ key, data }) => {
            this.updateStateIndicators(key, data);
        });
    }
    
    updateWalletUI(walletData) {
        const walletBtns = document.querySelectorAll('[id*="wallet"], [id*="keplr"]');
        walletBtns.forEach(btn => {
            if (walletData.connected) {
                btn.textContent = `Connected: ${walletData.address.substring(0, 8)}...`;
                btn.className = btn.className.replace('btn-outline-info', 'btn-success');
            } else {
                btn.textContent = 'Connect Wallet';
                btn.className = btn.className.replace('btn-success', 'btn-outline-info');
            }
        });
    }
    
    updateAIInsightsUI(insights) {
        const insightsContainer = document.getElementById('ai-insights-container');
        if (insightsContainer) {
            insightsContainer.innerHTML = insights.map(insight => `
                <div class="status-ribbon ${insight.priority}">
                    <span>${insight.message}</span>
                    <a href="${insight.route}" class="btn btn-sm btn-outline-light">${insight.action}</a>
                </div>
            `).join('');
        }
    }
    
    updateStateIndicators(stateKey, data) {
        const indicator = document.querySelector('.state-sync-indicator');
        if (indicator) {
            indicator.className = 'state-sync-indicator synced';
            indicator.textContent = `${stateKey} synced`;
            
            setTimeout(() => {
                indicator.textContent = 'All systems synced';
            }, 2000);
        }
    }
    
    // Cleanup
    destroy() {
        this.stopPeriodicSync();
        this.eventListeners.clear();
        this.stateCache.clear();
        
        // Remove event listeners
        window.removeEventListener('storage', this.handleStorageChange);
        window.removeEventListener('beforeunload', this.handleBeforeUnload);
        document.removeEventListener('visibilitychange', this.handleVisibilityChange);
        
        this.initialized = false;
    }
}

// Global instance
window.DaodiseoOrchestrator = new DaodiseoOrchestrator();

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DaodiseoOrchestrator;
}