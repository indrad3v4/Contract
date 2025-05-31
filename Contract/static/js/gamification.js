
            // DAODISEO Gamification System
            class GamificationManager {
                constructor() {
                    this.points = parseInt(localStorage.getItem('daodiseo_points') || '0');
                    this.achievements = JSON.parse(localStorage.getItem('daodiseo_achievements') || '[]');
                    this.updatePointsDisplay();
                }
                
                addPoints(amount, reason = '') {
                    this.points += amount;
                    localStorage.setItem('daodiseo_points', this.points.toString());
                    this.updatePointsDisplay();
                    this.showPointsNotification(amount, reason);
                }
                
                updatePointsDisplay() {
                    const pointsElement = document.getElementById('user-points');
                    if (pointsElement) {
                        pointsElement.textContent = this.points;
                    }
                }
                
                showPointsNotification(amount, reason) {
                    const notification = document.createElement('div');
                    notification.className = 'points-notification';
                    notification.innerHTML = `
                        <div class="points-gained">+${amount} pts</div>
                        <div class="points-reason">${reason}</div>
                    `;
                    document.body.appendChild(notification);
                    
                    setTimeout(() => {
                        notification.remove();
                    }, 3000);
                }
            }
            
            function showGamificationModal() {
                const modal = document.createElement('div');
                modal.className = 'gamification-modal';
                modal.innerHTML = `
                    <div class="modal-content">
                        <div class="modal-header">
                            <h2>Your DAODISEO Journey</h2>
                            <span class="close-modal" onclick="closeGamificationModal()">&times;</span>
                        </div>
                        <div class="modal-body">
                            <div class="points-section">
                                <div class="total-points">
                                    <span class="points-number">${gamificationManager.points}</span>
                                    <span class="points-label">Total Points</span>
                                </div>
                            </div>
                            <div class="achievements-section">
                                <h3>Available Rewards</h3>
                                <div class="reward-item">
                                    <div class="reward-icon">🏠</div>
                                    <div class="reward-info">
                                        <div class="reward-name">First Property Upload</div>
                                        <div class="reward-points">+50 pts</div>
                                    </div>
                                </div>
                                <div class="reward-item">
                                    <div class="reward-icon">💰</div>
                                    <div class="reward-info">
                                        <div class="reward-name">First Token Purchase</div>
                                        <div class="reward-points">+100 pts</div>
                                    </div>
                                </div>
                                <div class="reward-item">
                                    <div class="reward-icon">🔗</div>
                                    <div class="reward-info">
                                        <div class="reward-name">Wallet Connected</div>
                                        <div class="reward-points">+25 pts</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                document.body.appendChild(modal);
            }
            
            function closeGamificationModal() {
                const modal = document.querySelector('.gamification-modal');
                if (modal) {
                    modal.remove();
                }
            }
            
            // Initialize gamification system
            let gamificationManager;
            document.addEventListener('DOMContentLoaded', () => {
                gamificationManager = new GamificationManager();
            });
            