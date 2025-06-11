// Async Operation Handler - Prevents UI Blocking
console.log("Async handler loading...");

window.AsyncHandler = {
    taskQueue: [],
    isProcessing: false,
    
    init() {
        this.interceptBlockingOperations();
        this.startTaskProcessor();
        console.log("✅ Async handler active");
    },
    
    interceptBlockingOperations() {
        // Wrap expensive operations in async handlers
        const originalFeatherReplace = window.feather?.replace;
        if (originalFeatherReplace) {
            window.feather.replace = (...args) => {
                this.addTask(() => originalFeatherReplace.apply(window.feather, args));
            };
        }
        
        // Wrap Chart.js operations
        const originalChart = window.Chart;
        if (originalChart) {
            window.Chart = function(...args) {
                const instance = new originalChart(...args);
                return instance;
            };
            Object.setPrototypeOf(window.Chart, originalChart);
            Object.assign(window.Chart, originalChart);
        }
    },
    
    addTask(taskFunction) {
        this.taskQueue.push(taskFunction);
        if (!this.isProcessing) {
            this.processNextTask();
        }
    },
    
    async processNextTask() {
        if (this.taskQueue.length === 0) {
            this.isProcessing = false;
            return;
        }
        
        this.isProcessing = true;
        const task = this.taskQueue.shift();
        
        try {
            // Use requestIdleCallback if available, otherwise setTimeout
            if (window.requestIdleCallback) {
                window.requestIdleCallback(() => {
                    task();
                    this.processNextTask();
                });
            } else {
                setTimeout(() => {
                    task();
                    this.processNextTask();
                }, 0);
            }
        } catch (error) {
            console.warn('Async task failed:', error);
            this.processNextTask();
        }
    },
    
    wrapAsyncFunction(fn) {
        return (...args) => {
            return new Promise((resolve, reject) => {
                this.addTask(() => {
                    try {
                        const result = fn.apply(this, args);
                        resolve(result);
                    } catch (error) {
                        reject(error);
                    }
                });
            });
        };
    }
};

document.addEventListener('DOMContentLoaded', () => {
    window.AsyncHandler.init();
});
