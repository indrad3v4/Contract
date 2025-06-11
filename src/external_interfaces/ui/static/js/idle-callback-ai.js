// Idle Callback AI Processing - Background AI Execution
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
