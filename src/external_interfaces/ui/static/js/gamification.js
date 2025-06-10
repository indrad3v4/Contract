
// DAODISEO Gamification System
class GamificationSystem {
    constructor() {
        this.points = parseInt(localStorage.getItem('daodiseo_points') || '0');
        this.level = Math.floor(this.points / 100) + 1;
        this.init();
    }
    
    init() {
        this.updatePointsDisplay();
        this.bindEvents();
    }
    
    updatePointsDisplay() {
        const pointsElement = document.getElementById('userPoints');
        if (pointsElement) {
            pointsElement.textContent = `${this.points} pts`;
        }
    }
    
    bindEvents() {
        const pointsBtn = document.getElementById('pointsSystemBtn');
        if (pointsBtn) {
            pointsBtn.addEventListener('click', () => {
                const modal = new bootstrap.Modal(document.getElementById('blockchainRewardsModal'));
                modal.show();
            });
        }
    }
    
    addPoints(amount, action) {
        this.points += amount;
        localStorage.setItem('daodiseo_points', this.points.toString());
        this.updatePointsDisplay();
        this.showPointsAnimation(amount, action);
    }
    
    showPointsAnimation(points, action) {
        // Create floating animation
        const animation = document.createElement('div');
        animation.className = 'points-animation';
        animation.textContent = `+${points} pts`;
        animation.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--dds-gradient-brain);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: 600;
            z-index: 10000;
            animation: pointsFloat 3s ease-out forwards;
        `;
        
        document.body.appendChild(animation);
        setTimeout(() => animation.remove(), 3000);
    }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    window.gamificationSystem = new GamificationSystem();
});

// Add CSS animation
const style = document.createElement('style');
style.textContent = `
@keyframes pointsFloat {
    0% { transform: translateY(0) scale(1); opacity: 1; }
    50% { transform: translateY(-20px) scale(1.1); opacity: 1; }
    100% { transform: translateY(-60px) scale(0.8); opacity: 0; }
}
`;
document.head.appendChild(style);
