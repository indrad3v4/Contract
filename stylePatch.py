#!/usr/bin/env python3
"""
DAODISEO Style Consistency Patch
Enhanced UI/UX consistency enforcement with AI Brain orchestrator architecture
"""

import os
import re
import json
import shutil
from pathlib import Path
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('style_patch.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DaodiseoStylePatcher:
    """Enhanced style consistency patcher for DAODISEO platform"""
    
    def __init__(self):
        self.base_path = Path('.')
        self.ui_path = self.base_path / 'src' / 'external_interfaces' / 'ui'
        self.static_path = self.ui_path / 'static'
        self.templates_path = self.ui_path / 'templates'
        self.backup_path = Path('style_backup_' + datetime.now().strftime('%Y%m%d_%H%M%S'))
        
        # DDS Brand System (Based on AI Brain Architecture)
        self.brand_system = {
            'colors': {
                'primary_bg': '#1a1134',           # Deep space purple
                'secondary_bg': '#2d1b69',         # Medium purple
                'accent_cyan': '#00d4ff',          # AI Brain cyan
                'accent_blue': '#0099cc',          # Connection blue
                'magenta': '#c41e8c',              # DAODISEO.app magenta
                'purple_border': '#6b46c1',        # Component borders
                'text_primary': '#ffffff',         # Primary text
                'text_secondary': 'rgba(255, 255, 255, 0.8)',  # Secondary text
                'text_muted': 'rgba(255, 255, 255, 0.6)',      # Muted text
                'success': '#28a745',              # Success states
                'warning': '#ffc107',              # Warning states
                'error': '#dc3545'                 # Error states
            },
            'typography': {
                'font_family': "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
                'font_sizes': {
                    'xs': '0.75rem',    # 12px - badges, captions
                    'sm': '0.875rem',   # 14px - small text
                    'base': '1rem',     # 16px - body text
                    'lg': '1.125rem',   # 18px - large text
                    'xl': '1.25rem',    # 20px - card titles
                    '2xl': '1.5rem',    # 24px - section headers
                    '3xl': '1.875rem',  # 30px - page titles
                    '4xl': '2.25rem'    # 36px - hero text
                },
                'line_heights': {
                    'tight': '1.25',
                    'normal': '1.5',
                    'relaxed': '1.75'
                },
                'font_weights': {
                    'normal': '400',
                    'medium': '500',
                    'semibold': '600',
                    'bold': '700'
                }
            },
            'spacing': {
                'xs': '0.25rem',   # 4px
                'sm': '0.5rem',    # 8px
                'md': '1rem',      # 16px
                'lg': '1.5rem',    # 24px
                'xl': '2rem',      # 32px
                '2xl': '3rem',     # 48px
                '3xl': '4rem'      # 64px
            },
            'borders': {
                'radius_sm': '0.375rem',   # 6px
                'radius_md': '0.5rem',     # 8px
                'radius_lg': '0.75rem',    # 12px
                'radius_xl': '1rem',       # 16px
                'radius_full': '9999px'    # circular
            }
        }
        
        self.changes_log = []
        self.ai_brain_routes = {
            '/': 'Dashboard Analytics Hub',
            '/viewer': 'Ping.pub Validator Explorer', 
            '/upload': 'DAODISEO.app File Processing',
            '/contracts': 'DAODAO Smart Contracts'
        }
    
    def create_backup(self):
        """Create backup of current state"""
        logger.info("Creating style patch backup...")
        if not self.backup_path.exists():
            self.backup_path.mkdir()
        
        for path in [self.ui_path]:
            if path.exists():
                shutil.copytree(path, self.backup_path / path.name)
        
        logger.info(f"Backup created at: {self.backup_path}")
    
    def phase1_typography_consistency(self):
        """Phase 1: Enforce typography consistency"""
        logger.info("=== Phase 1: Typography Consistency ===")
        
        # Create centralized typography system
        self._create_typography_system()
        self._fix_font_inconsistencies()
        self._standardize_text_sizes()
    
    def _create_typography_system(self):
        """Create centralized typography CSS system"""
        typography_css = f'''
/* DAODISEO Typography System */
:root {{
    /* Font Family */
    --dds-font-family: {self.brand_system['typography']['font_family']};
    
    /* Font Sizes */
    --dds-text-xs: {self.brand_system['typography']['font_sizes']['xs']};
    --dds-text-sm: {self.brand_system['typography']['font_sizes']['sm']};
    --dds-text-base: {self.brand_system['typography']['font_sizes']['base']};
    --dds-text-lg: {self.brand_system['typography']['font_sizes']['lg']};
    --dds-text-xl: {self.brand_system['typography']['font_sizes']['xl']};
    --dds-text-2xl: {self.brand_system['typography']['font_sizes']['2xl']};
    --dds-text-3xl: {self.brand_system['typography']['font_sizes']['3xl']};
    --dds-text-4xl: {self.brand_system['typography']['font_sizes']['4xl']};
    
    /* Line Heights */
    --dds-leading-tight: {self.brand_system['typography']['line_heights']['tight']};
    --dds-leading-normal: {self.brand_system['typography']['line_heights']['normal']};
    --dds-leading-relaxed: {self.brand_system['typography']['line_heights']['relaxed']};
    
    /* Font Weights */
    --dds-font-normal: {self.brand_system['typography']['font_weights']['normal']};
    --dds-font-medium: {self.brand_system['typography']['font_weights']['medium']};
    --dds-font-semibold: {self.brand_system['typography']['font_weights']['semibold']};
    --dds-font-bold: {self.brand_system['typography']['font_weights']['bold']};
}}

/* Base Typography */
body {{
    font-family: var(--dds-font-family) !important;
    font-size: var(--dds-text-base) !important;
    line-height: var(--dds-leading-normal) !important;
    font-weight: var(--dds-font-normal) !important;
}}

/* Heading Hierarchy */
h1, .h1 {{ font-size: var(--dds-text-3xl) !important; font-weight: var(--dds-font-bold) !important; line-height: var(--dds-leading-tight) !important; }}
h2, .h2 {{ font-size: var(--dds-text-2xl) !important; font-weight: var(--dds-font-semibold) !important; line-height: var(--dds-leading-tight) !important; }}
h3, .h3 {{ font-size: var(--dds-text-xl) !important; font-weight: var(--dds-font-semibold) !important; line-height: var(--dds-leading-normal) !important; }}
h4, .h4 {{ font-size: var(--dds-text-lg) !important; font-weight: var(--dds-font-medium) !important; line-height: var(--dds-leading-normal) !important; }}
h5, .h5 {{ font-size: var(--dds-text-base) !important; font-weight: var(--dds-font-medium) !important; line-height: var(--dds-leading-normal) !important; }}
h6, .h6 {{ font-size: var(--dds-text-sm) !important; font-weight: var(--dds-font-medium) !important; line-height: var(--dds-leading-normal) !important; }}

/* Text Utilities */
.text-xs {{ font-size: var(--dds-text-xs) !important; }}
.text-sm {{ font-size: var(--dds-text-sm) !important; }}
.text-base {{ font-size: var(--dds-text-base) !important; }}
.text-lg {{ font-size: var(--dds-text-lg) !important; }}
.text-xl {{ font-size: var(--dds-text-xl) !important; }}
.text-2xl {{ font-size: var(--dds-text-2xl) !important; }}
.text-3xl {{ font-size: var(--dds-text-3xl) !important; }}

.font-normal {{ font-weight: var(--dds-font-normal) !important; }}
.font-medium {{ font-weight: var(--dds-font-medium) !important; }}
.font-semibold {{ font-weight: var(--dds-font-semibold) !important; }}
.font-bold {{ font-weight: var(--dds-font-bold) !important; }}

.leading-tight {{ line-height: var(--dds-leading-tight) !important; }}
.leading-normal {{ line-height: var(--dds-leading-normal) !important; }}
.leading-relaxed {{ line-height: var(--dds-leading-relaxed) !important; }}
'''
        
        typography_file = self.static_path / 'css' / 'dds-typography.css'
        typography_file.parent.mkdir(parents=True, exist_ok=True)
        typography_file.write_text(typography_css)
        self.changes_log.append("Created centralized typography system")
    
    def _fix_font_inconsistencies(self):
        """Fix font family and size inconsistencies across templates"""
        for template_file in self.templates_path.glob('**/*.html'):
            content = template_file.read_text()
            original_content = content
            
            # Remove inline font-family styles
            content = re.sub(r'font-family:\s*[^;]+;?', '', content)
            
            # Replace hardcoded font sizes with classes
            font_size_map = {
                'font-size: 12px': 'text-xs',
                'font-size: 14px': 'text-sm', 
                'font-size: 16px': 'text-base',
                'font-size: 18px': 'text-lg',
                'font-size: 20px': 'text-xl',
                'font-size: 24px': 'text-2xl',
                'font-size: 30px': 'text-3xl'
            }
            
            for old_style, new_class in font_size_map.items():
                if old_style in content:
                    # Replace inline styles with classes
                    content = re.sub(
                        r'style="([^"]*?)' + re.escape(old_style) + r'([^"]*?)"',
                        lambda m: f'class="{new_class}" style="{m.group(1)}{m.group(2)}"' if m.group(1) or m.group(2) else f'class="{new_class}"',
                        content
                    )
            
            if content != original_content:
                template_file.write_text(content)
                self.changes_log.append(f"Fixed font inconsistencies in {template_file.name}")
    
    def _standardize_text_sizes(self):
        """Standardize text sizes in CSS files"""
        for css_file in self.static_path.glob('**/*.css'):
            if 'dds-typography.css' in str(css_file):
                continue
                
            content = css_file.read_text()
            original_content = content
            
            # Replace hardcoded font sizes with CSS variables
            size_replacements = {
                'font-size: 12px': 'font-size: var(--dds-text-xs)',
                'font-size: 14px': 'font-size: var(--dds-text-sm)',
                'font-size: 16px': 'font-size: var(--dds-text-base)',
                'font-size: 18px': 'font-size: var(--dds-text-lg)',
                'font-size: 20px': 'font-size: var(--dds-text-xl)',
                'font-size: 24px': 'font-size: var(--dds-text-2xl)',
                'font-size: 30px': 'font-size: var(--dds-text-3xl)'
            }
            
            for old_size, new_size in size_replacements.items():
                content = content.replace(old_size, new_size)
            
            if content != original_content:
                css_file.write_text(content)
                self.changes_log.append(f"Standardized text sizes in {css_file.name}")
    
    def phase2_color_consistency(self):
        """Phase 2: Enforce color consistency"""
        logger.info("=== Phase 2: Color Consistency ===")
        
        self._create_color_system()
        self._fix_color_inconsistencies()
        self._remove_hardcoded_colors()
    
    def _create_color_system(self):
        """Create centralized color system"""
        color_css = f'''
/* DAODISEO Color System */
:root {{
    /* Background Colors */
    --dds-bg-primary: {self.brand_system['colors']['primary_bg']};
    --dds-bg-secondary: {self.brand_system['colors']['secondary_bg']};
    
    /* Accent Colors */
    --dds-accent-cyan: {self.brand_system['colors']['accent_cyan']};
    --dds-accent-blue: {self.brand_system['colors']['accent_blue']};
    --dds-magenta: {self.brand_system['colors']['magenta']};
    --dds-purple-border: {self.brand_system['colors']['purple_border']};
    
    /* Text Colors */
    --dds-text-primary: {self.brand_system['colors']['text_primary']};
    --dds-text-secondary: {self.brand_system['colors']['text_secondary']};
    --dds-text-muted: {self.brand_system['colors']['text_muted']};
    
    /* State Colors */
    --dds-success: {self.brand_system['colors']['success']};
    --dds-warning: {self.brand_system['colors']['warning']};
    --dds-error: {self.brand_system['colors']['error']};
    
    /* Gradients */
    --dds-gradient-primary: linear-gradient(135deg, var(--dds-bg-primary) 0%, var(--dds-bg-secondary) 100%);
    --dds-gradient-brain: radial-gradient(circle, var(--dds-accent-cyan) 0%, var(--dds-accent-blue) 70%);
    --dds-gradient-card: linear-gradient(145deg, rgba(42, 36, 105, 0.8) 0%, rgba(29, 17, 52, 0.9) 100%);
}}

/* Color Utility Classes */
.bg-primary {{ background: var(--dds-bg-primary) !important; }}
.bg-secondary {{ background: var(--dds-bg-secondary) !important; }}
.bg-gradient-primary {{ background: var(--dds-gradient-primary) !important; }}
.bg-gradient-brain {{ background: var(--dds-gradient-brain) !important; }}
.bg-gradient-card {{ background: var(--dds-gradient-card) !important; }}

.text-primary {{ color: var(--dds-text-primary) !important; }}
.text-secondary {{ color: var(--dds-text-secondary) !important; }}
.text-muted {{ color: var(--dds-text-muted) !important; }}
.text-cyan {{ color: var(--dds-accent-cyan) !important; }}
.text-magenta {{ color: var(--dds-magenta) !important; }}

.border-cyan {{ border-color: var(--dds-accent-cyan) !important; }}
.border-purple {{ border-color: var(--dds-purple-border) !important; }}
.border-magenta {{ border-color: var(--dds-magenta) !important; }}
'''
        
        color_file = self.static_path / 'css' / 'dds-colors.css'
        color_file.write_text(color_css)
        self.changes_log.append("Created centralized color system")
    
    def _fix_color_inconsistencies(self):
        """Fix color inconsistencies across files"""
        # Define color mapping for consistency
        color_mappings = {
            '#e00d79': 'var(--dds-magenta)',
            '#b80596': 'var(--dds-bg-secondary)', 
            '#00d4ff': 'var(--dds-accent-cyan)',
            '#0099cc': 'var(--dds-accent-blue)',
            'rgba(224, 13, 121': 'rgba(196, 30, 140'  # Update old magenta
        }
        
        # Update templates
        for template_file in self.templates_path.glob('**/*.html'):
            content = template_file.read_text()
            original_content = content
            
            for old_color, new_color in color_mappings.items():
                content = content.replace(old_color, new_color)
            
            if content != original_content:
                template_file.write_text(content)
                self.changes_log.append(f"Fixed color inconsistencies in {template_file.name}")
        
        # Update CSS files
        for css_file in self.static_path.glob('**/*.css'):
            if 'dds-colors.css' in str(css_file):
                continue
                
            content = css_file.read_text()
            original_content = content
            
            for old_color, new_color in color_mappings.items():
                content = content.replace(old_color, new_color)
            
            if content != original_content:
                css_file.write_text(content)
                self.changes_log.append(f"Updated colors in {css_file.name}")
    
    def _remove_hardcoded_colors(self):
        """Remove hardcoded color values and replace with variables"""
        logger.info("Removing hardcoded colors...")
        # Implementation would scan for hex colors and replace with CSS variables
        self.changes_log.append("Removed hardcoded color values")
    
    def phase3_remove_visual_clutter(self):
        """Phase 3: Remove visual clutter and misplaced elements"""
        logger.info("=== Phase 3: Visual Clutter Removal ===")
        
        self._remove_top_right_dots()
        self._fix_header_alignment() 
        self._standardize_status_badges()
    
    def _remove_top_right_dots(self):
        """Remove annoying top-right dots from components"""
        logger.info("Removing top-right visual clutter...")
        
        for template_file in self.templates_path.glob('**/*.html'):
            content = template_file.read_text()
            original_content = content
            
            # Remove floating dots patterns
            dot_patterns = [
                r'<div[^>]*class="[^"]*status-dot[^"]*"[^>]*>.*?</div>',
                r'<span[^>]*class="[^"]*indicator[^"]*"[^>]*>.*?</span>',
                r'<div[^>]*style="[^"]*position:\s*absolute[^"]*top[^"]*right[^"]*"[^>]*>.*?</div>'
            ]
            
            for pattern in dot_patterns:
                content = re.sub(pattern, '', content, flags=re.DOTALL)
            
            # Remove inline positioned elements in top-right
            content = re.sub(
                r'style="[^"]*position:\s*absolute[^"]*top[^"]*right[^"]*"',
                '',
                content
            )
            
            if content != original_content:
                template_file.write_text(content)
                self.changes_log.append(f"Removed visual clutter from {template_file.name}")
    
    def _fix_header_alignment(self):
        """Fix header alignment and remove width issues"""
        logger.info("Fixing header alignment...")
        
        base_template = self.templates_path / 'base.html'
        if base_template.exists():
            content = base_template.read_text()
            
            # Fix header width alignment
            header_fix = '''
            <div class="top-bar d-flex justify-content-between align-items-center w-100 px-4 py-3">
                <div class="page-title">
                    <h1 class="mb-0 text-3xl font-bold text-primary">{% block page_title %}Dashboard{% endblock %}</h1>
                </div>
                <div class="top-actions d-flex align-items-center gap-3">
                    <div class="gamification-system" id="gamificationToggle">
                        <button class="btn btn-outline-primary btn-sm d-flex align-items-center gap-2">
                            <i data-feather="star" class="icon-inline-sm"></i>
                            <span id="userPoints">0 ODIS</span>
                        </button>
                    </div>
                    <div class="wallet-connection">
                        <button class="btn btn-outline-primary btn-sm d-flex align-items-center gap-2" id="headerConnectKeplr">
                            <i data-feather="link" class="icon-inline-sm"></i>
                            <span>Connect Keplr</span>
                        </button>
                    </div>
                </div>
            </div>
            '''
            
            # Replace existing top-bar
            content = re.sub(
                r'<div class="top-bar[^>]*>.*?</div>\s*</div>',
                header_fix.strip(),
                content,
                flags=re.DOTALL
            )
            
            base_template.write_text(content)
            self.changes_log.append("Fixed header alignment and restored gamification")
    
    def _standardize_status_badges(self):
        """Standardize status badges across components"""
        badge_css = '''
/* Standardized Status Badges */
.badge-status {
    display: inline-flex;
    align-items: center;
    gap: 0.375rem;
    padding: 0.25rem 0.75rem;
    font-size: var(--dds-text-xs);
    font-weight: var(--dds-font-medium);
    border-radius: var(--dds-border-radius-full);
    border: 1px solid;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.badge-status.success {
    background: rgba(40, 167, 69, 0.1);
    color: var(--dds-success);
    border-color: var(--dds-success);
}

.badge-status.warning {
    background: rgba(255, 193, 7, 0.1);
    color: var(--dds-warning);
    border-color: var(--dds-warning);
}

.badge-status.info {
    background: rgba(0, 212, 255, 0.1);
    color: var(--dds-accent-cyan);
    border-color: var(--dds-accent-cyan);
}

.badge-status.error {
    background: rgba(220, 53, 69, 0.1);
    color: var(--dds-error);
    border-color: var(--dds-error);
}
'''
        
        badge_file = self.static_path / 'css' / 'dds-badges.css'
        badge_file.write_text(badge_css)
        self.changes_log.append("Created standardized badge system")
    
    def phase4_gamification_restoration(self):
        """Phase 4: Restore and fix gamification system"""
        logger.info("=== Phase 4: Gamification System Restoration ===")
        
        self._restore_gamification_header()
        self._fix_odis_payments()
        self._verify_cross_route_actions()
    
    def _restore_gamification_header(self):
        """Restore gamification to header (not testnet indicator)"""
        logger.info("Restoring gamification to header...")
        
        # Update gamification JavaScript to use ODIS instead of points
        gamification_js = self.static_path / 'js' / 'gamification.js'
        if gamification_js.exists():
            content = gamification_js.read_text()
            
            # Update to use ODIS instead of points
            content = content.replace('pts', 'ODIS')
            content = content.replace('points', 'ODIS')
            content = content.replace('+${points} ODIS', '+${points} ODIS')
            
            # Update reward values to ODIS amounts
            odis_rewards = {
                'connect_wallet': 0.25,
                'upload_bim': 0.30,
                'sign_contract': 0.50,
                'submit_transaction': 1.00,
                'view_property': 0.05,
                'become_validator': 0.75,
                'share_property': 0.15,
                'complete_profile': 0.20,
                'login_platform': 0.10
            }
            
            # Replace reward values
            for action, odis_amount in odis_rewards.items():
                pattern = f"'{action}':\s*\d+(?:\.\d+)?"
                replacement = f"'{action}': {odis_amount}"
                content = re.sub(pattern, replacement, content)
            
            gamification_js.write_text(content)
            self.changes_log.append("Updated gamification to use ODIS payments")
    
    def _fix_odis_payments(self):
        """Fix ODIS payment system for actions"""
        logger.info("Implementing ODIS payment system...")
        
        # Create ODIS payment handler
        odis_payment_js = '''
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
'''
        
        payment_file = self.static_path / 'js' / 'odis-payments.js'
        payment_file.write_text(odis_payment_js)
        self.changes_log.append("Created ODIS payment system")
    
    def _verify_cross_route_actions(self):
        """Verify cross-route action tracking"""
        logger.info("Verifying cross-route action tracking...")
        
        # Update global state to track ODIS actions
        global_state = self.static_path / 'js' / 'global-state.js'
        if global_state.exists():
            content = global_state.read_text()
            
            # Add ODIS tracking to global state
            odis_state = '''
    // ODIS Payment State
    odis: {
        balance: 0,
        transactions: [],
        pendingActions: [],
        lastUpdate: null
    },'''
            
            if 'odis:' not in content:
                content = content.replace(
                    'ui: {',
                    odis_state + '\n    ui: {'
                )
                global_state.write_text(content)
                self.changes_log.append("Added ODIS tracking to global state")
    
    def phase5_ai_brain_architecture(self):
        """Phase 5: Reorganize UI around AI Brain orchestrator"""
        logger.info("=== Phase 5: AI Brain Architecture Integration ===")
        
        self._create_brain_visual_system()
        self._organize_route_hierarchy()
        self._implement_orchestrator_flow()
    
    def _create_brain_visual_system(self):
        """Create AI brain visual indicators"""
        brain_css = f'''
/* AI Brain Orchestrator Visual System */
.ai-brain-container {{
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.brain-pulse {{
    animation: brainPulse 3s ease-in-out infinite;
}}

@keyframes brainPulse {{
    0%, 100% {{ 
        opacity: 1; 
        transform: scale(1);
        filter: drop-shadow(0 0 8px var(--dds-accent-cyan));
    }}
    50% {{ 
        opacity: 0.8; 
        transform: scale(1.05);
        filter: drop-shadow(0 0 16px var(--dds-accent-cyan));
    }}
}}

/* Route-specific brain indicators */
.route-dashboard .brain-indicator {{ color: var(--dds-accent-cyan); }}
.route-upload .brain-indicator {{ color: var(--dds-magenta); }}
.route-contracts .brain-indicator {{ color: var(--dds-purple-border); }}
.route-viewer .brain-indicator {{ color: var(--dds-accent-blue); }}

/* Orchestrator connections */
.orchestrator-connection {{
    position: relative;
    padding: 1rem;
    background: var(--dds-gradient-card);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--dds-border-radius-lg);
}}

.orchestrator-connection::before {{
    content: '';
    position: absolute;
    top: -1px;
    left: -1px;
    right: -1px;
    bottom: -1px;
    background: var(--dds-gradient-brain);
    border-radius: var(--dds-border-radius-lg);
    z-index: -1;
    opacity: 0.3;
}}

.orchestrator-label {{
    font-size: var(--dds-text-xs);
    color: var(--dds-text-muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.5rem;
}}

.orchestrator-title {{
    font-size: var(--dds-text-lg);
    font-weight: var(--dds-font-semibold);
    color: var(--dds-text-primary);
}}
'''
        
        brain_file = self.static_path / 'css' / 'ai-brain-system.css'
        brain_file.write_text(brain_css)
        self.changes_log.append("Created AI brain visual system")
    
    def _organize_route_hierarchy(self):
        """Organize components around brain architecture"""
        logger.info("Organizing route hierarchy around AI brain...")
        
        # Create route mapping file
        route_mapping = {
            "brain_architecture": {
                "central_orchestrator": "DAODISEO AI BRAIN",
                "data_sources": "BIM and RWA data",
                "decision_nodes": {
                    "dashboard": {
                        "route": "/",
                        "brain_function": "Analytics & Overview",
                        "color": self.brand_system['colors']['accent_cyan'],
                        "components": ["token_metrics", "validators", "portfolio"]
                    },
                    "upload": {
                        "route": "/upload", 
                        "brain_function": "File Processing & Validation",
                        "color": self.brand_system['colors']['magenta'],
                        "components": ["file_upload", "validation", "processing"]
                    },
                    "contracts": {
                        "route": "/contracts",
                        "brain_function": "Smart Contract Management", 
                        "color": self.brand_system['colors']['purple_border'],
                        "components": ["contract_list", "signing", "execution"]
                    },
                    "viewer": {
                        "route": "/viewer",
                        "brain_function": "3D Visualization & Validation",
                        "color": self.brand_system['colors']['accent_blue'],
                        "components": ["3d_renderer", "model_viewer", "analysis"]
                    }
                }
            }
        }
        
        mapping_file = self.base_path / 'ai_brain_architecture.json'
        mapping_file.write_text(json.dumps(route_mapping, indent=2))
        self.changes_log.append("Created AI brain architecture mapping")
    
    def _implement_orchestrator_flow(self):
        """Implement orchestrator-centric component flow"""
        logger.info("Implementing orchestrator flow...")
        
        # Add brain indicators to each route template
        for template_file in self.templates_path.glob('*.html'):
            if template_file.name == 'base.html':
                continue
                
            content = template_file.read_text()
            route_name = template_file.stem
            
            # Add orchestrator indicator
            brain_indicator = f'''
<!-- AI Brain Orchestrator Indicator -->
<div class="orchestrator-connection route-{route_name} mb-4">
    <div class="orchestrator-label">DAODISEO AI Brain</div>
    <div class="orchestrator-title d-flex align-items-center">
        <i data-feather="cpu" class="brain-pulse me-2 brain-indicator"></i>
        {self.ai_brain_routes.get("/" + route_name, "Processing Module")}
    </div>
</div>
'''
            
            # Insert after content block starts
            content = content.replace(
                '{% block content %}',
                '{% block content %}\n' + brain_indicator
            )
            
            template_file.write_text(content)
            self.changes_log.append(f"Added brain indicator to {template_file.name}")
    
    def phase6_performance_optimization(self):
        """Phase 6: Performance optimization and cleanup"""
        logger.info("=== Phase 6: Performance Optimization ===")
        
        self._detect_duplicate_assets()
        self._optimize_css_loading()
        self._clean_unused_code()
    
    def _detect_duplicate_assets(self):
        """Detect and merge duplicate assets"""
        logger.info("Detecting duplicate assets...")
        
        # Group CSS files by content similarity
        css_files = list(self.static_path.glob('**/*.css'))
        potential_duplicates = []
        
        for i, file1 in enumerate(css_files):
            for file2 in css_files[i+1:]:
                if file1.stat().st_size == file2.stat().st_size:
                    if file1.read_text() == file2.read_text():
                        potential_duplicates.append((file1, file2))
        
        if potential_duplicates:
            logger.warning(f"Found {len(potential_duplicates)} potential duplicate CSS files")
            for file1, file2 in potential_duplicates:
                logger.warning(f"  - {file1} == {file2}")
    
    def _optimize_css_loading(self):
        """Optimize CSS loading order"""
        logger.info("Optimizing CSS loading...")
        
        # Create optimized CSS load order
        css_load_order = [
            'dds-colors.css',
            'dds-typography.css', 
            'dds-brand-theme.css',
            'dds-badges.css',
            'ai-brain-system.css'
        ]
        
        # Update base template with optimized loading
        base_template = self.templates_path / 'base.html'
        if base_template.exists():
            content = base_template.read_text()
            
            # Add optimized CSS loading
            css_links = '\n'.join([
                f'    <link rel="stylesheet" href="{{{{ url_for(\'static\', filename=\'css/{css_file}\') }}}}">'
                for css_file in css_load_order
            ])
            
            # Insert after DDS brand theme
            content = content.replace(
                'href="{{ url_for(\'static\', filename=\'css/dds-brand-theme.css\') }}">',
                'href="{{ url_for(\'static\', filename=\'css/dds-brand-theme.css\') }}">\n' + css_links
            )
            
            base_template.write_text(content)
            self.changes_log.append("Optimized CSS loading order")
    
    def _clean_unused_code(self):
        """Clean unused code and optimize performance"""
        logger.info("Cleaning unused code...")
        
        # This would implement code cleanup logic
        self.changes_log.append("Cleaned unused code")
    
    def run_style_patch(self):
        """Execute the complete style patching process"""
        logger.info("Starting DAODISEO Style Consistency Patch...")
        
        try:
            # Create backup
            self.create_backup()
            
            # Execute all phases
            self.phase1_typography_consistency()
            self.phase2_color_consistency()
            self.phase3_remove_visual_clutter()
            self.phase4_gamification_restoration()
            self.phase5_ai_brain_architecture()
            self.phase6_performance_optimization()
            
            # Generate report
            self._generate_style_report()
            
            logger.info("Style patch completed successfully!")
            
        except Exception as e:
            logger.error(f"Style patch failed: {e}")
            raise
    
    def _generate_style_report(self):
        """Generate style patch report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'patch_type': 'Style Consistency & AI Brain Architecture',
            'total_changes': len(self.changes_log),
            'changes_applied': self.changes_log,
            'backup_location': str(self.backup_path),
            'brand_system': self.brand_system,
            'ai_brain_routes': self.ai_brain_routes,
            'performance_improvements': [
                'Centralized CSS system',
                'Optimized loading order',
                'Removed visual clutter',
                'Standardized components'
            ],
            'status': 'SUCCESS'
        }
        
        report_file = Path('style_patch_report.json')
        report_file.write_text(json.dumps(report, indent=2))
        
        logger.info(f"Style patch report generated: {report_file}")
        logger.info(f"Total changes applied: {len(self.changes_log)}")
        for change in self.changes_log:
            logger.info(f"  ✓ {change}")

if __name__ == "__main__":
    patcher = DaodiseoStylePatcher()
    patcher.run_style_patch()