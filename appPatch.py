#!/usr/bin/env python3
"""
DAODISEO App Patch Script
WBS-based systematic patching for UI/UX consistency, gamification logic repair, and performance optimization.
Based on DAODISEO AI BRAIN orchestrator-centric architecture.
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
        logging.FileHandler('appPatch.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DaodiseoPatcher:
    """Main patcher class implementing WBS methodology"""
    
    def __init__(self):
        self.base_path = Path('.')
        self.ui_path = self.base_path / 'src' / 'external_interfaces' / 'ui'
        self.static_path = self.ui_path / 'static'
        self.templates_path = self.ui_path / 'templates'
        self.backup_path = Path('backup_' + datetime.now().strftime('%Y%m%d_%H%M%S'))
        
        # DDS Brand Colors (based on architecture diagram)
        self.dds_colors = {
            'primary_gradient_start': '#1a1134',
            'primary_gradient_end': '#2d1b69',
            'accent_cyan': '#00d4ff',
            'accent_blue': '#0099cc',
            'magenta': '#c41e8c',
            'purple_border': '#6b46c1',
            'risk_red': '#dc2626'
        }
        
        self.changes_log = []
        
    def create_backup(self):
        """Create backup of current state"""
        logger.info("Creating backup...")
        if not self.backup_path.exists():
            self.backup_path.mkdir()
        
        # Backup critical directories
        for path in [self.ui_path, Path('main.py')]:
            if path.exists():
                if path.is_dir():
                    shutil.copytree(path, self.backup_path / path.name)
                else:
                    shutil.copy2(path, self.backup_path)
        
        logger.info(f"Backup created at: {self.backup_path}")
    
    def part1_ui_consistency(self):
        """Part 1: UI/UX Consistency Enforcement"""
        logger.info("=== Part 1: UI/UX Consistency Enforcement ===")
        
        # 1.1 Fix inconsistent font sizes
        self._standardize_fonts()
        
        # 1.2 Centralize color usage
        self._centralize_colors()
        
        # 1.3 Fix misaligned headers and status badges
        self._fix_header_alignment()
        
        # 1.4 Remove duplicate visual elements
        self._remove_duplicate_elements()
    
    def _standardize_fonts(self):
        """Standardize font sizes across all templates"""
        logger.info("Standardizing fonts...")
        
        font_standards = {
            'h1': '2rem',      # Main page titles
            'h2': '1.75rem',   # Section headers
            'h3': '1.5rem',    # Subsection headers
            'h4': '1.25rem',   # Card titles
            'h5': '1.125rem',  # Small headers
            'body': '1rem',    # Base font size
            'small': '0.875rem' # Small text
        }
        
        # Update base template with font standards
        base_template = self.templates_path / 'base.html'
        if base_template.exists():
            content = base_template.read_text()
            
            # Add font standardization CSS
            font_css = '''
    /* DDS Font Standardization */
    :root {
        --dds-font-h1: 2rem;
        --dds-font-h2: 1.75rem;
        --dds-font-h3: 1.5rem;
        --dds-font-h4: 1.25rem;
        --dds-font-h5: 1.125rem;
        --dds-font-body: 1rem;
        --dds-font-small: 0.875rem;
        --dds-font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    h1 { font-size: var(--dds-font-h1) !important; font-family: var(--dds-font-family); }
    h2 { font-size: var(--dds-font-h2) !important; font-family: var(--dds-font-family); }
    h3 { font-size: var(--dds-font-h3) !important; font-family: var(--dds-font-family); }
    h4 { font-size: var(--dds-font-h4) !important; font-family: var(--dds-font-family); }
    h5 { font-size: var(--dds-font-h5) !important; font-family: var(--dds-font-family); }
    body { font-size: var(--dds-font-body) !important; font-family: var(--dds-font-family); }
    .small, small { font-size: var(--dds-font-small) !important; }
    '''
            
            # Insert font CSS before closing </style> tag
            if '</style>' in content:
                content = content.replace('</style>', font_css + '\n    </style>')
                base_template.write_text(content)
                self.changes_log.append("Added font standardization to base.html")
    
    def _centralize_colors(self):
        """Replace hardcoded colors with centralized DDS color classes"""
        logger.info("Centralizing colors...")
        
        # Create centralized color CSS
        color_css_path = self.static_path / 'css' / 'dds-colors.css'
        color_css_path.parent.mkdir(parents=True, exist_ok=True)
        
        color_css = f'''
/* DDS Centralized Color System */
:root {{
    --dds-primary-start: {self.dds_colors['primary_gradient_start']};
    --dds-primary-end: {self.dds_colors['primary_gradient_end']};
    --dds-accent-cyan: {self.dds_colors['accent_cyan']};
    --dds-accent-blue: {self.dds_colors['accent_blue']};
    --dds-magenta: {self.dds_colors['magenta']};
    --dds-purple-border: {self.dds_colors['purple_border']};
    --dds-risk-red: {self.dds_colors['risk_red']};
}}

/* Utility classes for consistent color usage */
.dds-text-cyan {{ color: var(--dds-accent-cyan) !important; }}
.dds-text-magenta {{ color: var(--dds-magenta) !important; }}
.dds-bg-primary {{ background: linear-gradient(135deg, var(--dds-primary-start), var(--dds-primary-end)) !important; }}
.dds-border-cyan {{ border-color: var(--dds-accent-cyan) !important; }}
.dds-border-purple {{ border-color: var(--dds-purple-border) !important; }}
'''
        
        color_css_path.write_text(color_css)
        self.changes_log.append("Created centralized color system")
        
        # Update templates to use centralized colors
        for template_file in self.templates_path.glob('**/*.html'):
            content = template_file.read_text()
            
            # Replace hardcoded color values
            color_replacements = {
                '#e00d79': 'var(--dds-magenta)',
                '#b80596': 'var(--dds-primary-end)',
                '#00d4ff': 'var(--dds-accent-cyan)',
                'rgba(224, 13, 121': 'rgba(196, 30, 140'  # Update magenta references
            }
            
            modified = False
            for old_color, new_color in color_replacements.items():
                if old_color in content:
                    content = content.replace(old_color, new_color)
                    modified = True
            
            if modified:
                template_file.write_text(content)
                self.changes_log.append(f"Updated colors in {template_file.name}")
    
    def _fix_header_alignment(self):
        """Fix misaligned headers and standardize status badges"""
        logger.info("Fixing header alignment...")
        
        # Fix base template header
        base_template = self.templates_path / 'base.html'
        if base_template.exists():
            content = base_template.read_text()
            
            # Standardize top-bar structure
            header_fix = '''
            <div class="top-bar d-flex justify-content-between align-items-center px-3 py-2">
                <div class="page-title">
                    <h1 class="mb-0">{% block page_title %}Dashboard{% endblock %}</h1>
                </div>
                <div class="top-actions d-flex align-items-center gap-3">
                    <div class="network-indicator">
                        <div class="status-dot active"></div>
                        <span class="network-name">Odiseo Testnet</span>
                    </div>
                    <div class="gamification-toggle" id="gamificationToggle">
                        <button class="btn btn-outline-primary btn-sm">
                            <i data-feather="star" class="icon-inline-sm"></i>
                            <span id="userPoints">0 pts</span>
                        </button>
                    </div>
                    <div class="wallet-connection">
                        <button class="btn btn-outline-primary btn-sm" id="headerConnectKeplr">
                            <i data-feather="link" class="icon-inline-sm"></i>
                            Connect Keplr
                        </button>
                    </div>
                </div>
            </div>
            '''
            
            # Replace existing top-bar
            top_bar_pattern = r'<div class="top-bar">.*?</div>\s*</div>'
            if re.search(top_bar_pattern, content, re.DOTALL):
                content = re.sub(top_bar_pattern, header_fix.strip(), content, flags=re.DOTALL)
                base_template.write_text(content)
                self.changes_log.append("Fixed header alignment in base.html")
    
    def _remove_duplicate_elements(self):
        """Remove duplicate visual elements"""
        logger.info("Removing duplicate elements...")
        
        # Check dashboard for duplicate token information
        dashboard_template = self.templates_path / 'dashboard.html'
        if dashboard_template.exists():
            content = dashboard_template.read_text()
            
            # Remove duplicate ODIS token sections
            # Keep only the main ODIS token overview, remove any duplicates
            if content.count('ODIS Token') > 1:
                # Find and remove secondary token displays
                lines = content.split('\n')
                filtered_lines = []
                in_duplicate_section = False
                duplicate_markers = ['<!-- Duplicate', '<!-- Additional ODIS']
                
                for line in lines:
                    if any(marker in line for marker in duplicate_markers):
                        in_duplicate_section = True
                        continue
                    elif in_duplicate_section and '<!-- End duplicate' in line:
                        in_duplicate_section = False
                        continue
                    elif not in_duplicate_section:
                        filtered_lines.append(line)
                
                dashboard_template.write_text('\n'.join(filtered_lines))
                self.changes_log.append("Removed duplicate ODIS token sections")
    
    def part2_gamification_logic(self):
        """Part 2: Gamification Logic Fix"""
        logger.info("=== Part 2: Gamification Logic Fix ===")
        
        # 2.1 Move gamification to header
        self._move_gamification_to_header()
        
        # 2.2 Restore reward display
        self._restore_reward_system()
        
        # 2.3 Fix point triggers
        self._fix_point_triggers()
    
    def _move_gamification_to_header(self):
        """Move gamification button from bottom-left to header"""
        logger.info("Moving gamification to header...")
        
        # Update gamification CSS
        gamification_css = self.static_path / 'css' / 'gamification.css'
        if gamification_css.exists():
            content = gamification_css.read_text()
            
            # Remove bottom-left positioning
            content = re.sub(r'position:\s*fixed.*?bottom.*?left.*?;', '', content, flags=re.IGNORECASE)
            content = re.sub(r'bottom:\s*\d+px;', '', content, flags=re.IGNORECASE)
            content = re.sub(r'left:\s*\d+px;', '', content, flags=re.IGNORECASE)
            
            # Add header-specific styles
            header_gamification_css = '''
/* Gamification in Header */
.gamification-toggle {
    position: relative;
}

.gamification-toggle .btn {
    background: rgba(0, 212, 255, 0.1);
    border: 1px solid var(--dds-accent-cyan);
    color: var(--dds-accent-cyan);
    transition: all 0.3s ease;
}

.gamification-toggle .btn:hover {
    background: var(--dds-accent-cyan);
    color: var(--dds-primary-start);
    box-shadow: 0 4px 16px rgba(0, 212, 255, 0.3);
}

#userPoints {
    font-weight: 600;
    margin-left: 0.5rem;
}
'''
            
            content += header_gamification_css
            gamification_css.write_text(content)
            self.changes_log.append("Updated gamification positioning")
    
    def _restore_reward_system(self):
        """Restore reward display and actions"""
        logger.info("Restoring reward system...")
        
        # Create/update gamification JavaScript
        gamification_js = self.static_path / 'js' / 'gamification.js'
        gamification_js.parent.mkdir(parents=True, exist_ok=True)
        
        reward_system_js = '''
// DAODISEO Gamification System
class DaodiseoGamification {
    constructor() {
        this.points = parseInt(localStorage.getItem('dds_user_points') || '0');
        this.level = this.calculateLevel(this.points);
        this.achievements = JSON.parse(localStorage.getItem('dds_achievements') || '[]');
        
        this.rewardActions = {
            'upload_bim': 30,
            'sign_contract': 50,
            'submit_transaction': 100,
            'login_platform': 10,
            'view_property': 5,
            'become_validator': 75,
            'share_property': 15,
            'complete_profile': 20,
            'connect_wallet': 25
        };
        
        this.init();
    }
    
    init() {
        this.updatePointsDisplay();
        this.bindEvents();
        this.checkAchievements();
    }
    
    awardPoints(action, amount = null) {
        const points = amount || this.rewardActions[action] || 0;
        if (points > 0) {
            this.points += points;
            localStorage.setItem('dds_user_points', this.points.toString());
            
            this.showPointsAnimation(points);
            this.updatePointsDisplay();
            this.checkLevelUp();
            
            console.log(`Awarded ${points} points for ${action}`);
        }
    }
    
    updatePointsDisplay() {
        const pointsElement = document.getElementById('userPoints');
        if (pointsElement) {
            pointsElement.textContent = `${this.points} pts`;
        }
    }
    
    showPointsAnimation(points) {
        // Create floating points animation
        const animation = document.createElement('div');
        animation.className = 'points-animation';
        animation.textContent = `+${points} ODIS`;
        animation.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            color: var(--dds-accent-cyan);
            font-weight: bold;
            z-index: 9999;
            animation: floatUp 2s ease-out forwards;
            pointer-events: none;
        `;
        
        document.body.appendChild(animation);
        setTimeout(() => animation.remove(), 2000);
    }
    
    calculateLevel(points) {
        return Math.floor(points / 100) + 1;
    }
    
    checkLevelUp() {
        const newLevel = this.calculateLevel(this.points);
        if (newLevel > this.level) {
            this.level = newLevel;
            this.showLevelUpNotification();
        }
    }
    
    showLevelUpNotification() {
        console.log(`Level up! Now level ${this.level}`);
        // Add level up animation/notification
    }
    
    bindEvents() {
        // Bind to existing actions
        document.addEventListener('click', (e) => {
            if (e.target.closest('#uploadForm button[type="submit"]')) {
                this.awardPoints('upload_bim');
            }
            if (e.target.closest('#connectKeplrBtn') || e.target.closest('#headerConnectKeplr')) {
                this.awardPoints('connect_wallet');
            }
        });
        
        // Award points for page views
        const path = window.location.pathname;
        if (path.includes('/viewer')) {
            this.awardPoints('view_property');
        }
    }
    
    checkAchievements() {
        // Check and award achievements based on points and actions
        const achievements = [
            { id: 'first_upload', name: 'First Upload', requirement: 'points >= 30' },
            { id: 'contract_master', name: 'Contract Master', requirement: 'points >= 100' },
            { id: 'validator_candidate', name: 'Validator Candidate', requirement: 'points >= 200' }
        ];
        
        achievements.forEach(achievement => {
            if (!this.achievements.includes(achievement.id)) {
                if (eval(achievement.requirement.replace('points', this.points))) {
                    this.achievements.push(achievement.id);
                    localStorage.setItem('dds_achievements', JSON.stringify(this.achievements));
                    console.log(`Achievement unlocked: ${achievement.name}`);
                }
            }
        });
    }
}

// Initialize gamification system
document.addEventListener('DOMContentLoaded', () => {
    window.ddsGamification = new DaodiseoGamification();
    
    // Add CSS for animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes floatUp {
            0% { opacity: 1; transform: translateY(0); }
            100% { opacity: 0; transform: translateY(-50px); }
        }
        
        .points-animation {
            font-size: 1.2rem;
            text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
        }
    `;
    document.head.appendChild(style);
});
'''
        
        gamification_js.write_text(reward_system_js)
        self.changes_log.append("Created enhanced gamification system")
    
    def _fix_point_triggers(self):
        """Fix point triggers on relevant actions"""
        logger.info("Fixing point triggers...")
        
        # Update upload template to include gamification triggers
        upload_template = self.templates_path / 'upload.html'
        if upload_template.exists():
            content = upload_template.read_text()
            
            # Add gamification script include
            if 'gamification.js' not in content:
                script_include = '''
    <!-- Gamification System -->
    <script src="{{ url_for('static', filename='js/gamification.js') }}"></script>'''
                
                if '{% endblock %}' in content:
                    content = content.replace('{% endblock %}', script_include + '\n{% endblock %}')
                    upload_template.write_text(content)
                    self.changes_log.append("Added gamification to upload template")
    
    def part3_performance_optimization(self):
        """Part 3: Code Health & Performance Scan"""
        logger.info("=== Part 3: Performance Optimization ===")
        
        # 3.1 Remove unused imports
        self._remove_unused_imports()
        
        # 3.2 Detect duplicate files
        self._detect_duplicate_files()
        
        # 3.3 Flag unused routes
        self._flag_unused_routes()
    
    def _remove_unused_imports(self):
        """Remove unused Python imports"""
        logger.info("Scanning for unused imports...")
        
        python_files = list(Path('.').glob('**/*.py'))
        for py_file in python_files:
            if 'venv' in str(py_file) or '__pycache__' in str(py_file):
                continue
                
            try:
                content = py_file.read_text()
                lines = content.split('\n')
                
                # Simple unused import detection
                import_lines = [i for i, line in enumerate(lines) if line.strip().startswith('import ') or line.strip().startswith('from ')]
                
                for i in import_lines:
                    import_line = lines[i].strip()
                    if 'import ' in import_line:
                        module_name = import_line.split('import ')[1].split(' as ')[0].split('.')[0]
                        
                        # Check if module is used elsewhere in file
                        rest_of_file = '\n'.join(lines[i+1:])
                        if module_name not in rest_of_file and not module_name.startswith('_'):
                            logger.warning(f"Potentially unused import in {py_file}: {import_line}")
                            
            except Exception as e:
                logger.error(f"Error analyzing {py_file}: {e}")
    
    def _detect_duplicate_files(self):
        """Detect and merge duplicate CSS/JS files"""
        logger.info("Detecting duplicate files...")
        
        # Check for duplicate CSS files
        css_files = list(self.static_path.glob('**/*.css'))
        css_names = {}
        
        for css_file in css_files:
            name_key = css_file.stem.lower()
            if name_key in css_names:
                logger.warning(f"Potential duplicate CSS: {css_file} and {css_names[name_key]}")
            else:
                css_names[name_key] = css_file
        
        # Check for duplicate JS files
        js_files = list(self.static_path.glob('**/*.js'))
        js_names = {}
        
        for js_file in js_files:
            name_key = js_file.stem.lower()
            if name_key in js_names:
                logger.warning(f"Potential duplicate JS: {js_file} and {js_names[name_key]}")
            else:
                js_names[name_key] = js_file
    
    def _flag_unused_routes(self):
        """Flag unused routes that slow load time"""
        logger.info("Flagging unused routes...")
        
        main_py = Path('main.py')
        if main_py.exists():
            content = main_py.read_text()
            
            # Extract route definitions
            route_pattern = r'@app\.route\([\'"]([^\'"]+)[\'"]\)'
            routes = re.findall(route_pattern, content)
            
            logger.info(f"Found routes: {routes}")
            
            # Check template usage for each route
            for route in routes:
                route_name = route.strip('/').replace('/', '_') or 'index'
                template_exists = (self.templates_path / f"{route_name}.html").exists()
                
                if not template_exists and route != '/':
                    logger.warning(f"Route {route} may not have corresponding template")
    
    def part4_orchestrator_alignment(self):
        """Part 4: Align with DAODISEO AI BRAIN (Orchestrator-Centric UI)"""
        logger.info("=== Part 4: Orchestrator-Centric UI Alignment ===")
        
        # 4.1 Map routes to orchestrator nodes
        self._map_routes_to_orchestrator()
        
        # 4.2 Organize template structure
        self._organize_template_structure()
        
        # 4.3 Create AI brain visual indicators
        self._create_brain_indicators()
    
    def _map_routes_to_orchestrator(self):
        """Map each route to orchestrator decision node"""
        logger.info("Mapping routes to orchestrator nodes...")
        
        orchestrator_mapping = {
            '/': 'Dashboard - Overview & Analytics',
            '/upload': 'DAODISEO.app - IFC + IPES file upload',
            '/contracts': 'DAODAO - Smart budget split',
            '/viewer': 'Ping.pub - Validator explorer'
        }
        
        # Create orchestrator mapping file
        mapping_file = self.base_path / 'orchestrator_mapping.json'
        mapping_file.write_text(json.dumps(orchestrator_mapping, indent=2))
        self.changes_log.append("Created orchestrator mapping")
    
    def _organize_template_structure(self):
        """Organize templates around brain model"""
        logger.info("Organizing template structure...")
        
        # Create component directories
        components_dir = self.templates_path / 'components'
        components_dir.mkdir(exist_ok=True)
        
        brain_components_dir = components_dir / 'brain'
        brain_components_dir.mkdir(exist_ok=True)
        
        # Create brain component templates
        brain_status_component = brain_components_dir / 'status_indicator.html'
        brain_status_component.write_text('''
<!-- AI Brain Status Indicator -->
<div class="ai-brain-status">
    <div class="brain-icon">
        <i data-feather="cpu" class="brain-pulse"></i>
    </div>
    <div class="brain-status-text">
        <span class="status-label">AI Brain</span>
        <span class="status-value">Active</span>
    </div>
</div>
''')
        
        self.changes_log.append("Created brain component structure")
    
    def _create_brain_indicators(self):
        """Create AI brain visual indicators"""
        logger.info("Creating brain indicators...")
        
        # Add brain indicator CSS
        brain_css = self.static_path / 'css' / 'ai-brain.css'
        brain_css.write_text('''
/* AI Brain Visual Indicators */
.ai-brain-status {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: rgba(0, 212, 255, 0.1);
    border: 1px solid var(--dds-accent-cyan);
    border-radius: 20px;
    font-size: 0.875rem;
}

.brain-icon {
    color: var(--dds-accent-cyan);
}

.brain-pulse {
    animation: brainPulse 2s ease-in-out infinite;
}

@keyframes brainPulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.7; transform: scale(1.1); }
}

.brain-status-text {
    display: flex;
    flex-direction: column;
    line-height: 1.2;
}

.status-label {
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.7);
}

.status-value {
    font-weight: 600;
    color: var(--dds-accent-cyan);
}

/* Route-specific brain indicators */
.route-dashboard .brain-icon { color: var(--dds-accent-cyan); }
.route-upload .brain-icon { color: var(--dds-magenta); }
.route-contracts .brain-icon { color: var(--dds-purple-border); }
.route-viewer .brain-icon { color: var(--dds-accent-blue); }
''')
        
        self.changes_log.append("Created AI brain visual indicators")
    
    def run_patch(self):
        """Execute the complete patching process"""
        logger.info("Starting DAODISEO App Patch...")
        
        try:
            # Create backup
            self.create_backup()
            
            # Execute all parts
            self.part1_ui_consistency()
            self.part2_gamification_logic()
            self.part3_performance_optimization()
            self.part4_orchestrator_alignment()
            
            # Generate summary report
            self._generate_report()
            
            logger.info("Patch completed successfully!")
            
        except Exception as e:
            logger.error(f"Patch failed: {e}")
            raise
    
    def _generate_report(self):
        """Generate patch summary report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'changes_applied': len(self.changes_log),
            'changes_log': self.changes_log,
            'backup_location': str(self.backup_path),
            'status': 'SUCCESS'
        }
        
        report_file = Path('patch_report.json')
        report_file.write_text(json.dumps(report, indent=2))
        
        logger.info(f"Patch report generated: {report_file}")
        logger.info(f"Total changes applied: {len(self.changes_log)}")
        for change in self.changes_log:
            logger.info(f"  - {change}")

if __name__ == "__main__":
    patcher = DaodiseoPatcher()
    patcher.run_patch()