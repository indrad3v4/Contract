
// ODIS Payment System for Actions
class OdisPaymentSystem {
    constructor() {
        this.balance = parseFloat(localStorage.getItem('odis_balance') || '0');
        this.transactions = JSON.parse(localStorage.getItem('odis_transactions') || '[]');
        this.actionPrices = {
            'connect_wallet': 0.25,
            'upload_bim': 0.30, 
            'sign_contract': 0.50,
            'submit_transaction': 1.00,
            'view_property': 0.05,
            'become_validator': 0.75,
            'share_property': 0.15,
            'complete_profile': 0.20,
            'login_platform': 0.10
        };
    }
    
    canAfford(action) {
        const price = this.actionPrices[action] || 0;
        return this.balance >= price;
    }
    
    processPayment(action) {
        const price = this.actionPrices[action] || 0;
        if (this.canAfford(action)) {
            this.balance -= price;
            this.recordTransaction(action, price);
            this.updateBalance();
            return true;
        }
        return false;
    }
    
    recordTransaction(action, amount) {
        const transaction = {
            id: Date.now(),
            action: action,
            amount: amount,
            timestamp: new Date().toISOString(),
            type: 'payment'
        };
        this.transactions.unshift(transaction);
        localStorage.setItem('odis_transactions', JSON.stringify(this.transactions.slice(0, 100)));
    }
    
    updateBalance() {
        localStorage.setItem('odis_balance', this.balance.toString());
        this.updateBalanceDisplay();
    }
    
    updateBalanceDisplay() {
        const balanceElements = document.querySelectorAll('#userPoints, .odis-balance');
        balanceElements.forEach(element => {
            element.textContent = `${this.balance.toFixed(2)} ODIS`;
        });
    }
    
    addOdis(amount, reason = 'reward') {
        this.balance += amount;
        this.recordTransaction(reason, amount);
        this.updateBalance();
        this.showBalanceNotification(`+${amount} ODIS received`);
    }
    
    showBalanceNotification(message) {
        // Implementation for balance change notifications
        console.log(message);
    }
}

// Initialize ODIS payment system
window.odisPaymentSystem = new OdisPaymentSystem();
