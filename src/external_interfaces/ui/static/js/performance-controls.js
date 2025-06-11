// Performance Controls for On-Demand AI
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
