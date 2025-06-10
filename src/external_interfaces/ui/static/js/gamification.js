// DAODISEO Gamification System
class DaodiseoGamification {
    constructor() {
        this.ODIS = parseInt(localStorage.getItem('dds_user_ODIS') || '0');
        this.level = this.calculateLevel(this.ODIS);
        this.achievements = JSON.parse(localStorage.getItem('dds_achievements') || '[]');
        
        this.rewardActions = {
            'upload_bim': 0.3,
            'sign_contract': 0.5,
            'submit_transaction': 1.0,
            'login_platform': 0.1,
            'view_property': 0.05,
            'become_validator': 0.75,
            'share_property': 0.15,
            'complete_profile': 0.2,
            'connect_wallet': 0.25
        };
        
        this.init();
    }
    
    init() {
        this.updatePointsDisplay();
        this.bindEvents();
        this.checkAchievements();
        this.createGamificationModal();
    }
    
    awardPoints(action, amount = null) {
        const ODIS = amount || this.rewardActions[action] || 0;
        if (ODIS > 0) {
            this.ODIS += ODIS;
            localStorage.setItem('dds_user_ODIS', this.ODIS.toString());
            
            this.showPointsAnimation(ODIS);
            this.updatePointsDisplay();
            this.checkLevelUp();
            
            console.log(`Awarded ${ODIS} ODIS for ${action}`);
        }
    }
    
    updatePointsDisplay() {
        const ODISElement = document.getElementById('userPoints');
        if (ODISElement) {
            ODISElement.textContent = `${this.ODIS} ODIS`;
        }
    }
    
    showPointsAnimation(ODIS) {
        const animation = document.createElement('div');
        animation.className = 'ODIS-animation';
        animation.textContent = `+${ODIS} ODIS`;
        animation.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            color: var(--dds-accent-cyan);
            font-weight: bold;
            z-index: 9999;
            animation: floatUp 2s ease-out forwards;
            pointer-events: none;
            font-size: 1.2rem;
            text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
        `;
        
        document.body.appendChild(animation);
        setTimeout(() => animation.remove(), 2000);
    }
    
    calculateLevel(ODIS) {
        return Math.floor(ODIS / 100) + 1;
    }
    
    checkLevelUp() {
        const newLevel = this.calculateLevel(this.ODIS);
        if (newLevel > this.level) {
            this.level = newLevel;
            this.showLevelUpNotification();
        }
    }
    
    showLevelUpNotification() {
        console.log(`Level up! Now level ${this.level}`);
        this.showNotification(`Level Up! You're now level ${this.level}`, 'success');
    }
    
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `dds-notification dds-notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            background: var(--dds-gradient-card);
            border: 1px solid var(--dds-accent-cyan);
            border-radius: 12px;
            color: var(--dds-white);
            z-index: 10000;
            animation: slideInRight 0.3s ease-out;
        `;
        
        document.body.appendChild(notification);
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
    
    createGamificationModal() {
        const modal = document.createElement('div');
        modal.id = 'gamificationModal';
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i data-feather="star" class="icon-inline me-2"></i>
                            Blockchain Rewards
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="row">
                            <div class="col-md-4">
                                <div class="level-display text-center mb-4">
                                    <div class="level-circle">
                                        <span class="level-number">${this.level}</span>
                                    </div>
                                    <div class="level-text mt-2">
                                        <div class="level-title">Level ${this.level}</div>
                                        <div class="level-subtitle">${this.ODIS} ODIS (${100 - (this.ODIS % 100)} to next level)</div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-8">
                                <div class="achievements-section">
                                    <h6 class="mb-3">Achievements</h6>
                                    <div class="achievements-grid">
                                        <div class="achievement-item ${this.achievements.includes('first_upload') ? 'completed' : ''}">
                                            <i data-feather="upload" class="achievement-icon"></i>
                                            <div class="achievement-text">
                                                <div class="achievement-name">First Upload</div>
                                                <div class="achievement-desc">Upload your first BIM model</div>
                                            </div>
                                        </div>
                                        <div class="achievement-item ${this.achievements.includes('contract_master') ? 'completed' : ''}">
                                            <i data-feather="file-text" class="achievement-icon"></i>
                                            <div class="achievement-text">
                                                <div class="achievement-name">Contract Master</div>
                                                <div class="achievement-desc">Sign your first smart contract</div>
                                            </div>
                                        </div>
                                        <div class="achievement-item ${this.achievements.includes('validator_candidate') ? 'completed' : ''}">
                                            <i data-feather="shield" class="achievement-icon"></i>
                                            <div class="achievement-text">
                                                <div class="achievement-name">Validator Candidate</div>
                                                <div class="achievement-desc">Reach 200 ODIS</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="mt-4">
                            <h6 class="mb-3">Actions & Points</h6>
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="action-item">
                                        <i data-feather="link" class="action-icon"></i>
                                        <span class="action-name">Connect Keplr wallet</span>
                                        <span class="action-ODIS">+25</span>
                                    </div>
                                    <div class="action-item">
                                        <i data-feather="upload" class="action-icon"></i>
                                        <span class="action-name">Upload a BIM model</span>
                                        <span class="action-ODIS">+30</span>
                                    </div>
                                    <div class="action-item">
                                        <i data-feather="file-text" class="action-icon"></i>
                                        <span class="action-name">Sign a smart contract</span>
                                        <span class="action-ODIS">+50</span>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="action-item">
                                        <i data-feather="eye" class="action-icon"></i>
                                        <span class="action-name">View a property contract</span>
                                        <span class="action-ODIS">+5</span>
                                    </div>
                                    <div class="action-item">
                                        <i data-feather="log-in" class="action-icon"></i>
                                        <span class="action-name">Log into the platform</span>
                                        <span class="action-ODIS">+10</span>
                                    </div>
                                    <div class="action-item">
                                        <i data-feather="send" class="action-icon"></i>
                                        <span class="action-name">Submit a blockchain transaction</span>
                                        <span class="action-ODIS">+100</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
    }
    
    bindEvents() {
        // Bind gamification toggle button
        document.addEventListener('click', (e) => {
            if (e.target.closest('#gamificationToggle')) {
                const modal = new bootstrap.Modal(document.getElementById('gamificationModal'));
                modal.show();
            }
            
            // Award ODIS for specific actions
            if (e.target.closest('#uploadForm button[type="submit"]')) {
                this.awardPoints('upload_bim');
            }
            if (e.target.closest('#connectKeplrBtn') || e.target.closest('#headerConnectKeplr')) {
                this.awardPoints('connect_wallet');
            }
            if (e.target.closest('.btn-delegate')) {
                this.awardPoints('become_validator');
            }
        });
        
        // Award ODIS for page views
        const path = window.location.pathname;
        if (path.includes('/viewer') && !sessionStorage.getItem('viewed_property_' + path)) {
            this.awardPoints('view_property');
            sessionStorage.setItem('viewed_property_' + path, 'true');
        }
        
        // Award login ODIS (once per session)
        if (!sessionStorage.getItem('login_ODIS_awarded')) {
            this.awardPoints('login_platform');
            sessionStorage.setItem('login_ODIS_awarded', 'true');
        }
    }
    
    checkAchievements() {
        const achievements = [
            { id: 'first_upload', name: 'First Upload', requirement: 'ODIS >= 30' },
            { id: 'contract_master', name: 'Contract Master', requirement: 'ODIS >= 100' },
            { id: 'validator_candidate', name: 'Validator Candidate', requirement: 'ODIS >= 200' }
        ];
        
        achievements.forEach(achievement => {
            if (!this.achievements.includes(achievement.id)) {
                if (eval(achievement.requirement.replace('ODIS', this.ODIS))) {
                    this.achievements.push(achievement.id);
                    localStorage.setItem('dds_achievements', JSON.stringify(this.achievements));
                    this.showNotification(`Achievement unlocked: ${achievement.name}`, 'success');
                }
            }
        });
    }
}

// Initialize gamification system
document.addEventListener('DOMContentLoaded', () => {
    window.ddsGamification = new DaodiseoGamification();
    
    // Add CSS for animations and styling
    const style = document.createElement('style');
    style.textContent = `
        @keyframes floatUp {
            0% { opacity: 1; transform: translateY(0); }
            100% { opacity: 0; transform: translateY(-50px); }
        }
        
        @keyframes slideInRight {
            0% { transform: translateX(100%); opacity: 0; }
            100% { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes slideOutRight {
            0% { transform: translateX(0); opacity: 1; }
            100% { transform: translateX(100%); opacity: 0; }
        }
        
        .ODIS-animation {
            font-size: 1.2rem;
            text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
        }
        
        .level-circle {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: var(--dds-gradient-brain);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto;
            border: 2px solid var(--dds-accent-cyan);
            box-shadow: var(--dds-shadow-brain);
        }
        
        .level-number {
            font-size: 2rem;
            font-weight: 700;
            color: var(--dds-white);
        }
        
        .level-title {
            font-weight: 600;
            color: var(--dds-accent-cyan);
        }
        
        .level-subtitle {
            font-size: 0.875rem;
            color: rgba(255, 255, 255, 0.7);
        }
        
        .achievement-item {
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 0.75rem;
            margin-bottom: 0.5rem;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }
        
        .achievement-item.completed {
            background: rgba(0, 212, 255, 0.1);
            border-color: var(--dds-accent-cyan);
        }
        
        .achievement-icon {
            width: 24px;
            height: 24px;
            color: var(--dds-accent-cyan);
        }
        
        .achievement-name {
            font-weight: 600;
            color: var(--dds-white);
        }
        
        .achievement-desc {
            font-size: 0.875rem;
            color: rgba(255, 255, 255, 0.7);
        }
        
        .action-item {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.5rem 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .action-icon {
            width: 20px;
            height: 20px;
            color: var(--dds-accent-cyan);
        }
        
        .action-name {
            flex: 1;
            color: var(--dds-white);
        }
        
        .action-ODIS {
            font-weight: 600;
            color: var(--dds-accent-cyan);
        }
    `;
    document.head.appendChild(style);
});