// Enhanced Transaction List with Real Blockchain Data
console.log("Enhanced transaction list loading with blockchain integration...");

class EnhancedTransactionList {
    constructor() {
        this.transactionContainer = null;
        this.initialize();
    }
    
    async initialize() {
        this.transactionContainer = document.querySelector('.recent-transactions-content');
        if (!this.transactionContainer) {
            setTimeout(() => this.initialize(), 500);
            return;
        }
        
        await this.loadTransactions();
        this.startPeriodicUpdates();
    }
    
    async loadTransactions() {
        try {
            console.log("Loading recent transactions...");
            const response = await fetch('/api/blockchain/recent-transactions');
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success && data.data?.transactions) {
                this.displayTransactions(data.data.transactions);
                console.log("✅ Transactions loaded successfully");
            } else {
                this.showEmptyState();
            }
            
        } catch (error) {
            console.error('Failed to load transactions:', error);
            this.showErrorState();
        }
    }
    
    displayTransactions(transactions) {
        if (!transactions || transactions.length === 0) {
            this.showEmptyState();
            return;
        }
        
        const transactionHtml = transactions.map(tx => `
            <div class="transaction-item" data-tx-hash="${tx.hash}">
                <div class="transaction-icon">
                    <i data-feather="${this.getTransactionIcon(tx.type)}"></i>
                </div>
                <div class="transaction-details">
                    <div class="transaction-type">${tx.type || 'Transaction'}</div>
                    <div class="transaction-hash">${this.formatHash(tx.hash)}</div>
                    <div class="transaction-time">${this.formatTime(tx.timestamp)}</div>
                </div>
                <div class="transaction-amount">
                    <span class="amount">${tx.amount || '0'} ODIS</span>
                    <span class="status-badge ${tx.status || 'pending'}">${tx.status || 'pending'}</span>
                </div>
            </div>
        `).join('');
        
        this.transactionContainer.innerHTML = transactionHtml;
        
        // Initialize feather icons for transaction icons
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
    }
    
    showEmptyState() {
        this.transactionContainer.innerHTML = `
            <div class="empty-state">
                <i data-feather="activity"></i>
                <p>No recent transactions</p>
                <small>Transactions will appear here once network activity begins</small>
            </div>
        `;
        
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
    }
    
    showErrorState() {
        this.transactionContainer.innerHTML = `
            <div class="error-state">
                <i data-feather="alert-circle"></i>
                <p>Unable to load transactions</p>
                <button onclick="location.reload()" class="retry-button">Retry</button>
            </div>
        `;
        
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
    }
    
    getTransactionIcon(type) {
        const iconMap = {
            'send': 'arrow-up-right',
            'receive': 'arrow-down-left', 
            'stake': 'lock',
            'unstake': 'unlock',
            'vote': 'check-circle',
            'delegate': 'users'
        };
        
        return iconMap[type?.toLowerCase()] || 'activity';
    }
    
    formatHash(hash) {
        if (!hash) return 'N/A';
        return hash.length > 12 ? `${hash.slice(0, 6)}...${hash.slice(-6)}` : hash;
    }
    
    formatTime(timestamp) {
        if (!timestamp) return 'Unknown time';
        
        try {
            const date = new Date(timestamp);
            const now = new Date();
            const diffMs = now - date;
            const diffMins = Math.floor(diffMs / 60000);
            
            if (diffMins < 1) return 'Just now';
            if (diffMins < 60) return `${diffMins}m ago`;
            if (diffMins < 1440) return `${Math.floor(diffMins / 60)}h ago`;
            return `${Math.floor(diffMins / 1440)}d ago`;
        } catch {
            return 'Unknown time';
        }
    }
    
    startPeriodicUpdates() {
        // Refresh every 30 seconds
        setInterval(() => {
            this.loadTransactions();
        }, 30000);
        
        console.log("✅ Transaction list periodic updates started");
    }
}

// Initialize enhanced transaction list
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        new EnhancedTransactionList();
    }, 2000);
});

// Add transaction list styling
const transactionStyle = document.createElement('style');
transactionStyle.textContent = `
.transaction-item {
    display: flex;
    align-items: center;
    padding: 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    transition: background-color 0.2s ease;
}

.transaction-item:hover {
    background: rgba(255, 255, 255, 0.05);
}

.transaction-icon {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    background: rgba(0, 255, 157, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 12px;
}

.transaction-icon i {
    color: #00ff9d;
    width: 20px;
    height: 20px;
}

.transaction-details {
    flex: 1;
}

.transaction-type {
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 2px;
}

.transaction-hash {
    font-size: 0.85rem;
    color: #a0a0a0;
    margin-bottom: 2px;
}

.transaction-time {
    font-size: 0.8rem;
    color: #707070;
}

.transaction-amount {
    text-align: right;
}

.transaction-amount .amount {
    display: block;
    font-weight: 600;
    color: #00ff9d;
    margin-bottom: 4px;
}

.empty-state, .error-state {
    text-align: center;
    padding: 40px 20px;
    color: #a0a0a0;
}

.empty-state i, .error-state i {
    width: 48px;
    height: 48px;
    margin-bottom: 16px;
    opacity: 0.5;
}

.retry-button {
    margin-top: 12px;
    padding: 8px 16px;
    background: rgba(0, 255, 157, 0.2);
    border: 1px solid #00ff9d;
    border-radius: 6px;
    color: #00ff9d;
    cursor: pointer;
    transition: all 0.2s ease;
}

.retry-button:hover {
    background: rgba(0, 255, 157, 0.3);
}
`;
document.head.appendChild(transactionStyle);
