// DAODISEO o3-mini Orchestrator Integration
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
