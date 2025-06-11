// Web Worker Manager - Offloads Heavy Computations
console.log("Web worker manager loading...");

window.WebWorkerManager = {
    workers: new Map(),
    
    init() {
        this.createDataProcessingWorker();
        this.setupWorkerCommunication();
        console.log("✅ Web worker manager active");
    },
    
    createDataProcessingWorker() {
        // Create worker for data processing
        const workerCode = `
            self.onmessage = function(e) {
                const { type, data, id } = e.data;
                
                try {
                    let result;
                    
                    switch(type) {
                        case 'processChartData':
                            result = processChartData(data);
                            break;
                        case 'formatLargeNumbers':
                            result = formatLargeNumbers(data);
                            break;
                        case 'calculateMetrics':
                            result = calculateMetrics(data);
                            break;
                        default:
                            throw new Error('Unknown task type: ' + type);
                    }
                    
                    self.postMessage({ success: true, result, id });
                } catch (error) {
                    self.postMessage({ success: false, error: error.message, id });
                }
            };
            
            function processChartData(data) {
                // Process chart data without blocking UI
                return data.map(item => ({
                    ...item,
                    processed: true,
                    timestamp: Date.now()
                }));
            }
            
            function formatLargeNumbers(numbers) {
                return numbers.map(num => {
                    if (num >= 1000000) {
                        return (num / 1000000).toFixed(1) + 'M';
                    } else if (num >= 1000) {
                        return (num / 1000).toFixed(1) + 'K';
                    }
                    return num.toString();
                });
            }
            
            function calculateMetrics(data) {
                // Heavy calculation example
                const result = {
                    total: data.reduce((sum, item) => sum + (item.value || 0), 0),
                    average: 0,
                    max: Math.max(...data.map(item => item.value || 0)),
                    min: Math.min(...data.map(item => item.value || 0))
                };
                
                result.average = result.total / data.length;
                
                return result;
            }
        `;
        
        const blob = new Blob([workerCode], { type: 'application/javascript' });
        const worker = new Worker(URL.createObjectURL(blob));
        
        this.workers.set('dataProcessor', worker);
    },
    
    setupWorkerCommunication() {
        this.workers.forEach((worker, name) => {
            worker.onmessage = (e) => {
                this.handleWorkerMessage(name, e.data);
            };
            
            worker.onerror = (error) => {
                console.error(`Worker ${name} error:`, error);
            };
        });
    },
    
    handleWorkerMessage(workerName, data) {
        const { success, result, error, id } = data;
        
        if (success) {
            this.resolveTask(id, result);
        } else {
            this.rejectTask(id, new Error(error));
        }
    },
    
    pendingTasks: new Map(),
    taskIdCounter: 0,
    
    runTask(workerName, taskType, taskData) {
        return new Promise((resolve, reject) => {
            const taskId = ++this.taskIdCounter;
            this.pendingTasks.set(taskId, { resolve, reject });
            
            const worker = this.workers.get(workerName);
            if (!worker) {
                reject(new Error(`Worker ${workerName} not found`));
                return;
            }
            
            worker.postMessage({
                type: taskType,
                data: taskData,
                id: taskId
            });
        });
    },
    
    resolveTask(taskId, result) {
        const task = this.pendingTasks.get(taskId);
        if (task) {
            task.resolve(result);
            this.pendingTasks.delete(taskId);
        }
    },
    
    rejectTask(taskId, error) {
        const task = this.pendingTasks.get(taskId);
        if (task) {
            task.reject(error);
            this.pendingTasks.delete(taskId);
        }
    },
    
    // Helper methods for common tasks
    async processChartData(data) {
        return this.runTask('dataProcessor', 'processChartData', data);
    },
    
    async formatNumbers(numbers) {
        return this.runTask('dataProcessor', 'formatLargeNumbers', numbers);
    },
    
    async calculateMetrics(data) {
        return this.runTask('dataProcessor', 'calculateMetrics', data);
    },
    
    terminate() {
        this.workers.forEach(worker => worker.terminate());
        this.workers.clear();
        this.pendingTasks.clear();
    }
};

// Initialize web workers
document.addEventListener('DOMContentLoaded', () => {
    if (typeof Worker !== 'undefined') {
        window.WebWorkerManager.init();
    } else {
        console.warn('Web Workers not supported in this browser');
    }
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (window.WebWorkerManager) {
        window.WebWorkerManager.terminate();
    }
});
