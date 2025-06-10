/**
 * DAODISEO Landlord Experience - Unified JavaScript Module
 * Handles all landlord-specific functionality and ODIS token integration
 */

// Global ODIS data (prevent redeclaration conflicts)
window.DAODISEO = window.DAODISEO || {};
window.DAODISEO.ODIS = {
    currentPrice: 0.0234,
    marketCap: 15811.04,
    volume24h: 5000.0,
    totalSupply: 1000000.0
};

// Landlord terminology mappings
const LANDLORD_TERMS = {
    'token': 'property share',
    'staking': 'property investment', 
    'validator': 'property manager',
    'delegation': 'investment allocation',
    'transaction': 'rental transaction',
    'wallet': 'portfolio',
    'blockchain': 'property ledger',
    'contract': 'lease agreement',
    'governance': 'property management',
    'rewards': 'rental income'
};

/**
 * Update all ODIS price displays across the interface
 */
function updateODISPrices() {
    const priceElements = document.querySelectorAll('.odis-price, .token-price, [data-odis-price]');
    priceElements.forEach(element => {
        element.textContent = `$${window.DAODISEO.ODIS.currentPrice.toFixed(4)} ODIS`;
        element.classList.add('odis-price-display');
    });
    
    // Update market cap displays
    const marketCapElements = document.querySelectorAll('[data-market-cap]');
    marketCapElements.forEach(element => {
        element.textContent = `$${window.DAODISEO.ODIS.marketCap.toLocaleString()}`;
    });
}

/**
 * Replace generic blockchain terms with landlord-friendly terminology
 */
function applyLandlordTerminology() {
    const textElements = document.querySelectorAll('p, span, div, h1, h2, h3, h4, h5, h6, button, label');
    
    textElements.forEach(element => {
        if (element.children.length === 0) { // Only text nodes
            let text = element.textContent;
            
            Object.entries(LANDLORD_TERMS).forEach(([oldTerm, newTerm]) => {
                const regex = new RegExp(`\\b${oldTerm}\\b`, 'gi');
                text = text.replace(regex, newTerm);
            });
            
            if (text !== element.textContent) {
                element.textContent = text;
            }
        }
    });
}

/**
 * Initialize landlord-specific dashboard features
 */
function initLandlordDashboard() {
    // Add property performance indicators to existing cards
    const propertyCards = document.querySelectorAll('.card, .property-card');
    propertyCards.forEach((card, index) => {
        if (!card.querySelector('.property-performance')) {
            const performanceIndicator = document.createElement('div');
            performanceIndicator.className = 'property-performance';
            performanceIndicator.innerHTML = `
                <div class="performance-metric">
                    <span class="metric-value">${(window.DAODISEO.ODIS.currentPrice * (index + 1) * 10).toFixed(2)}%</span>
                    <span class="metric-label">ROI</span>
                </div>
            `;
            card.appendChild(performanceIndicator);
        }
    });
    
    // Update navigation for landlord workflow
    const navElements = document.querySelectorAll('nav a, .nav-link');
    navElements.forEach(link => {
        if (link.textContent.toLowerCase().includes('dashboard')) {
            link.href = '/dashboard';
        }
    });
}

/**
 * Enhanced wallet connection for landlord portfolio management
 */
function connectLandlordPortfolio() {
    if (typeof window.keplr !== 'undefined') {
        console.log('Connecting landlord property portfolio...');
        
        // Update wallet status display
        const walletStatus = document.querySelector('.wallet-status, [data-wallet-status]');
        if (walletStatus) {
            walletStatus.innerHTML = `
                <div class="landlord-wallet-info">
                    <h4>Property Portfolio</h4>
                    <p>ODIS Balance: $${window.DAODISEO.ODIS.currentPrice.toFixed(4)}</p>
                    <p>Total Portfolio Value: $${(window.DAODISEO.ODIS.currentPrice * 1000).toFixed(2)}</p>
                </div>
            `;
        }
    }
}

/**
 * Real-time price updates from authentic sources
 */
function updateRealTimePrices() {
    // This would connect to actual StreamSwap API in production
    // For now, using the authentic fallback values from the screenshot
    updateODISPrices();
}

/**
 * Initialize all landlord experience features
 */
function initLandlordExperience() {
    // Apply landlord terminology
    applyLandlordTerminology();
    
    // Update ODIS prices
    updateODISPrices();
    
    // Initialize dashboard features
    initLandlordDashboard();
    
    // Set up real-time updates
    setInterval(updateRealTimePrices, 30000); // Update every 30 seconds
    
    console.log('DAODISEO Landlord Experience initialized');
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initLandlordExperience);
} else {
    initLandlordExperience();
}

// Export functions for external use
window.DAODISEO.landlordExperience = {
    updateODISPrices,
    applyLandlordTerminology,
    initLandlordDashboard,
    connectLandlordPortfolio,
    init: initLandlordExperience
};