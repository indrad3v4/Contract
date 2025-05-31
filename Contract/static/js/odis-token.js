
            // ODIS Token Price Fetching and StreamSwap Integration
            class ODISTokenManager {
                constructor() {
                    this.streamswapUrl = 'https://app.streamswap.io';
                    this.init();
                }
                
                init() {
                    this.updatePrices();
                    setInterval(() => this.updatePrices(), 30000); // Update every 30 seconds
                }
                
                async updatePrices() {
                    try {
                        // Simulated price data - replace with real API call
                        const priceData = {
                            price: 0.1204,
                            change: 2.19,
                            high24h: 0.1289,
                            low24h: 0.1156,
                            volume: 2.5,
                            marketCap: 12.4
                        };
                        
                        this.updatePriceDisplay(priceData);
                    } catch (error) {
                        console.error('Error fetching ODIS price:', error);
                    }
                }
                
                updatePriceDisplay(data) {
                    const priceElement = document.getElementById('odis-price');
                    const changeElement = document.getElementById('odis-change');
                    const highElement = document.getElementById('odis-high');
                    const lowElement = document.getElementById('odis-low');
                    const volumeElement = document.getElementById('odis-volume');
                    const marketCapElement = document.getElementById('odis-market-cap');
                    
                    if (priceElement) priceElement.textContent = `$${data.price.toFixed(4)}`;
                    if (changeElement) {
                        changeElement.textContent = `↗ ${data.change}%`;
                        changeElement.className = data.change >= 0 ? 'price-change positive' : 'price-change negative';
                    }
                    if (highElement) highElement.textContent = `$${data.high24h.toFixed(4)}`;
                    if (lowElement) lowElement.textContent = `$${data.low24h.toFixed(4)}`;
                    if (volumeElement) volumeElement.textContent = `$${data.volume}M`;
                    if (marketCapElement) marketCapElement.textContent = `$${data.marketCap}M`;
                }
            }
            
            function buyODIS() {
                // Open StreamSwap in new tab
                window.open('https://app.streamswap.io/swap?from=uosmo&to=uodis', '_blank');
            }
            
            // Initialize ODIS token manager when DOM is loaded
            document.addEventListener('DOMContentLoaded', () => {
                new ODISTokenManager();
            });
            