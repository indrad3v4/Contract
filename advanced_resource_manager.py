#!/usr/bin/env python3
"""
Advanced Resource Manager - 10 Additional Optimizations
Fixes grid layout, error handling, component overflow, and performance issues
"""

import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AdvancedResourceManager:
    """Resource management agent for architectural optimization"""
    
    def __init__(self):
        self.src_path = Path("src")
        self.static_css_path = self.src_path / "external_interfaces" / "ui" / "static" / "css"
        self.static_js_path = self.src_path / "external_interfaces" / "ui" / "static" / "js"
        self.templates_path = self.src_path / "external_interfaces" / "ui" / "templates"
        
    def implement_all_optimizations(self):
        """Implement all 10 advanced optimizations"""
        logger.info("Implementing advanced resource optimizations...")
        
        try:
            self.fix_1_grid_template_system()
            self.fix_2_sticky_footer_layout()
            self.fix_3_vertical_bim_assistant()
            self.fix_4_condense_stakeholder_chart()
            self.fix_5_card_body_scroll_limits()
            self.fix_6_error_toast_positioning()
            self.fix_7_idle_callback_ai()
            self.fix_8_collapsible_ai_output()
            self.fix_9_modal_stack_hierarchy()
            self.fix_10_throttled_fetch_queue()
            
            logger.info("✅ All advanced optimizations implemented")
            
        except Exception as e:
            logger.error(f"❌ Advanced optimization failed: {e}")
            raise
    
    def fix_1_grid_template_system(self):
        """Fix 1: Switch to proper CSS Grid system"""
        grid_system_css = self.static_css_path / "grid-template-system.css"
        
        content = '''/* Grid Template System - Proper Container Management */

/* Main dashboard grid container */
.dashboard-container {
    display: grid !important;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    grid-auto-rows: auto;
    gap: 1.5rem;
    padding: 1rem;
    max-width: 100vw;
    overflow-x: hidden;
}

/* Force cards to stay within grid bounds */
.card, .dashboard-card {
    display: flex;
    flex-direction: column;
    min-height: 0; /* Prevents overflow */
    max-width: 100%;
    overflow: hidden;
    contain: layout style paint;
}

/* Card content overflow management */
.card-body {
    flex: 1;
    min-height: 0;
    overflow-y: auto;
    max-height: 400px;
    padding: 1rem;
}

/* Stats cards specific grid */
.stats-cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
}

/* Transaction and chart grid */
.content-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin-bottom: 2rem;
}

/* Single column for mobile */
@media (max-width: 768px) {
    .dashboard-container {
        grid-template-columns: 1fr;
        padding: 0.5rem;
        gap: 1rem;
    }
    
    .content-grid {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
    
    .card-body {
        max-height: 300px;
    }
}

/* Prevent component overflow */
.chart-container,
.transaction-list,
.validator-list {
    max-width: 100%;
    overflow: hidden;
    position: relative;
}

/* Chart specific containment */
canvas {
    max-width: 100% !important;
    height: auto !important;
}

/* BIM assistant containment */
.bim-wrapper {
    display: flex;
    flex-direction: column;
    height: 100%;
    max-height: 400px;
    overflow: hidden;
}

.bim-content {
    flex: 1;
    min-height: 0;
    overflow: auto;
}

/* Stakeholder chart containment */
.stakeholder-chart-wrapper {
    max-width: 100%;
    max-height: 350px;
    overflow: hidden;
    position: relative;
}

/* Force layout containment for all components */
.component-wrapper {
    contain: layout style paint;
    overflow: hidden;
    max-width: 100%;
}
'''
        
        with open(grid_system_css, 'w') as f:
            f.write(content)
        
        logger.info("✅ Fix 1: Grid template system implemented")
    
    def fix_2_sticky_footer_layout(self):
        """Fix 2: Sticky footer that doesn't obstruct content"""
        footer_layout_css = self.static_css_path / "footer-layout.css"
        
        content = '''/* Sticky Footer Layout - Non-obstructive */

/* Main page structure */
html, body {
    height: 100%;
    margin: 0;
    padding: 0;
}

body {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    padding-bottom: 80px; /* Space for footer */
}

/* Main content area */
.main-content {
    flex: 1;
    overflow-y: auto;
    padding-bottom: 2rem;
}

/* Footer positioning */
footer, .footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 60px;
    background: rgba(0, 0, 0, 0.9);
    backdrop-filter: blur(10px);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    z-index: 100;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 0.9rem;
}

/* Sidebar adjustment for sticky footer */
.sidebar {
    margin-bottom: 80px;
}

/* Dashboard wrapper */
.dashboard-wrapper {
    margin-bottom: 2rem;
    min-height: calc(100vh - 140px); /* Account for header and footer */
}

/* Responsive footer */
@media (max-width: 768px) {
    body {
        padding-bottom: 70px;
    }
    
    footer, .footer {
        height: 50px;
        font-size: 0.8rem;
    }
    
    .dashboard-wrapper {
        min-height: calc(100vh - 120px);
    }
}

/* Footer content layout */
.footer-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    max-width: 1200px;
    padding: 0 1rem;
}

.footer-links {
    display: flex;
    gap: 1rem;
}

.footer-links a {
    color: #00ff9d;
    text-decoration: none;
    font-size: 0.8rem;
}

.footer-links a:hover {
    opacity: 0.8;
}
'''
        
        with open(footer_layout_css, 'w') as f:
            f.write(content)
        
        logger.info("✅ Fix 2: Sticky footer layout implemented")
    
    def fix_3_vertical_bim_assistant(self):
        """Fix 3: Vertical BIM assistant layout"""
        bim_vertical_css = self.static_css_path / "bim-vertical.css"
        
        content = '''/* BIM Assistant Vertical Layout */

/* BIM card container */
.bim-assistant-card {
    display: flex;
    flex-direction: column;
    height: 100%;
    max-height: 500px;
    min-height: 400px;
}

/* BIM header */
.bim-header {
    flex-shrink: 0;
    padding: 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 255, 157, 0.1);
}

/* BIM content wrapper */
.bim-wrapper {
    display: flex;
    flex-direction: column;
    flex: 1;
    min-height: 0;
    overflow: hidden;
}

/* 3D viewer area */
.bim-viewer {
    flex: 2;
    min-height: 200px;
    background: #1a1a1a;
    border-radius: 8px;
    margin: 1rem;
    position: relative;
    overflow: hidden;
}

/* BIM controls */
.bim-controls {
    flex-shrink: 0;
    padding: 1rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.3);
}

/* BIM action buttons */
.bim-actions {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-top: 1rem;
}

.bim-btn {
    padding: 0.75rem;
    background: linear-gradient(135deg, #00ff9d, #00d4aa);
    color: #000;
    border: none;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}

.bim-btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0, 255, 157, 0.3);
}

/* BIM status indicator */
.bim-status {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
    font-size: 0.9rem;
}

.bim-status-indicator {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #00ff9d;
    animation: pulse 2s ease-in-out infinite alternate;
}

@keyframes pulse {
    from { opacity: 1; }
    to { opacity: 0.5; }
}

/* Investment integration */
.bim-investment {
    background: rgba(0, 255, 157, 0.05);
    border: 1px solid rgba(0, 255, 157, 0.2);
    border-radius: 6px;
    padding: 1rem;
    margin-top: 1rem;
}

.investment-value {
    font-size: 1.2rem;
    font-weight: 700;
    color: #00ff9d;
    margin-bottom: 0.5rem;
}

/* Mobile responsive */
@media (max-width: 768px) {
    .bim-assistant-card {
        max-height: 400px;
        min-height: 300px;
    }
    
    .bim-viewer {
        min-height: 150px;
        margin: 0.5rem;
    }
    
    .bim-actions {
        flex-direction: row;
        gap: 0.5rem;
    }
    
    .bim-btn {
        flex: 1;
        padding: 0.5rem;
        font-size: 0.8rem;
    }
}
'''
        
        with open(bim_vertical_css, 'w') as f:
            f.write(content)
        
        logger.info("✅ Fix 3: Vertical BIM assistant implemented")
    
    def fix_4_condense_stakeholder_chart(self):
        """Fix 4: Condense stakeholder chart to prevent overflow"""
        stakeholder_css = self.static_css_path / "stakeholder-condense.css"
        
        content = '''/* Stakeholder Chart Condensed Layout */

/* Stakeholder chart container */
.stakeholder-chart-container {
    max-width: 100%;
    max-height: 350px;
    overflow: hidden;
    position: relative;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 8px;
    padding: 1rem;
}

/* Chart wrapper */
.stakeholder-chart-wrapper {
    width: 100%;
    height: 300px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Chart canvas containment */
.stakeholder-chart-wrapper canvas {
    max-width: 100% !important;
    max-height: 100% !important;
    width: auto !important;
    height: auto !important;
}

/* Chart legend positioning */
.chart-legend {
    position: absolute;
    bottom: 10px;
    left: 10px;
    right: 10px;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    justify-content: center;
    font-size: 0.8rem;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.25rem 0.5rem;
    background: rgba(0, 0, 0, 0.5);
    border-radius: 4px;
    backdrop-filter: blur(5px);
}

.legend-color {
    width: 12px;
    height: 12px;
    border-radius: 2px;
}

/* Stakeholder stats */
.stakeholder-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 0.5rem;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.stakeholder-stat {
    text-align: center;
    padding: 0.5rem;
    background: rgba(0, 255, 157, 0.05);
    border-radius: 4px;
}

.stat-value {
    font-size: 1.1rem;
    font-weight: 700;
    color: #00ff9d;
    display: block;
}

.stat-label {
    font-size: 0.75rem;
    color: #a0a0a0;
    margin-top: 0.25rem;
}

/* Mobile responsive */
@media (max-width: 768px) {
    .stakeholder-chart-container {
        max-height: 300px;
        padding: 0.75rem;
    }
    
    .stakeholder-chart-wrapper {
        height: 200px;
    }
    
    .chart-legend {
        font-size: 0.7rem;
        gap: 0.25rem;
    }
    
    .stakeholder-stats {
        grid-template-columns: repeat(2, 1fr);
        gap: 0.25rem;
    }
    
    .stakeholder-stat {
        padding: 0.25rem;
    }
    
    .stat-value {
        font-size: 0.9rem;
    }
}

/* Chart loading state */
.chart-loading {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: #a0a0a0;
    font-size: 0.9rem;
}

.chart-loading::after {
    content: '';
    width: 20px;
    height: 20px;
    border: 2px solid transparent;
    border-top: 2px solid #00ff9d;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-left: 0.5rem;
}

/* Chart error state */
.chart-error {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: #ff4757;
    font-size: 0.9rem;
    text-align: center;
}
'''
        
        with open(stakeholder_css, 'w') as f:
            f.write(content)
        
        logger.info("✅ Fix 4: Stakeholder chart condensed")
    
    def fix_5_card_body_scroll_limits(self):
        """Fix 5: Card body scroll limits to prevent infinite expansion"""
        scroll_limits_css = self.static_css_path / "card-scroll-limits.css"
        
        content = '''/* Card Body Scroll Limits */

/* Universal card body limits */
.card-body {
    max-height: 400px;
    overflow-y: auto;
    overflow-x: hidden;
    scrollbar-width: thin;
    scrollbar-color: #00ff9d transparent;
}

/* Webkit scrollbar styling */
.card-body::-webkit-scrollbar {
    width: 4px;
}

.card-body::-webkit-scrollbar-track {
    background: transparent;
}

.card-body::-webkit-scrollbar-thumb {
    background: #00ff9d;
    border-radius: 2px;
}

.card-body::-webkit-scrollbar-thumb:hover {
    background: #00d4aa;
}

/* Specific component scroll limits */
.recent-transactions-content {
    max-height: 350px;
    overflow-y: auto;
}

.validator-list {
    max-height: 400px;
    overflow-y: auto;
}

.ai-analysis-content {
    max-height: 300px;
    overflow-y: auto;
    word-wrap: break-word;
    overflow-wrap: break-word;
}

/* Transaction item containment */
.transaction-item {
    padding: 0.75rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    word-break: break-all;
    overflow-wrap: break-word;
}

.transaction-item:last-child {
    border-bottom: none;
}

/* Validator item containment */
.validator-item {
    padding: 0.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Text overflow handling */
.text-overflow {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.text-wrap {
    word-wrap: break-word;
    overflow-wrap: break-word;
    hyphens: auto;
}

/* Long content fade effect */
.fade-bottom {
    position: relative;
}

.fade-bottom::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 20px;
    background: linear-gradient(transparent, rgba(0, 0, 0, 0.8));
    pointer-events: none;
}

/* Mobile scroll adjustments */
@media (max-width: 768px) {
    .card-body {
        max-height: 300px;
    }
    
    .recent-transactions-content {
        max-height: 250px;
    }
    
    .validator-list {
        max-height: 300px;
    }
    
    .ai-analysis-content {
        max-height: 200px;
    }
}

/* Scroll indicators */
.scroll-indicator {
    position: absolute;
    right: 8px;
    top: 50%;
    transform: translateY(-50%);
    color: #00ff9d;
    font-size: 0.8rem;
    opacity: 0.6;
    pointer-events: none;
}

/* Content containers */
.content-container {
    position: relative;
    max-height: inherit;
    overflow: hidden;
}

/* Expand/collapse functionality */
.expandable-content {
    max-height: 200px;
    overflow: hidden;
    transition: max-height 0.3s ease;
}

.expandable-content.expanded {
    max-height: 500px;
}

.expand-toggle {
    background: none;
    border: none;
    color: #00ff9d;
    cursor: pointer;
    font-size: 0.8rem;
    padding: 0.5rem;
    text-decoration: underline;
}

.expand-toggle:hover {
    opacity: 0.8;
}
'''
        
        with open(scroll_limits_css, 'w') as f:
            f.write(content)
        
        logger.info("✅ Fix 5: Card scroll limits implemented")
    
    def fix_6_error_toast_positioning(self):
        """Fix 6: Move error toasts to top-center position"""
        toast_positioning_css = self.static_css_path / "toast-positioning.css"
        
        content = '''/* Error Toast Positioning - Top Center */

/* Toast container */
.toast-container {
    position: fixed;
    top: 1rem;
    left: 50%;
    transform: translateX(-50%);
    z-index: 9999;
    pointer-events: none;
    max-width: 500px;
    width: 90%;
}

/* Individual toast */
.toast, .error-toast, .success-toast, .warning-toast {
    background: rgba(0, 0, 0, 0.9);
    backdrop-filter: blur(10px);
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 0.5rem;
    border-left: 4px solid #ff4757;
    color: #fff;
    font-size: 0.9rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    animation: slideDown 0.3s ease;
    pointer-events: auto;
    position: relative;
    max-width: 100%;
    word-wrap: break-word;
}

/* Toast types */
.success-toast {
    border-left-color: #00ff9d;
}

.warning-toast {
    border-left-color: #ffa500;
}

.info-toast {
    border-left-color: #4a90e2;
}

/* Toast animations */
@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes slideUp {
    from {
        opacity: 1;
        transform: translateY(0);
    }
    to {
        opacity: 0;
        transform: translateY(-20px);
    }
}

.toast.fade-out {
    animation: slideUp 0.3s ease forwards;
}

/* Toast close button */
.toast-close {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    background: none;
    border: none;
    color: #fff;
    cursor: pointer;
    font-size: 1.2rem;
    line-height: 1;
    opacity: 0.7;
    padding: 0;
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.toast-close:hover {
    opacity: 1;
}

/* Toast content */
.toast-content {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    margin-right: 2rem;
}

.toast-icon {
    flex-shrink: 0;
    font-size: 1.1rem;
}

.toast-message {
    flex: 1;
    line-height: 1.4;
}

.toast-title {
    font-weight: 600;
    margin-bottom: 0.25rem;
}

/* Error-specific styling */
.keplr-error, .wallet-error {
    border-left-color: #ff6b7a;
    background: rgba(255, 107, 122, 0.1);
}

.ai-error {
    border-left-color: #ffa500;
    background: rgba(255, 165, 0, 0.1);
}

.network-error {
    border-left-color: #ff4757;
    background: rgba(255, 71, 87, 0.1);
}

/* Mobile responsive */
@media (max-width: 768px) {
    .toast-container {
        top: 0.5rem;
        width: 95%;
        max-width: none;
    }
    
    .toast {
        padding: 0.75rem;
        font-size: 0.8rem;
    }
    
    .toast-content {
        gap: 0.5rem;
        margin-right: 1.5rem;
    }
    
    .toast-close {
        top: 0.25rem;
        right: 0.25rem;
        font-size: 1rem;
    }
}

/* Toast progress bar */
.toast-progress {
    position: absolute;
    bottom: 0;
    left: 0;
    height: 3px;
    background: #00ff9d;
    border-radius: 0 0 8px 8px;
    animation: progressBar 5s linear forwards;
}

@keyframes progressBar {
    from { width: 100%; }
    to { width: 0%; }
}

/* Stack management */
.toast:nth-child(1) { z-index: 9999; }
.toast:nth-child(2) { z-index: 9998; }
.toast:nth-child(3) { z-index: 9997; }
.toast:nth-child(4) { z-index: 9996; }
.toast:nth-child(5) { z-index: 9995; }
'''
        
        with open(toast_positioning_css, 'w') as f:
            f.write(content)
        
        logger.info("✅ Fix 6: Error toast positioning implemented")
    
    def fix_7_idle_callback_ai(self):
        """Fix 7: Use requestIdleCallback for AI processing"""
        idle_callback_js = self.static_js_path / "idle-callback-ai.js"
        
        content = '''// Idle Callback AI Processing - Background AI Execution
console.log("Idle callback AI system loading...");

window.IdleCallbackAI = {
    taskQueue: [],
    isProcessing: false,
    maxIdleTime: 50, // milliseconds
    
    init() {
        this.interceptAIOperations();
        this.startIdleProcessor();
        console.log("✅ Idle callback AI system active");
    },
    
    interceptAIOperations() {
        // Intercept OnDemandAI operations
        if (window.OnDemandAI) {
            const originalRunAnalysis = window.OnDemandAI.runAnalysis;
            
            window.OnDemandAI.runAnalysis = (cardId, button) => {
                this.scheduleIdleTask(() => {
                    return originalRunAnalysis.call(window.OnDemandAI, cardId, button);
                }, 'ai-analysis', { cardId, button });
            };
        }
        
        // Intercept Chart.js operations
        if (window.Chart) {
            const originalChartCreate = window.Chart;
            
            window.Chart = function(...args) {
                const instance = new originalChartCreate(...args);
                
                // Defer chart rendering
                if (instance.render) {
                    const originalRender = instance.render;
                    instance.render = () => {
                        window.IdleCallbackAI.scheduleIdleTask(() => {
                            originalRender.call(instance);
                        }, 'chart-render');
                    };
                }
                
                return instance;
            };
            
            Object.setPrototypeOf(window.Chart, originalChartCreate);
            Object.assign(window.Chart, originalChartCreate);
        }
    },
    
    scheduleIdleTask(taskFunction, taskType, metadata = {}) {
        const task = {
            id: Date.now() + Math.random(),
            function: taskFunction,
            type: taskType,
            metadata: metadata,
            priority: this.getTaskPriority(taskType),
            timestamp: Date.now()
        };
        
        this.taskQueue.push(task);
        this.taskQueue.sort((a, b) => b.priority - a.priority);
        
        if (!this.isProcessing) {
            this.processNextIdleTask();
        }
    },
    
    getTaskPriority(taskType) {
        const priorities = {
            'user-interaction': 100,
            'ai-analysis': 80,
            'chart-render': 60,
            'data-processing': 40,
            'background-sync': 20
        };
        
        return priorities[taskType] || 50;
    },
    
    processNextIdleTask() {
        if (this.taskQueue.length === 0) {
            this.isProcessing = false;
            return;
        }
        
        this.isProcessing = true;
        
        if (window.requestIdleCallback) {
            window.requestIdleCallback((deadline) => {
                this.executeTasksInIdleTime(deadline);
            }, { timeout: 1000 });
        } else {
            // Fallback for browsers without requestIdleCallback
            setTimeout(() => {
                this.executeTasksInIdleTime({ timeRemaining: () => this.maxIdleTime });
            }, 0);
        }
    },
    
    executeTasksInIdleTime(deadline) {
        while (deadline.timeRemaining() > 5 && this.taskQueue.length > 0) {
            const task = this.taskQueue.shift();
            
            try {
                const startTime = performance.now();
                
                // Execute task
                if (typeof task.function === 'function') {
                    const result = task.function();
                    
                    // Handle promises
                    if (result instanceof Promise) {
                        result.catch(error => {
                            console.warn(`Idle task ${task.type} failed:`, error);
                        });
                    }
                }
                
                const executionTime = performance.now() - startTime;
                this.logTaskExecution(task, executionTime);
                
            } catch (error) {
                console.warn(`Idle task ${task.type} failed:`, error);
            }
        }
        
        // Continue processing if there are more tasks
        if (this.taskQueue.length > 0) {
            this.processNextIdleTask();
        } else {
            this.isProcessing = false;
        }
    },
    
    logTaskExecution(task, executionTime) {
        if (window.PerformanceMonitor) {
            window.PerformanceMonitor.recordTaskExecution(task.type, executionTime);
        }
    },
    
    // High-priority task for immediate execution
    executeImmediate(taskFunction, taskType = 'user-interaction') {
        this.scheduleIdleTask(taskFunction, taskType);
        
        // Force immediate processing if idle
        if (!this.isProcessing && window.requestIdleCallback) {
            window.requestIdleCallback((deadline) => {
                this.executeTasksInIdleTime(deadline);
            });
        }
    },
    
    // Cancel tasks by type
    cancelTasksByType(taskType) {
        this.taskQueue = this.taskQueue.filter(task => task.type !== taskType);
    },
    
    // Get queue status
    getQueueStatus() {
        return {
            queueLength: this.taskQueue.length,
            isProcessing: this.isProcessing,
            taskTypes: this.taskQueue.map(task => task.type)
        };
    },
    
    // Clear all pending tasks
    clearQueue() {
        this.taskQueue = [];
        this.isProcessing = false;
    }
};

// Auto-initialize
document.addEventListener('DOMContentLoaded', () => {
    window.IdleCallbackAI.init();
});

// Expose global helper for immediate tasks
window.scheduleIdleTask = (fn, type, metadata) => {
    if (window.IdleCallbackAI) {
        window.IdleCallbackAI.scheduleIdleTask(fn, type, metadata);
    } else {
        setTimeout(fn, 0);
    }
};

window.executeImmediate = (fn, type) => {
    if (window.IdleCallbackAI) {
        window.IdleCallbackAI.executeImmediate(fn, type);
    } else {
        fn();
    }
};
'''
        
        with open(idle_callback_js, 'w') as f:
            f.write(content)
        
        logger.info("✅ Fix 7: Idle callback AI implemented")
    
    def fix_8_collapsible_ai_output(self):
        """Fix 8: Collapsible AI output panels"""
        collapsible_ai_js = self.static_js_path / "collapsible-ai.js"
        
        content = '''// Collapsible AI Output - Prevents UI Overflow
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
'''
        
        with open(collapsible_ai_js, 'w') as f:
            f.write(content)
        
        logger.info("✅ Fix 8: Collapsible AI output implemented")
    
    def fix_9_modal_stack_hierarchy(self):
        """Fix 9: Modal z-index hierarchy management"""
        modal_stack_js = self.static_js_path / "modal-stack.js"
        
        content = '''// Modal Stack Management - Proper Z-index Hierarchy
console.log("Modal stack management loading...");

window.ModalStackManager = {
    modalStack: [],
    baseZIndex: 1040,
    
    init() {
        this.setupModalInterception();
        this.fixExistingModals();
        console.log("✅ Modal stack manager active");
    },
    
    setupModalInterception() {
        // Intercept Bootstrap modal events
        document.addEventListener('show.bs.modal', (e) => {
            this.onModalShow(e.target);
        });
        
        document.addEventListener('hide.bs.modal', (e) => {
            this.onModalHide(e.target);
        });
        
        // Intercept custom modal operations
        document.addEventListener('click', (e) => {
            if (e.target.matches('.modal-trigger, [data-modal]')) {
                const modalId = e.target.dataset.modal || e.target.getAttribute('href')?.substring(1);
                if (modalId) {
                    const modal = document.getElementById(modalId);
                    if (modal) {
                        this.showModal(modal);
                    }
                }
            } else if (e.target.matches('.modal-close, .modal-dismiss')) {
                const modal = e.target.closest('.modal');
                if (modal) {
                    this.hideModal(modal);
                }
            }
        });
        
        // Handle Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.modalStack.length > 0) {
                const topModal = this.modalStack[this.modalStack.length - 1];
                this.hideModal(topModal.element);
            }
        });
    },
    
    fixExistingModals() {
        const modals = document.querySelectorAll('.modal');
        
        modals.forEach(modal => {
            this.prepareModal(modal);
        });
    },
    
    prepareModal(modal) {
        // Ensure proper structure
        if (!modal.querySelector('.modal-dialog')) {
            const content = modal.innerHTML;
            modal.innerHTML = `
                <div class="modal-dialog">
                    <div class="modal-content">
                        ${content}
                    </div>
                </div>
            `;
        }
        
        // Add backdrop if missing
        if (!modal.querySelector('.modal-backdrop')) {
            const backdrop = document.createElement('div');
            backdrop.className = 'modal-backdrop';
            backdrop.onclick = () => this.hideModal(modal);
            modal.appendChild(backdrop);
        }
        
        // Add close button if missing
        if (!modal.querySelector('.modal-close')) {
            const closeBtn = document.createElement('button');
            closeBtn.className = 'modal-close';
            closeBtn.innerHTML = '×';
            closeBtn.onclick = () => this.hideModal(modal);
            
            const modalContent = modal.querySelector('.modal-content');
            if (modalContent) {
                modalContent.insertBefore(closeBtn, modalContent.firstChild);
            }
        }
    },
    
    onModalShow(modal) {
        this.showModal(modal);
    },
    
    onModalHide(modal) {
        this.hideModal(modal);
    },
    
    showModal(modal) {
        if (!modal) return;
        
        this.prepareModal(modal);
        
        const zIndex = this.baseZIndex + (this.modalStack.length * 10);
        const backdropZIndex = zIndex - 5;
        
        // Set z-indexes
        modal.style.zIndex = zIndex;
        
        const backdrop = modal.querySelector('.modal-backdrop');
        if (backdrop) {
            backdrop.style.zIndex = backdropZIndex;
        }
        
        // Add to stack
        const modalData = {
            element: modal,
            zIndex: zIndex,
            timestamp: Date.now()
        };
        
        this.modalStack.push(modalData);
        
        // Show modal
        modal.classList.add('show');
        modal.style.display = 'block';
        
        // Disable body scroll
        document.body.style.overflow = 'hidden';
        
        // Focus management
        const firstFocusable = modal.querySelector('button, input, select, textarea, [tabindex]:not([tabindex="-1"])');
        if (firstFocusable) {
            firstFocusable.focus();
        }
    },
    
    hideModal(modal) {
        if (!modal) return;
        
        // Remove from stack
        const index = this.modalStack.findIndex(item => item.element === modal);
        if (index >= 0) {
            this.modalStack.splice(index, 1);
        }
        
        // Hide modal
        modal.classList.remove('show');
        modal.style.display = 'none';
        
        // Re-enable body scroll if no modals
        if (this.modalStack.length === 0) {
            document.body.style.overflow = '';
        }
        
        // Focus management - return to previous modal or body
        if (this.modalStack.length > 0) {
            const topModal = this.modalStack[this.modalStack.length - 1];
            topModal.element.focus();
        } else {
            document.body.focus();
        }
    },
    
    hideAllModals() {
        while (this.modalStack.length > 0) {
            const modal = this.modalStack[this.modalStack.length - 1];
            this.hideModal(modal.element);
        }
    },
    
    getActiveModals() {
        return this.modalStack.map(item => ({
            id: item.element.id,
            zIndex: item.zIndex,
            timestamp: item.timestamp
        }));
    }
};

// Auto-initialize
document.addEventListener('DOMContentLoaded', () => {
    window.ModalStackManager.init();
});

// Global modal controls
window.showModal = (modalId) => {
    const modal = document.getElementById(modalId);
    if (modal && window.ModalStackManager) {
        window.ModalStackManager.showModal(modal);
    }
};

window.hideModal = (modalId) => {
    const modal = typeof modalId === 'string' ? document.getElementById(modalId) : modalId;
    if (modal && window.ModalStackManager) {
        window.ModalStackManager.hideModal(modal);
    }
};

// Add modal CSS
const modalStyle = document.createElement('style');
modalStyle.textContent = `
.modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: none;
    align-items: center;
    justify-content: center;
    z-index: 1050;
}

.modal.show {
    display: flex;
}

.modal-backdrop {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(5px);
    z-index: 1040;
}

.modal-dialog {
    position: relative;
    z-index: 1051;
    max-width: 90%;
    max-height: 90%;
    overflow: auto;
}

.modal-content {
    background: rgba(0, 0, 0, 0.95);
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    position: relative;
    padding: 2rem;
    color: #fff;
}

.modal-close {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: none;
    border: none;
    color: #fff;
    font-size: 1.5rem;
    cursor: pointer;
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: background 0.2s ease;
}

.modal-close:hover {
    background: rgba(255, 255, 255, 0.1);
}
`;
document.head.appendChild(modalStyle);
'''
        
        with open(modal_stack_js, 'w') as f:
            f.write(content)
        
        logger.info("✅ Fix 9: Modal stack hierarchy implemented")
    
    def fix_10_throttled_fetch_queue(self):
        """Fix 10: Throttled fetch queue to prevent API overload"""
        fetch_queue_js = self.static_js_path / "fetch-queue.js"
        
        content = '''// Throttled Fetch Queue - Prevents API Overload
console.log("Throttled fetch queue loading...");

window.FetchQueueManager = {
    queue: [],
    activeRequests: 0,
    maxConcurrent: 2,
    requestDelay: 300, // ms between requests
    lastRequestTime: 0,
    
    init() {
        this.interceptFetch();
        this.startQueueProcessor();
        console.log("✅ Fetch queue manager active");
    },
    
    interceptFetch() {
        const originalFetch = window.fetch;
        
        window.fetch = (...args) => {
            return this.queuedFetch(originalFetch, ...args);
        };
    },
    
    queuedFetch(originalFetch, ...args) {
        return new Promise((resolve, reject) => {
            const request = {
                id: Date.now() + Math.random(),
                originalFetch,
                args,
                resolve,
                reject,
                timestamp: Date.now(),
                priority: this.getRequestPriority(args[0])
            };
            
            this.queue.push(request);
            this.queue.sort((a, b) => b.priority - a.priority);
            
            this.processQueue();
        });
    },
    
    getRequestPriority(url) {
        if (typeof url === 'string') {
            if (url.includes('/orchestrator/')) return 100; // AI requests
            if (url.includes('/blockchain/stats')) return 80; // Stats
            if (url.includes('/rpc/')) return 60; // RPC calls
            if (url.includes('/bim-agent/')) return 40; // BIM
        }
        return 50; // Default priority
    },
    
    processQueue() {
        if (this.activeRequests >= this.maxConcurrent || this.queue.length === 0) {
            return;
        }
        
        const now = Date.now();
        const timeSinceLastRequest = now - this.lastRequestTime;
        
        if (timeSinceLastRequest < this.requestDelay) {
            setTimeout(() => this.processQueue(), this.requestDelay - timeSinceLastRequest);
            return;
        }
        
        const request = this.queue.shift();
        this.executeRequest(request);
    },
    
    async executeRequest(request) {
        this.activeRequests++;
        this.lastRequestTime = Date.now();
        
        try {
            const response = await request.originalFetch(...request.args);
            request.resolve(response);
            
            // Log successful request
            this.logRequest(request, 'success');
            
        } catch (error) {
            request.reject(error);
            
            // Log failed request
            this.logRequest(request, 'error', error);
            
        } finally {
            this.activeRequests--;
            
            // Process next request after delay
            setTimeout(() => this.processQueue(), this.requestDelay);
        }
    },
    
    logRequest(request, status, error = null) {
        const url = typeof request.args[0] === 'string' ? request.args[0] : 'unknown';
        const duration = Date.now() - request.timestamp;
        
        if (window.PerformanceMonitor) {
            window.PerformanceMonitor.recordRequest(url, status, duration);
        }
        
        if (status === 'error') {
            console.warn(`Fetch failed for ${url}:`, error);
        }
    },
    
    startQueueProcessor() {
        // Periodic queue processing
        setInterval(() => {
            this.processQueue();
        }, 100);
    },
    
    // Priority fetch for critical requests
    priorityFetch(...args) {
        const originalFetch = window.fetch.__original || fetch;
        
        return new Promise((resolve, reject) => {
            const request = {
                id: Date.now() + Math.random(),
                originalFetch,
                args,
                resolve,
                reject,
                timestamp: Date.now(),
                priority: 1000 // Highest priority
            };
            
            this.queue.unshift(request); // Add to front
            this.processQueue();
        });
    },
    
    // Batch fetch for multiple requests
    batchFetch(requests) {
        const promises = requests.map(request => {
            if (Array.isArray(request)) {
                return this.queuedFetch(window.fetch.__original || fetch, ...request);
            } else {
                return this.queuedFetch(window.fetch.__original || fetch, request);
            }
        });
        
        return Promise.all(promises);
    },
    
    // Cancel requests by URL pattern
    cancelRequests(urlPattern) {
        this.queue = this.queue.filter(request => {
            const url = typeof request.args[0] === 'string' ? request.args[0] : '';
            
            if (url.includes(urlPattern)) {
                request.reject(new Error('Request cancelled'));
                return false;
            }
            
            return true;
        });
    },
    
    // Get queue status
    getStatus() {
        return {
            queueLength: this.queue.length,
            activeRequests: this.activeRequests,
            maxConcurrent: this.maxConcurrent,
            requestDelay: this.requestDelay
        };
    },
    
    // Adjust throttling parameters
    setThrottling(maxConcurrent, requestDelay) {
        this.maxConcurrent = maxConcurrent;
        this.requestDelay = requestDelay;
    },
    
    // Clear queue
    clearQueue() {
        this.queue.forEach(request => {
            request.reject(new Error('Queue cleared'));
        });
        this.queue = [];
    }
};

// Store original fetch for priority requests
if (!window.fetch.__original) {
    window.fetch.__original = window.fetch;
}

// Auto-initialize
document.addEventListener('DOMContentLoaded', () => {
    window.FetchQueueManager.init();
});

// Global helpers
window.priorityFetch = (...args) => {
    if (window.FetchQueueManager) {
        return window.FetchQueueManager.priorityFetch(...args);
    }
    return fetch(...args);
};

window.batchFetch = (requests) => {
    if (window.FetchQueueManager) {
        return window.FetchQueueManager.batchFetch(requests);
    }
    return Promise.all(requests.map(req => fetch(req)));
};

// Expose queue management
window.getFetchQueueStatus = () => {
    return window.FetchQueueManager?.getStatus() || { error: 'Queue manager not initialized' };
};
'''
        
        with open(fetch_queue_js, 'w') as f:
            f.write(content)
        
        logger.info("✅ Fix 10: Throttled fetch queue implemented")
    
    def update_template_with_fixes(self):
        """Update template to include all advanced fixes"""
        template_file = self.templates_path / "dashboard_production.html"
        
        if not template_file.exists():
            logger.warning("Template not found")
            return
        
        with open(template_file, 'r') as f:
            content = f.read()
        
        # Add advanced optimization scripts and styles
        advanced_includes = '''
    <!-- Advanced Resource Management -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/grid-template-system.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/footer-layout.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/bim-vertical.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/stakeholder-condense.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/card-scroll-limits.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/toast-positioning.css') }}">
    
    <script src="{{ url_for('static', filename='js/idle-callback-ai.js') }}"></script>
    <script src="{{ url_for('static', filename='js/collapsible-ai.js') }}"></script>
    <script src="{{ url_for('static', filename='js/modal-stack.js') }}"></script>
    <script src="{{ url_for('static', filename='js/fetch-queue.js') }}"></script>
</body>'''
        
        if 'grid-template-system.css' not in content:
            content = content.replace('</body>', advanced_includes)
        
        # Update dashboard container structure
        if 'dashboard-container' in content:
            content = content.replace(
                'class="dashboard-container"',
                'class="dashboard-container main-content"'
            )
        
        # Add proper footer structure if missing
        if '<footer' not in content and '</body>' in content:
            footer_html = '''
    <footer class="footer">
        <div class="footer-content">
            <span>DAODISEO - Blockchain Real Estate Investment Platform</span>
            <div class="footer-links">
                <a href="#privacy">Privacy</a>
                <a href="#terms">Terms</a>
                <a href="#support">Support</a>
            </div>
        </div>
    </footer>
</body>'''
            content = content.replace('</body>', footer_html)
        
        with open(template_file, 'w') as f:
            f.write(content)
        
        logger.info("✅ Template updated with advanced fixes")

def main():
    """Execute all advanced resource optimizations"""
    try:
        manager = AdvancedResourceManager()
        manager.implement_all_optimizations()
        manager.update_template_with_fixes()
        
        print("\n" + "="*80)
        print("🎯 ADVANCED RESOURCE MANAGEMENT COMPLETE")
        print("="*80)
        print("✅ 1. Grid Template System: Proper container management prevents overflow")
        print("✅ 2. Sticky Footer Layout: Non-obstructive footer positioning")
        print("✅ 3. Vertical BIM Assistant: Contained 3D viewer with proper controls")
        print("✅ 4. Condensed Stakeholder Chart: Fixed chart bleeding and sizing")
        print("✅ 5. Card Scroll Limits: Prevents infinite expansion with scrollable content")
        print("✅ 6. Error Toast Positioning: Top-center error messages")
        print("✅ 7. Idle Callback AI: Background AI processing prevents UI blocking")
        print("✅ 8. Collapsible AI Output: Expandable panels prevent content overflow")
        print("✅ 9. Modal Stack Hierarchy: Proper z-index management for overlays")
        print("✅ 10. Throttled Fetch Queue: API request limiting prevents overload")
        print("="*80)
        print("🚀 Dashboard should now have proper layout containment")
        print("⚡ Components stay within borders, errors show properly")
        print("🧠 AI processing happens in background without blocking UI")
        print("📱 Responsive design works correctly on all screen sizes")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ Advanced optimization failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()