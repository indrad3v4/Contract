#!/usr/bin/env python3
"""
Brand & UX Enhancement Script for DAODISEO
Fixes branding, logo, typography, and component visibility issues
"""

import os
import re
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DAODISEOBrandFixer:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.ui_path = self.base_path / "src" / "external_interfaces" / "ui"
        self.templates_path = self.ui_path / "templates"
        self.static_path = self.ui_path / "static"
        
        # Brand colors from existing app
        self.brand_colors = {
            "primary_pink": "#e00d79",
            "secondary_purple": "#8b5cf6",
            "accent_blue": "#6366f1",
            "gradient": "linear-gradient(135deg, #e00d79, #8b5cf6, #6366f1)"
        }
        
    def update_logo_and_branding(self) -> bool:
        """Update logo and branding elements"""
        try:
            base_template = self.templates_path / "base.html"
            content = base_template.read_text()
            
            # Update logo source to new DAODISEO logo
            content = re.sub(
                r'<img src="\{\{ url_for\(\'static\', filename=\'img/cosmic-logo\.svg\'\) \}\}" alt=".*?">',
                '<img src="{{ url_for(\'static\', filename=\'img/daodiseo-logo.svg\') }}" alt="DAODISEO" class="brand-logo">',
                content
            )
            
            # Update app title to DAODISEO.APP in caps with brand styling
            content = re.sub(
                r'<div class="app-title">.*?</div>',
                '<div class="app-title brand-title">DAODISEO.APP</div>',
                content
            )
            
            base_template.write_text(content)
            logger.info("✓ Updated logo and brand title")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update logo and branding: {e}")
            return False
    
    def fix_component_visibility_issues(self) -> bool:
        """Fix color dots and component visibility issues"""
        try:
            # Update main CSS file
            custom_css_path = self.static_path / "css" / "brand-fixes.css"
            
            css_content = f'''/* DAODISEO Brand & UX Fixes */

/* Brand Logo Styling */
.brand-logo {{
    width: 40px;
    height: 40px;
    filter: drop-shadow(0 2px 8px rgba(224, 13, 121, 0.3));
}}

/* Brand Title Styling */
.brand-title {{
    font-weight: 800;
    font-size: 1.2rem;
    letter-spacing: 0.5px;
    background: {self.brand_colors["gradient"]};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-transform: uppercase;
    text-shadow: 0 2px 4px rgba(224, 13, 121, 0.2);
}}

/* Fix Component Color Dots Visibility */
.card .position-absolute,
.card .status-indicator,
.card .color-dot {{
    z-index: 10 !important;
    position: relative !important;
    top: auto !important;
    right: auto !important;
    margin-left: auto;
    margin-bottom: 8px;
}}

/* Dashboard Components Enhanced Visibility */
.dashboard-stats .card,
.widget-card,
.stat-card {{
    position: relative;
    overflow: visible;
    border: 1px solid rgba(224, 13, 121, 0.2);
    background: linear-gradient(135deg, rgba(224, 13, 121, 0.05), rgba(139, 92, 246, 0.05));
}}

.dashboard-stats .card::before {{
    content: '';
    position: absolute;
    top: 12px;
    right: 12px;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: {self.brand_colors["gradient"]};
    z-index: 15;
    box-shadow: 0 2px 6px rgba(224, 13, 121, 0.4);
}}

/* Component Headers with Brand Colors */
.card-header,
.widget-header {{
    background: linear-gradient(90deg, rgba(224, 13, 121, 0.1), rgba(139, 92, 246, 0.1)) !important;
    border-bottom: 2px solid rgba(224, 13, 121, 0.3) !important;
    color: #fff !important;
}}

/* Status Indicators */
.status-indicator {{
    background: {self.brand_colors["primary_pink"]} !important;
    box-shadow: 0 0 12px rgba(224, 13, 121, 0.6);
    animation: brandPulse 2s ease-in-out infinite;
}}

@keyframes brandPulse {{
    0%, 100% {{ opacity: 1; transform: scale(1); }}
    50% {{ opacity: 0.8; transform: scale(1.1); }}
}}

/* Enhanced Sidebar Styling */
.sidebar {{
    background: linear-gradient(180deg, rgba(33, 37, 41, 0.95), rgba(52, 58, 64, 0.95));
    border-right: 2px solid rgba(224, 13, 121, 0.3);
}}

.sidebar-header {{
    background: linear-gradient(135deg, rgba(224, 13, 121, 0.1), rgba(139, 92, 246, 0.1));
    border-bottom: 2px solid rgba(224, 13, 121, 0.3);
    padding: 20px;
}}

/* Navigation Links */
.nav-link.active,
.nav-link:hover {{
    background: linear-gradient(90deg, rgba(224, 13, 121, 0.2), rgba(139, 92, 246, 0.1)) !important;
    border-left: 4px solid {self.brand_colors["primary_pink"]} !important;
    color: #fff !important;
}}

/* Network Status */
.network-status .status-indicator.active {{
    background: {self.brand_colors["primary_pink"]};
    box-shadow: 0 0 8px rgba(224, 13, 121, 0.8);
}}

/* Fix Token Widget Color Dots */
.odis-trading-widget::before {{
    content: '';
    position: absolute;
    top: 16px;
    right: 16px;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: {self.brand_colors["gradient"]};
    z-index: 20;
    box-shadow: 0 2px 8px rgba(224, 13, 121, 0.5);
}}

/* Chart and Stats Containers */
.chart-container,
.stats-container {{
    border: 1px solid rgba(224, 13, 121, 0.2);
    border-radius: 8px;
    background: linear-gradient(135deg, rgba(224, 13, 121, 0.03), rgba(139, 92, 246, 0.03));
    position: relative;
}}

.chart-container::after,
.stats-container::after {{
    content: '';
    position: absolute;
    top: 8px;
    right: 8px;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: {self.brand_colors["primary_pink"]};
    z-index: 10;
}}

/* Button Styling */
.btn-primary {{
    background: {self.brand_colors["gradient"]} !important;
    border: none !important;
    color: white !important;
    font-weight: 600;
}}

.btn-primary:hover {{
    background: linear-gradient(135deg, #c00b6a, #7c3aed, #5b21b6) !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(224, 13, 121, 0.4);
}}

/* Enhanced Cards */
.card {{
    background: rgba(33, 37, 41, 0.8) !important;
    border: 1px solid rgba(224, 13, 121, 0.2) !important;
    backdrop-filter: blur(10px);
}}

/* Typography Enhancements */
h1, h2, h3, h4, h5, h6 {{
    color: #fff;
    font-weight: 600;
}}

.text-muted {{
    color: rgba(255, 255, 255, 0.7) !important;
}}

/* Top Bar Enhancements */
.top-bar {{
    background: linear-gradient(90deg, rgba(224, 13, 121, 0.1), rgba(139, 92, 246, 0.05));
    border-bottom: 2px solid rgba(224, 13, 121, 0.3);
}}

/* Points System Styling */
.points-system {{
    background: linear-gradient(135deg, rgba(255, 193, 7, 0.2), rgba(224, 13, 121, 0.1));
    border: 2px solid rgba(224, 13, 121, 0.4);
}}

/* Wallet Connection Styling */
.wallet-connection .btn {{
    background: {self.brand_colors["gradient"]};
    border: none;
    color: white;
    font-weight: 600;
}}

/* Modal Enhancements */
.modal-content {{
    background: linear-gradient(135deg, rgba(33, 37, 41, 0.95), rgba(52, 58, 64, 0.95)) !important;
    border: 2px solid rgba(224, 13, 121, 0.3) !important;
    backdrop-filter: blur(15px);
}}

/* Responsive Fixes */
@media (max-width: 768px) {{
    .brand-title {{
        font-size: 1rem;
    }}
    
    .brand-logo {{
        width: 32px;
        height: 32px;
    }}
}}

/* Animation for Color Dots */
@keyframes colorDotPulse {{
    0%, 100% {{ 
        opacity: 1; 
        transform: scale(1);
        box-shadow: 0 2px 8px rgba(224, 13, 121, 0.5);
    }}
    50% {{ 
        opacity: 0.8; 
        transform: scale(1.2);
        box-shadow: 0 4px 12px rgba(224, 13, 121, 0.8);
    }}
}}

.card::before,
.chart-container::after,
.stats-container::after {{
    animation: colorDotPulse 3s ease-in-out infinite;
}}'''
            
            custom_css_path.write_text(css_content)
            
            # Update base template to include brand fixes CSS
            base_template = self.templates_path / "base.html"
            content = base_template.read_text()
            
            if 'brand-fixes.css' not in content:
                css_insertion = '    <link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/brand-fixes.css\') }}">'
                content = content.replace(
                    '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/daodiseo-ux.css\') }}">',
                    f'<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/daodiseo-ux.css\') }}">\n{css_insertion}'
                )
                base_template.write_text(content)
            
            logger.info("✓ Fixed component visibility and color issues")
            return True
            
        except Exception as e:
            logger.error(f"Failed to fix component visibility: {e}")
            return False
    
    def enhance_dashboard_components(self) -> bool:
        """Enhance dashboard components with proper styling"""
        try:
            dashboard_template = self.templates_path / "dashboard.html"
            if not dashboard_template.exists():
                logger.warning("Dashboard template not found, skipping dashboard enhancements")
                return True
                
            content = dashboard_template.read_text()
            
            # Add proper classes to dashboard components
            content = re.sub(
                r'<div class="card">',
                '<div class="card widget-card">',
                content
            )
            
            # Add status indicators to stat cards
            content = re.sub(
                r'<div class="card-header">',
                '<div class="card-header widget-header">',
                content
            )
            
            dashboard_template.write_text(content)
            logger.info("✓ Enhanced dashboard components")
            return True
            
        except Exception as e:
            logger.error(f"Failed to enhance dashboard components: {e}")
            return False
    
    def fix_css_import_issue(self) -> bool:
        """Fix the CSS import issue in base template"""
        try:
            base_template = self.templates_path / "base.html"
            content = base_template.read_text()
            
            # Fix the malformed CSS link
            content = content.replace(
                '"{%20url_for(\'static\',%20filename=\'css/micro-rewards.css\')%20}"',
                '"{{ url_for(\'static\', filename=\'css/micro-rewards.css\') }}"'
            )
            
            base_template.write_text(content)
            logger.info("✓ Fixed CSS import issue")
            return True
            
        except Exception as e:
            logger.error(f"Failed to fix CSS import: {e}")
            return False
    
    def run_all_fixes(self) -> dict:
        """Execute all brand and UX fixes"""
        logger.info("Starting DAODISEO Brand & UX Fixes...")
        
        results = {
            "logo_branding": self.update_logo_and_branding(),
            "component_visibility": self.fix_component_visibility_issues(),
            "dashboard_enhancement": self.enhance_dashboard_components(),
            "css_import_fix": self.fix_css_import_issue()
        }
        
        success_count = sum(results.values())
        total_count = len(results)
        
        logger.info(f"Brand & UX Fixes completed: {success_count}/{total_count} fixes successful")
        
        if success_count == total_count:
            logger.info("🎉 All brand and UX fixes completed successfully!")
            logger.info("✓ Logo updated to DAODISEO brand")
            logger.info("✓ Title changed to 'DAODISEO.APP' in brand colors and caps")
            logger.info("✓ Component color dots visibility fixed")
            logger.info("✓ Dashboard components enhanced")
            logger.info("✓ CSS import issues resolved")
        else:
            logger.warning("Some fixes failed. Check logs for details.")
            
        return results

def main():
    print("DAODISEO Brand & UX Fixer")
    print("=" * 40)
    
    fixer = DAODISEOBrandFixer()
    results = fixer.run_all_fixes()
    
    print("\nSummary:")
    print("-" * 30)
    for fix, success in results.items():
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"{fix.replace('_', ' ').title()}: {status}")
    
    print(f"\nOverall: {sum(results.values())}/{len(results)} fixes completed")
    
    if all(results.values()):
        print("\n🎉 DAODISEO Brand & UX fixes completed successfully!")
        print("\nChanges applied:")
        print("• Logo updated to provided DAODISEO design")
        print("• Brand title now shows 'DAODISEO.APP' in pink gradient and caps")
        print("• Component color dots are now properly visible")
        print("• Enhanced visual consistency across all components")
        print("• Fixed CSS import issues")

if __name__ == "__main__":
    main()