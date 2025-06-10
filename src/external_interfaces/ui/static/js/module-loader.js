/**
 * Module Loader - Prevents duplicate class definitions and conflicts
 */
(function() {
    'use strict';
    
    // Global module registry
    window.DAODISEO = window.DAODISEO || {};
    window.DAODISEO.modules = window.DAODISEO.modules || {};
    window.DAODISEO.instances = window.DAODISEO.instances || {};
    
    // Module registration function
    window.DAODISEO.registerModule = function(name, moduleClass) {
        if (this.modules[name]) {
            console.warn(`Module ${name} already registered, skipping duplicate`);
            return false;
        }
        
        this.modules[name] = moduleClass;
        console.log(`Module ${name} registered successfully`);
        return true;
    };
    
    // Safe module initialization
    window.DAODISEO.initModule = function(name, ...args) {
        if (this.instances[name]) {
            console.warn(`Module ${name} already initialized`);
            return this.instances[name];
        }
        
        const ModuleClass = this.modules[name];
        if (!ModuleClass) {
            console.error(`Module ${name} not found`);
            return null;
        }
        
        try {
            this.instances[name] = new ModuleClass(...args);
            console.log(`Module ${name} initialized successfully`);
            return this.instances[name];
        } catch (error) {
            console.error(`Failed to initialize module ${name}:`, error);
            return null;
        }
    };
    
    // Initialize all registered modules
    window.DAODISEO.initializeAll = function() {
        const moduleNames = Object.keys(this.modules);
        moduleNames.forEach(name => {
            if (!this.instances[name]) {
                this.initModule(name);
            }
        });
    };
    
    // Clean restart function
    window.DAODISEO.restart = function() {
        // Clear instances
        Object.keys(this.instances).forEach(name => {
            const instance = this.instances[name];
            if (instance && typeof instance.destroy === 'function') {
                instance.destroy();
            }
        });
        
        this.instances = {};
        this.initializeAll();
    };
    
})();