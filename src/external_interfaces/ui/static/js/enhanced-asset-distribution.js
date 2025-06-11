// Enhanced Asset Distribution with Real Blockchain Data
console.log("Enhanced asset distribution loading with blockchain integration...");

class EnhancedAssetDistribution {
    constructor() {
        this.chartCanvas = null;
        this.chart = null;
        this.initialize();
    }
    
    async initialize() {
        // Wait for Chart.js to be available
        if (typeof Chart === 'undefined') {
            setTimeout(() => this.initialize(), 500);
            return;
        }
        
        this.chartCanvas = document.querySelector('#asset-distribution-chart');
        if (!this.chartCanvas) {
            setTimeout(() => this.initialize(), 500);
            return;
        }
        
        await this.loadAssetDistribution();
        this.startPeriodicUpdates();
    }
    
    async loadAssetDistribution() {
        try {
            console.log("Loading asset distribution data...");
            const response = await fetch('/api/blockchain/asset-distribution');
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success && data.data?.distribution) {
                this.createChart(data.data.distribution);
                console.log("✅ Asset distribution loaded successfully");
            } else {
                this.showErrorState();
            }
            
        } catch (error) {
            console.error('Failed to load asset distribution:', error);
            this.showErrorState();
        }
    }
    
    createChart(distributionData) {
        if (this.chart) {
            this.chart.destroy();
        }
        
        const ctx = this.chartCanvas.getContext('2d');
        
        // Process distribution data
        const labels = distributionData.map(item => item.name || item.asset || 'Unknown');
        const values = distributionData.map(item => item.value || item.percentage || 0);
        const colors = this.generateColors(labels.length);
        
        this.chart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: colors.backgrounds,
                    borderColor: colors.borders,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#ffffff',
                            padding: 20,
                            usePointStyle: true,
                            font: {
                                size: 12
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        borderColor: '#00ff9d',
                        borderWidth: 1,
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                const percentage = ((value / context.dataset.data.reduce((a, b) => a + b, 0)) * 100).toFixed(1);
                                return `${label}: ${value.toFixed(2)}% (${percentage}% of total)`;
                            }
                        }
                    }
                },
                cutout: '60%',
                animation: {
                    animateRotate: true,
                    duration: 1000
                }
            }
        });
        
        // Add center text showing total
        this.addCenterText();
    }
    
    addCenterText() {
        const chartContainer = this.chartCanvas.parentElement;
        let centerText = chartContainer.querySelector('.chart-center-text');
        
        if (!centerText) {
            centerText = document.createElement('div');
            centerText.className = 'chart-center-text';
            chartContainer.style.position = 'relative';
            chartContainer.appendChild(centerText);
        }
        
        centerText.innerHTML = `
            <div class="center-label">Total Assets</div>
            <div class="center-value">100%</div>
        `;
    }
    
    generateColors(count) {
        const baseColors = [
            '#00ff9d', '#00d4aa', '#00a8b7', '#007cc4', '#0050d1',
            '#2d24de', '#5a00eb', '#8700f8', '#b400ff', '#e100ff'
        ];
        
        const backgrounds = [];
        const borders = [];
        
        for (let i = 0; i < count; i++) {
            const color = baseColors[i % baseColors.length];
            backgrounds.push(color + '80'); // 50% opacity
            borders.push(color);
        }
        
        return { backgrounds, borders };
    }
    
    showErrorState() {
        const chartContainer = this.chartCanvas.parentElement;
        chartContainer.innerHTML = `
            <div class="chart-error-state">
                <i data-feather="pie-chart"></i>
                <p>Unable to load asset distribution</p>
                <button onclick="location.reload()" class="retry-button">Retry</button>
            </div>
        `;
        
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
    }
    
    startPeriodicUpdates() {
        // Refresh every 60 seconds
        setInterval(() => {
            this.loadAssetDistribution();
        }, 60000);
        
        console.log("✅ Asset distribution periodic updates started");
    }
}

// Initialize enhanced asset distribution
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        new EnhancedAssetDistribution();
    }, 2500);
});

// Add asset distribution styling
const assetStyle = document.createElement('style');
assetStyle.textContent = `
.chart-center-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    pointer-events: none;
}

.center-label {
    font-size: 0.9rem;
    color: #a0a0a0;
    margin-bottom: 4px;
}

.center-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #00ff9d;
}

.chart-error-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 300px;
    color: #a0a0a0;
}

.chart-error-state i {
    width: 48px;
    height: 48px;
    margin-bottom: 16px;
    opacity: 0.5;
}

.chart-error-state .retry-button {
    margin-top: 12px;
    padding: 8px 16px;
    background: rgba(0, 255, 157, 0.2);
    border: 1px solid #00ff9d;
    border-radius: 6px;
    color: #00ff9d;
    cursor: pointer;
    transition: all 0.2s ease;
}

.chart-error-state .retry-button:hover {
    background: rgba(0, 255, 157, 0.3);
}
`;
document.head.appendChild(assetStyle);
