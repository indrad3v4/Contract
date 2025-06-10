
// Namespace wrapper to prevent variable conflicts
(function() {
    'use strict';
    



// Data Source Agents JavaScript Enhancement

class DataSourceAgentManager {
    constructor() {
        this.agents = ['token-value', 'total-reserves', 'staking-apy', 'daily-rewards'];
        this.updateInterval = 30000; // 30 seconds
        this.isRunning = false;
    }
    
    init() {
        this.startAgentUpdates();
        this.bindEvents();
        this.loadInitialData();
    }
    
    startAgentUpdates() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        this.updateAllAgents();
        this.intervalId = setInterval(() => {
            this.updateAllAgents();
        }, this.updateInterval);
        
        console.log('Data Source Agents started');
    }
    
    stopAgentUpdates() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
        }
        this.isRunning = false;
        console.log('Data Source Agents stopped');
    }
    
    async updateAllAgents() {
        const timestamp = new Date().toLocaleTimeString();
        
        for (const agent of this.agents) {
            try {
                await this.updateAgent(agent, timestamp);
            } catch (error) {
                console.error(`Failed to update agent ${agent}:`, error);
                this.setAgentError(agent);
            }
        }
    }
    
    async updateAgent(agentType, timestamp) {
        const timeElement = document.getElementById(`${agentType.replace('-', '-')}-update-time`);
        if (timeElement) {
            timeElement.textContent = timestamp;
        }
        
        switch (agentType) {
            case 'token-value':
                await this.updateTokenValueAgent();
                break;
            case 'total-reserves':
                await this.updateTotalReservesAgent();
                break;
            case 'staking-apy':
                await this.updateStakingApyAgent();
                break;
            case 'daily-rewards':
                await this.updateDailyRewardsAgent();
                break;
        }
    }
    
    async updateTokenValueAgent() {
        try {
            const response = await fetch('/api/blockchain/token-price');
            const data = await response.json();
            
            const priceElement = document.getElementById('token-current-price');
            const changeElement = document.getElementById('token-24h-change');
            const volumeElement = document.getElementById('token-volume');
            
            if (priceElement && data.price) {
                priceElement.textContent = `$${data.price.toFixed(4)}`;
            }
            
            if (changeElement && data.change_24h !== undefined) {
                const changeValue = data.change_24h;
                changeElement.textContent = `${changeValue >= 0 ? '+' : ''}${changeValue.toFixed(2)}%`;
                changeElement.className = changeValue >= 0 ? 'value change-positive' : 'value change-negative';
            }
            
            if (volumeElement && data.volume) {
                volumeElement.textContent = this.formatNumber(data.volume);
            }
        } catch (error) {
            console.error('Failed to update token value agent:', error);
        }
    }
    
    async updateTotalReservesAgent() {
        try {
            const response = await fetch('/api/blockchain/stats');
            const data = await response.json();
            
            const totalElement = document.getElementById('total-reserves-value');
            const availableElement = document.getElementById('available-reserves');
            const stakedElement = document.getElementById('staked-reserves');
            
            if (totalElement && data.total_supply) {
                totalElement.textContent = this.formatNumber(data.total_supply);
            }
            
            if (availableElement && data.circulating_supply) {
                availableElement.textContent = this.formatNumber(data.circulating_supply);
            }
            
            if (stakedElement && data.bonded_tokens) {
                stakedElement.textContent = this.formatNumber(data.bonded_tokens);
            }
        } catch (error) {
            console.error('Failed to update total reserves agent:', error);
        }
    }
    
    async updateStakingApyAgent() {
        try {
            const response = await fetch('/api/blockchain/stakeholder-distribution');
            const data = await response.json();
            
            const apyElement = document.getElementById('staking-apy-value');
            const validatorsElement = document.getElementById('active-validators');
            const userStakeElement = document.getElementById('user-stake');
            
            if (apyElement && data.staking_apy) {
                apyElement.textContent = data.staking_apy.toFixed(2);
            }
            
            if (validatorsElement && data.validators) {
                validatorsElement.textContent = data.validators.length;
            }
            
            if (userStakeElement) {
                userStakeElement.textContent = '0.00'; // Would be from user's wallet
            }
        } catch (error) {
            console.error('Failed to update staking APY agent:', error);
        }
    }
    
    async updateDailyRewardsAgent() {
        try {
            // This would connect to actual rewards API
            const dailyElement = document.getElementById('daily-rewards-value');
            const pendingElement = document.getElementById('pending-rewards');
            const claimedElement = document.getElementById('claimed-rewards');
            
            // Mock data for now - would be replaced with actual API
            if (dailyElement) {
                dailyElement.textContent = '12.34';
            }
            
            if (pendingElement) {
                pendingElement.textContent = '45.67';
            }
            
            if (claimedElement) {
                claimedElement.textContent = '123.45';
            }
        } catch (error) {
            console.error('Failed to update daily rewards agent:', error);
        }
    }
    
    setAgentError(agentType) {
        const card = document.querySelector(`[data-agent="${agentType}"]`);
        if (card) {
            const indicator = card.querySelector('.status-indicator');
            if (indicator) {
                indicator.classList.remove('active');
                indicator.style.background = '#ef4444';
            }
        }
    }
    
    formatNumber(num) {
        if (num >= 1e9) {
            return (num / 1e9).toFixed(2) + 'B';
        } else if (num >= 1e6) {
            return (num / 1e6).toFixed(2) + 'M';
        } else if (num >= 1e3) {
            return (num / 1e3).toFixed(2) + 'K';
        }
        return num.toString();
    }
    
    bindEvents() {
        // Bind refresh button
        const refreshBtn = document.querySelector('.refresh-agents-btn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.updateAllAgents();
            });
        }
        
        // Bind agent card clicks for detailed views
        document.querySelectorAll('.agent-card').forEach(card => {
            card.addEventListener('click', (e) => {
                const agentType = card.dataset.agent;
                this.showAgentDetails(agentType);
            });
        });
    }
    
    showAgentDetails(agentType) {
        // Future implementation for detailed agent views
        console.log(`Show details for ${agentType} agent`);
    }
    
    loadInitialData() {
        // Load initial data immediately
        this.updateAllAgents();
    }
}

// Global function for refresh button
function refreshDataSourceAgents() {
    if (window.dataSourceAgentManager) {
        window.dataSourceAgentManager.updateAllAgents();
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.dataSourceAgentManager = new DataSourceAgentManager();
    window.dataSourceAgentManager.init();
});

    
})();
