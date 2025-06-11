// Orchestrator DOM Integration Fix - Ensures Data Reaches Components
console.log("Orchestrator DOM integration fix loading...");

window.OrchestratorDOMFix = {
    agentEndpoints: {
        'network-health': '/api/rpc/network-status',
        'transactions': '/api/rpc/transactions', 
        'validators': '/api/blockchain/stats',
        'token-metrics': '/api/blockchain/stats',
        'staking-metrics': '/api/blockchain/stats'
    },
    
    retryConfig: {
        maxRetries: 3,
        baseDelay: 1000,
        backoffMultiplier: 2
    },
    
    init() {
        this.interceptFailedCalls();
        this.setupAgentStatusUpdates();
        console.log("✅ Orchestrator DOM fix active");
    },
    
    interceptFailedCalls() {
        // Override console.error to catch API failures
        const originalError = console.error;
        console.error = (...args) => {
            const message = args.join(' ');
            
            if (message.includes('Failed to load')) {
                this.handleFailedLoad(message);
            }
            
            return originalError.apply(console, args);
        };
    },
    
    handleFailedLoad(errorMessage) {
        // Extract agent type from error message
        const agentType = this.extractAgentType(errorMessage);
        
        if (agentType && this.agentEndpoints[agentType]) {
            console.log(`Retrying failed ${agentType} with fallback endpoint`);
            this.retryAgentLoad(agentType);
        }
    },
    
    extractAgentType(errorMessage) {
        const types = Object.keys(this.agentEndpoints);
        return types.find(type => errorMessage.includes(type));
    },
    
    async retryAgentLoad(agentType, attempt = 1) {
        if (attempt > this.retryConfig.maxRetries) {
            this.setAgentError(agentType);
            return;
        }
        
        try {
            const endpoint = this.agentEndpoints[agentType];
            const response = await fetch(endpoint);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            this.updateAgentWithData(agentType, data);
            
        } catch (error) {
            console.warn(`Retry ${attempt} failed for ${agentType}:`, error);
            
            const delay = this.retryConfig.baseDelay * Math.pow(this.retryConfig.backoffMultiplier, attempt - 1);
            
            setTimeout(() => {
                this.retryAgentLoad(agentType, attempt + 1);
            }, delay);
        }
    },
    
    updateAgentWithData(agentType, data) {
        const agentCard = this.findAgentCard(agentType);
        
        if (!agentCard) {
            console.warn(`Agent card not found for ${agentType}`);
            return;
        }
        
        // Update agent status
        this.updateAgentStatus(agentCard, 'success', 'Connected');
        
        // Update agent data based on type
        this.populateAgentData(agentCard, agentType, data);
    },
    
    findAgentCard(agentType) {
        // Look for agent cards by data attributes or class names
        const selectors = [
            `[data-agent="${agentType}"]`,
            `[data-card-id*="${agentType}"]`,
            `.${agentType}-agent`,
            `.agent-${agentType}`
        ];
        
        for (const selector of selectors) {
            const card = document.querySelector(selector);
            if (card) return card;
        }
        
        // Fallback: search by content
        const cards = document.querySelectorAll('.card, .agent-card');
        return Array.from(cards).find(card => {
            const text = card.textContent.toLowerCase();
            return text.includes(agentType.replace('-', ' '));
        });
    },
    
    updateAgentStatus(agentCard, status, message) {
        // Find status elements
        const statusBadge = agentCard.querySelector('.status-badge, .agent-status');
        const statusText = agentCard.querySelector('.status-text, .agent-message');
        
        if (statusBadge) {
            statusBadge.className = `status-badge ${status}`;
            statusBadge.textContent = message;
        }
        
        if (statusText) {
            statusText.textContent = message;
        }
        
        // Update card visual state
        agentCard.classList.remove('loading', 'error', 'success');
        agentCard.classList.add(status);
    },
    
    populateAgentData(agentCard, agentType, data) {
        const valueElement = agentCard.querySelector('.card-value, .agent-value');
        
        if (!valueElement) return;
        
        switch (agentType) {
            case 'network-health':
                if (data.result?.sync_info) {
                    const blockHeight = data.result.sync_info.latest_block_height;
                    valueElement.textContent = `Block ${blockHeight}`;
                }
                break;
                
            case 'transactions':
                if (data.result?.txs) {
                    valueElement.textContent = `${data.result.txs.length} transactions`;
                }
                break;
                
            case 'validators':
                if (data.validators_count !== undefined) {
                    valueElement.textContent = `${data.validators_count} validators`;
                } else if (data.result?.validators) {
                    valueElement.textContent = `${data.result.validators.length} validators`;
                }
                break;
                
            case 'token-metrics':
                if (data.token_price !== undefined) {
                    valueElement.textContent = `$${data.token_price}`;
                } else if (data.price) {
                    valueElement.textContent = `$${data.price}`;
                }
                break;
                
            case 'staking-metrics':
                if (data.staking_apy !== undefined) {
                    valueElement.textContent = `${(data.staking_apy * 100).toFixed(1)}% APY`;
                } else if (data.apy) {
                    valueElement.textContent = `${data.apy}% APY`;
                }
                break;
        }
    },
    
    setAgentError(agentType) {
        const agentCard = this.findAgentCard(agentType);
        
        if (agentCard) {
            this.updateAgentStatus(agentCard, 'error', 'Connection failed');
            
            // Add retry button
            this.addRetryButton(agentCard, agentType);
        }
    },
    
    addRetryButton(agentCard, agentType) {
        if (agentCard.querySelector('.retry-button')) return;
        
        const retryButton = document.createElement('button');
        retryButton.className = 'retry-button';
        retryButton.textContent = 'Retry';
        retryButton.onclick = () => {
            retryButton.remove();
            this.retryAgentLoad(agentType);
        };
        
        const cardBody = agentCard.querySelector('.card-body, .agent-body');
        if (cardBody) {
            cardBody.appendChild(retryButton);
        }
    },
    
    setupAgentStatusUpdates() {
        // Periodically check for failed agents
        setInterval(() => {
            this.checkAgentHealth();
        }, 30000); // Check every 30 seconds
    },
    
    checkAgentHealth() {
        const errorCards = document.querySelectorAll('.card.error, .agent-card.error');
        
        errorCards.forEach(card => {
            const agentType = this.detectAgentType(card);
            if (agentType) {
                console.log(`Auto-retrying failed agent: ${agentType}`);
                this.retryAgentLoad(agentType);
            }
        });
    },
    
    detectAgentType(card) {
        // Try to detect agent type from card content or attributes
        const text = card.textContent.toLowerCase();
        
        if (text.includes('network') || text.includes('health')) return 'network-health';
        if (text.includes('transaction')) return 'transactions';
        if (text.includes('validator')) return 'validators';
        if (text.includes('token') || text.includes('price')) return 'token-metrics';
        if (text.includes('staking') || text.includes('apy')) return 'staking-metrics';
        
        return null;
    }
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    window.OrchestratorDOMFix.init();
});

// Add retry button styles
const retryStyle = document.createElement('style');
retryStyle.textContent = `
.retry-button {
    background: #ff4757;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.8rem;
    margin-top: 0.5rem;
}

.retry-button:hover {
    background: #ff3838;
}

.card.error, .agent-card.error {
    border-left: 3px solid #ff4757;
    background: rgba(255, 71, 87, 0.1);
}

.card.success, .agent-card.success {
    border-left: 3px solid #00ff9d;
    background: rgba(0, 255, 157, 0.1);
}

.status-badge.success {
    background: #00ff9d;
    color: #000;
}

.status-badge.error {
    background: #ff4757;
    color: #fff;
}
`;
document.head.appendChild(retryStyle);
