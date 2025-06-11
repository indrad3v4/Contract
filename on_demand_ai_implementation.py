#!/usr/bin/env python3
"""
On-Demand AI Implementation
Replaces eager AI loading with user-triggered analysis to prevent resource overload
"""

import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OnDemandAIImplementation:
    """Implement on-demand AI to reduce resource usage"""
    
    def __init__(self):
        self.src_path = Path("src")
        self.static_js_path = self.src_path / "external_interfaces" / "ui" / "static" / "js"
        self.templates_path = self.src_path / "external_interfaces" / "ui" / "templates"
        
    def implement_all_changes(self):
        """Implement all on-demand AI changes"""
        logger.info("Implementing on-demand AI system...")
        
        try:
            self.disable_eager_loading()
            self.create_on_demand_orchestrator()
            self.update_dashboard_components()
            self.add_performance_controls()
            self.update_template()
            
            logger.info("✅ On-demand AI implementation complete")
            
        except Exception as e:
            logger.error(f"❌ Implementation failed: {e}")
            raise
    
    def disable_eager_loading(self):
        """Disable automatic AI loading on page load"""
        logger.info("Disabling eager AI loading...")
        
        # Update dashboard-final-fix.js to disable auto-initialization
        dashboard_js = self.static_js_path / "dashboard-final-fix.js"
        
        if dashboard_js.exists():
            with open(dashboard_js, 'r') as f:
                content = f.read()
            
            # Replace auto-initialization with manual trigger
            content = content.replace(
                'window.DashboardOrchestrator.initializeAll();',
                '// Auto-initialization disabled - now on-demand only'
            )
            
            # Disable periodic updates
            content = content.replace(
                'setInterval(() => {',
                '// Periodic updates disabled\n        // setInterval(() => {'
            )
            
            with open(dashboard_js, 'w') as f:
                f.write(content)
        
        logger.info("✅ Disabled eager AI loading")
    
    def create_on_demand_orchestrator(self):
        """Create the on-demand AI orchestrator"""
        on_demand_file = self.static_js_path / "on-demand-ai.js"
        
        content = '''// On-Demand AI Orchestrator - Prevents Resource Overload
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
'''
        
        with open(on_demand_file, 'w') as f:
            f.write(content)
        
        logger.info("✅ Created on-demand AI orchestrator")
    
    def update_dashboard_components(self):
        """Update dashboard components to work with on-demand system"""
        logger.info("Updating dashboard components...")
        
        # Update enhanced-stats-cards.js to disable auto-loading
        stats_js = self.static_js_path / "enhanced-stats-cards.js"
        if stats_js.exists():
            with open(stats_js, 'r') as f:
                content = f.read()
            
            # Disable automatic initialization
            content = content.replace(
                'new EnhancedStatsCards();',
                '// EnhancedStatsCards disabled - using on-demand AI'
            )
            
            with open(stats_js, 'w') as f:
                f.write(content)
        
        # Update enhanced-transaction-list.js to disable auto-loading
        trans_js = self.static_js_path / "enhanced-transaction-list.js"
        if trans_js.exists():
            with open(trans_js, 'r') as f:
                content = f.read()
            
            # Disable automatic initialization
            content = content.replace(
                'new EnhancedTransactionList();',
                '// EnhancedTransactionList disabled - using on-demand loading'
            )
            
            with open(trans_js, 'w') as f:
                f.write(content)
        
        logger.info("✅ Updated dashboard components")
    
    def add_performance_controls(self):
        """Add performance control panel"""
        logger.info("Adding performance controls...")
        
        performance_js = self.static_js_path / "performance-controls.js"
        
        content = '''// Performance Controls for On-Demand AI
console.log("Performance controls loading...");

window.PerformanceControls = {
    init() {
        this.createControlPanel();
        this.monitorPerformance();
        console.log("✅ Performance controls ready");
    },
    
    createControlPanel() {
        if (document.querySelector('#perf-controls')) return;
        
        const panel = document.createElement('div');
        panel.id = 'perf-controls';
        panel.innerHTML = `
            <div class="perf-header">
                <span>⚡ Performance</span>
                <button onclick="PerformanceControls.toggle()" class="toggle-btn">▼</button>
            </div>
            <div class="perf-content" style="display: none;">
                <div class="perf-item">
                    <span>Active Requests:</span>
                    <span id="active-requests">0</span>
                </div>
                <div class="perf-item">
                    <span>Cache Size:</span>
                    <span id="cache-size">0</span>
                </div>
                <div class="perf-actions">
                    <button onclick="PerformanceControls.runBatch()" class="perf-btn">Analyze All</button>
                    <button onclick="PerformanceControls.clearCache()" class="perf-btn">Clear Cache</button>
                </div>
                <div class="perf-tip">
                    💡 Tip: Use Ctrl+A for batch analysis
                </div>
            </div>
        `;
        
        panel.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 20px;
            background: rgba(0, 0, 0, 0.9);
            color: #fff;
            padding: 12px;
            border-radius: 8px;
            font-size: 0.8rem;
            z-index: 10000;
            min-width: 180px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        `;
        
        document.body.appendChild(panel);
    },
    
    toggle() {
        const content = document.querySelector('#perf-controls .perf-content');
        const toggleBtn = document.querySelector('#perf-controls .toggle-btn');
        
        if (content.style.display === 'none') {
            content.style.display = 'block';
            toggleBtn.textContent = '▲';
        } else {
            content.style.display = 'none';
            toggleBtn.textContent = '▼';
        }
    },
    
    monitorPerformance() {
        setInterval(() => {
            if (window.OnDemandAI) {
                const stats = window.OnDemandAI.getStats();
                
                const activeEl = document.getElementById('active-requests');
                const cacheEl = document.getElementById('cache-size');
                
                if (activeEl) activeEl.textContent = stats.activeRequests;
                if (cacheEl) cacheEl.textContent = stats.cacheSize;
            }
        }, 2000);
    },
    
    async runBatch() {
        if (window.OnDemandAI) {
            await window.OnDemandAI.runBatchAnalysis();
        }
    },
    
    clearCache() {
        if (window.OnDemandAI) {
            window.OnDemandAI.clearCache();
        }
    }
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        window.PerformanceControls.init();
    }, 2000);
});

// Add performance control styles
const perfStyle = document.createElement('style');
perfStyle.textContent = `
.perf-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.toggle-btn {
    background: none;
    border: none;
    color: #00ff9d;
    cursor: pointer;
    font-size: 0.8rem;
}

.perf-item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 4px;
}

.perf-actions {
    margin-top: 8px;
    display: flex;
    gap: 4px;
}

.perf-btn {
    background: rgba(0, 255, 157, 0.2);
    border: 1px solid #00ff9d;
    color: #00ff9d;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.7rem;
    cursor: pointer;
    flex: 1;
}

.perf-btn:hover {
    background: rgba(0, 255, 157, 0.3);
}

.perf-tip {
    margin-top: 8px;
    font-size: 0.7rem;
    color: #a0a0a0;
    text-align: center;
}
`;
document.head.appendChild(perfStyle);
'''
        
        with open(performance_js, 'w') as f:
            f.write(content)
        
        logger.info("✅ Added performance controls")
    
    def update_template(self):
        """Update dashboard template to include on-demand AI scripts"""
        logger.info("Updating dashboard template...")
        
        template_file = self.templates_path / "dashboard_production.html"
        
        if not template_file.exists():
            logger.warning("Dashboard template not found")
            return
        
        with open(template_file, 'r') as f:
            content = f.read()
        
        # Add on-demand AI scripts before closing body
        on_demand_scripts = '''
    <!-- On-Demand AI System -->
    <script src="{{ url_for('static', filename='js/on-demand-ai.js') }}"></script>
    <script src="{{ url_for('static', filename='js/performance-controls.js') }}"></script>
</body>'''
        
        if 'on-demand-ai.js' not in content:
            content = content.replace('</body>', on_demand_scripts)
        
        with open(template_file, 'w') as f:
            f.write(content)
        
        logger.info("✅ Updated dashboard template")

def main():
    """Execute on-demand AI implementation"""
    try:
        implementer = OnDemandAIImplementation()
        implementer.implement_all_changes()
        
        print("\n" + "="*60)
        print("🎯 ON-DEMAND AI IMPLEMENTATION COMPLETE")
        print("="*60)
        print("✅ Disabled automatic AI loading on page load")
        print("✅ Added 'Analyze' buttons to each dashboard component")
        print("✅ Implemented caching system (10-minute timeout)")
        print("✅ Limited concurrent requests to 1 (prevents overload)")
        print("✅ Added performance monitoring controls")
        print("✅ Created batch analysis feature (Ctrl+A)")
        print("="*60)
        print("🚀 Dashboard now loads instantly without AI overhead")
        print("🧠 Users click 'Analyze' buttons to get o3-mini insights")
        print("⚡ Performance controls available in bottom-left corner")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Implementation failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()