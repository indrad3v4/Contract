
// Enhanced Components Manager - Prevents conflicts
class ComponentManager {
    constructor() {
        this.components = new Map();
        this.initialized = new Set();
    }
    
    register(name, componentClass) {
        if (this.components.has(name)) {
            console.warn(`Component ${name} already registered, skipping duplicate`);
            return;
        }
        
        this.components.set(name, componentClass);
        console.log(`Component ${name} registered successfully`);
    }
    
    initialize(name, ...args) {
        if (this.initialized.has(name)) {
            console.warn(`Component ${name} already initialized`);
            return this.components.get(name);
        }
        
        const ComponentClass = this.components.get(name);
        if (!ComponentClass) {
            console.error(`Component ${name} not found`);
            return null;
        }
        
        try {
            const instance = new ComponentClass(...args);
            this.initialized.add(name);
            console.log(`Component ${name} initialized successfully`);
            return instance;
        } catch (error) {
            console.error(`Failed to initialize component ${name}:`, error);
            return null;
        }
    }
    
    initializeAll() {
        const components = [
            'EnhancedStatsCards',
            'EnhancedTransactionList', 
            'EnhancedAssetDistribution',
            'DataSourceAgentManager'
        ];
        
        components.forEach(name => {
            if (!this.initialized.has(name)) {
                this.initialize(name);
            }
        });
    }
}

window.componentManager = new ComponentManager();

// Safe component registration
function registerComponent(name, componentClass) {
    window.componentManager.register(name, componentClass);
}

// Safe initialization
function initializeComponent(name, ...args) {
    return window.componentManager.initialize(name, ...args);
}
