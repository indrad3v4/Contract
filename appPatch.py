#!/usr/bin/env python3
"""
DAODISEO App Patcher v2.0 - UI/UX Fix
====================================

This patch addresses the critical UI/UX issues seen in the screenshots:
1. Remove all visual dots and inconsistent badges
2. Fix header alignment and gamification placement
3. Enforce DDS brand colors throughout
4. Clean up spacing and typography
5. Make the interface actually look professional

Author: UI/UX Developer
Date: June 2025
"""

import os
import re
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('uiux_patch_report.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class UIUXPatcher:
    """Professional UI/UX patcher for DAODISEO"""
    
    def __init__(self):
        self.base_dir = Path(".")
        self.templates_dir = self.base_dir / "src" / "external_interfaces" / "ui" / "templates"
        self.static_dir = self.base_dir / "src" / "external_interfaces" / "ui" / "static"
        self.css_dir = self.static_dir / "css"
        self.js_dir = self.static_dir / "js"
        
        # Ensure directories exist
        self.css_dir.mkdir(parents=True, exist_ok=True)
        self.js_dir.mkdir(parents=True, exist_ok=True)
        
        self.fixes_applied = []
        
    def run_patch(self):
        """Execute the complete UI/UX patch"""
        print("🎨 DAODISEO UI/UX Patcher v2.0")
        print("=" * 50)
        logger.info("🎨 Starting UI/UX patch process")
        
        try:
            # 1. Create clean DDS stylesheet
            self.create_clean_dds_stylesheet()
            
            # 2. Fix header and gamification
            self.fix_header_gamification()
            
            # 3. Remove visual dots and clean badges
            self.remove_visual_dots()
            
            # 4. Fix spacing and typography
            self.fix_spacing_typography()
            
            # 5. Update base template
            self.update_base_template()
            
            # 6. Generate report
            self.generate_report()
            
            logger.info("✅ UI/UX patch completed successfully!")
            print("\n🎉 UI/UX patch completed successfully!")
            
        except Exception as e:
            logger.error(f"❌ Patch failed: {e}")
            print(f"\n❌ Patch failed: {e}")
            raise
            
    def create_clean_dds_stylesheet(self):
        """Create a clean, professional DDS stylesheet"""
        logger.info("📝 Creating clean DDS stylesheet...")
        
        css_content = """
/* DAODISEO Clean UI/UX Stylesheet v2.0 */
/* Professional, consistent, dot-free design */

:root {
    --dds-primary: #e00d79;
    --dds-primary-dark: #b80596;
    --dds-accent: #00d4ff;
    --dds-bg-dark: #1a1a1a;
    --dds-bg-card: #2a2a2a;
    --dds-text-primary: #ffffff;
    --dds-text-secondary: #cccccc;
    --dds-text-muted: #999999;
    --dds-border: #333333;
    --dds-success: #00ff88;
    --dds-warning: #ffaa00;
    --dds-error: #ff4444;
}

/* Reset and base styles */
* {
    box-sizing: border-box;
}

body {
    font-family: 'Helvetica Neue', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: 16px;
    line-height: 1.5;
    color: var(--dds-text-primary);
    background: linear-gradient(135deg, #1a1a1a 0%, #2d1b69 100%);
    margin: 0;
    padding: 0;
    min-height: 100vh;
}

/* Header styles */
.dds-header {
    background: rgba(26, 26, 26, 0.95);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--dds-border);
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 100;
}

.dds-header-left {
    display: flex;
    align-items: center;
    gap: 2rem;
}

.dds-header-right {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.dds-logo {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--dds-primary);
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Gamification button in header */
.dds-gamification-btn {
    background: linear-gradient(135deg, var(--dds-primary), var(--dds-primary-dark));
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;
}

.dds-gamification-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(224, 13, 121, 0.4);
}

/* Clean cards without dots */
.dds-card {
    background: var(--dds-bg-card);
    border: 1px solid var(--dds-border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}

.dds-card:hover {
    border-color: var(--dds-accent);
    transform: translateY(-2px);
}

.dds-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--dds-border);
}

.dds-card-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--dds-text-primary);
    margin: 0;
}

/* Clean status badges without dots */
.dds-status {
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.875rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.dds-status-active {
    background: rgba(0, 255, 136, 0.2);
    color: var(--dds-success);
    border: 1px solid var(--dds-success);
}

.dds-status-pending {
    background: rgba(255, 170, 0, 0.2);
    color: var(--dds-warning);
    border: 1px solid var(--dds-warning);
}

.dds-status-verified {
    background: rgba(0, 212, 255, 0.2);
    color: var(--dds-accent);
    border: 1px solid var(--dds-accent);
}

/* Buttons */
.dds-btn {
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-weight: 600;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.3s ease;
    cursor: pointer;
    border: none;
    font-size: 0.9rem;
}

.dds-btn-primary {
    background: linear-gradient(135deg, var(--dds-primary), var(--dds-primary-dark));
    color: white;
}

.dds-btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(224, 13, 121, 0.4);
}

.dds-btn-outline {
    background: transparent;
    color: var(--dds-accent);
    border: 2px solid var(--dds-accent);
}

.dds-btn-outline:hover {
    background: var(--dds-accent);
    color: var(--dds-bg-dark);
}

/* Grid layouts */
.dds-grid {
    display: grid;
    gap: 1.5rem;
}

.dds-grid-2 {
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}

.dds-grid-3 {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}

.dds-grid-4 {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
}

/* Sidebar */
.dds-sidebar {
    background: rgba(26, 26, 26, 0.95);
    backdrop-filter: blur(10px);
    border-right: 1px solid var(--dds-border);
    padding: 2rem 1rem;
    height: 100vh;
    position: fixed;
    left: 0;
    top: 0;
    width: 250px;
    z-index: 90;
}

.dds-sidebar-nav {
    list-style: none;
    padding: 0;
    margin: 2rem 0 0 0;
}

.dds-sidebar-nav li {
    margin-bottom: 0.5rem;
}

.dds-sidebar-nav a {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    color: var(--dds-text-secondary);
    text-decoration: none;
    border-radius: 8px;
    transition: all 0.3s ease;
}

.dds-sidebar-nav a:hover,
.dds-sidebar-nav a.active {
    background: rgba(224, 13, 121, 0.1);
    color: var(--dds-primary);
}

/* Main content */
.dds-main {
    margin-left: 250px;
    padding: 2rem;
    min-height: 100vh;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    color: var(--dds-text-primary);
    font-weight: 600;
    line-height: 1.3;
    margin-bottom: 1rem;
}

h1 { font-size: 2.5rem; }
h2 { font-size: 2rem; }
h3 { font-size: 1.75rem; }
h4 { font-size: 1.5rem; }
h5 { font-size: 1.25rem; }
h6 { font-size: 1rem; }

p {
    color: var(--dds-text-secondary);
    margin-bottom: 1rem;
}

/* Utilities */
.dds-mb-1 { margin-bottom: 0.5rem; }
.dds-mb-2 { margin-bottom: 1rem; }
.dds-mb-3 { margin-bottom: 1.5rem; }
.dds-mb-4 { margin-bottom: 2rem; }

.dds-mt-1 { margin-top: 0.5rem; }
.dds-mt-2 { margin-top: 1rem; }
.dds-mt-3 { margin-top: 1.5rem; }
.dds-mt-4 { margin-top: 2rem; }

.dds-text-center { text-align: center; }
.dds-text-right { text-align: right; }

.dds-flex { display: flex; }
.dds-flex-between { justify-content: space-between; }
.dds-flex-center { justify-content: center; }
.dds-flex-align-center { align-items: center; }

/* Remove all visual dots and circles */
.badge::before,
.status-dot,
.dot,
.circle-indicator,
.visual-dot {
    display: none !important;
}

/* Override Bootstrap badges */
.badge {
    background: none !important;
    border: none !important;
    padding: 0.25rem 0.75rem !important;
    border-radius: 20px !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
}

.badge-info {
    background: rgba(0, 212, 255, 0.2) !important;
    color: var(--dds-accent) !important;
    border: 1px solid var(--dds-accent) !important;
}

.badge-success {
    background: rgba(0, 255, 136, 0.2) !important;
    color: var(--dds-success) !important;
    border: 1px solid var(--dds-success) !important;
}

.badge-warning {
    background: rgba(255, 170, 0, 0.2) !important;
    color: var(--dds-warning) !important;
    border: 1px solid var(--dds-warning) !important;
}

/* Modal styles */
.dds-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.dds-modal-content {
    background: var(--dds-bg-card);
    border-radius: 12px;
    padding: 2rem;
    max-width: 500px;
    width: 90%;
    max-height: 80vh;
    overflow-y: auto;
}

.dds-modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--dds-border);
}

.dds-modal-close {
    background: none;
    border: none;
    color: var(--dds-text-secondary);
    font-size: 1.5rem;
    cursor: pointer;
}

/* Responsive design */
@media (max-width: 768px) {
    .dds-sidebar {
        transform: translateX(-100%);
        transition: transform 0.3s ease;
    }
    
    .dds-sidebar.open {
        transform: translateX(0);
    }
    
    .dds-main {
        margin-left: 0;
    }
    
    .dds-header {
        padding: 1rem;
    }
    
    .dds-grid-2,
    .dds-grid-3,
    .dds-grid-4 {
        grid-template-columns: 1fr;
    }
}
"""
        
        css_file = self.css_dir / "dds-clean.css"
        css_file.write_text(css_content, encoding='utf-8')
        logger.info(f"✅ Created clean stylesheet: {css_file}")
        self.fixes_applied.append("Created clean DDS stylesheet")
        
    def fix_header_gamification(self):
        """Fix header and move gamification back to header"""
        logger.info("🎮 Fixing header and gamification placement...")
        
        # Update base template to fix header
        base_template = self.templates_dir / "base.html"
        if base_template.exists():
            content = base_template.read_text(encoding='utf-8')
            
            # Remove old gamification from bottom
            content = re.sub(r'<div[^>]*class="[^"]*gamification[^"]*"[^>]*>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
            
            # Find and replace header section
            header_pattern = r'(<header[^>]*>.*?</header>)'
            new_header = '''<header class="dds-header">
    <div class="dds-header-left">
        <a href="/" class="dds-logo">
            <span>💎</span>
            DAODISEO.APP
        </a>
    </div>
    <div class="dds-header-right">
        <button class="dds-gamification-btn" onclick="openGamificationModal()">
            <span>⭐</span>
            <span id="odis-balance">0 ODIS</span>
        </button>
        <button class="dds-btn dds-btn-outline" onclick="connectKeplr()">
            Connect Keplr
        </button>
    </div>
</header>'''
            
            if re.search(header_pattern, content, flags=re.DOTALL):
                content = re.sub(header_pattern, new_header, content, flags=re.DOTALL)
            else:
                # If no header found, add it after body tag
                content = re.sub(r'(<body[^>]*>)', r'\1\n' + new_header, content)
            
            # Add gamification modal
            modal_html = '''
<!-- Gamification Modal -->
<div id="gamificationModal" class="dds-modal" style="display: none;">
    <div class="dds-modal-content">
        <div class="dds-modal-header">
            <h3>ODIS Rewards</h3>
            <button class="dds-modal-close" onclick="closeGamificationModal()">&times;</button>
        </div>
        <div class="dds-modal-body">
            <div class="dds-card">
                <h4>Earn ODIS Tokens</h4>
                <div class="reward-actions">
                    <div class="reward-item">
                        <span>Upload BIM File</span>
                        <span class="reward-amount">+30 ODIS</span>
                    </div>
                    <div class="reward-item">
                        <span>Sign Contract</span>
                        <span class="reward-amount">+50 ODIS</span>
                    </div>
                    <div class="reward-item">
                        <span>Connect Keplr</span>
                        <span class="reward-amount">+25 ODIS</span>
                    </div>
                    <div class="reward-item">
                        <span>Verify Property</span>
                        <span class="reward-amount">+40 ODIS</span>
                    </div>
                    <div class="reward-item">
                        <span>Complete Transaction</span>
                        <span class="reward-amount">+60 ODIS</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>'''
            
            # Add modal before closing body tag
            content = re.sub(r'(</body>)', modal_html + r'\n\1', content)
            
            base_template.write_text(content, encoding='utf-8')
            logger.info("✅ Fixed header and gamification")
            self.fixes_applied.append("Fixed header and moved gamification")
            
    def remove_visual_dots(self):
        """Remove all visual dots and clean up badges"""
        logger.info("🎯 Removing visual dots and cleaning badges...")
        
        template_files = list(self.templates_dir.rglob("*.html"))
        
        for template_path in template_files:
            try:
                content = template_path.read_text(encoding='utf-8')
                original_content = content
                
                # Remove visual dots and circles
                dot_patterns = [
                    r'<span[^>]*class="[^"]*dot[^"]*"[^>]*>.*?</span>',
                    r'<div[^>]*class="[^"]*circle[^"]*"[^>]*>.*?</div>',
                    r'<i[^>]*class="[^"]*dot[^"]*"[^>]*></i>',
                    r'<span[^>]*class="[^"]*status-dot[^"]*"[^>]*>.*?</span>',
                    r'●', r'•', r'◦', r'○'
                ]
                
                for pattern in dot_patterns:
                    content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
                
                # Clean up badge styles
                badge_replacements = [
                    (r'<span[^>]*class="[^"]*badge[^"]*bg-info[^"]*"[^>]*>([^<]*)</span>', 
                     r'<span class="dds-status dds-status-verified">\1</span>'),
                    (r'<span[^>]*class="[^"]*badge[^"]*bg-success[^"]*"[^>]*>([^<]*)</span>', 
                     r'<span class="dds-status dds-status-active">\1</span>'),
                    (r'<span[^>]*class="[^"]*badge[^"]*bg-warning[^"]*"[^>]*>([^<]*)</span>', 
                     r'<span class="dds-status dds-status-pending">\1</span>'),
                ]
                
                for old_pattern, new_pattern in badge_replacements:
                    content = re.sub(old_pattern, new_pattern, content, flags=re.IGNORECASE)
                
                # Remove inline styles that add dots
                content = re.sub(r'style="[^"]*::before[^"]*"', '', content, flags=re.IGNORECASE)
                content = re.sub(r'style="[^"]*content:\s*["\'][\u2022\u25cf\u25cb]["\'][^"]*"', '', content, flags=re.IGNORECASE)
                
                if content != original_content:
                    template_path.write_text(content, encoding='utf-8')
                    logger.info(f"✅ Cleaned visual dots in: {template_path}")
                    
            except Exception as e:
                logger.error(f"❌ Error cleaning {template_path}: {e}")
                
        self.fixes_applied.append("Removed visual dots and cleaned badges")
        
    def fix_spacing_typography(self):
        """Fix spacing and typography issues"""
        logger.info("📝 Fixing spacing and typography...")
        
        template_files = list(self.templates_dir.rglob("*.html"))
        
        for template_path in template_files:
            try:
                content = template_path.read_text(encoding='utf-8')
                original_content = content
                
                # Fix font references
                content = re.sub(r'font-family:\s*[^;]+;', 'font-family: "Helvetica Neue", sans-serif;', content, flags=re.IGNORECASE)
                
                # Replace inconsistent spacing classes
                spacing_fixes = [
                    (r'class="([^"]*)\s*m-[0-9]+([^"]*)"', r'class="\1 dds-mb-2\2"'),
                    (r'class="([^"]*)\s*p-[0-9]+([^"]*)"', r'class="\1 dds-mb-2\2"'),
                    (r'style="margin:[^"]+"', ''),
                    (r'style="padding:[^"]+"', ''),
                ]
                
                for old_pattern, new_pattern in spacing_fixes:
                    content = re.sub(old_pattern, new_pattern, content, flags=re.IGNORECASE)
                
                if content != original_content:
                    template_path.write_text(content, encoding='utf-8')
                    logger.info(f"✅ Fixed spacing in: {template_path}")
                    
            except Exception as e:
                logger.error(f"❌ Error fixing spacing in {template_path}: {e}")
                
        self.fixes_applied.append("Fixed spacing and typography")
        
    def update_base_template(self):
        """Update base template with clean DDS styling"""
        logger.info("🔧 Updating base template...")
        
        base_template = self.templates_dir / "base.html"
        if base_template.exists():
            content = base_template.read_text(encoding='utf-8')
            
            # Add clean CSS link
            css_link = '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/dds-clean.css\') }}">'
            
            if css_link not in content:
                # Add after other CSS links or in head
                if '<link rel="stylesheet"' in content:
                    content = re.sub(r'(<link rel="stylesheet"[^>]*>)', r'\1\n    ' + css_link, content, count=1)
                elif '<head>' in content:
                    content = re.sub(r'(<head>)', r'\1\n    ' + css_link, content)
                else:
                    content = css_link + '\n' + content
            
            # Add gamification JavaScript
            gamification_js = '''
<script>
function openGamificationModal() {
    document.getElementById('gamificationModal').style.display = 'flex';
}

function closeGamificationModal() {
    document.getElementById('gamificationModal').style.display = 'none';
}

function connectKeplr() {
    // Keplr wallet connection logic
    console.log('Connecting Keplr wallet...');
    // Award 25 ODIS for connecting
    awardODIS(25, 'Connect Keplr');
}

function awardODIS(amount, action) {
    const currentBalance = parseInt(document.getElementById('odis-balance').textContent) || 0;
    const newBalance = currentBalance + amount;
    document.getElementById('odis-balance').textContent = newBalance + ' ODIS';
    
    // Show notification
    console.log(`Awarded ${amount} ODIS for ${action}`);
}

// Close modal when clicking outside
document.addEventListener('click', function(event) {
    const modal = document.getElementById('gamificationModal');
    if (event.target === modal) {
        closeGamificationModal();
    }
});
</script>
'''
            
            # Add JavaScript before closing body tag
            if '</body>' in content and 'openGamificationModal' not in content:
                content = re.sub(r'(</body>)', gamification_js + r'\n\1', content)
            
            base_template.write_text(content, encoding='utf-8')
            logger.info("✅ Updated base template")
            self.fixes_applied.append("Updated base template with clean styling")
            
    def generate_report(self):
        """Generate patch report"""
        logger.info("📊 Generating patch report...")
        
        report = {
            "patch_version": "2.0",
            "timestamp": datetime.now().isoformat(),
            "fixes_applied": self.fixes_applied,
            "summary": {
                "total_fixes": len(self.fixes_applied),
                "focus": "UI/UX cleanup and professional styling",
                "key_improvements": [
                    "Removed all visual dots and circles",
                    "Fixed header alignment and gamification",
                    "Applied clean DDS brand styling",
                    "Improved typography and spacing",
                    "Created professional interface"
                ]
            }
        }
        
        report_file = self.base_dir / "uiux_patch_report.json"
        report_file.write_text(json.dumps(report, indent=2), encoding='utf-8')
        logger.info(f"✅ Generated report: {report_file}")
        

def main():
    """Main execution function"""
    try:
        patcher = UIUXPatcher()
        patcher.run_patch()
        
        print("\n🎯 Next steps:")
        print("1. Refresh your browser to see the changes")
        print("2. Check that all visual dots are removed")
        print("3. Verify gamification button is in header")
        print("4. Test the ODIS reward system")
        print("5. Review the clean, professional styling")
        
    except Exception as e:
        print(f"\n❌ UI/UX patch failed: {e}")
        logger.error(f"UI/UX patch failed: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main())