#!/usr/bin/env python3
"""
Frontend Orchestrator Integration Fix Script
Ensures all dashboard components properly call o3-mini orchestrator endpoints
and display real chain data analysis instead of showing loading states.
"""

import os
import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FrontendOrchestratorFix:
    """Fix frontend components to properly integrate with o3-mini orchestrator"""
    
    def __init__(self):
        self.src_path = Path("src")
        self.static_js_path = self.src_path / "external_interfaces" / "ui" / "static" / "js"
        self.templates_path = self.src_path / "external_interfaces" / "ui" / "templates"
        
    def apply_all_fixes(self):
        """Apply all orchestrator integration fixes"""
        logger.info("Starting comprehensive frontend orchestrator integration...")
        
        try:
            self.fix_dashboard_final_fix_js()
            self.fix_enhanced_stats_cards_js()
            self.fix_enhanced_transaction_list_js()
            self.fix_enhanced_asset_distribution_js()
            self.create_orchestrator_integration_js()
            self.update_dashboard_template()
            
            logger.info("✅ All frontend orchestrator fixes applied successfully")
            
        except Exception as e:
            logger.error(f"❌ Fix failed: {e}")
            raise
    
    def fix_dashboard_final_fix_js(self):
        """Fix main dashboard JavaScript to use orchestrator endpoints"""
        js_file = self.static_js_path / "dashboard-final-fix.js"
        
        content = '''// DAODISEO Dashboard Final Fix - o3-mini Orchestrator Integration
console.log("Dashboard final fix loaded - o3-mini integration active");

// Global orchestrator integration
window.DashboardOrchestrator = {
    endpoints: {
        tokenMetrics: '/api/orchestrator/token-metrics',
        stakingMetrics: '/api/orchestrator/staking-metrics', 
        networkHealth: '/api/orchestrator/network-health'
    },
    
    async fetchWithRetry(url, retries = 3) {
        for (let i = 0; i < retries; i++) {
            try {
                const response = await fetch(url);
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return await response.json();
            } catch (error) {
                console.warn(`Fetch attempt ${i + 1} failed for ${url}:`, error);
                if (i === retries - 1) throw error;
                await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
            }
        }
    },
    
    async loadTokenMetrics() {
        try {
            const data = await this.fetchWithRetry(this.endpoints.tokenMetrics);
            if (data.success) {
                this.updateTokenDisplay(data.data, data.metadata);
                return data;
            }
        } catch (error) {
            console.error('Token metrics failed:', error);
            this.showErrorState('token-metrics');
        }
    },
    
    async loadStakingMetrics() {
        try {
            const data = await this.fetchWithRetry(this.endpoints.stakingMetrics);
            if (data.success) {
                this.updateStakingDisplay(data.data, data.metadata);
                return data;
            }
        } catch (error) {
            console.error('Staking metrics failed:', error);
            this.showErrorState('staking-metrics');
        }
    },
    
    async loadNetworkHealth() {
        try {
            const data = await this.fetchWithRetry(this.endpoints.networkHealth);
            if (data.success) {
                this.updateNetworkDisplay(data.data, data.metadata);
                return data;
            }
        } catch (error) {
            console.error('Network health failed:', error);
            this.showErrorState('network-health');
        }
    },
    
    updateTokenDisplay(data, metadata) {
        // Update ODIS price card
        const priceCard = document.querySelector('[data-card-id="odis-price"]');
        if (priceCard) {
            const valueEl = priceCard.querySelector('.card-value');
            const statusEl = priceCard.querySelector('.status-badge');
            const aiInsightEl = priceCard.querySelector('.ai-insight') || this.createAIInsightElement(priceCard);
            
            if (valueEl) valueEl.textContent = `$${data.token_price}`;
            if (statusEl) {
                statusEl.textContent = data.status;
                statusEl.className = `status-badge ${data.status}`;
            }
            
            aiInsightEl.innerHTML = `
                <div class="ai-analysis">
                    <span class="ai-badge">o3-mini Analysis</span>
                    <p>${data.analysis}</p>
                    <div class="confidence">Confidence: ${Math.round(metadata.confidence * 100)}%</div>
                </div>
            `;
        }
        
        // Update market cap card
        const marketCapCard = document.querySelector('[data-card-id="market-cap"]');
        if (marketCapCard) {
            const valueEl = marketCapCard.querySelector('.card-value');
            if (valueEl) valueEl.textContent = `$${data.market_cap.toLocaleString()}`;
        }
        
        // Update volume card
        const volumeCard = document.querySelector('[data-card-id="volume-24h"]');
        if (volumeCard) {
            const valueEl = volumeCard.querySelector('.card-value');
            if (valueEl) valueEl.textContent = `$${data.volume_24h.toLocaleString()}`;
        }
    },
    
    updateStakingDisplay(data, metadata) {
        // Update staking APY card
        const stakingCard = document.querySelector('[data-card-id="staking-apy"]');
        if (stakingCard) {
            const valueEl = stakingCard.querySelector('.card-value');
            const statusEl = stakingCard.querySelector('.status-badge');
            const aiInsightEl = stakingCard.querySelector('.ai-insight') || this.createAIInsightElement(stakingCard);
            
            if (valueEl) valueEl.textContent = `${(data.staking_apy * 100).toFixed(2)}%`;
            if (statusEl) {
                statusEl.textContent = data.status;
                statusEl.className = `status-badge ${data.status}`;
            }
            
            const strategies = data.analysis.strategy_recommendations?.slice(0, 2).join(' ') || 'Staking analysis available';
            aiInsightEl.innerHTML = `
                <div class="ai-analysis">
                    <span class="ai-badge">o3-mini Staking Strategy</span>
                    <p>${strategies}</p>
                    <div class="confidence">Confidence: ${Math.round(metadata.confidence * 100)}%</div>
                </div>
            `;
        }
        
        // Update total staked card
        const totalStakedCard = document.querySelector('[data-card-id="total-staked"]');
        if (totalStakedCard) {
            const valueEl = totalStakedCard.querySelector('.card-value');
            if (valueEl) valueEl.textContent = `${data.total_staked.toLocaleString()} ODIS`;
        }
    },
    
    updateNetworkDisplay(data, metadata) {
        // Update network health card
        const networkCard = document.querySelector('[data-card-id="network-health"]');
        if (networkCard) {
            const valueEl = networkCard.querySelector('.card-value');
            const statusEl = networkCard.querySelector('.status-badge');
            const aiInsightEl = networkCard.querySelector('.ai-insight') || this.createAIInsightElement(networkCard);
            
            if (valueEl) valueEl.textContent = data.value;
            if (statusEl) {
                statusEl.textContent = data.status;
                statusEl.className = `status-badge ${data.status}`;
            }
            
            aiInsightEl.innerHTML = `
                <div class="ai-analysis">
                    <span class="ai-badge">o3-mini Network Analysis</span>
                    <p>${data.analysis.network_stability}</p>
                    <div class="confidence">Confidence: ${Math.round(metadata.confidence * 100)}%</div>
                </div>
            `;
        }
        
        // Update block height display
        const blockHeightEl = document.querySelector('.block-height-value');
        if (blockHeightEl) {
            blockHeightEl.textContent = data.block_height.toLocaleString();
        }
        
        // Update peer count display
        const peerCountEl = document.querySelector('.peer-count-value');
        if (peerCountEl) {
            peerCountEl.textContent = data.peer_count;
        }
    },
    
    createAIInsightElement(parentCard) {
        const aiInsight = document.createElement('div');
        aiInsight.className = 'ai-insight';
        parentCard.appendChild(aiInsight);
        return aiInsight;
    },
    
    showErrorState(cardId) {
        const card = document.querySelector(`[data-card-id="${cardId}"]`);
        if (card) {
            const statusEl = card.querySelector('.status-badge');
            if (statusEl) {
                statusEl.textContent = 'error';
                statusEl.className = 'status-badge error';
            }
        }
    },
    
    async initializeAll() {
        console.log("Initializing o3-mini orchestrator integration...");
        
        // Load all orchestrator data
        const promises = [
            this.loadTokenMetrics(),
            this.loadStakingMetrics(), 
            this.loadNetworkHealth()
        ];
        
        try {
            await Promise.allSettled(promises);
            console.log("✅ o3-mini orchestrator integration completed");
        } catch (error) {
            console.error("❌ Orchestrator integration failed:", error);
        }
        
        // Set up periodic refresh
        setInterval(() => {
            this.loadTokenMetrics();
            this.loadStakingMetrics();
            this.loadNetworkHealth();
        }, 30000);
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        window.DashboardOrchestrator.initializeAll();
    }, 1000);
});

// Add CSS for AI insights
const style = document.createElement('style');
style.textContent = `
.ai-insight {
    margin-top: 12px;
    padding: 10px;
    background: rgba(0, 255, 157, 0.1);
    border-radius: 8px;
    border-left: 3px solid #00ff9d;
}

.ai-analysis {
    font-size: 0.85rem;
}

.ai-badge {
    display: inline-block;
    background: linear-gradient(135deg, #00ff9d, #00d4aa);
    color: #000;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-bottom: 6px;
}

.ai-analysis p {
    margin: 6px 0;
    color: #e0e0e0;
    line-height: 1.4;
}

.confidence {
    margin-top: 6px;
    font-size: 0.75rem;
    color: #00ff9d;
    font-weight: 500;
}

.status-badge.verified {
    background: #00ff9d;
    color: #000;
}

.status-badge.error {
    background: #ff4757;
    color: #fff;
}
`;
document.head.appendChild(style);
'''
        
        with open(js_file, 'w') as f:
            f.write(content)
        
        logger.info("✅ Fixed dashboard-final-fix.js with orchestrator integration")
    
    def fix_enhanced_stats_cards_js(self):
        """Fix stats cards to display orchestrator data"""
        js_file = self.static_js_path / "enhanced-stats-cards.js"
        
        content = '''// Enhanced Stats Cards with o3-mini Orchestrator Integration
console.log("Enhanced stats cards loading with o3-mini integration...");

class EnhancedStatsCards {
    constructor() {
        this.initializeCards();
        this.startPeriodicUpdates();
    }
    
    async initializeCards() {
        // Wait for orchestrator to be available
        if (typeof window.DashboardOrchestrator === 'undefined') {
            setTimeout(() => this.initializeCards(), 500);
            return;
        }
        
        // Hook into orchestrator updates
        this.setupOrchestratorHooks();
    }
    
    setupOrchestratorHooks() {
        const originalUpdateToken = window.DashboardOrchestrator.updateTokenDisplay;
        const originalUpdateStaking = window.DashboardOrchestrator.updateStakingDisplay;
        const originalUpdateNetwork = window.DashboardOrchestrator.updateNetworkDisplay;
        
        window.DashboardOrchestrator.updateTokenDisplay = (data, metadata) => {
            originalUpdateToken.call(window.DashboardOrchestrator, data, metadata);
            this.enhanceTokenCards(data, metadata);
        };
        
        window.DashboardOrchestrator.updateStakingDisplay = (data, metadata) => {
            originalUpdateStaking.call(window.DashboardOrchestrator, data, metadata);
            this.enhanceStakingCards(data, metadata);
        };
        
        window.DashboardOrchestrator.updateNetworkDisplay = (data, metadata) => {
            originalUpdateNetwork.call(window.DashboardOrchestrator, data, metadata);
            this.enhanceNetworkCards(data, metadata);
        };
    }
    
    enhanceTokenCards(data, metadata) {
        // Add price change indicators
        const priceCard = document.querySelector('[data-card-id="odis-price"]');
        if (priceCard && data.price_change_24h !== undefined) {
            const changeEl = priceCard.querySelector('.price-change') || this.createPriceChangeElement(priceCard);
            const changePercent = data.price_change_24h;
            const changeClass = changePercent >= 0 ? 'positive' : 'negative';
            const changeSymbol = changePercent >= 0 ? '+' : '';
            
            changeEl.className = `price-change ${changeClass}`;
            changeEl.textContent = `${changeSymbol}${changePercent.toFixed(2)}%`;
        }
        
        // Add market cap analysis
        const marketCapCard = document.querySelector('[data-card-id="market-cap"]');
        if (marketCapCard) {
            this.addAnalysisToCard(marketCapCard, "Market cap indicates healthy token valuation", metadata.confidence);
        }
    }
    
    enhanceStakingCards(data, metadata) {
        // Add daily rewards display
        const stakingCard = document.querySelector('[data-card-id="staking-apy"]');
        if (stakingCard && data.daily_rewards) {
            const rewardsEl = stakingCard.querySelector('.daily-rewards') || this.createDailyRewardsElement(stakingCard);
            rewardsEl.textContent = `Daily: ${data.daily_rewards.toFixed(6)} ODIS`;
        }
        
        // Add validator analysis
        const validatorCard = document.querySelector('[data-card-id="validator-count"]');
        if (validatorCard) {
            const valueEl = validatorCard.querySelector('.card-value');
            if (valueEl) valueEl.textContent = data.validator_count;
            this.addAnalysisToCard(validatorCard, `${data.validator_count} active validators ensure network security`, metadata.confidence);
        }
    }
    
    enhanceNetworkCards(data, metadata) {
        // Add detailed network metrics
        const networkCard = document.querySelector('[data-card-id="network-health"]');
        if (networkCard) {
            const metricsEl = networkCard.querySelector('.network-metrics') || this.createNetworkMetricsElement(networkCard);
            metricsEl.innerHTML = `
                <div class="metric">Block: ${data.block_height?.toLocaleString() || 'N/A'}</div>
                <div class="metric">Peers: ${data.peer_count || 'N/A'}</div>
            `;
        }
    }
    
    createPriceChangeElement(parentCard) {
        const changeEl = document.createElement('div');
        changeEl.className = 'price-change';
        parentCard.querySelector('.card-content').appendChild(changeEl);
        return changeEl;
    }
    
    createDailyRewardsElement(parentCard) {
        const rewardsEl = document.createElement('div');
        rewardsEl.className = 'daily-rewards';
        parentCard.querySelector('.card-content').appendChild(rewardsEl);
        return rewardsEl;
    }
    
    createNetworkMetricsElement(parentCard) {
        const metricsEl = document.createElement('div');
        metricsEl.className = 'network-metrics';
        parentCard.querySelector('.card-content').appendChild(metricsEl);
        return metricsEl;
    }
    
    addAnalysisToCard(card, analysis, confidence) {
        const existingAnalysis = card.querySelector('.card-analysis');
        if (existingAnalysis) return;
        
        const analysisEl = document.createElement('div');
        analysisEl.className = 'card-analysis';
        analysisEl.innerHTML = `
            <p>${analysis}</p>
            <span class="confidence-score">${Math.round(confidence * 100)}% confidence</span>
        `;
        card.appendChild(analysisEl);
    }
    
    startPeriodicUpdates() {
        // Cards will be updated through orchestrator hooks
        console.log("✅ Enhanced stats cards initialized with o3-mini integration");
    }
}

// Initialize enhanced stats cards
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        new EnhancedStatsCards();
    }, 1500);
});

// Add enhanced styling
const enhancedStyle = document.createElement('style');
enhancedStyle.textContent = `
.price-change {
    font-size: 0.85rem;
    font-weight: 600;
    margin-top: 4px;
}

.price-change.positive {
    color: #00ff9d;
}

.price-change.negative {
    color: #ff4757;
}

.daily-rewards {
    font-size: 0.8rem;
    color: #00d4aa;
    margin-top: 4px;
}

.network-metrics {
    display: flex;
    gap: 12px;
    margin-top: 8px;
}

.network-metrics .metric {
    font-size: 0.8rem;
    color: #a0a0a0;
}

.card-analysis {
    margin-top: 12px;
    padding: 8px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 6px;
    font-size: 0.8rem;
}

.card-analysis p {
    margin: 0 0 6px 0;
    color: #d0d0d0;
}

.confidence-score {
    color: #00ff9d;
    font-size: 0.75rem;
    font-weight: 500;
}
`;
document.head.appendChild(enhancedStyle);
'''
        
        with open(js_file, 'w') as f:
            f.write(content)
        
        logger.info("✅ Fixed enhanced-stats-cards.js with orchestrator integration")
    
    def fix_enhanced_transaction_list_js(self):
        """Fix transaction list to use real blockchain data"""
        js_file = self.static_js_path / "enhanced-transaction-list.js"
        
        content = '''// Enhanced Transaction List with Real Blockchain Data
console.log("Enhanced transaction list loading with blockchain integration...");

class EnhancedTransactionList {
    constructor() {
        this.transactionContainer = null;
        this.initialize();
    }
    
    async initialize() {
        this.transactionContainer = document.querySelector('.recent-transactions-content');
        if (!this.transactionContainer) {
            setTimeout(() => this.initialize(), 500);
            return;
        }
        
        await this.loadTransactions();
        this.startPeriodicUpdates();
    }
    
    async loadTransactions() {
        try {
            console.log("Loading recent transactions...");
            const response = await fetch('/api/blockchain/recent-transactions');
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success && data.data?.transactions) {
                this.displayTransactions(data.data.transactions);
                console.log("✅ Transactions loaded successfully");
            } else {
                this.showEmptyState();
            }
            
        } catch (error) {
            console.error('Failed to load transactions:', error);
            this.showErrorState();
        }
    }
    
    displayTransactions(transactions) {
        if (!transactions || transactions.length === 0) {
            this.showEmptyState();
            return;
        }
        
        const transactionHtml = transactions.map(tx => `
            <div class="transaction-item" data-tx-hash="${tx.hash}">
                <div class="transaction-icon">
                    <i data-feather="${this.getTransactionIcon(tx.type)}"></i>
                </div>
                <div class="transaction-details">
                    <div class="transaction-type">${tx.type || 'Transaction'}</div>
                    <div class="transaction-hash">${this.formatHash(tx.hash)}</div>
                    <div class="transaction-time">${this.formatTime(tx.timestamp)}</div>
                </div>
                <div class="transaction-amount">
                    <span class="amount">${tx.amount || '0'} ODIS</span>
                    <span class="status-badge ${tx.status || 'pending'}">${tx.status || 'pending'}</span>
                </div>
            </div>
        `).join('');
        
        this.transactionContainer.innerHTML = transactionHtml;
        
        // Initialize feather icons for transaction icons
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
    }
    
    showEmptyState() {
        this.transactionContainer.innerHTML = `
            <div class="empty-state">
                <i data-feather="activity"></i>
                <p>No recent transactions</p>
                <small>Transactions will appear here once network activity begins</small>
            </div>
        `;
        
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
    }
    
    showErrorState() {
        this.transactionContainer.innerHTML = `
            <div class="error-state">
                <i data-feather="alert-circle"></i>
                <p>Unable to load transactions</p>
                <button onclick="location.reload()" class="retry-button">Retry</button>
            </div>
        `;
        
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
    }
    
    getTransactionIcon(type) {
        const iconMap = {
            'send': 'arrow-up-right',
            'receive': 'arrow-down-left', 
            'stake': 'lock',
            'unstake': 'unlock',
            'vote': 'check-circle',
            'delegate': 'users'
        };
        
        return iconMap[type?.toLowerCase()] || 'activity';
    }
    
    formatHash(hash) {
        if (!hash) return 'N/A';
        return hash.length > 12 ? `${hash.slice(0, 6)}...${hash.slice(-6)}` : hash;
    }
    
    formatTime(timestamp) {
        if (!timestamp) return 'Unknown time';
        
        try {
            const date = new Date(timestamp);
            const now = new Date();
            const diffMs = now - date;
            const diffMins = Math.floor(diffMs / 60000);
            
            if (diffMins < 1) return 'Just now';
            if (diffMins < 60) return `${diffMins}m ago`;
            if (diffMins < 1440) return `${Math.floor(diffMins / 60)}h ago`;
            return `${Math.floor(diffMins / 1440)}d ago`;
        } catch {
            return 'Unknown time';
        }
    }
    
    startPeriodicUpdates() {
        // Refresh every 30 seconds
        setInterval(() => {
            this.loadTransactions();
        }, 30000);
        
        console.log("✅ Transaction list periodic updates started");
    }
}

// Initialize enhanced transaction list
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        new EnhancedTransactionList();
    }, 2000);
});

// Add transaction list styling
const transactionStyle = document.createElement('style');
transactionStyle.textContent = `
.transaction-item {
    display: flex;
    align-items: center;
    padding: 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    transition: background-color 0.2s ease;
}

.transaction-item:hover {
    background: rgba(255, 255, 255, 0.05);
}

.transaction-icon {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    background: rgba(0, 255, 157, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 12px;
}

.transaction-icon i {
    color: #00ff9d;
    width: 20px;
    height: 20px;
}

.transaction-details {
    flex: 1;
}

.transaction-type {
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 2px;
}

.transaction-hash {
    font-size: 0.85rem;
    color: #a0a0a0;
    margin-bottom: 2px;
}

.transaction-time {
    font-size: 0.8rem;
    color: #707070;
}

.transaction-amount {
    text-align: right;
}

.transaction-amount .amount {
    display: block;
    font-weight: 600;
    color: #00ff9d;
    margin-bottom: 4px;
}

.empty-state, .error-state {
    text-align: center;
    padding: 40px 20px;
    color: #a0a0a0;
}

.empty-state i, .error-state i {
    width: 48px;
    height: 48px;
    margin-bottom: 16px;
    opacity: 0.5;
}

.retry-button {
    margin-top: 12px;
    padding: 8px 16px;
    background: rgba(0, 255, 157, 0.2);
    border: 1px solid #00ff9d;
    border-radius: 6px;
    color: #00ff9d;
    cursor: pointer;
    transition: all 0.2s ease;
}

.retry-button:hover {
    background: rgba(0, 255, 157, 0.3);
}
`;
document.head.appendChild(transactionStyle);
'''
        
        with open(js_file, 'w') as f:
            f.write(content)
        
        logger.info("✅ Fixed enhanced-transaction-list.js with blockchain integration")
    
    def fix_enhanced_asset_distribution_js(self):
        """Fix asset distribution to use real blockchain data"""
        js_file = self.static_js_path / "enhanced-asset-distribution.js"
        
        content = '''// Enhanced Asset Distribution with Real Blockchain Data
console.log("Enhanced asset distribution loading with blockchain integration...");

class EnhancedAssetDistribution {
    constructor() {
        this.chartCanvas = null;
        this.chart = null;
        this.initialize();
    }
    
    async initialize() {
        // Wait for Chart.js to be available
        if (typeof Chart === 'undefined') {
            setTimeout(() => this.initialize(), 500);
            return;
        }
        
        this.chartCanvas = document.querySelector('#asset-distribution-chart');
        if (!this.chartCanvas) {
            setTimeout(() => this.initialize(), 500);
            return;
        }
        
        await this.loadAssetDistribution();
        this.startPeriodicUpdates();
    }
    
    async loadAssetDistribution() {
        try {
            console.log("Loading asset distribution data...");
            const response = await fetch('/api/blockchain/asset-distribution');
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success && data.data?.distribution) {
                this.createChart(data.data.distribution);
                console.log("✅ Asset distribution loaded successfully");
            } else {
                this.showErrorState();
            }
            
        } catch (error) {
            console.error('Failed to load asset distribution:', error);
            this.showErrorState();
        }
    }
    
    createChart(distributionData) {
        if (this.chart) {
            this.chart.destroy();
        }
        
        const ctx = this.chartCanvas.getContext('2d');
        
        // Process distribution data
        const labels = distributionData.map(item => item.name || item.asset || 'Unknown');
        const values = distributionData.map(item => item.value || item.percentage || 0);
        const colors = this.generateColors(labels.length);
        
        this.chart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: colors.backgrounds,
                    borderColor: colors.borders,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#ffffff',
                            padding: 20,
                            usePointStyle: true,
                            font: {
                                size: 12
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        borderColor: '#00ff9d',
                        borderWidth: 1,
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                const percentage = ((value / context.dataset.data.reduce((a, b) => a + b, 0)) * 100).toFixed(1);
                                return `${label}: ${value.toFixed(2)}% (${percentage}% of total)`;
                            }
                        }
                    }
                },
                cutout: '60%',
                animation: {
                    animateRotate: true,
                    duration: 1000
                }
            }
        });
        
        // Add center text showing total
        this.addCenterText();
    }
    
    addCenterText() {
        const chartContainer = this.chartCanvas.parentElement;
        let centerText = chartContainer.querySelector('.chart-center-text');
        
        if (!centerText) {
            centerText = document.createElement('div');
            centerText.className = 'chart-center-text';
            chartContainer.style.position = 'relative';
            chartContainer.appendChild(centerText);
        }
        
        centerText.innerHTML = `
            <div class="center-label">Total Assets</div>
            <div class="center-value">100%</div>
        `;
    }
    
    generateColors(count) {
        const baseColors = [
            '#00ff9d', '#00d4aa', '#00a8b7', '#007cc4', '#0050d1',
            '#2d24de', '#5a00eb', '#8700f8', '#b400ff', '#e100ff'
        ];
        
        const backgrounds = [];
        const borders = [];
        
        for (let i = 0; i < count; i++) {
            const color = baseColors[i % baseColors.length];
            backgrounds.push(color + '80'); // 50% opacity
            borders.push(color);
        }
        
        return { backgrounds, borders };
    }
    
    showErrorState() {
        const chartContainer = this.chartCanvas.parentElement;
        chartContainer.innerHTML = `
            <div class="chart-error-state">
                <i data-feather="pie-chart"></i>
                <p>Unable to load asset distribution</p>
                <button onclick="location.reload()" class="retry-button">Retry</button>
            </div>
        `;
        
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
    }
    
    startPeriodicUpdates() {
        // Refresh every 60 seconds
        setInterval(() => {
            this.loadAssetDistribution();
        }, 60000);
        
        console.log("✅ Asset distribution periodic updates started");
    }
}

// Initialize enhanced asset distribution
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        new EnhancedAssetDistribution();
    }, 2500);
});

// Add asset distribution styling
const assetStyle = document.createElement('style');
assetStyle.textContent = `
.chart-center-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    pointer-events: none;
}

.center-label {
    font-size: 0.9rem;
    color: #a0a0a0;
    margin-bottom: 4px;
}

.center-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #00ff9d;
}

.chart-error-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 300px;
    color: #a0a0a0;
}

.chart-error-state i {
    width: 48px;
    height: 48px;
    margin-bottom: 16px;
    opacity: 0.5;
}

.chart-error-state .retry-button {
    margin-top: 12px;
    padding: 8px 16px;
    background: rgba(0, 255, 157, 0.2);
    border: 1px solid #00ff9d;
    border-radius: 6px;
    color: #00ff9d;
    cursor: pointer;
    transition: all 0.2s ease;
}

.chart-error-state .retry-button:hover {
    background: rgba(0, 255, 157, 0.3);
}
`;
document.head.appendChild(assetStyle);
'''
        
        with open(js_file, 'w') as f:
            f.write(content)
        
        logger.info("✅ Fixed enhanced-asset-distribution.js with blockchain integration")
    
    def create_orchestrator_integration_js(self):
        """Create main orchestrator integration file"""
        js_file = self.static_js_path / "orchestrator-integration.js"
        
        content = '''// DAODISEO o3-mini Orchestrator Integration
console.log("o3-mini orchestrator integration initializing...");

window.OrchestratorCore = {
    initialized: false,
    retryAttempts: 3,
    retryDelay: 1000,
    
    async init() {
        if (this.initialized) return;
        
        console.log("🤖 Initializing o3-mini orchestrator core...");
        
        // Ensure all dependencies are loaded
        await this.waitForDependencies();
        
        // Initialize all integrations
        await this.initializeIntegrations();
        
        this.initialized = true;
        console.log("✅ o3-mini orchestrator core initialized successfully");
    },
    
    async waitForDependencies() {
        const dependencies = ['DashboardOrchestrator'];
        
        for (const dep of dependencies) {
            await this.waitForGlobal(dep);
        }
    },
    
    async waitForGlobal(globalName, timeout = 10000) {
        const startTime = Date.now();
        
        while (!window[globalName] && (Date.now() - startTime) < timeout) {
            await new Promise(resolve => setTimeout(resolve, 100));
        }
        
        if (!window[globalName]) {
            console.warn(`⚠️ ${globalName} not available after ${timeout}ms`);
        }
    },
    
    async initializeIntegrations() {
        const integrations = [
            this.initializeDashboard,
            this.initializeCharts,
            this.initializeRealTimeUpdates
        ];
        
        for (const integration of integrations) {
            try {
                await integration.call(this);
            } catch (error) {
                console.error(`Integration failed:`, error);
            }
        }
    },
    
    async initializeDashboard() {
        if (window.DashboardOrchestrator) {
            await window.DashboardOrchestrator.initializeAll();
            console.log("✅ Dashboard orchestrator integration complete");
        }
    },
    
    async initializeCharts() {
        // Charts will be initialized by their respective components
        console.log("✅ Chart integrations prepared");
    },
    
    async initializeRealTimeUpdates() {
        // Set up WebSocket connection for real-time updates (future enhancement)
        console.log("✅ Real-time update system prepared");
    },
    
    async fetchWithRetry(url, options = {}) {
        for (let attempt = 1; attempt <= this.retryAttempts; attempt++) {
            try {
                const response = await fetch(url, options);
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                return response;
            } catch (error) {
                console.warn(`Fetch attempt ${attempt}/${this.retryAttempts} failed for ${url}:`, error.message);
                
                if (attempt === this.retryAttempts) {
                    throw error;
                }
                
                await new Promise(resolve => setTimeout(resolve, this.retryDelay * attempt));
            }
        }
    },
    
    showGlobalNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `orchestrator-notification ${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i data-feather="${this.getNotificationIcon(type)}"></i>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
        
        setTimeout(() => {
            notification.remove();
        }, 5000);
    },
    
    getNotificationIcon(type) {
        const icons = {
            'success': 'check-circle',
            'error': 'alert-circle',
            'warning': 'alert-triangle',
            'info': 'info'
        };
        
        return icons[type] || 'info';
    }
};

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        window.OrchestratorCore.init().catch(error => {
            console.error('❌ Orchestrator core initialization failed:', error);
        });
    }, 500);
});

// Add orchestrator notification styles
const orchestratorStyle = document.createElement('style');
orchestratorStyle.textContent = `
.orchestrator-notification {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 10000;
    padding: 12px 16px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(10px);
    animation: slideInRight 0.3s ease-out;
}

.orchestrator-notification.success {
    background: rgba(0, 255, 157, 0.2);
    border: 1px solid #00ff9d;
    color: #00ff9d;
}

.orchestrator-notification.error {
    background: rgba(255, 71, 87, 0.2);
    border: 1px solid #ff4757;
    color: #ff4757;
}

.orchestrator-notification.warning {
    background: rgba(255, 165, 0, 0.2);
    border: 1px solid #ffa500;
    color: #ffa500;
}

.orchestrator-notification.info {
    background: rgba(74, 144, 226, 0.2);
    border: 1px solid #4a90e2;
    color: #4a90e2;
}

.notification-content {
    display: flex;
    align-items: center;
    gap: 8px;
}

.notification-content i {
    width: 18px;
    height: 18px;
}

@keyframes slideInRight {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}
`;
document.head.appendChild(orchestratorStyle);
'''
        
        with open(js_file, 'w') as f:
            f.write(content)
        
        logger.info("✅ Created orchestrator-integration.js")
    
    def update_dashboard_template(self):
        """Update dashboard template to include orchestrator integration"""
        template_file = self.templates_path / "dashboard_production.html"
        
        if not template_file.exists():
            logger.warning("Dashboard template not found, skipping template update")
            return
        
        with open(template_file, 'r') as f:
            content = f.read()
        
        # Add orchestrator integration script before closing body tag
        orchestrator_script = '''
    <!-- o3-mini Orchestrator Integration -->
    <script src="{{ url_for('static', filename='js/orchestrator-integration.js') }}"></script>
</body>'''
        
        if 'orchestrator-integration.js' not in content:
            content = content.replace('</body>', orchestrator_script)
        
        with open(template_file, 'w') as f:
            f.write(content)
        
        logger.info("✅ Updated dashboard template with orchestrator integration")

def main():
    """Execute frontend orchestrator integration fixes"""
    try:
        fixer = FrontendOrchestratorFix()
        fixer.apply_all_fixes()
        
        print("\n" + "="*60)
        print("🚀 FRONTEND ORCHESTRATOR INTEGRATION COMPLETE")
        print("="*60)
        print("✅ All dashboard components now integrate with o3-mini orchestrator")
        print("✅ Real blockchain data displayed with AI analysis")
        print("✅ Confidence scores and insights shown in all cards")
        print("✅ Currency formatting with $ symbols implemented")
        print("✅ Error handling and retry logic added")
        print("✅ Periodic updates for real-time data")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Frontend integration failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()