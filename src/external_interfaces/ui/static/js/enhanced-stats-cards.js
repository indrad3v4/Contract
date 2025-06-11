// Enhanced Stats Cards with o3-mini Orchestrator Integration
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
