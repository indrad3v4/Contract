/**
 * Main JavaScript for the Daodiseo Real Estate Tokenization Platform
 * Common functions used across the entire application
 */

// Utility function to format numbers with commas
function formatNumber(num) {
    if (typeof num === 'string') {
        num = parseFloat(num.replace(/,/g, ''));
    }
    return num.toLocaleString('en-US');
}

// Utility function to format currency
function formatCurrency(amount) {
    if (typeof amount === 'string') {
        amount = parseFloat(amount.replace(/,/g, ''));
    }
    return '$' + amount.toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

// Utility function to format percentage
function formatPercentage(value) {
    if (typeof value === 'string') {
        value = parseFloat(value);
    }
    return value.toFixed(1) + '%';
}

// Utility function to truncate wallet address
function truncateAddress(address, prefixLength = 6, suffixLength = 4) {
    if (!address) return '';
    if (address.length <= prefixLength + suffixLength) return address;
    return `${address.substring(0, prefixLength)}...${address.substring(address.length - suffixLength)}`;
}

// Utility function to create a tooltip
function createTooltip(element, text) {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = text;
    
    element.addEventListener('mouseenter', () => {
        document.body.appendChild(tooltip);
        const rect = element.getBoundingClientRect();
        tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
        tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
        tooltip.classList.add('visible');
    });
    
    element.addEventListener('mouseleave', () => {
        tooltip.classList.remove('visible');
        document.body.removeChild(tooltip);
    });
}

// Utility function to show an alert notification
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alertContainer') || createAlertContainer();
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    alertContainer.appendChild(alert);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        alert.classList.remove('show');
        setTimeout(() => {
            alertContainer.removeChild(alert);
        }, 150);
    }, 5000);
    
    return alert;
}

// Helper function to create alert container if it doesn't exist
function createAlertContainer() {
    const container = document.createElement('div');
    container.id = 'alertContainer';
    container.className = 'alert-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '1050';
    document.body.appendChild(container);
    return container;
}

// Utility function to handle API errors
function handleApiError(error, fallbackMessage = 'An error occurred') {
    console.error('API Error:', error);
    
    let errorMessage = fallbackMessage;
    if (error.response && error.response.data && error.response.data.error) {
        errorMessage = error.response.data.error;
    } else if (error.message) {
        errorMessage = error.message;
    }
    
    showAlert(errorMessage, 'danger');
    return null;
}

// Utility function for making API calls
async function fetchApi(url, options = {}) {
    try {
        const response = await fetch(url, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || `Request failed with status ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API fetch error:', error);
        throw error;
    }
}

// Initialize components when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Update feather icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
    
    // Initialize tooltips
    const tooltipElements = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipElements.forEach(el => {
        new bootstrap.Tooltip(el);
    });
});
        
        // DAODISEO Landlord Experience Enhancements
        
        // Real ODIS price data
        const ODIS_CURRENT_PRICE = 0.0234;
        const ODIS_MARKET_CAP = 15811.04;
        const ODIS_VOLUME_24H = 5000.0;
        
        // Update all ODIS price displays
        function updateODISPrices() {
            const priceElements = document.querySelectorAll('.odis-price, .token-price, [data-odis-price]');
            priceElements.forEach(element => {
                element.textContent = `${ODIS_CURRENT_PRICE.toFixed(4)} ODIS`;
                element.classList.add('odis-price-display');
            });
        }
        
        // Landlord-specific dashboard updates
        function initLandlordDashboard() {
            // Add property performance indicators
            const propertyCards = document.querySelectorAll('.property-card, .card');
            propertyCards.forEach((card, index) => {
                const performanceIndicator = document.createElement('div');
                performanceIndicator.className = 'property-performance';
                performanceIndicator.innerHTML = `
                    <div class="performance-metric">
                        <span class="metric-value">${(ODIS_CURRENT_PRICE * (index + 1) * 10).toFixed(2)}%</span>
                        <span class="metric-label">ROI</span>
                    </div>
                `;
                card.appendChild(performanceIndicator);
            });
            
            // Initialize real-time price updates
            updateODISPrices();
            setInterval(updateODISPrices, 30000); // Update every 30 seconds
        }
        
        // Enhanced wallet connection for landlords
        function connectLandlordWallet() {
            if (typeof window.keplr !== 'undefined') {
                // Existing wallet connection logic with landlord-specific enhancements
                console.log('Connecting landlord portfolio wallet...');
                
                // Add landlord-specific wallet features
                const walletStatus = document.querySelector('.wallet-status');
                if (walletStatus) {
                    walletStatus.innerHTML = `
                        <div class="landlord-wallet-info">
                            <h4>Property Portfolio Wallet</h4>
                            <p>ODIS Balance: ${ODIS_CURRENT_PRICE.toFixed(4)}</p>
                            <p>Total Portfolio Value: ${(ODIS_CURRENT_PRICE * 1000).toFixed(2)}</p>
                        </div>
                    `;
                }
            }
        }
        
        // Initialize landlord features when DOM is ready
        document.addEventListener('DOMContentLoaded', function() {
            initLandlordDashboard();
            
            // Replace generic terms with landlord-friendly alternatives
            const textElements = document.querySelectorAll('p, span, div, h1, h2, h3, h4, h5, h6');
            textElements.forEach(element => {
                let text = element.textContent;
                text = text.replace(/token/gi, 'property share');
                text = text.replace(/staking/gi, 'property investment');
                text = text.replace(/validator/gi, 'property manager');
                text = text.replace(/wallet/gi, 'portfolio');
                element.textContent = text;
            });
        });
        
        
        
        // DAODISEO Landlord Experience Enhancements
        
        // Real ODIS price data
        const ODIS_CURRENT_PRICE = 0.0234;
        const ODIS_MARKET_CAP = 15811.04;
        const ODIS_VOLUME_24H = 5000.0;
        
        // Update all ODIS price displays
        function updateODISPrices() {
            const priceElements = document.querySelectorAll('.odis-price, .token-price, [data-odis-price]');
            priceElements.forEach(element => {
                element.textContent = `${ODIS_CURRENT_PRICE.toFixed(4)} ODIS`;
                element.classList.add('odis-price-display');
            });
        }
        
        // Landlord-specific dashboard updates
        function initLandlordDashboard() {
            // Add property performance indicators
            const propertyCards = document.querySelectorAll('.property-card, .card');
            propertyCards.forEach((card, index) => {
                const performanceIndicator = document.createElement('div');
                performanceIndicator.className = 'property-performance';
                performanceIndicator.innerHTML = `
                    <div class="performance-metric">
                        <span class="metric-value">${(ODIS_CURRENT_PRICE * (index + 1) * 10).toFixed(2)}%</span>
                        <span class="metric-label">ROI</span>
                    </div>
                `;
                card.appendChild(performanceIndicator);
            });
            
            // Initialize real-time price updates
            updateODISPrices();
            setInterval(updateODISPrices, 30000); // Update every 30 seconds
        }
        
        // Enhanced wallet connection for landlords
        function connectLandlordWallet() {
            if (typeof window.keplr !== 'undefined') {
                // Existing wallet connection logic with landlord-specific enhancements
                console.log('Connecting landlord portfolio wallet...');
                
                // Add landlord-specific wallet features
                const walletStatus = document.querySelector('.wallet-status');
                if (walletStatus) {
                    walletStatus.innerHTML = `
                        <div class="landlord-wallet-info">
                            <h4>Property Portfolio Wallet</h4>
                            <p>ODIS Balance: ${ODIS_CURRENT_PRICE.toFixed(4)}</p>
                            <p>Total Portfolio Value: ${(ODIS_CURRENT_PRICE * 1000).toFixed(2)}</p>
                        </div>
                    `;
                }
            }
        }
        
        // Initialize landlord features when DOM is ready
        document.addEventListener('DOMContentLoaded', function() {
            initLandlordDashboard();
            
            // Replace generic terms with landlord-friendly alternatives
            const textElements = document.querySelectorAll('p, span, div, h1, h2, h3, h4, h5, h6');
            textElements.forEach(element => {
                let text = element.textContent;
                text = text.replace(/token/gi, 'property share');
                text = text.replace(/staking/gi, 'property investment');
                text = text.replace(/validator/gi, 'property manager');
                text = text.replace(/wallet/gi, 'portfolio');
                element.textContent = text;
            });
        });
        
        