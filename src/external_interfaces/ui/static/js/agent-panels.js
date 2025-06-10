/**
 * Data Source Agent Panels JavaScript
 * Handles agent panel interactions and real-time updates
 */

class AgentPanelManager {
    constructor() {
        this.agents = new Map();
        this.updateInterval = null;
        this.websocket = null;
        this.initialize();
    }

    initialize() {
        console.log('Initializing Agent Panel Manager');
        this.setupEventListeners();
        this.startPeriodicUpdates();
        this.initializeWebSocket();
    }

    setupEventListeners() {
        // Agent action buttons
        document.addEventListener('click', (e) => {
            if (e.target.matches('.agent-btn[data-action]')) {
                const action = e.target.dataset.action;
                const agentId = e.target.closest('.agent-panel').dataset.agentId;
                this.executeAgentAction(agentId, action);
            }
        });

        // Panel refresh buttons
        document.addEventListener('click', (e) => {
            if (e.target.matches('.agent-refresh-btn')) {
                const agentId = e.target.closest('.agent-panel').dataset.agentId;
                this.refreshAgent(agentId);
            }
        });
    }

    async fetchAgentStatus() {
        try {
            const response = await fetch('/api/agents/status');
            if (!response.ok) throw new Error('Failed to fetch agent status');
            return await response.json();
        } catch (error) {
            console.error('Error fetching agent status:', error);
            return null;
        }
    }

    async updateAgentPanels() {
        const statusData = await this.fetchAgentStatus();
        if (!statusData) return;

        Object.entries(statusData.agents).forEach(([agentId, agentData]) => {
            this.updateAgentPanel(agentId, agentData);
        });
    }

    updateAgentPanel(agentId, agentData) {
        const panel = document.querySelector(`[data-agent-id="${agentId}"]`);
        if (!panel) return;

        // Update status
        const statusElement = panel.querySelector('.agent-status');
        if (statusElement) {
            statusElement.className = `agent-status ${agentData.status}`;
            statusElement.textContent = agentData.status;
        }

        // Update metrics
        this.updateMetrics(panel, agentData.metrics);
        
        // Update insights
        this.updateInsights(panel, agentData.recent_insights);
        
        // Store agent data
        this.agents.set(agentId, agentData);
    }

    updateMetrics(panel, metrics) {
        const successRateElement = panel.querySelector('.metric-success-rate');
        const responseTimeElement = panel.querySelector('.metric-response-time');
        const requestsElement = panel.querySelector('.metric-requests');
        const errorsElement = panel.querySelector('.metric-errors');

        if (successRateElement) {
            successRateElement.textContent = `${(metrics.success_rate * 100).toFixed(1)}%`;
        }
        if (responseTimeElement) {
            responseTimeElement.textContent = `${metrics.avg_response_time.toFixed(2)}s`;
        }
        if (requestsElement) {
            requestsElement.textContent = metrics.requests_processed;
        }
        if (errorsElement) {
            errorsElement.textContent = metrics.error_count;
        }
    }

    updateInsights(panel, insights) {
        const insightsContainer = panel.querySelector('.agent-insights');
        if (!insightsContainer || !insights) return;

        insightsContainer.innerHTML = '';
        
        insights.slice(0, 3).forEach(insight => {
            const insightElement = this.createInsightElement(insight);
            insightsContainer.appendChild(insightElement);
        });
    }

    createInsightElement(insight) {
        const element = document.createElement('div');
        element.className = 'insight-item';
        
        element.innerHTML = `
            <div class="insight-type">
                ${insight.insight_type.replace('_', ' ')}
                <span class="insight-confidence">${(insight.confidence * 100).toFixed(0)}%</span>
            </div>
            <div class="insight-content">
                ${this.formatInsightData(insight.data)}
            </div>
        `;
        
        return element;
    }

    formatInsightData(data) {
        if (typeof data === 'object') {
            const key = Object.keys(data)[0];
            const value = data[key];
            return `${key}: ${value}`;
        }
        return String(data);
    }

    async executeAgentAction(agentId, action) {
        const panel = document.querySelector(`[data-agent-id="${agentId}"]`);
        if (!panel) return;

        // Show loading state
        this.setAgentLoading(panel, true);

        try {
            const response = await fetch(`/api/agents/${agentId}/action`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]')?.content
                },
                body: JSON.stringify({ action })
            });

            if (!response.ok) throw new Error('Action failed');
            
            const result = await response.json();
            
            // Update panel with results
            if (result.success) {
                this.showSuccessMessage(panel, 'Action completed successfully');
                // Refresh agent data
                await this.refreshAgent(agentId);
            } else {
                this.showErrorMessage(panel, result.error || 'Action failed');
            }
            
        } catch (error) {
            console.error('Agent action error:', error);
            this.showErrorMessage(panel, 'Network error occurred');
        } finally {
            this.setAgentLoading(panel, false);
        }
    }

    async refreshAgent(agentId) {
        const panel = document.querySelector(`[data-agent-id="${agentId}"]`);
        if (!panel) return;

        this.setAgentLoading(panel, true);

        try {
            const response = await fetch(`/api/agents/${agentId}/status`);
            if (!response.ok) throw new Error('Refresh failed');
            
            const agentData = await response.json();
            this.updateAgentPanel(agentId, agentData);
            
        } catch (error) {
            console.error('Agent refresh error:', error);
            this.showErrorMessage(panel, 'Failed to refresh agent');
        } finally {
            this.setAgentLoading(panel, false);
        }
    }

    setAgentLoading(panel, loading) {
        const loadingOverlay = panel.querySelector('.agent-loading-overlay');
        
        if (loading) {
            if (!loadingOverlay) {
                const overlay = document.createElement('div');
                overlay.className = 'agent-loading-overlay';
                overlay.innerHTML = '<div class="agent-loading">Processing...</div>';
                panel.appendChild(overlay);
            }
        } else {
            if (loadingOverlay) {
                loadingOverlay.remove();
            }
        }
    }

    showSuccessMessage(panel, message) {
        this.showMessage(panel, message, 'success');
    }

    showErrorMessage(panel, message) {
        this.showMessage(panel, message, 'error');
    }

    showMessage(panel, message, type) {
        // Remove existing messages
        const existingMessage = panel.querySelector('.agent-message');
        if (existingMessage) existingMessage.remove();

        // Create new message
        const messageElement = document.createElement('div');
        messageElement.className = `agent-message agent-message-${type}`;
        messageElement.textContent = message;
        
        panel.appendChild(messageElement);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (messageElement.parentNode) {
                messageElement.remove();
            }
        }, 3000);
    }

    startPeriodicUpdates() {
        // Update every 30 seconds
        this.updateInterval = setInterval(() => {
            this.updateAgentPanels();
        }, 30000);
        
        // Initial update
        this.updateAgentPanels();
    }

    initializeWebSocket() {
        try {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.location.host}/ws/agents`;
            
            this.websocket = new WebSocket(wsUrl);
            
            this.websocket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                if (data.type === 'agent_update') {
                    this.updateAgentPanel(data.agent_id, data.agent_data);
                }
            };
            
            this.websocket.onerror = (error) => {
                console.log('WebSocket connection not available, using polling only');
            };
            
        } catch (error) {
            console.log('WebSocket not supported, using polling only');
        }
    }

    destroy() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }
        if (this.websocket) {
            this.websocket.close();
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.agentPanelManager = new AgentPanelManager();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (window.agentPanelManager) {
        window.agentPanelManager.destroy();
    }
});
