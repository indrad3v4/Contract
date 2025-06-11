
/**
 * Enhanced Transaction List with Real Blockchain Data and AI Classification
 */
class EnhancedTransactionList {
    constructor() {
        this.rpcEndpoint = 'https://testnet-rpc.daodiseo.chaintools.tech';
        this.container = document.querySelector('.transaction-list');
        this.aiEnabled = false;
        this.lastUpdate = 0;
        this.updateInterval = 15000; // 15 seconds
        this.init();
    }

    async init() {
        await this.checkAIAvailability();
        await this.loadRealTransactions();
        this.startAutoUpdate();
    }

    async checkAIAvailability() {
        try {
            const response = await fetch('/api/bim-agent/enhanced-status');
            const data = await response.json();
            this.aiEnabled = data.success && data.enhanced_mode;
        } catch (error) {
            this.aiEnabled = false;
        }
    }

    async loadRealTransactions() {
        try {
            const [recentTxs, unconfirmedTxs] = await Promise.all([
                this.fetchRecentTransactions(),
                this.fetchUnconfirmedTransactions()
            ]);

            const processedTxs = await this.processTransactions([...recentTxs, ...unconfirmedTxs]);
            
            if (this.aiEnabled) {
                const classifiedTxs = await this.classifyWithAI(processedTxs);
                this.renderTransactions(classifiedTxs);
            } else {
                this.renderTransactions(processedTxs);
            }
        } catch (error) {
            console.error('Failed to load real transactions:', error);
            this.showErrorState();
        }
    }

    async fetchRecentTransactions() {
        try {
            const response = await fetch(`${this.rpcEndpoint}/tx_search?query=""`);
            const data = await response.json();
            return data.result?.txs?.slice(0, 10) || [];
        } catch {
            return [];
        }
    }

    async fetchUnconfirmedTransactions() {
        try {
            const response = await fetch(`${this.rpcEndpoint}/unconfirmed_txs?limit=5`);
            const data = await response.json();
            return data.result?.txs?.map(tx => ({ ...tx, unconfirmed: true })) || [];
        } catch {
            return [];
        }
    }

    async processTransactions(rawTxs) {
        return rawTxs.map(tx => {
            const decoded = this.decodeTxData(tx);
            return {
                hash: tx.hash || this.generateTxHash(),
                height: tx.height || 'Pending',
                timestamp: tx.timestamp || new Date(),
                type: decoded.type || 'transfer',
                amount: decoded.amount || '0',
                from: decoded.from || 'Unknown',
                to: decoded.to || 'Unknown',
                status: tx.unconfirmed ? 'pending' : 'confirmed',
                data: decoded
            };
        });
    }

    decodeTxData(tx) {
        try {
            // Decode base64 transaction data
            const txData = atob(tx.tx || '');
            
            // Basic transaction type detection
            if (txData.includes('MsgSend')) {
                return { type: 'transfer', amount: this.extractAmount(txData) };
            } else if (txData.includes('MsgDelegate')) {
                return { type: 'delegation', amount: this.extractAmount(txData) };
            } else if (txData.includes('MsgCreateValidator')) {
                return { type: 'validator_creation', amount: '0' };
            } else {
                return { type: 'unknown', amount: '0' };
            }
        } catch {
            return { type: 'unknown', amount: '0' };
        }
    }

    extractAmount(txData) {
        // Extract amount from transaction data
        const amountMatch = txData.match(/"amount":"(\d+)"/);
        return amountMatch ? parseInt(amountMatch[1]) / 1000000 : 0; // Convert from micro-units
    }

    async classifyWithAI(transactions) {
        if (!this.aiEnabled || transactions.length === 0) return transactions;

        try {
            const response = await fetch('/api/bim-agent/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': this.getCsrfToken()
                },
                body: JSON.stringify({
                    message: `Classify and analyze these blockchain transactions for real estate context: ${JSON.stringify(transactions.slice(0, 5))}`,
                    enhanced: true,
                    context: { 
                        component: 'transaction_list',
                        action: 'classify_transactions'
                    }
                })
            });

            const data = await response.json();
            if (data.success) {
                return this.applyAIClassification(transactions, data.response);
            }
        } catch (error) {
            console.warn('AI classification failed:', error);
        }

        return transactions;
    }

    applyAIClassification(transactions, aiResponse) {
        // Apply AI insights to transaction classification
        return transactions.map((tx, index) => {
            // Enhanced classification based on AI analysis
            const aiClassification = this.extractAIClassification(aiResponse, index);
            return {
                ...tx,
                aiClassification: aiClassification,
                riskScore: this.calculateRiskScore(tx, aiClassification),
                businessContext: this.getBusinessContext(tx.type)
            };
        });
    }

    extractAIClassification(aiResponse, index) {
        // Extract AI insights for specific transaction
        const insights = aiResponse.split('\n').filter(line => 
            line.includes('Transaction') || line.includes('Risk') || line.includes('Type')
        );
        return insights[index] || 'Standard transaction';
    }

    calculateRiskScore(tx, aiClassification) {
        let score = 0;
        
        if (tx.amount > 10000) score += 0.3;
        if (tx.status === 'pending') score += 0.2;
        if (aiClassification.includes('risk') || aiClassification.includes('suspicious')) score += 0.5;
        
        return Math.min(score, 1.0);
    }

    getBusinessContext(txType) {
        const contexts = {
            'transfer': 'Token Transfer',
            'delegation': 'Staking Operation',
            'validator_creation': 'Network Governance',
            'property_tokenization': 'Real Estate Tokenization',
            'contract_signature': 'Legal Document Signing',
            'unknown': 'General Transaction'
        };
        return contexts[txType] || contexts.unknown;
    }

    renderTransactions(transactions) {
        if (!this.container) return;

        this.container.innerHTML = transactions.map(tx => this.renderTransaction(tx)).join('');
        
        // Add click handlers for transaction details
        this.container.querySelectorAll('.transaction-item').forEach(item => {
            item.addEventListener('click', (e) => this.showTransactionDetails(e, tx));
        });
    }

    renderTransaction(tx) {
        const iconClass = this.getTransactionIcon(tx.type);
        const statusBadge = this.getStatusBadge(tx.status);
        const riskIndicator = tx.riskScore > 0.5 ? '<i class="risk-indicator" data-feather="alert-triangle"></i>' : '';
        
        return `
            <div class="transaction-item" data-tx-hash="${tx.hash}">
                <div class="transaction-icon ${tx.status}">
                    <i data-feather="${iconClass}"></i>
                </div>
                <div class="transaction-details">
                    <div class="transaction-title">
                        ${tx.businessContext} 
                        ${statusBadge}
                        ${riskIndicator}
                    </div>
                    <div class="transaction-meta">
                        <span class="transaction-address">${this.truncateAddress(tx.hash)}</span>
                        <span class="transaction-time">${this.formatTime(tx.timestamp)}</span>
                        ${tx.aiClassification ? `<span class="ai-insight" title="${tx.aiClassification}">AI</span>` : ''}
                    </div>
                </div>
                <div class="transaction-value ${tx.amount > 0 ? 'success' : tx.amount < 0 ? 'warning' : ''}">
                    ${tx.amount > 0 ? '+' : ''}${tx.amount} ODIS
                </div>
            </div>
        `;
    }

    getTransactionIcon(type) {
        const icons = {
            'transfer': 'arrow-right',
            'delegation': 'shield',
            'validator_creation': 'server',
            'property_tokenization': 'home',
            'contract_signature': 'file-text',
            'unknown': 'help-circle'
        };
        return icons[type] || icons.unknown;
    }

    getStatusBadge(status) {
        const badges = {
            'confirmed': '<span class="badge bg-success">CONFIRMED</span>',
            'pending': '<span class="badge bg-warning">PENDING</span>',
            'failed': '<span class="badge bg-danger">FAILED</span>'
        };
        return badges[status] || '';
    }

    truncateAddress(address) {
        if (!address || address.length < 10) return address;
        return `${address.slice(0, 6)}...${address.slice(-4)}`;
    }

    formatTime(timestamp) {
        const now = new Date();
        const time = new Date(timestamp);
        const diff = now - time;
        
        if (diff < 3600000) { // Less than 1 hour
            return `${Math.floor(diff / 60000)} min ago`;
        } else if (diff < 86400000) { // Less than 1 day
            return `${Math.floor(diff / 3600000)} hours ago`;
        } else {
            return `${Math.floor(diff / 86400000)} days ago`;
        }
    }

    showTransactionDetails(event, tx) {
        // Create modal or expanded view for transaction details
        const modal = document.createElement('div');
        modal.className = 'transaction-modal';
        modal.innerHTML = `
            <div class="transaction-modal-content">
                <div class="transaction-modal-header">
                    <h5>Transaction Details</h5>
                    <button class="close-modal">&times;</button>
                </div>
                <div class="transaction-modal-body">
                    <div class="detail-row">
                        <span class="label">Hash:</span>
                        <span class="value">${tx.hash}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Type:</span>
                        <span class="value">${tx.businessContext}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Amount:</span>
                        <span class="value">${tx.amount} ODIS</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Status:</span>
                        <span class="value">${tx.status}</span>
                    </div>
                    ${tx.aiClassification ? `
                    <div class="detail-row">
                        <span class="label">AI Analysis:</span>
                        <span class="value">${tx.aiClassification}</span>
                    </div>
                    ` : ''}
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        modal.querySelector('.close-modal').addEventListener('click', () => {
            document.body.removeChild(modal);
        });
    }

    startAutoUpdate() {
        setInterval(() => {
            this.loadRealTransactions();
        }, this.updateInterval);
    }

    showErrorState() {
        if (this.container) {
            this.container.innerHTML = `
                <div class="transaction-error">
                    <i data-feather="alert-circle"></i>
                    <span>Unable to load transaction data</span>
                </div>
            `;
        }
    }

    generateTxHash() {
        return '0x' + Array.from({ length: 8 }, () => 
            Math.floor(Math.random() * 16).toString(16)
        ).join('').toUpperCase();
    }

    getCsrfToken() {
        return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
    }
}

// Initialize enhanced transaction list
document.addEventListener('DOMContentLoaded', () => {
    new EnhancedTransactionList();
});
