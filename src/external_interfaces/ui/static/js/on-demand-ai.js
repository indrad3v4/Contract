// On-Demand AI Orchestrator - Prevents Resource Overload
console.log("On-demand AI system loading...");

window.OnDemandAI = {
    cache: new Map(),
    activeRequests: new Set(),
    maxConcurrentRequests: 1, // Limit to 1 to prevent overload
    cacheTimeout: 10 * 60 * 1000, // 10 minutes
    
    init() {
        this.addAIButtons();
        this.setupEventListeners();
        console.log("✅ On-demand AI system ready");
    },
    
    addAIButtons() {
        const cards = document.querySelectorAll('[data-card-id]');
        
        cards.forEach(card => {
            if (card.querySelector('.ai-btn')) return;
            
            const cardId = card.dataset.cardId;
            const button = this.createAIButton(cardId);
            
            // Add button to card header or top
            const cardHeader = card.querySelector('.card-header') || card.querySelector('.card-title')?.parentElement;
            if (cardHeader) {
                cardHeader.style.display = 'flex';
                cardHeader.style.justifyContent = 'space-between';
                cardHeader.style.alignItems = 'center';
                cardHeader.appendChild(button);
            } else {
                card.style.position = 'relative';
                button.style.position = 'absolute';
                button.style.top = '10px';
                button.style.right = '10px';
                card.appendChild(button);
            }
        });
    },
    
    createAIButton(cardId) {
        const button = document.createElement('button');
        button.className = 'ai-btn';
        button.dataset.cardId = cardId;
        button.innerHTML = '🧠 Analyze';
        button.onclick = () => this.runAnalysis(cardId, button);
        
        button.style.cssText = `
            background: linear-gradient(135deg, #00ff9d, #00d4aa);
            border: none;
            color: #000;
            padding: 6px 12px;
            border-radius: 16px;
            font-size: 0.75rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            white-space: nowrap;
        `;
        
        return button;
    },
    
    setupEventListeners() {
        // Global keyboard shortcut for batch analysis
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'a') {
                e.preventDefault();
                this.runBatchAnalysis();
            }
        });
    },
    
    async runAnalysis(cardId, button) {
        const cacheKey = cardId;
        
        // Check cache first
        if (this.cache.has(cacheKey)) {
            const cached = this.cache.get(cacheKey);
            if (Date.now() - cached.timestamp < this.cacheTimeout) {
                this.displayCachedResult(cardId, cached.data);
                this.showTooltip(button, 'Loaded from cache', 'info');
                return;
            }
        }
        
        // Check concurrent limit
        if (this.activeRequests.size >= this.maxConcurrentRequests) {
            this.showTooltip(button, 'Please wait...', 'warning');
            return;
        }
        
        this.setButtonLoading(button, true);
        this.activeRequests.add(cacheKey);
        
        try {
            const analysisType = this.getAnalysisType(cardId);
            const endpoint = this.getEndpoint(analysisType);
            
            const response = await fetch(endpoint);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            
            const data = await response.json();
            
            if (data.success) {
                // Cache result
                this.cache.set(cacheKey, {
                    data: data,
                    timestamp: Date.now()
                });
                
                this.displayResult(cardId, data.data, data.metadata);
                this.showTooltip(button, 'Analysis complete!', 'success');
            } else {
                throw new Error(data.details || 'Analysis failed');
            }
            
        } catch (error) {
            console.error(`AI analysis failed for ${cardId}:`, error);
            this.showTooltip(button, 'Analysis failed', 'error');
            this.displayError(cardId, error.message);
        } finally {
            this.setButtonLoading(button, false);
            this.activeRequests.delete(cacheKey);
        }
    },
    
    getAnalysisType(cardId) {
        const typeMap = {
            'odis-price': 'token-metrics',
            'market-cap': 'token-metrics', 
            'volume-24h': 'token-metrics',
            'staking-apy': 'staking-metrics',
            'total-staked': 'staking-metrics',
            'network-health': 'network-health'
        };
        return typeMap[cardId] || 'token-metrics';
    },
    
    getEndpoint(analysisType) {
        const endpoints = {
            'token-metrics': '/api/orchestrator/token-metrics',
            'staking-metrics': '/api/orchestrator/staking-metrics', 
            'network-health': '/api/orchestrator/network-health'
        };
        return endpoints[analysisType];
    },
    
    setButtonLoading(button, loading) {
        if (loading) {
            button.innerHTML = '⏳ Thinking...';
            button.disabled = true;
            button.style.opacity = '0.7';
        } else {
            button.innerHTML = '🧠 Analyze';
            button.disabled = false;
            button.style.opacity = '1';
        }
    },
    
    displayResult(cardId, data, metadata) {
        const card = document.querySelector(`[data-card-id="${cardId}"]`);
        if (!card) return;
        
        // Update main value
        const valueEl = card.querySelector('.card-value');
        if (valueEl) {
            if (data.token_price !== undefined) {
                valueEl.textContent = `$${data.token_price}`;
            } else if (data.staking_apy !== undefined) {
                valueEl.textContent = `${(data.staking_apy * 100).toFixed(1)}%`;
            } else if (data.health_score !== undefined) {
                valueEl.textContent = `${data.health_score}/100`;
            }
        }
        
        // Update status
        const statusEl = card.querySelector('.status-badge');
        if (statusEl) {
            statusEl.textContent = data.status || 'analyzed';
            statusEl.className = `status-badge verified`;
        }
        
        // Add AI insight
        this.addAIInsight(card, data, metadata);
    },
    
    displayCachedResult(cardId, cachedData) {
        this.displayResult(cardId, cachedData.data, cachedData.metadata);
    },
    
    addAIInsight(card, data, metadata) {
        // Remove existing insight
        const existingInsight = card.querySelector('.ai-insight');
        if (existingInsight) existingInsight.remove();
        
        const insight = document.createElement('div');
        insight.className = 'ai-insight';
        
        const analysis = this.extractAnalysis(data);
        const confidence = metadata?.confidence || 0.85;
        
        insight.innerHTML = `
            <div class="ai-content">
                <div class="ai-badge">o3-mini</div>
                <p>${analysis}</p>
                <div class="ai-meta">
                    <span>Confidence: ${Math.round(confidence * 100)}%</span>
                    <span>Updated: ${new Date().toLocaleTimeString()}</span>
                </div>
            </div>
        `;
        
        insight.style.cssText = `
            margin-top: 12px;
            padding: 10px;
            background: rgba(0, 255, 157, 0.1);
            border-radius: 6px;
            border-left: 3px solid #00ff9d;
            font-size: 0.8rem;
        `;
        
        card.appendChild(insight);
    },
    
    extractAnalysis(data) {
        if (typeof data.analysis === 'string') {
            return data.analysis;
        } else if (data.analysis?.strategy_recommendations) {
            return data.analysis.strategy_recommendations[0] || 'Analysis completed';
        } else if (data.analysis?.network_stability) {
            return data.analysis.network_stability;
        }
        return 'AI analysis completed successfully';
    },
    
    displayError(cardId, errorMsg) {
        const card = document.querySelector(`[data-card-id="${cardId}"]`);
        if (!card) return;
        
        const errorEl = document.createElement('div');
        errorEl.className = 'ai-error';
        errorEl.innerHTML = `
            <div style="color: #ff4757; font-size: 0.8rem; margin-top: 8px;">
                ⚠️ AI analysis unavailable
            </div>
        `;
        card.appendChild(errorEl);
        
        setTimeout(() => errorEl.remove(), 5000);
    },
    
    showTooltip(button, message, type) {
        const tooltip = document.createElement('div');
        tooltip.className = `ai-tooltip ${type}`;
        tooltip.textContent = message;
        
        const colors = {
            success: '#00ff9d',
            error: '#ff4757', 
            warning: '#ffa500',
            info: '#4a90e2'
        };
        
        tooltip.style.cssText = `
            position: absolute;
            top: -30px;
            left: 50%;
            transform: translateX(-50%);
            background: ${colors[type] || colors.info};
            color: #000;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.7rem;
            white-space: nowrap;
            z-index: 1000;
        `;
        
        button.style.position = 'relative';
        button.appendChild(tooltip);
        
        setTimeout(() => tooltip.remove(), 2000);
    },
    
    async runBatchAnalysis() {
        const cards = document.querySelectorAll('[data-card-id]');
        const visibleCards = Array.from(cards).filter(card => {
            const rect = card.getBoundingClientRect();
            return rect.top >= 0 && rect.bottom <= window.innerHeight;
        });
        
        console.log(`Running batch analysis on ${visibleCards.length} visible cards...`);
        
        for (const card of visibleCards) {
            const button = card.querySelector('.ai-btn');
            if (button && !button.disabled) {
                await this.runAnalysis(card.dataset.cardId, button);
                await new Promise(resolve => setTimeout(resolve, 1000)); // 1 second delay between requests
            }
        }
    },
    
    clearCache() {
        this.cache.clear();
        console.log("AI cache cleared");
    },
    
    getStats() {
        return {
            cacheSize: this.cache.size,
            activeRequests: this.activeRequests.size,
            cachedItems: Array.from(this.cache.keys())
        };
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        window.OnDemandAI.init();
    }, 1500);
});

// Add AI insight styling
const aiStyle = document.createElement('style');
aiStyle.textContent = `
.ai-insight .ai-badge {
    background: linear-gradient(135deg, #00ff9d, #00d4aa);
    color: #000;
    padding: 2px 6px;
    border-radius: 10px;
    font-size: 0.7rem;
    font-weight: 600;
    margin-bottom: 6px;
    display: inline-block;
}

.ai-insight p {
    margin: 6px 0;
    color: #e0e0e0;
    line-height: 1.4;
}

.ai-meta {
    display: flex;
    justify-content: space-between;
    margin-top: 6px;
    font-size: 0.7rem;
    color: #00ff9d;
    opacity: 0.8;
}

.ai-btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0, 255, 157, 0.3);
}
`;
document.head.appendChild(aiStyle);
