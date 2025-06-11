/**
 * Dashboard Layout Fix Script
 * Fixes component overlapping, orchestrator loading, and proper scrolling
 */

class DashboardLayoutFix {
    constructor() {
        this.orchestratorEndpoints = {
            'token-metrics': '/api/orchestrator/token-metrics',
            'staking-metrics': '/api/orchestrator/staking-metrics', 
            'network-health': '/api/orchestrator/network-health'
        };
        this.init();
    }

    init() {
        this.fixLayout();
        this.setupOrchestrator();
        this.loadOrchestratorData();
    }

    // Fix layout spacing and component positioning
    fixLayout() {
        // Ensure main content has proper padding and scrolling
        const mainContent = document.querySelector('.main-content');
        if (mainContent) {
            mainContent.style.paddingBottom = '3rem';
            mainContent.style.overflowY = 'auto';
            mainContent.style.height = 'calc(100vh - 140px)';
        }

        // Fix dashboard grid spacing
        const dashboardGrid = document.querySelector('.dashboard-grid');
        if (dashboardGrid) {
            dashboardGrid.style.gap = '2rem';
            dashboardGrid.style.paddingBottom = '2rem';
            dashboardGrid.style.minHeight = 'auto';
        }

        // Ensure agent cards don't overlap
        const agentCards = document.querySelectorAll('.agent-card');
        agentCards.forEach(card => {
            card.style.marginBottom = '1rem';
            card.style.position = 'relative';
            card.style.zIndex = 'auto';
        });

        // Fix footer positioning
        const footer = document.querySelector('.dashboard-footer');
        if (footer) {
            footer.style.position = 'relative';
            footer.style.marginTop = '2rem';
            footer.style.width = '100%';
        }
    }

    // Setup orchestrator integration
    setupOrchestrator() {
        // Add insight sections to all cards
        this.addInsightSections();
        
        // Setup currency formatting
        this.setupCurrencyFormatting();
        
        // Start periodic updates
        this.startPeriodicUpdates();
    }

    addInsightSections() {
        const cards = document.querySelectorAll('.agent-card');
        cards.forEach(card => {
            const cardId = card.getAttribute('data-card-type');
            if (cardId && !card.querySelector('.agent-insight')) {
                this.addInsightToCard(card, cardId);
            }
        });
    }

    addInsightToCard(card, cardId) {
        const insight = document.createElement('div');
        insight.className = 'agent-insight mt-2';
        insight.innerHTML = `
            <div class="insight-header">
                <span class="insight-label">o3-mini Analysis</span>
                <span class="confidence" id="${cardId}-confidence">Loading...</span>
            </div>
            <div class="insight-content" id="${cardId}-analysis">Connecting to orchestrator...</div>
        `;
        
        const cardBody = card.querySelector('.agent-card-body') || card;
        cardBody.appendChild(insight);
    }

    setupCurrencyFormatting() {
        window.formatCurrency = (value) => {
            if (value === null || value === undefined || isNaN(value)) {
                return '$0.00';
            }
            return new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD',
                minimumFractionDigits: 2,
                maximumFractionDigits: 8
            }).format(value);
        };
    }

    async loadOrchestratorData() {
        for (const [key, endpoint] of Object.entries(this.orchestratorEndpoints)) {
            try {
                const response = await fetch(endpoint);
                const data = await response.json();
                
                if (data.success) {
                    this.updateCardWithOrchestratorData(key, data);
                } else {
                    this.updateCardError(key, 'Analysis Error');
                }
            } catch (error) {
                console.log(`Failed to load ${key}:`, error);
                this.updateCardError(key, 'Connection Error');
            }
        }
    }

    updateCardWithOrchestratorData(cardType, data) {
        const cardId = this.getCardIdFromType(cardType);
        if (!cardId) return;

        const card = document.querySelector(`[data-card-type="${cardId}"]`);
        if (!card) return;

        // Update main value
        const valueElement = card.querySelector('.agent-value');
        if (valueElement && data.data) {
            const value = this.extractValueFromData(cardType, data.data);
            valueElement.textContent = value;
        }

        // Update status badge
        const badge = card.querySelector('.agent-badge');
        if (badge) {
            badge.className = 'agent-badge verified';
            badge.textContent = 'Verified';
        }

        // Update analysis
        const analysisElement = card.querySelector(`#${cardId}-analysis`);
        if (analysisElement && data.data.analysis) {
            analysisElement.textContent = typeof data.data.analysis === 'string' 
                ? data.data.analysis 
                : JSON.stringify(data.data.analysis);
        }

        // Update confidence
        const confidenceElement = card.querySelector(`#${cardId}-confidence`);
        if (confidenceElement && data.metadata && data.metadata.confidence) {
            confidenceElement.textContent = `Confidence: ${Math.round(data.metadata.confidence * 100)}%`;
        }
    }

    updateCardError(cardType, errorMessage) {
        const cardId = this.getCardIdFromType(cardType);
        if (!cardId) return;

        const card = document.querySelector(`[data-card-type="${cardId}"]`);
        if (!card) return;

        const badge = card.querySelector('.agent-badge');
        if (badge) {
            badge.className = 'agent-badge error';
            badge.textContent = 'Error';
        }

        const analysisElement = card.querySelector(`#${cardId}-analysis`);
        if (analysisElement) {
            analysisElement.textContent = errorMessage;
        }
    }

    getCardIdFromType(type) {
        const mapping = {
            'token-metrics': 'token-value',
            'staking-metrics': 'staking-apy', 
            'network-health': 'network-health'
        };
        return mapping[type];
    }

    extractValueFromData(type, data) {
        switch (type) {
            case 'token-metrics':
                return data.token_price ? window.formatCurrency(data.token_price) : '$0.0000';
            case 'staking-metrics':
                return data.staking_apy ? `${(data.staking_apy * 100).toFixed(2)}%` : '0.00%';
            case 'network-health':
                return data.health_score ? `${data.health_score}/100` : 'Unknown';
            default:
                return 'N/A';
        }
    }

    startPeriodicUpdates() {
        // Update every 30 seconds
        setInterval(() => {
            this.loadOrchestratorData();
        }, 30000);
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('Dashboard layout fix loading...');
    new DashboardLayoutFix();
    console.log('Dashboard layout fix initialized - o3-mini orchestrator active');
});

// Also initialize if DOM is already loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new DashboardLayoutFix();
    });
} else {
    new DashboardLayoutFix();
}