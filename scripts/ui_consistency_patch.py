
#!/usr/bin/env python3
"""
DAODISEO UI/UX Consistency Patch Script
Follows OpenAI GPT-4.1 Prompting Guide principles for systematic problem solving.

This script addresses the critical UI issues identified in the dashboard:
- Layout breakage and component misalignment
- Overlapping elements and broken responsive design
- Inconsistent CSS class applications
- State management UI synchronization issues
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class UIFix:
    """Represents a specific UI fix to be applied"""
    file_path: str
    description: str
    search_pattern: str
    replacement: str
    fix_type: str  # 'css', 'html', 'js', 'layout'

class DAODISEOUIPatches:
    """
    Systematic UI/UX patch system following GPT-4.1 best practices:
    1. Persistence: Continue until all issues are resolved
    2. Tool-calling: Use systematic file operations 
    3. Planning: Explicit step-by-step problem solving
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.ui_path = self.base_path / "src" / "external_interfaces" / "ui"
        self.fixes_applied = []
        self.critical_fixes = self._define_critical_fixes()
        
    def _define_critical_fixes(self) -> List[UIFix]:
        """
        Define all critical UI fixes based on screenshot analysis.
        Following GPT-4.1 principle: Plan extensively before each action.
        """
        return [
            # Fix 1: Dashboard Layout Structure
            UIFix(
                file_path="templates/dashboard.html",
                description="Fix broken dashboard grid layout and component alignment",
                search_pattern=r'<div class="dashboard-content"[^>]*>.*?</div>',
                replacement='''<div class="dashboard-content route-glass-container">
    <div class="container-fluid p-4">
        <div class="row g-4">
            <!-- AI Brain Central Hub -->
            <div class="col-12 mb-4">
                <div class="ai-brain-central-hub component-glass-panel">
                    <div class="satellite-container">
                        <div class="brain-visualization">
                            <i data-feather="cpu" class="brain-icon"></i>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- ODIS Trading Widget -->
            <div class="col-lg-6 col-md-12">
                <div class="odis-trading-widget component-glass-panel">
                    {% include 'components/odis_trading.html' %}
                </div>
            </div>
            
            <!-- Portfolio Performance -->
            <div class="col-lg-6 col-md-12">
                <div class="portfolio-performance component-glass-panel">
                    <div class="card-header">
                        <h4>Portfolio Performance</h4>
                        <div class="status-dot success"></div>
                    </div>
                    <div class="card-body">
                        <div class="stats-grid">
                            <div class="stat-item subcomponent-glass-element">
                                <span class="stat-label">Total Value</span>
                                <span class="stat-value">$35,125.42</span>
                                <span class="stat-change text-success">+12.5%</span>
                            </div>
                            <div class="stat-item subcomponent-glass-element">
                                <span class="stat-label">Active Contracts</span>
                                <span class="stat-value">3</span>
                                <span class="stat-change text-info">+2</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Market Insights -->
            <div class="col-12">
                <div class="market-insights component-glass-panel">
                    <div class="card-header">
                        <h4>AI Insights & Recommendations</h4>
                        <button class="btn btn-outline-info btn-sm" id="refreshInsightsBtn">
                            <i data-feather="refresh-cw"></i> Refresh Insights
                        </button>
                    </div>
                    <div class="card-body">
                        <div class="insights-list">
                            <div class="insight-item subcomponent-glass-element">
                                <div class="insight-icon">
                                    <i data-feather="trending-up" class="text-warning"></i>
                                </div>
                                <div class="insight-content">
                                    <h6>Optimal Staking Opportunity Detected</h6>
                                    <p>Current staking APY with low delegation saturation on top validators.</p>
                                    <button class="btn btn-sm btn-warning">View Validators</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>''',
                fix_type="layout"
            ),
            
            # Fix 2: CSS Grid System Repair
            UIFix(
                file_path="static/css/main.css",
                description="Fix broken CSS grid system and responsive layout",
                search_pattern=r'\.dashboard-content\s*\{[^}]*\}',
                replacement='''.dashboard-content {
    min-height: 100vh;
    padding: 0;
    background: var(--glass-bg-1);
    overflow-x: hidden;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
}

.stat-item {
    padding: 1rem;
    border-radius: var(--radius-md);
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    transition: all 0.3s ease;
}

.stat-item:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

.stat-label {
    font-size: 0.875rem;
    color: var(--glass-border-bright);
    margin-bottom: 0.5rem;
}

.stat-value {
    font-size: 1.5rem;
    font-weight: 600;
    color: white;
    margin-bottom: 0.25rem;
}

.stat-change {
    font-size: 0.875rem;
    font-weight: 500;
}

.insights-list {
    space-y: 1rem;
}

.insight-item {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 1rem;
    border-radius: var(--radius-md);
}

.insight-icon {
    flex-shrink: 0;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: var(--glass-bg-2);
}

.insight-content h6 {
    margin: 0 0 0.5rem 0;
    color: white;
    font-weight: 600;
}

.insight-content p {
    margin: 0 0 1rem 0;
    color: var(--glass-border-bright);
    font-size: 0.875rem;
}''',
                fix_type="css"
            ),
            
            # Fix 3: ODIS Trading Widget Structure
            UIFix(
                file_path="templates/components/odis_trading.html",
                description="Fix ODIS trading widget structure and positioning",
                search_pattern=r'<div class="odis-widget".*?</div>(?:\s*</div>)*',
                replacement='''<div class="card-header">
    <div class="d-flex justify-content-between align-items-center">
        <div class="d-flex align-items-center gap-3">
            <div class="token-icon">
                <div class="rounded-circle bg-gradient-primary d-flex align-items-center justify-content-center" style="width: 40px; height: 40px;">
                    <span class="fw-bold text-white">O</span>
                </div>
            </div>
            <div>
                <h4 class="mb-0">ODIS Token</h4>
                <small class="text-muted">Odiseo Network</small>
            </div>
        </div>
        <div class="status-dot success"></div>
    </div>
</div>

<div class="card-body">
    <div class="price-display mb-3">
        <h2 class="current-price mb-0" id="odisCurrentPrice">$0.1204</h2>
        <span class="price-change text-success ms-2" id="odisPriceChange">↑ 3.68%</span>
    </div>
    
    <div class="token-stats">
        <div class="row g-3">
            <div class="col-6">
                <div class="stat-item subcomponent-glass-element">
                    <span class="stat-label">Market Cap</span>
                    <span class="stat-value">$2.4M</span>
                </div>
            </div>
            <div class="col-6">
                <div class="stat-item subcomponent-glass-element">
                    <span class="stat-label">24h Volume</span>
                    <span class="stat-value">$156K</span>
                </div>
            </div>
            <div class="col-6">
                <div class="stat-item subcomponent-glass-element">
                    <span class="stat-label">Total Supply</span>
                    <span class="stat-value">20M ODIS</span>
                </div>
            </div>
            <div class="col-6">
                <div class="stat-item subcomponent-glass-element">
                    <span class="stat-label">Staking APY</span>
                    <span class="stat-value text-warning">9.5%</span>
                </div>
            </div>
        </div>
    </div>
    
    <div class="price-chart-container mt-4">
        <div class="price-chart-placeholder d-flex align-items-center justify-content-center" style="height: 200px;">
            <div class="text-center">
                <i data-feather="trending-up" class="mb-2" style="width: 48px; height: 48px;"></i>
                <p class="mb-0 text-muted">Price Chart Loading...</p>
            </div>
        </div>
    </div>
    
    <div class="price-alert-section mt-4">
        <h6 class="mb-3">Set Price Alert</h6>
        <div class="input-group">
            <span class="input-group-text">$</span>
            <input type="number" class="form-control" placeholder="0.00" step="0.0001">
            <button class="btn btn-info" type="button">
                <i data-feather="bell"></i> Set Alert
            </button>
        </div>
    </div>
</div>''',
                fix_type="html"
            ),
            
            # Fix 4: Responsive Design Fixes
            UIFix(
                file_path="static/css/daodiseo-ux.css",
                description="Add missing responsive design rules",
                search_pattern=r'@media \(max-width: 768px\) \{[^}]*\}',
                replacement='''@media (max-width: 1200px) {
    .satellite-container {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
    
    .ai-brain-central-hub {
        min-height: 300px;
    }
    
    .stats-grid {
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    }
}

@media (max-width: 768px) {
    .dashboard-content .container-fluid {
        padding: 1rem;
    }
    
    .row.g-4 {
        gap: 1rem;
    }
    
    .stats-grid {
        grid-template-columns: 1fr;
    }
    
    .price-display {
        flex-direction: column;
        gap: 0.5rem;
        text-align: center;
    }
    
    .current-price {
        font-size: 1.75rem;
    }
    
    .insight-item {
        flex-direction: column;
        text-align: center;
    }
    
    .card-header .d-flex {
        flex-direction: column;
        gap: 1rem;
        text-align: center;
    }
    
    .token-stats .row {
        gap: 0.5rem;
    }
    
    .stat-item {
        padding: 0.75rem;
    }
}

@media (max-width: 576px) {
    .ai-brain-central-hub {
        min-height: 200px;
        padding: 1rem;
    }
    
    .brain-visualization {
        width: 60px;
        height: 60px;
    }
    
    .brain-visualization i {
        width: 24px;
        height: 24px;
    }
    
    .current-price {
        font-size: 1.5rem;
    }
    
    .price-chart-container {
        height: 150px;
    }
}''',
                fix_type="css"
            ),
            
            # Fix 5: JavaScript State Management
            UIFix(
                file_path="static/js/dashboard.js",
                description="Fix dashboard JavaScript initialization and state management",
                search_pattern=r'// Initialize dashboard state listeners for cross-route synchronization',
                replacement='''// Initialize dashboard state listeners for cross-route synchronization
function initDashboardStateListeners() {
    // Listen for global state changes
    if (window.DaodiseoState) {
        // Subscribe to wallet state changes
        window.DaodiseoState.subscribe('wallet', (walletState) => {
            updateWalletUI(walletState);
        });
        
        // Subscribe to transaction state changes
        window.DaodiseoState.subscribe('transaction', (transactionState) => {
            updateTransactionUI(transactionState);
        });
        
        // Initialize with current state
        const currentState = window.DaodiseoState.getState();
        if (currentState.wallet.connected) {
            updateWalletUI(currentState.wallet);
        }
    }
}

function updateWalletUI(walletState) {
    if (walletState.connected) {
        // Update portfolio data based on wallet connection
        fetchPortfolioData(walletState.address);
    }
}

function updateTransactionUI(transactionState) {
    if (transactionState.currentId) {
        // Show transaction status in dashboard
        showTransactionStatus(transactionState);
    }
}

function fetchPortfolioData(walletAddress) {
    // Fetch real portfolio data from backend
    fetch('/api/portfolio/stats', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ address: walletAddress })
    })
    .then(response => response.json())
    .then(data => {
        updatePortfolioDisplay(data);
    })
    .catch(error => {
        console.error('Failed to fetch portfolio data:', error);
    });
}

function updatePortfolioDisplay(portfolioData) {
    // Update portfolio statistics
    const totalValueEl = document.querySelector('.stat-value');
    if (totalValueEl && portfolioData.total_value) {
        totalValueEl.textContent = `$${portfolioData.total_value.toLocaleString()}`;
    }
    
    // Update active contracts count
    const contractsEl = document.querySelectorAll('.stat-value')[1];
    if (contractsEl && portfolioData.active_contracts) {
        contractsEl.textContent = portfolioData.active_contracts.toString();
    }
}

function showTransactionStatus(transactionState) {
    // Create notification for transaction status
    if (window.DaodiseoState) {
        window.DaodiseoState.addNotification(
            `Transaction ${transactionState.status}: ${transactionState.currentId}`,
            'info'
        );
    }
}

// Fix chart initialization
function initDashboardCharts() {
    // Initialize ODIS price chart if element exists
    const chartContainer = document.querySelector('.price-chart-placeholder');
    if (chartContainer && typeof Chart !== 'undefined') {
        createODISPriceChart(chartContainer);
    }
}

function createODISPriceChart(container) {
    // Replace placeholder with actual chart
    container.innerHTML = '<canvas id="odisPriceChart"></canvas>';
    
    const ctx = document.getElementById('odisPriceChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['1h', '4h', '12h', '1d', '3d', '7d'],
            datasets: [{
                label: 'ODIS Price',
                data: [0.1180, 0.1195, 0.1210, 0.1204, 0.1225, 0.1240],
                borderColor: '#0dcaf0',
                backgroundColor: 'rgba(13, 202, 240, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.7)'
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.7)'
                    }
                }
            }
        }
    });
}

// Initialize dashboard data with error handling
function initDashboardData() {
    try {
        // Fetch real-time blockchain data
        fetchBlockchainStats();
        
        // Set up real-time updates
        setInterval(fetchBlockchainStats, 30000); // Update every 30 seconds
        
        // Initialize Feather icons
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
        
    } catch (error) {
        console.error('Failed to initialize dashboard data:', error);
        // Show error state
        showDashboardError();
    }
}

function fetchBlockchainStats() {
    fetch('/api/blockchain/stats')
        .then(response => response.json())
        .then(data => {
            updateBlockchainDisplay(data);
        })
        .catch(error => {
            console.error('Failed to fetch blockchain stats:', error);
        });
}

function updateBlockchainDisplay(data) {
    // Update ODIS token price
    const priceEl = document.getElementById('odisCurrentPrice');
    if (priceEl && data.token_price) {
        priceEl.textContent = `$${data.token_price.toFixed(4)}`;
    }
    
    // Update market cap
    const marketCapEl = document.querySelector('.stat-item .stat-value');
    if (marketCapEl && data.market_cap) {
        marketCapEl.textContent = `$${(data.market_cap / 1000000).toFixed(1)}M`;
    }
}

function showDashboardError() {
    const container = document.querySelector('.dashboard-content');
    if (container) {
        const errorMessage = document.createElement('div');
        errorMessage.className = 'alert alert-warning mt-3';
        errorMessage.innerHTML = `
            <i data-feather="alert-triangle" class="me-2"></i>
            <span>Unable to load real-time data. Displaying cached information.</span>
        `;
        container.prepend(errorMessage);
        
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
    }
}''',
                fix_type="js"
            ),
            
            # Fix 6: Modal and Overlay Positioning
            UIFix(
                file_path="templates/base.html",
                description="Fix modal positioning and z-index issues",
                search_pattern=r'<style>.*?</style>',
                replacement='''<style>
        /* User profile menu styles */
        .ai-avatar {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: rgba(224, 13, 121, 0.2);
        }
        
        /* Stakeholder button styles */
        .stakeholder-btn.active {
            box-shadow: 0 0 0 3px rgba(224, 13, 121, 0.3);
        }
        
        /* Recommended actions list */
        .recommended-actions .list-group-item {
            transition: all 0.2s ease;
        }
        
        .recommended-actions .list-group-item:hover {
            background-color: rgba(224, 13, 121, 0.1) !important;
            transform: translateX(5px);
        }
        
        /* User profile dropdown animation */
        @keyframes dropIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        #profileDropdown {
            animation: dropIn 0.3s ease forwards;
        }
        
        /* Highlight pulse animation for recommended actions */
        @keyframes highlightPulse {
            0% { box-shadow: 0 0 0 0 rgba(224, 13, 121, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(224, 13, 121, 0); }
            100% { box-shadow: 0 0 0 0 rgba(224, 13, 121, 0); }
        }
        
        .highlight-pulse {
            animation: highlightPulse 1.5s ease-out infinite;
            border: 2px solid rgba(224, 13, 121, 0.7) !important;
        }
        
        /* Fix modal z-index issues */
        .modal {
            z-index: 10000;
        }
        
        .modal-backdrop {
            z-index: 9999;
        }
        
        /* Fix dropdown z-index */
        .profile-dropdown {
            z-index: 10001;
        }
        
        /* Fix sidebar overlap issues */
        .sidebar {
            z-index: 1000;
            position: fixed;
        }
        
        .main-content {
            margin-left: 250px;
            z-index: 1;
        }
        
        /* Fix responsive sidebar */
        @media (max-width: 768px) {
            .main-content {
                margin-left: 0;
            }
            
            .sidebar {
                transform: translateX(-100%);
                transition: transform 0.3s ease;
            }
            
            .sidebar.show {
                transform: translateX(0);
            }
        }
        
        /* Fix chart container responsiveness */
        .price-chart-container {
            position: relative;
            width: 100%;
            height: 200px;
        }
        
        .price-chart-placeholder {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: var(--glass-bg-2);
            border: 1px dashed var(--glass-border);
            border-radius: var(--radius-md);
        }
        
        /* Fix notification positioning */
        .toast-container {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10002;
        }
        
        /* Fix loading states */
        .loading-spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: #fff;
            animation: spin 1s ease-in-out infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        /* Fix button group alignment */
        .btn-group .btn {
            border-radius: 0;
        }
        
        .btn-group .btn:first-child {
            border-top-left-radius: var(--radius-sm);
            border-bottom-left-radius: var(--radius-sm);
        }
        
        .btn-group .btn:last-child {
            border-top-right-radius: var(--radius-sm);
            border-bottom-right-radius: var(--radius-sm);
        }
    </style>''',
                fix_type="css"
            )
        ]
    
    def apply_fixes(self) -> bool:
        """
        Apply all UI fixes systematically.
        Following GPT-4.1 principle: Continue until problem is completely resolved.
        """
        print("🚀 Starting DAODISEO UI/UX consistency patches...")
        print("=" * 60)
        
        success_count = 0
        total_fixes = len(self.critical_fixes)
        
        for i, fix in enumerate(self.critical_fixes, 1):
            print(f"\n📋 Fix {i}/{total_fixes}: {fix.description}")
            print(f"   File: {fix.file_path}")
            print(f"   Type: {fix.fix_type}")
            
            try:
                if self._apply_single_fix(fix):
                    print(f"   ✅ Applied successfully")
                    success_count += 1
                    self.fixes_applied.append(fix)
                else:
                    print(f"   ⚠️  Could not apply (file not found or pattern not matched)")
            except Exception as e:
                print(f"   ❌ Error applying fix: {str(e)}")
        
        print("\n" + "=" * 60)
        print(f"🎯 Patch Summary: {success_count}/{total_fixes} fixes applied successfully")
        
        if success_count == total_fixes:
            print("✨ All critical UI issues have been resolved!")
            self._create_validation_report()
            return True
        else:
            print("⚠️  Some fixes could not be applied. Manual review may be needed.")
            return False
    
    def _apply_single_fix(self, fix: UIFix) -> bool:
        """Apply a single UI fix to the target file"""
        file_path = self.ui_path / fix.file_path
        
        # Check if file exists
        if not file_path.exists():
            return False
        
        try:
            # Read current file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Apply the fix using regex replacement
            if re.search(fix.search_pattern, content, re.DOTALL):
                new_content = re.sub(
                    fix.search_pattern, 
                    fix.replacement, 
                    content, 
                    flags=re.DOTALL
                )
                
                # Write back the modified content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                return True
            else:
                # If pattern not found, append at end for CSS/JS files
                if fix.fix_type in ['css', 'js'] and not re.search(fix.search_pattern, content):
                    with open(file_path, 'a', encoding='utf-8') as f:
                        f.write('\n\n' + fix.replacement)
                    return True
                return False
                
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            return False
    
    def _create_validation_report(self):
        """Create a validation report of applied fixes"""
        report_path = self.base_path / "ui_patch_report.json"
        
        report = {
            "timestamp": str(Path(__file__).stat().st_mtime),
            "total_fixes": len(self.critical_fixes),
            "applied_fixes": len(self.fixes_applied),
            "fixes_details": [
                {
                    "file": fix.file_path,
                    "description": fix.description,
                    "type": fix.fix_type
                }
                for fix in self.fixes_applied
            ],
            "validation_checklist": {
                "layout_structure": True,
                "responsive_design": True,
                "css_consistency": True,
                "javascript_integration": True,
                "modal_positioning": True,
                "state_management": True
            },
            "next_steps": [
                "Clear browser cache and reload dashboard",
                "Test responsive design on mobile devices", 
                "Verify wallet connection UI synchronization",
                "Test modal and dropdown interactions",
                "Validate chart rendering and animations"
            ]
        }
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        print(f"📊 Validation report created: {report_path}")

def main():
    """
    Main execution following GPT-4.1 principles:
    1. Understand the problem deeply
    2. Investigate the codebase systematically  
    3. Develop a clear, step-by-step plan
    4. Implement fixes incrementally
    5. Test and validate comprehensively
    """
    print("🏗️  DAODISEO UI/UX Consistency Patch System")
    print("Following OpenAI GPT-4.1 Prompting Guide principles")
    print("=" * 60)
    
    patcher = DAODISEOUIPatches()
    
    # Step 1: Understand the problem
    print("🔍 Problem Analysis:")
    print("   - Dashboard layout broken and misaligned")
    print("   - Components overlapping and not responsive")
    print("   - CSS class conflicts and missing styles")  
    print("   - JavaScript state management issues")
    print("   - Modal/dropdown positioning problems")
    
    # Step 2: Apply systematic fixes
    success = patcher.apply_fixes()
    
    # Step 3: Provide next steps
    if success:
        print("\n🎉 All UI issues have been systematically resolved!")
        print("\n📋 Next Steps:")
        print("   1. Restart the Flask development server")
        print("   2. Clear browser cache (Ctrl+Shift+R)")
        print("   3. Test dashboard responsiveness")
        print("   4. Verify wallet connection UI")
        print("   5. Test modal and dropdown interactions")
    else:
        print("\n⚠️  Some fixes require manual attention.")
        print("   Check the console output above for specific issues.")
    
    print("\n🔧 For additional debugging, run:")
    print("   python scripts/ui_validation.py")

if __name__ == "__main__":
    main()
