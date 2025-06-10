/**
 * DAODISEO Gamification System
 * Handles blockchain rewards, ODIS payments, and cross-route action tracking
 */

class GamificationSystem {
    constructor() {
        this.actions = {
            'connect-wallet': { points: 25, cost: 0.01, name: 'Connect Keplr wallet' },
            'sign-contract': { points: 50, cost: 0.02, name: 'Sign a smart contract' },
            'submit-transaction': { points: 100, cost: 0.05, name: 'Submit a blockchain transaction' },
            'login': { points: 10, cost: 0.005, name: 'Log into the platform' },
            'view-contract': { points: 5, cost: 0.002, name: 'View a property contract' },
            'upload-bim': { points: 30, cost: 0.015, name: 'Upload a BIM model' },
            'share-property': { points: 15, cost: 0.008, name: 'Share a property' },
            'become-validator': { points: 75, cost: 0.04, name: 'Become a validator' },
            'complete-profile': { points: 20, cost: 0.01, name: 'Complete your profile' }
        };
        
        this.achievements = {
            'wallet': { name: 'Wallet Connected', description: 'Connected Keplr wallet' },
            'contract': { name: 'Contract Signer', description: 'Signed first smart contract' },
            'transaction': { name: 'Transaction Master', description: 'Submitted first transaction' },
            'validator': { name: 'Network Validator', description: 'Became a validator' },
            'search': { name: 'Explorer', description: 'Used search functionality' }
        };
        
        this.userLevel = 1;
        this.userPoints = 0;
        this.completedActions = new Set();
        this.earnedAchievements = new Set();
        
        this.loadUserProgress();
        this.bindActionTracking();
    }

    // Load user progress from global state
    loadUserProgress() {
        if (typeof GlobalState !== 'undefined') {
            const gamificationState = GlobalState.getState('gamification') || {};
            this.userPoints = gamificationState.points || 0;
            this.userLevel = gamificationState.level || 1;
            this.completedActions = new Set(gamificationState.completedActions || []);
            this.earnedAchievements = new Set(gamificationState.achievements || []);
        }
        
        this.updatePointsDisplay();
    }

    // Save user progress to global state
    saveUserProgress() {
        if (typeof GlobalState !== 'undefined') {
            GlobalState.setState('gamification', {
                points: this.userPoints,
                level: this.userLevel,
                completedActions: Array.from(this.completedActions),
                achievements: Array.from(this.earnedAchievements)
            });
        }
    }

    // Update points display in header
    updatePointsDisplay() {
        const pointsBadge = document.getElementById('userPoints');
        const levelText = document.querySelector('.level-text');
        
        if (pointsBadge) {
            pointsBadge.textContent = `${this.userPoints} pts`;
        }
        
        if (levelText) {
            levelText.textContent = `Level ${this.userLevel}`;
        }
    }

    // Bind action tracking to various UI events
    bindActionTracking() {
        // Track wallet connection
        document.addEventListener('walletConnected', () => {
            this.completeAction('connect-wallet');
            this.earnAchievement('wallet');
        });

        // Track contract signing
        document.addEventListener('contractSigned', () => {
            this.completeAction('sign-contract');
            this.earnAchievement('contract');
        });

        // Track transaction submission
        document.addEventListener('transactionSubmitted', () => {
            this.completeAction('submit-transaction');
            this.earnAchievement('transaction');
        });

        // Track BIM upload
        document.addEventListener('bimUploaded', () => {
            this.completeAction('upload-bim');
        });

        // Track contract viewing
        document.addEventListener('contractViewed', () => {
            this.completeAction('view-contract');
        });

        // Track property sharing
        document.addEventListener('propertyShared', () => {
            this.completeAction('share-property');
        });

        // Track validator actions
        document.addEventListener('validatorAction', () => {
            this.completeAction('become-validator');
            this.earnAchievement('validator');
        });

        // Track search usage
        document.addEventListener('searchUsed', () => {
            this.earnAchievement('search');
        });

        // Track login
        if (this.userPoints === 0 && !this.completedActions.has('login')) {
            this.completeAction('login');
        }
    }

    // Complete an action and award points
    async completeAction(actionId) {
        if (this.completedActions.has(actionId)) {
            return; // Action already completed
        }

        const action = this.actions[actionId];
        if (!action) {
            console.warn(`Unknown action: ${actionId}`);
            return;
        }

        try {
            // Check if user has sufficient ODIS for the action
            const hasBalance = await this.checkOdisBalance(action.cost);
            if (!hasBalance) {
                this.showInsufficientBalanceNotification(action.cost);
                return;
            }

            // Process ODIS payment
            await this.processOdisPayment(action.cost, action.name);

            // Award points
            this.userPoints += action.points;
            this.completedActions.add(actionId);

            // Check for level up
            this.checkLevelUp();

            // Save progress
            this.saveUserProgress();

            // Update UI
            this.updatePointsDisplay();
            this.showActionCompletedNotification(action);

            // Mark action as completed in modal
            this.markActionCompleted(actionId);

        } catch (error) {
            console.error('Error completing action:', error);
            this.showErrorNotification('Failed to complete action. Please try again.');
        }
    }

    // Check if user has sufficient ODIS balance
    async checkOdisBalance(requiredAmount) {
        try {
            // Get wallet address from global state
            const walletState = GlobalState.getState('wallet');
            if (!walletState || !walletState.address) {
                return false;
            }

            // Check balance via blockchain API
            const response = await fetch(`/api/blockchain/balance/${walletState.address}`);
            const data = await response.json();
            
            const balance = parseFloat(data.balance) || 0;
            return balance >= requiredAmount;
            
        } catch (error) {
            console.error('Error checking ODIS balance:', error);
            return false;
        }
    }

    // Process ODIS payment for action
    async processOdisPayment(amount, actionName) {
        try {
            const walletState = GlobalState.getState('wallet');
            if (!walletState || !walletState.address) {
                throw new Error('Wallet not connected');
            }

            // Create payment transaction
            const paymentData = {
                from_address: walletState.address,
                to_address: 'odiseo1gamification0pool0address0000000000000000', // Gamification pool
                amount: Math.round(amount * 1000000), // Convert to uodis
                memo: `Gamification payment for: ${actionName}`
            };

            const response = await fetch('/api/blockchain/send-tokens', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(paymentData)
            });

            if (!response.ok) {
                throw new Error('Payment transaction failed');
            }

            const result = await response.json();
            console.log('ODIS payment processed:', result);

        } catch (error) {
            console.error('Error processing ODIS payment:', error);
            throw error;
        }
    }

    // Check for level up
    checkLevelUp() {
        const pointsForNextLevel = this.userLevel * 100;
        if (this.userPoints >= pointsForNextLevel) {
            this.userLevel++;
            this.showLevelUpNotification();
        }
    }

    // Earn an achievement
    earnAchievement(achievementId) {
        if (this.earnedAchievements.has(achievementId)) {
            return; // Achievement already earned
        }

        const achievement = this.achievements[achievementId];
        if (!achievement) {
            return;
        }

        this.earnedAchievements.add(achievementId);
        this.saveUserProgress();
        this.showAchievementNotification(achievement);
        this.markAchievementEarned(achievementId);
    }

    // Mark action as completed in modal
    markActionCompleted(actionId) {
        const actionElement = document.querySelector(`[data-action="${actionId}"]`);
        if (actionElement) {
            actionElement.classList.add('completed');
            actionElement.style.opacity = '0.6';
            actionElement.style.pointerEvents = 'none';
        }
    }

    // Mark achievement as earned in modal
    markAchievementEarned(achievementId) {
        const achievementElement = document.querySelector(`[data-achievement="${achievementId}"]`);
        if (achievementElement) {
            achievementElement.classList.add('earned');
        }
    }

    // Show notifications
    showActionCompletedNotification(action) {
        this.showNotification(
            `Action Completed! +${action.points} points`,
            `You earned ${action.points} points for: ${action.name}`,
            'success'
        );
    }

    showLevelUpNotification() {
        this.showNotification(
            `Level Up! 🎉`,
            `Congratulations! You reached Level ${this.userLevel}`,
            'success'
        );
    }

    showAchievementNotification(achievement) {
        this.showNotification(
            `Achievement Unlocked! 🏆`,
            `${achievement.name}: ${achievement.description}`,
            'achievement'
        );
    }

    showInsufficientBalanceNotification(requiredAmount) {
        this.showNotification(
            `Insufficient ODIS Balance`,
            `You need ${requiredAmount} ODIS to complete this action. Please add funds to your wallet.`,
            'warning'
        );
    }

    showErrorNotification(message) {
        this.showNotification('Error', message, 'error');
    }

    // Generic notification system
    showNotification(title, message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <div class="notification-title">${title}</div>
                <div class="notification-message">${message}</div>
            </div>
            <button class="notification-close">&times;</button>
        `;

        // Add to page
        document.body.appendChild(notification);

        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);

        // Manual close
        notification.querySelector('.notification-close').addEventListener('click', () => {
            notification.remove();
        });
    }

    // Update modal with current user data
    updateModal() {
        // Update level progress
        const levelNumber = document.querySelector('.level-number');
        const currentPointsSpan = document.getElementById('currentPoints');
        const levelProgress = document.getElementById('levelProgress');

        if (levelNumber) levelNumber.textContent = this.userLevel;
        if (currentPointsSpan) currentPointsSpan.textContent = `${this.userPoints} points`;

        if (levelProgress) {
            const pointsForNextLevel = this.userLevel * 100;
            const progressPercent = (this.userPoints % 100);
            levelProgress.style.width = `${progressPercent}%`;
        }

        // Mark completed actions
        this.completedActions.forEach(actionId => {
            this.markActionCompleted(actionId);
        });

        // Mark earned achievements
        this.earnedAchievements.forEach(achievementId => {
            this.markAchievementEarned(achievementId);
        });

        // Add action click handlers
        document.querySelectorAll('.action-item').forEach(item => {
            const actionId = item.dataset.action;
            if (!this.completedActions.has(actionId)) {
                item.addEventListener('click', () => {
                    this.completeAction(actionId);
                });
            }
        });
    }
}

// Global functions
window.updateGamificationModal = function() {
    if (window.gamificationSystem) {
        window.gamificationSystem.updateModal();
    }
};

window.initGamificationSystem = function() {
    window.gamificationSystem = new GamificationSystem();
};

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    window.initGamificationSystem();
});

// CSS for notifications
const notificationCSS = `
.notification {
    position: fixed;
    top: 20px;
    right: 20px;
    background: var(--dds-gradient-card);
    border: 1px solid var(--dds-accent-cyan);
    border-radius: 12px;
    padding: 1rem;
    max-width: 300px;
    z-index: 10000;
    animation: slideInRight 0.3s ease-out;
    box-shadow: var(--dds-shadow-elevated);
}

.notification-success {
    border-color: var(--dds-accent-cyan);
    background: rgba(0, 212, 255, 0.1);
}

.notification-warning {
    border-color: var(--dds-magenta);
    background: rgba(196, 30, 140, 0.1);
}

.notification-error {
    border-color: var(--dds-risk-red);
    background: rgba(220, 38, 38, 0.1);
}

.notification-achievement {
    border-color: gold;
    background: rgba(255, 215, 0, 0.1);
}

.notification-content {
    color: var(--dds-white);
}

.notification-title {
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.notification-message {
    font-size: 0.875rem;
    opacity: 0.9;
}

.notification-close {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    background: none;
    border: none;
    color: var(--dds-white);
    font-size: 1.2rem;
    cursor: pointer;
    opacity: 0.7;
}

.notification-close:hover {
    opacity: 1;
}

@keyframes slideInRight {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}
`;

// Inject notification CSS
const style = document.createElement('style');
style.textContent = notificationCSS;
document.head.appendChild(style);