// Collapsible AI Output - Prevents UI Overflow
console.log("Collapsible AI output system loading...");

window.CollapsibleAI = {
    expandedPanels: new Set(),
    
    init() {
        this.setupCollapsiblePanels();
        this.interceptAIOutput();
        console.log("✅ Collapsible AI system active");
    },
    
    setupCollapsiblePanels() {
        // Find all AI output containers
        const aiContainers = document.querySelectorAll('.ai-insight, .ai-analysis, .ai-output');
        
        aiContainers.forEach(container => {
            this.makeCollapsible(container);
        });
    },
    
    makeCollapsible(container) {
        if (container.querySelector('.ai-toggle')) return; // Already collapsible
        
        const content = container.innerHTML;
        const containerId = this.generateId(container);
        
        container.innerHTML = `
            <div class="ai-panel-header">
                <button class="ai-toggle" data-target="${containerId}">
                    <span class="ai-toggle-icon">▼</span>
                    <span class="ai-toggle-text">AI Analysis</span>
                </button>
                <div class="ai-panel-status">
                    <span class="ai-confidence"></span>
                    <span class="ai-timestamp"></span>
                </div>
            </div>
            <div class="ai-panel-content collapsed" id="${containerId}">
                ${content}
            </div>
        `;
        
        // Add event listener
        const toggle = container.querySelector('.ai-toggle');
        toggle.addEventListener('click', (e) => {
            e.preventDefault();
            this.togglePanel(containerId);
        });
    },
    
    generateId(container) {
        const cardId = container.closest('[data-card-id]')?.dataset.cardId || 'unknown';
        return `ai-panel-${cardId}-${Date.now()}`;
    },
    
    togglePanel(panelId) {
        const panel = document.getElementById(panelId);
        const toggle = document.querySelector(`[data-target="${panelId}"]`);
        
        if (!panel || !toggle) return;
        
        const isExpanded = this.expandedPanels.has(panelId);
        
        if (isExpanded) {
            this.collapsePanel(panelId, panel, toggle);
        } else {
            this.expandPanel(panelId, panel, toggle);
        }
    },
    
    expandPanel(panelId, panel, toggle) {
        panel.classList.remove('collapsed');
        panel.classList.add('expanded');
        
        toggle.querySelector('.ai-toggle-icon').textContent = '▲';
        toggle.querySelector('.ai-toggle-text').textContent = 'Hide Analysis';
        
        this.expandedPanels.add(panelId);
        
        // Animate expansion
        panel.style.maxHeight = panel.scrollHeight + 'px';
    },
    
    collapsePanel(panelId, panel, toggle) {
        panel.classList.remove('expanded');
        panel.classList.add('collapsed');
        
        toggle.querySelector('.ai-toggle-icon').textContent = '▼';
        toggle.querySelector('.ai-toggle-text').textContent = 'Show Analysis';
        
        this.expandedPanels.delete(panelId);
        
        // Animate collapse
        panel.style.maxHeight = '0px';
    },
    
    interceptAIOutput() {
        // Intercept AI output creation
        const originalAddAIInsight = window.OnDemandAI?.addAIInsight;
        
        if (originalAddAIInsight) {
            window.OnDemandAI.addAIInsight = (card, data, metadata) => {
                // Call original function
                originalAddAIInsight.call(window.OnDemandAI, card, data, metadata);
                
                // Make the new insight collapsible
                setTimeout(() => {
                    const insight = card.querySelector('.ai-insight:last-child');
                    if (insight) {
                        this.makeCollapsible(insight);
                        this.updatePanelStatus(insight, metadata);
                    }
                }, 100);
            };
        }
    },
    
    updatePanelStatus(container, metadata) {
        const confidenceEl = container.querySelector('.ai-confidence');
        const timestampEl = container.querySelector('.ai-timestamp');
        
        if (confidenceEl && metadata?.confidence) {
            confidenceEl.textContent = `${Math.round(metadata.confidence * 100)}% confident`;
        }
        
        if (timestampEl) {
            timestampEl.textContent = new Date().toLocaleTimeString();
        }
    },
    
    collapseAll() {
        this.expandedPanels.forEach(panelId => {
            const panel = document.getElementById(panelId);
            const toggle = document.querySelector(`[data-target="${panelId}"]`);
            
            if (panel && toggle) {
                this.collapsePanel(panelId, panel, toggle);
            }
        });
    },
    
    expandAll() {
        const allPanels = document.querySelectorAll('.ai-panel-content');
        
        allPanels.forEach(panel => {
            const panelId = panel.id;
            const toggle = document.querySelector(`[data-target="${panelId}"]`);
            
            if (toggle) {
                this.expandPanel(panelId, panel, toggle);
            }
        });
    }
};

// Auto-initialize
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        window.CollapsibleAI.init();
    }, 1500);
});

// Global controls
window.collapseAllAI = () => window.CollapsibleAI?.collapseAll();
window.expandAllAI = () => window.CollapsibleAI?.expandAll();

// Add CSS styles
const collapsibleStyle = document.createElement('style');
collapsibleStyle.textContent = `
.ai-panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem;
    background: rgba(0, 255, 157, 0.1);
    border-radius: 6px 6px 0 0;
    border-bottom: 1px solid rgba(0, 255, 157, 0.2);
}

.ai-toggle {
    background: none;
    border: none;
    color: #00ff9d;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;
    font-weight: 600;
    padding: 0;
}

.ai-toggle:hover {
    opacity: 0.8;
}

.ai-toggle-icon {
    transition: transform 0.2s ease;
    font-size: 0.8rem;
}

.ai-panel-status {
    display: flex;
    gap: 1rem;
    font-size: 0.75rem;
    color: #a0a0a0;
}

.ai-panel-content {
    overflow: hidden;
    transition: max-height 0.3s ease;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 0 0 6px 6px;
}

.ai-panel-content.collapsed {
    max-height: 0;
}

.ai-panel-content.expanded {
    max-height: 500px;
    padding: 1rem;
}

.ai-confidence {
    color: #00ff9d;
    font-weight: 600;
}
`;
document.head.appendChild(collapsibleStyle);
