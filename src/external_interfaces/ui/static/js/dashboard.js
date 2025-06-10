/**
 * Dashboard JavaScript for the Daodiseo Real Estate Tokenization Platform
 * Provides interactive charts and dashboard data
 */

// Initialize dashboard components
document.addEventListener('DOMContentLoaded', () => {
    initDashboardData();
    initDashboardCharts();
    initDashboardStateListeners();
});

// Initialize dashboard state listeners for cross-route synchronization
function initDashboardStateListeners() {
    // Listen for transaction events from other routes
    document.addEventListener('transactionCreated', (event) => {
        const { transactionId, hash, type } = event.detail;
        console.log('Dashboard received transaction event:', { transactionId, hash, type });
        
        // Update portfolio metrics to reflect new transaction
        refreshPortfolioData();
        
        // Add to recent transactions list
        addRecentTransaction({ transactionId, hash, type });
    });
    
    // Listen for file upload events to update asset counts
    document.addEventListener('fileUploaded', (event) => {
        const { fileName, fileHash } = event.detail;
        console.log('Dashboard received file upload event:', { fileName, fileHash });
        
        // Refresh verified assets count
        refreshAssetMetrics();
    });
    
    // Listen for wallet state changes
    document.addEventListener('stateChange:wallet', (event) => {
        const walletState = event.detail.data;
        updateWalletDashboard(walletState);
    });
    
    // Listen for contract state changes
    document.addEventListener('stateChange:contracts', (event) => {
        const contractsState = event.detail.data;
        updateContractMetrics(contractsState);
    });
}

// Initialize dashboard data from API
async function initDashboardData() {
    try {
        // Fetch blockchain statistics from API
        const statsData = await fetchApi('/api/blockchain/stats');
        
        // Update ODIS token metrics with real data
        updateOdisTokenMetrics(statsData);
        
        // Update portfolio dashboard metrics
        updateDashboardMetrics(statsData);
        
        // Load validators data
        await loadValidatorsData();
        
        // Initialize real-time price updates
        initPriceUpdates();
        
    } catch (error) {
        console.error('Error initializing dashboard data:', error);
        showAlert('Failed to load blockchain data. Please check your connection.', 'warning');
    }
}

// Update ODIS token metrics with real blockchain data
function updateOdisTokenMetrics(data) {
    // Update current price
    const priceElement = document.getElementById('odis-price');
    if (priceElement && data.token_price) {
        priceElement.textContent = `$${data.token_price.toFixed(4)}`;
    }
    
    // Update price change
    const changeElement = document.getElementById('odis-change');
    if (changeElement && data.price_change_24h !== undefined) {
        const change = data.price_change_24h;
        changeElement.textContent = `${change >= 0 ? '+' : ''}${change.toFixed(2)}%`;
        changeElement.className = change >= 0 ? 'text-success' : 'text-danger';
    }
    
    // Update market cap
    const marketCapElement = document.getElementById('market-cap');
    if (marketCapElement && data.market_cap) {
        marketCapElement.textContent = formatCurrency(data.market_cap / 1000000) + 'M';
    }
    
    // Update 24h volume
    const volumeElement = document.getElementById('volume-24h');
    if (volumeElement && data.volume_24h) {
        volumeElement.textContent = formatCurrency(data.volume_24h / 1000000) + 'M';
    }
    
    // Update 24h high/low
    const highElement = document.getElementById('high-24h');
    const lowElement = document.getElementById('low-24h');
    if (highElement && data.high_24h) {
        highElement.textContent = `$${data.high_24h.toFixed(4)}`;
    }
    if (lowElement && data.low_24h) {
        lowElement.textContent = `$${data.low_24h.toFixed(4)}`;
    }
    
    // Update staking APY
    const stakingApyElement = document.getElementById('staking-apy');
    if (stakingApyElement && data.staking_apy) {
        stakingApyElement.textContent = `${data.staking_apy.toFixed(1)}%`;
    }
}

// Load validators data from blockchain
async function loadValidatorsData() {
    try {
        // Get validators from stats API which fetches real validator data
        const statsData = await fetchApi('/api/blockchain/stats');
        const validators = statsData.validators || [];
        
        // Update validators count
        const validatorsCountElement = document.getElementById('active-validators-count');
        if (validatorsCountElement) {
            validatorsCountElement.textContent = validators.length;
        }
        
        // Calculate total voting power
        const totalVotingPower = validators.reduce((sum, v) => sum + (parseFloat(v.voting_power) || 0), 0);
        const totalPowerElement = document.getElementById('total-voting-power');
        if (totalPowerElement) {
            totalPowerElement.textContent = formatNumber(Math.round(totalVotingPower / 1000000)) + 'M';
        }
        
        // Populate validators grid
        populateValidatorsGrid(validators);
        
        // Update staking overview
        updateStakingOverview(statsData);
        
    } catch (error) {
        console.error('Error loading validators data:', error);
    }
}

// Populate validators grid with real data
function populateValidatorsGrid(validators) {
    const validatorsGrid = document.getElementById('validators-grid');
    if (!validatorsGrid) return;
    
    // Clear existing content
    validatorsGrid.innerHTML = '';
    
    // Create validator cards
    validators.slice(0, 9).forEach((validator, index) => {
        const validatorCard = createValidatorCard(validator, index);
        validatorsGrid.appendChild(validatorCard);
    });
    
    // Refresh icons
    feather.replace();
}

// Create validator card element
function createValidatorCard(validator, index) {
    const col = document.createElement('div');
    col.className = 'col-md-4 mb-3';
    
    // Extract validator data
    const moniker = validator.description?.moniker || validator.moniker || `Validator ${index + 1}`;
    const votingPower = parseFloat(validator.voting_power) || 0;
    const commission = parseFloat(validator.commission?.commission_rates?.rate) || 0;
    const status = validator.status || 'BOND_STATUS_BONDED';
    const jailed = validator.jailed || false;
    
    // Determine status
    let statusClass = 'active';
    let statusText = 'Active';
    if (jailed) {
        statusClass = 'jailed';
        statusText = 'Jailed';
    } else if (status !== 'BOND_STATUS_BONDED') {
        statusClass = 'inactive';
        statusText = 'Inactive';
    }
    
    col.innerHTML = `
        <div class="validator-card slide-in">
            <div class="validator-header d-flex align-items-center mb-2">
                <div class="validator-avatar me-3">
                    <div class="rounded-circle bg-primary d-flex align-items-center justify-content-center" style="width: 32px; height: 32px;">
                        <i data-feather="shield" style="width: 16px; height: 16px;"></i>
                    </div>
                </div>
                <div class="flex-grow-1">
                    <div class="validator-name">${moniker}</div>
                    <div class="validator-status">
                        <span class="status-indicator ${statusClass}"></span>
                        <span class="status-text">${statusText}</span>
                    </div>
                </div>
            </div>
            <div class="validator-metrics">
                <div class="row">
                    <div class="col-6">
                        <div class="metric-small">
                            <div class="metric-value">${formatNumber(Math.round(votingPower / 1000000))}M</div>
                            <div class="metric-label">Voting Power</div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="metric-small">
                            <div class="metric-value">${(commission * 100).toFixed(1)}%</div>
                            <div class="metric-label">Commission</div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="validator-actions mt-2">
                <button class="btn btn-sm btn-outline-primary me-2" ${jailed ? 'disabled' : ''}>
                    <i data-feather="trending-up" class="icon-inline-sm"></i>
                    Delegate
                </button>
                <button class="btn btn-sm btn-outline-secondary">
                    <i data-feather="info" class="icon-inline-sm"></i>
                    Details
                </button>
            </div>
        </div>
    `;
    
    return col;
}

// Update staking overview with real data
function updateStakingOverview(data) {
    // Update total staked
    const totalStakedElement = document.getElementById('total-staked');
    if (totalStakedElement && data.total_staked) {
        totalStakedElement.textContent = formatCurrency(data.total_staked / 1000000) + 'M ODIS';
    }
    
    // Update staking ratio
    const stakingRatioElement = document.getElementById('staking-ratio');
    if (stakingRatioElement && data.staking_ratio) {
        stakingRatioElement.textContent = `${(data.staking_ratio * 100).toFixed(1)}%`;
    }
}

// Initialize real-time price updates
function initPriceUpdates() {
    // Update prices every 30 seconds
    setInterval(async () => {
        try {
            const statsData = await fetchApi('/api/blockchain/stats');
            updateOdisTokenMetrics(statsData);
        } catch (error) {
            console.warn('Failed to update prices:', error);
        }
    }, 30000);
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

// Refresh portfolio data after cross-route events
async function refreshPortfolioData() {
    try {
        const statsData = await fetchApi('/api/blockchain/stats');
        updateDashboardMetrics(statsData);
    } catch (error) {
        console.warn('Failed to refresh portfolio data:', error);
    }
}

// Refresh asset metrics after file uploads
async function refreshAssetMetrics() {
    try {
        const assetData = await fetchApi('/api/blockchain/asset-distribution');
        updateAssetDistribution(assetData);
    } catch (error) {
        console.warn('Failed to refresh asset metrics:', error);
    }
}

// Add recent transaction to dashboard
function addRecentTransaction(transaction) {
    const recentTransactionsList = document.querySelector('.recent-transactions-list');
    if (!recentTransactionsList) return;
    
    const transactionElement = document.createElement('div');
    transactionElement.className = 'transaction-item d-flex justify-content-between align-items-center py-2 border-bottom';
    transactionElement.innerHTML = `
        <div>
            <div class="fw-medium">${transaction.type.charAt(0).toUpperCase() + transaction.type.slice(1)} Transaction</div>
            <small class="text-muted">ID: ${transaction.transactionId}</small>
        </div>
        <div class="text-end">
            <div class="badge bg-success">Completed</div>
            <small class="d-block text-muted">Just now</small>
        </div>
    `;
    
    // Insert at the top of the list
    recentTransactionsList.insertBefore(transactionElement, recentTransactionsList.firstChild);
    
    // Limit to 5 recent transactions
    const transactionItems = recentTransactionsList.querySelectorAll('.transaction-item');
    if (transactionItems.length > 5) {
        recentTransactionsList.removeChild(transactionItems[transactionItems.length - 1]);
    }
}

// Update wallet dashboard display
function updateWalletDashboard(walletState) {
    const walletAddressElement = document.querySelector('.wallet-address-display');
    const walletBalanceElement = document.querySelector('.wallet-balance-display');
    
    if (walletState.connected && walletState.address) {
        if (walletAddressElement) {
            const shortAddress = walletState.address.slice(0, 8) + '...' + walletState.address.slice(-4);
            walletAddressElement.textContent = shortAddress;
        }
        
        if (walletBalanceElement && walletState.balance) {
            walletBalanceElement.textContent = formatNumber(walletState.balance) + ' ODIS';
        }
    } else {
        if (walletAddressElement) {
            walletAddressElement.textContent = 'Not Connected';
        }
        if (walletBalanceElement) {
            walletBalanceElement.textContent = '0 ODIS';
        }
    }
}

// Update contract metrics in dashboard
function updateContractMetrics(contractsState) {
    const activeContractsElement = document.querySelector('.active-contracts-count');
    const pendingContractsElement = document.querySelector('.pending-contracts-count');
    
    if (activeContractsElement) {
        activeContractsElement.textContent = contractsState.active?.length || 0;
    }
    
    if (pendingContractsElement) {
        pendingContractsElement.textContent = contractsState.pending?.length || 0;
    }
}

// Update asset distribution chart
function updateAssetDistribution(assetData) {
    const assetChart = document.querySelector('#assetDistributionChart');
    if (assetChart && window.assetDistributionChart) {
        // Update chart data if chart instance exists
        window.assetDistributionChart.data.datasets[0].data = assetData.values;
        window.assetDistributionChart.data.labels = assetData.labels;
        window.assetDistributionChart.update();
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