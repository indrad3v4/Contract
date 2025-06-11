// DAODISEO Dashboard Final Fix - o3-mini Orchestrator Integration
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
