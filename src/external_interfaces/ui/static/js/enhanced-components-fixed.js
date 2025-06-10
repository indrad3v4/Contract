/**
 * Enhanced Components - Clean Implementation without conflicts
 */
(function() {
    'use strict';
    
    // Only initialize if not already done
    if (window.DAODISEO_ENHANCED_LOADED) {
        return;
    }
    window.DAODISEO_ENHANCED_LOADED = true;
    
    // Enhanced Stats Cards
    class EnhancedStatsCardsFixed {
        constructor() {
            this.rpcEndpoint = 'https://testnet-rpc.daodiseo.chaintools.tech';
            this.updateInterval = 30000;
            this.aiEnabled = false;
            this.init();
        }

        async init() {
            await this.checkAIAvailability();
            await this.loadRealData();
            this.startAutoUpdate();
        }

        async checkAIAvailability() {
            try {
                const response = await fetch('/api/bim-agent/enhanced-status');
                const data = await response.json();
                this.aiEnabled = data.success && data.enhanced_mode;
            } catch (error) {
                console.warn('AI Assistant not available for stats enhancement');
                this.aiEnabled = false;
            }
        }

        async loadRealData() {
            try {
                const response = await fetch('/api/blockchain/stats');
                const data = await response.json();
                
                if (data && !data.error) {
                    this.updateStatsDisplay(data);
                }
            } catch (error) {
                console.error('Failed to load blockchain stats:', error);
            }
        }

        updateStatsDisplay(data) {
            const elements = {
                totalValue: document.getElementById('total-value'),
                activeContracts: document.getElementById('active-contracts'),
                stakingRewards: document.getElementById('staking-rewards'),
                networkHealth: document.getElementById('network-health')
            };

            if (elements.totalValue && data.total_supply) {
                elements.totalValue.textContent = this.formatNumber(data.total_supply);
            }
            
            if (elements.activeContracts && data.validators_count) {
                elements.activeContracts.textContent = data.validators_count;
            }
            
            if (elements.stakingRewards && data.bonded_tokens) {
                elements.stakingRewards.textContent = this.formatNumber(data.bonded_tokens);
            }
            
            if (elements.networkHealth) {
                elements.networkHealth.textContent = data.block_height ? 'Active' : 'Loading';
            }
        }

        formatNumber(num) {
            if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B';
            if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M';
            if (num >= 1e3) return (num / 1e3).toFixed(2) + 'K';
            return num.toString();
        }

        startAutoUpdate() {
            setInterval(() => {
                this.loadRealData();
            }, this.updateInterval);
        }
    }

    // Enhanced Transaction List
    class EnhancedTransactionListFixed {
        constructor() {
            this.apiEndpoint = '/api/blockchain/recent-transactions';
            this.maxTransactions = 10;
            this.init();
        }

        async init() {
            await this.loadTransactions();
            this.setupAutoRefresh();
        }

        async loadTransactions() {
            try {
                const response = await fetch(this.apiEndpoint);
                const data = await response.json();
                
                if (data && data.transactions) {
                    this.renderTransactions(data.transactions);
                }
            } catch (error) {
                console.error('Failed to load transactions:', error);
            }
        }

        renderTransactions(transactions) {
            const container = document.getElementById('transaction-list');
            if (!container) return;

            container.innerHTML = transactions.slice(0, this.maxTransactions).map(tx => `
                <div class="transaction-item" data-tx-hash="${tx.hash}">
                    <div class="tx-info">
                        <span class="tx-type">${tx.type}</span>
                        <span class="tx-amount">${tx.amount} ODIS</span>
                    </div>
                    <div class="tx-meta">
                        <span class="tx-time">${this.formatTime(tx.timestamp)}</span>
                        <span class="tx-status ${tx.status}">${tx.status}</span>
                    </div>
                </div>
            `).join('');
        }

        formatTime(timestamp) {
            return new Date(timestamp).toLocaleTimeString();
        }

        setupAutoRefresh() {
            setInterval(() => {
                this.loadTransactions();
            }, 15000);
        }
    }

    // Enhanced Asset Distribution
    class EnhancedAssetDistributionFixed {
        constructor() {
            this.chartContainer = document.getElementById('asset-distribution-chart');
            this.init();
        }

        async init() {
            if (!this.chartContainer) return;
            
            await this.loadAssetData();
            this.setupChart();
        }

        async loadAssetData() {
            try {
                const response = await fetch('/api/blockchain/asset-distribution');
                const data = await response.json();
                
                if (data && data.distribution) {
                    this.assetData = data.distribution;
                }
            } catch (error) {
                console.error('Failed to load asset distribution:', error);
                this.assetData = [];
            }
        }

        setupChart() {
            if (!this.assetData || this.assetData.length === 0) return;

            // Simple canvas-based pie chart
            const canvas = document.createElement('canvas');
            canvas.width = 300;
            canvas.height = 300;
            this.chartContainer.innerHTML = '';
            this.chartContainer.appendChild(canvas);

            const ctx = canvas.getContext('2d');
            this.drawPieChart(ctx, this.assetData);
        }

        drawPieChart(ctx, data) {
            const centerX = 150;
            const centerY = 150;
            const radius = 120;
            let currentAngle = 0;

            const colors = ['#6366f1', '#a855f7', '#ec4899', '#10b981', '#f59e0b'];

            data.forEach((item, index) => {
                const sliceAngle = (item.percentage / 100) * 2 * Math.PI;
                
                ctx.beginPath();
                ctx.moveTo(centerX, centerY);
                ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle);
                ctx.closePath();
                ctx.fillStyle = colors[index % colors.length];
                ctx.fill();
                
                currentAngle += sliceAngle;
            });
        }
    }

    // Initialize components when DOM is ready
    function initializeEnhancedComponents() {
        try {
            new EnhancedStatsCardsFixed();
            new EnhancedTransactionListFixed();
            new EnhancedAssetDistributionFixed();
            console.log('Enhanced components initialized successfully');
        } catch (error) {
            console.error('Failed to initialize enhanced components:', error);
        }
    }

    // Initialize
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeEnhancedComponents);
    } else {
        initializeEnhancedComponents();
    }

})();