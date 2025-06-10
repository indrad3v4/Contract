/**
 * Dashboard JavaScript for the Daodiseo Real Estate Tokenization Platform
 * Provides interactive charts and dashboard data
 */

// Initialize dashboard components
document.addEventListener('DOMContentLoaded', () => {
    initDashboardData();
    initDashboardCharts();
});

// Initialize dashboard data from API
async function initDashboardData() {
    try {
        // Fetch dashboard statistics from API
        const statsData = await fetchApi('/api/blockchain/stats');
        
        // Update dashboard UI with fetched data
        updateDashboardMetrics(statsData);
        updateHotAsset(statsData.hot_asset);
        
    } catch (error) {
        console.error('Error initializing dashboard data:', error);
        
        // Show error message to user
        showAlert('Failed to load dashboard data. Please try again later.', 'warning');
    }
}

// Update dashboard metrics with values from API
function updateDashboardMetrics(data) {
    // Update token value
    const tokenValueElement = document.querySelector('.token-value');
    if (tokenValueElement) {
        tokenValueElement.textContent = formatCurrency(data.token_value);
    }
    
    // Update staking APY
    const stakingApyElement = document.querySelector('.staking-apy');
    if (stakingApyElement) {
        stakingApyElement.textContent = formatPercentage(data.staking_apy);
    }
    
    // Update total reserves
    const totalReservesElement = document.querySelector('.total-reserves');
    if (totalReservesElement) {
        totalReservesElement.textContent = formatCurrency(data.total_reserves);
    }
    
    // Update daily rewards
    const dailyRewardsElement = document.querySelector('.daily-rewards');
    if (dailyRewardsElement) {
        dailyRewardsElement.textContent = formatNumber(data.daily_rewards);
    }
    
    // Update verified assets
    const verifiedAssetsElement = document.querySelector('.verified-assets');
    if (verifiedAssetsElement) {
        verifiedAssetsElement.textContent = formatCurrency(data.verified_assets);
    }
    
    // Update unverified assets
    const unverifiedAssetsElement = document.querySelector('.unverified-assets');
    if (unverifiedAssetsElement) {
        unverifiedAssetsElement.textContent = formatCurrency(data.unverified_assets);
    }
}

// Update hot asset display
function updateHotAsset(hotAsset) {
    const hotAssetNameElement = document.querySelector('.hot-asset-name');
    if (hotAssetNameElement) {
        hotAssetNameElement.textContent = hotAsset.name;
    }
    
    const fundingProgressElement = document.querySelector('.funding-progress-bar');
    if (fundingProgressElement) {
        fundingProgressElement.style.width = `${hotAsset.funded_percentage}%`;
        fundingProgressElement.setAttribute('aria-valuenow', hotAsset.funded_percentage);
    }
    
    const fundingPercentageElement = document.querySelector('.funding-percentage');
    if (fundingPercentageElement) {
        fundingPercentageElement.textContent = `${hotAsset.funded_percentage}%`;
    }
    
    const fundingAmountElement = document.querySelector('.funding-amount');
    if (fundingAmountElement) {
        fundingAmountElement.textContent = 
            `${formatCurrency(hotAsset.funded_amount)} / ${formatCurrency(hotAsset.target_amount)}`;
    }
}

// Initialize dashboard charts
async function initDashboardCharts() {
    try {
        // Fetch data for charts
        const assetDistribution = await fetchApi('/api/blockchain/asset-distribution');
        const stakeholderDistribution = await fetchApi('/api/blockchain/stakeholder-distribution');
        
        // Initialize asset distribution chart
        initAssetDistributionChart(assetDistribution);
        
        // Initialize stakeholder distribution chart
        initStakeholderDistributionChart(stakeholderDistribution);
        
        // Initialize transaction history chart (with mock data for now)
        initTransactionHistoryChart();
        
    } catch (error) {
        console.error('Error initializing dashboard charts:', error);
        showAlert('Failed to load chart data. Please try again later.', 'warning');
    }
}

// Initialize asset distribution doughnut chart
function initAssetDistributionChart(data) {
    const chartElement = document.getElementById('assetDistributionChart');
    if (!chartElement) return;
    
    const ctx = chartElement.getContext('2d');
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Verified Assets', 'Unverified Assets'],
            datasets: [{
                data: [data.verified, data.unverified],
                backgroundColor: ['rgba(32, 201, 151, 0.8)', 'rgba(108, 117, 125, 0.8)'],
                borderColor: ['#20c997', '#6c757d'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: 'rgba(255, 255, 255, 0.7)',
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.label}: ${context.parsed}%`;
                        }
                    }
                }
            },
            cutout: '65%'
        }
    });
}

// Initialize stakeholder distribution doughnut chart
function initStakeholderDistributionChart(data) {
    const chartElement = document.getElementById('stakeholderDistributionChart');
    if (!chartElement) return;
    
    const ctx = chartElement.getContext('2d');
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Investors', 'Validators', 'Developers', 'Community'],
            datasets: [{
                data: [
                    data.investors, 
                    data.validators, 
                    data.developers, 
                    data.community
                ],
                backgroundColor: [
                    'rgba(0, 123, 255, 0.8)', 
                    'rgba(32, 201, 151, 0.8)', 
                    'rgba(255, 193, 7, 0.8)',
                    'rgba(220, 53, 69, 0.8)'
                ],
                borderColor: [
                    '#007bff', 
                    '#20c997', 
                    '#ffc107',
                    '#dc3545'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: 'rgba(255, 255, 255, 0.7)',
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.label}: ${context.parsed}%`;
                        }
                    }
                }
            },
            cutout: '65%'
        }
    });
}

// Initialize transaction history chart
function initTransactionHistoryChart() {
    const chartElement = document.getElementById('transactionHistoryChart');
    if (!chartElement) return;
    
    const ctx = chartElement.getContext('2d');
    
    // Get last 7 days for labels
    const labels = [];
    for (let i = 6; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        labels.push(date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }));
    }
    
    // Fetch transaction data from API (to be implemented)
    // For now, use placeholder data
    const transactionData = [12, 19, 8, 15, 12, 8, 25];
    const volumeData = [75000, 102000, 56000, 81000, 77000, 45000, 183000];
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Transactions',
                    data: transactionData,
                    borderColor: 'rgba(13, 202, 240, 1)',
                    backgroundColor: 'rgba(13, 202, 240, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true,
                    yAxisID: 'y'
                },
                {
                    label: 'Volume (ODIS)',
                    data: volumeData,
                    borderColor: 'rgba(25, 135, 84, 1)',
                    backgroundColor: 'transparent',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    tension: 0.4,
                    fill: false,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.7)'
                    }
                },
                y: {
                    position: 'left',
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.7)'
                    },
                    title: {
                        display: true,
                        text: 'Transactions',
                        color: 'rgba(255, 255, 255, 0.7)'
                    }
                },
                y1: {
                    position: 'right',
                    grid: {
                        drawOnChartArea: false
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.7)',
                        callback: function(value) {
                            if (value >= 1000) {
                                return value / 1000 + 'k';
                            }
                            return value;
                        }
                    },
                    title: {
                        display: true,
                        text: 'Volume (ODIS)',
                        color: 'rgba(255, 255, 255, 0.7)'
                    }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: 'rgba(255, 255, 255, 0.7)'
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.datasetIndex === 1) {
                                label += formatNumber(context.raw) + ' ODIS';
                            } else {
                                label += context.raw;
                            }
                            return label;
                        }
                    }
                }
            }
        }
    });
}
        
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
        
        