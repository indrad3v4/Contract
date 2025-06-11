// Lazy Loading System - Loads Components Only When Needed
console.log("Lazy loader loading...");

window.LazyLoader = {
    observers: new Map(),
    loadedComponents: new Set(),
    
    init() {
        this.setupIntersectionObserver();
        this.markLazyComponents();
        console.log("✅ Lazy loader active");
    },
    
    setupIntersectionObserver() {
        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.loadComponent(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '50px'
        });
    },
    
    markLazyComponents() {
        // Mark charts for lazy loading
        const charts = document.querySelectorAll('#asset-distribution-chart, .chart-container');
        charts.forEach(chart => {
            if (!this.loadedComponents.has(chart)) {
                this.observer.observe(chart);
            }
        });
        
        // Mark heavy lists for lazy loading
        const lists = document.querySelectorAll('.recent-transactions-content, .validator-list');
        lists.forEach(list => {
            if (!this.loadedComponents.has(list)) {
                this.observer.observe(list);
            }
        });
    },
    
    loadComponent(element) {
        if (this.loadedComponents.has(element)) return;
        
        this.loadedComponents.add(element);
        this.observer.unobserve(element);
        
        // Load component based on type
        if (element.id === 'asset-distribution-chart') {
            this.loadAssetChart(element);
        } else if (element.classList.contains('recent-transactions-content')) {
            this.loadTransactionList(element);
        }
    },
    
    loadAssetChart(chartElement) {
        // Only load chart when visible
        if (typeof window.EnhancedAssetDistribution !== 'undefined') {
            setTimeout(() => {
                new window.EnhancedAssetDistribution();
            }, 100);
        }
    },
    
    loadTransactionList(listElement) {
        // Only load transactions when visible
        if (typeof window.EnhancedTransactionList !== 'undefined') {
            setTimeout(() => {
                new window.EnhancedTransactionList();
            }, 100);
        }
    }
};

document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        window.LazyLoader.init();
    }, 1000);
});
