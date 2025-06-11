/**
 * Dashboard Optimized Layout Fix
 * Addresses rate limiting, component overflow, and API throttling
 */

class DashboardOptimized {
    constructor() {
        this.requestQueue = new Map();
        this.lastRequestTime = 0;
        this.minInterval = 5000; // 5 seconds between requests
        this.maxRetries = 2;
        this.init();
    }

    init() {
        this.fixLayout();
        this.setupThrottledOrchestrator();
        this.addCurrencyFormatting();
        this.setupComponentHeights();
        this.setupFooterSpacing();
    }

    fixLayout() {
        // Ensure proper component spacing
        const mainContent = document.querySelector('.dashboard-content, .main-content');
        if (mainContent) {
            mainContent.style.paddingBottom = '140px';
            mainContent.style.marginBottom = '80px';
        }

        // Fix grid layout
        const grid = document.querySelector('.dashboard-grid');
        if (grid) {
            grid.style.paddingBottom = '140px';
            grid.style.marginBottom = '80px';
        }
    }

    setupComponentHeights() {
        // Ensure all agent cards are properly sized
        const cards = document.querySelectorAll('.agent-card');
        cards.forEach(card => {
            card.style.minHeight = '440px';
            card.style.display = 'flex';
            card.style.flexDirection = 'column';
            
            // Add AI insight areas to cards that don't have them
            if (!card.querySelector('.agent-insight')) {
                this.addOptimizedInsight(card);
            }
        });
    }

    setupFooterSpacing() {
        // Ensure footer doesn't overlap content
        const footer = document.querySelector('.dashboard-footer, footer');
        if (footer) {
            footer.style.position = 'fixed';
            footer.style.bottom = '0';
            footer.style.left = '280px';
            footer.style.right = '0';
            footer.style.zIndex = '998';
        }
    }

    addOptimizedInsight(card) {
        const cardId = card.id || 'card-' + Math.random().toString(36).substr(2, 9);
        card.id = cardId;

        const insight = document.createElement('div');
        insight.className = 'agent-insight optimized';
        insight.style.cssText = `
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 1rem;
            margin-top: 1rem;
            max-height: 180px;
            overflow-y: auto;
            flex-grow: 1;
        `;
        
        insight.innerHTML = `
            <div class="insight-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <span class="insight-label" style="color: #00d4ff; font-weight: 600; font-size: 0.875rem;">🤖 o3-mini Analysis</span>
                <span class="confidence" id="${cardId}-confidence" style="color: #ffd700; font-size: 0.75rem;">Ready to load</span>
            </div>
            <div class="insight-content" id="${cardId}-analysis" style="color: #e0e0e0; font-size: 0.8rem; line-height: 1.4; white-space: pre-wrap;">
                Click to load o3-mini analysis with real blockchain data
            </div>
            <button class="load-analysis-btn" onclick="dashboardOptimized.loadAnalysisForCard('${cardId}')" 
                    style="margin-top: 0.5rem; padding: 0.25rem 0.5rem; background: #00d4ff; color: #000; border: none; border-radius: 4px; font-size: 0.75rem; cursor: pointer;">
                Load Analysis
            </button>
        `;
        
        card.appendChild(insight);
    }

    setupThrottledOrchestrator() {
        // Replace automatic loading with on-demand loading
        this.loadButtons = document.querySelectorAll('.load-analysis-btn');
        console.log('Throttled orchestrator ready - click buttons to load o3-mini analysis');
    }

    async loadAnalysisForCard(cardId) {
        const card = document.getElementById(cardId);
        if (!card) return;

        const analysisElement = card.querySelector(`#${cardId}-analysis`);
        const confidenceElement = card.querySelector(`#${cardId}-confidence`);
        const button = card.querySelector('.load-analysis-btn');

        if (button) button.disabled = true;
        if (analysisElement) analysisElement.textContent = 'Loading blockchain data...\n⏳ Connecting to testnet-rpc.daodiseo.chaintools.tech\n🧠 Initializing o3-mini analysis';
        if (confidenceElement) confidenceElement.textContent = 'Loading...';

        // Determine endpoint based on card content/title
        let endpoint = 'token-metrics';
        const cardTitle = card.querySelector('h3, .card-title, .agent-title');
        if (cardTitle) {
            const title = cardTitle.textContent.toLowerCase();
            if (title.includes('staking') || title.includes('apy')) {
                endpoint = 'staking-metrics';
            } else if (title.includes('network') || title.includes('health')) {
                endpoint = 'network-health';
            }
        }

        try {
            const response = await this.throttledRequest(`/api/orchestrator/${endpoint}`);
            
            if (response.success && response.data) {
                this.updateCardWithData(card, response, cardId);
            } else {
                throw new Error('Invalid response format');
            }
        } catch (error) {
            console.error(`Failed to load ${endpoint}:`, error);
            if (analysisElement) {
                analysisElement.textContent = `❌ Analysis failed: ${error.message}\nTry again in a few moments`;
            }
            if (confidenceElement) {
                confidenceElement.textContent = 'Error';
                confidenceElement.style.color = '#ff4444';
            }
        } finally {
            if (button) {
                button.disabled = false;
                button.textContent = 'Reload Analysis';
            }
        }
    }

    async throttledRequest(url) {
        const now = Date.now();
        const timeSinceLastRequest = now - this.lastRequestTime;
        
        if (timeSinceLastRequest < this.minInterval) {
            const waitTime = this.minInterval - timeSinceLastRequest;
            await new Promise(resolve => setTimeout(resolve, waitTime));
        }

        this.lastRequestTime = Date.now();
        
        const response = await fetch(url);
        if (response.status === 429) {
            throw new Error('Rate limited - please wait before requesting again');
        }
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    }

    updateCardWithData(card, data, cardId) {
        const analysisElement = card.querySelector(`#${cardId}-analysis`);
        const confidenceElement = card.querySelector(`#${cardId}-confidence`);

        if (data.data && data.data.analysis) {
            let formattedAnalysis = '✅ Analysis Complete\n\n';
            
            if (typeof data.data.analysis === 'string') {
                formattedAnalysis += data.data.analysis;
            } else if (typeof data.data.analysis === 'object') {
                for (const [key, value] of Object.entries(data.data.analysis)) {
                    if (Array.isArray(value)) {
                        formattedAnalysis += `${key.replace(/_/g, ' ').toUpperCase()}:\n`;
                        value.forEach(item => formattedAnalysis += `• ${item}\n`);
                        formattedAnalysis += '\n';
                    } else {
                        formattedAnalysis += `${key.replace(/_/g, ' ').toUpperCase()}: ${value}\n\n`;
                    }
                }
            }

            if (analysisElement) {
                analysisElement.textContent = formattedAnalysis;
            }
        }

        if (data.metadata && data.metadata.confidence && confidenceElement) {
            const confidence = Math.round(data.metadata.confidence * 100);
            confidenceElement.textContent = `Confidence: ${confidence}%`;
            confidenceElement.style.color = confidence > 80 ? '#00ff88' : '#ffd700';
        }

        // Update main card values if available
        this.updateCardValues(card, data.data);
    }

    updateCardValues(card, data) {
        // Update price displays with proper formatting
        const priceElements = card.querySelectorAll('[data-field*="price"], [data-field*="value"]');
        priceElements.forEach(el => {
            if (data.token_price) {
                el.textContent = this.formatCurrency(data.token_price);
            }
        });

        // Update percentage displays
        const percentElements = card.querySelectorAll('[data-field*="change"], [data-field*="apy"]');
        percentElements.forEach(el => {
            if (data.price_change_24h) {
                el.textContent = `${data.price_change_24h > 0 ? '+' : ''}${data.price_change_24h.toFixed(2)}%`;
                el.style.color = data.price_change_24h > 0 ? '#00ff88' : '#ff4444';
            } else if (data.staking_apy) {
                el.textContent = `${data.staking_apy.toFixed(2)}%`;
            }
        });
    }

    addCurrencyFormatting() {
        window.formatCurrency = (value) => {
            if (value === null || value === undefined || isNaN(value)) {
                return '$0.00';
            }
            
            const num = parseFloat(value);
            if (num >= 1000000) {
                return `$${(num / 1000000).toFixed(1)}M`;
            } else if (num >= 1000) {
                return `$${(num / 1000).toFixed(1)}K`;
            } else {
                return `$${num.toFixed(2)}`;
            }
        };
    }

    formatCurrency(value) {
        return window.formatCurrency(value);
    }
}

// Initialize optimized dashboard
let dashboardOptimized;
document.addEventListener('DOMContentLoaded', () => {
    console.log('Dashboard optimized layout loading...');
    dashboardOptimized = new DashboardOptimized();
    console.log('Dashboard optimized - o3-mini available on-demand');
});

// Export for global access
window.dashboardOptimized = dashboardOptimized;