
#!/usr/bin/env python3
"""
UI Validation Script - Verify that all UI fixes have been applied correctly
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

class UIValidator:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.ui_path = self.base_path / "src" / "external_interfaces" / "ui"
        
    def validate_all(self) -> bool:
        """Run comprehensive UI validation"""
        print("🔍 Running DAODISEO UI Validation...")
        print("=" * 50)
        
        validations = [
            ("CSS Structure", self.validate_css_structure),
            ("HTML Templates", self.validate_html_templates),
            ("JavaScript Integration", self.validate_js_integration),
            ("Responsive Design", self.validate_responsive_design),
            ("Component Structure", self.validate_component_structure)
        ]
        
        results = []
        for name, validation_func in validations:
            print(f"\n📋 Validating {name}...")
            result = validation_func()
            results.append(result)
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {status}")
        
        overall_success = all(results)
        print("\n" + "=" * 50)
        print(f"🎯 Overall Status: {'✅ ALL VALIDATIONS PASSED' if overall_success else '❌ SOME VALIDATIONS FAILED'}")
        
        return overall_success
    
    def validate_css_structure(self) -> bool:
        """Validate CSS structure and classes"""
        css_files = [
            "static/css/main.css",
            "static/css/daodiseo-ux.css", 
            "static/css/liquid-glass-system.css"
        ]
        
        required_classes = [
            "route-glass-container",
            "component-glass-panel", 
            "subcomponent-glass-element",
            "stats-grid",
            "stat-item",
            "insight-item"
        ]
        
        for css_file in css_files:
            file_path = self.ui_path / css_file
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for class_name in required_classes:
                    if f".{class_name}" not in content:
                        print(f"   ⚠️  Missing class: {class_name} in {css_file}")
                        return False
        
        return True
    
    def validate_html_templates(self) -> bool:
        """Validate HTML template structure"""
        dashboard_path = self.ui_path / "templates/dashboard.html"
        
        if not dashboard_path.exists():
            return False
        
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_elements = [
            "route-glass-container",
            "ai-brain-central-hub",
            "component-glass-panel",
            "odis-trading-widget"
        ]
        
        for element in required_elements:
            if element not in content:
                print(f"   ⚠️  Missing element: {element}")
                return False
        
        return True
    
    def validate_js_integration(self) -> bool:
        """Validate JavaScript integration"""
        js_path = self.ui_path / "static/js/dashboard.js"
        
        if not js_path.exists():
            return False
        
        with open(js_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_functions = [
            "initDashboardStateListeners",
            "updateWalletUI",
            "fetchPortfolioData",
            "initDashboardCharts"
        ]
        
        for func in required_functions:
            if f"function {func}" not in content:
                print(f"   ⚠️  Missing function: {func}")
                return False
        
        return True
    
    def validate_responsive_design(self) -> bool:
        """Validate responsive design breakpoints"""
        css_files = [
            "static/css/main.css",
            "static/css/daodiseo-ux.css"
        ]
        
        required_breakpoints = [
            "@media (max-width: 1200px)",
            "@media (max-width: 768px)",
            "@media (max-width: 576px)"
        ]
        
        found_breakpoints = set()
        
        for css_file in css_files:
            file_path = self.ui_path / css_file
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for breakpoint in required_breakpoints:
                    if breakpoint in content:
                        found_breakpoints.add(breakpoint)
        
        return len(found_breakpoints) >= 2  # At least 2 breakpoints
    
    def validate_component_structure(self) -> bool:
        """Validate component structure"""
        odis_component = self.ui_path / "templates/components/odis_trading.html"
        
        if not odis_component.exists():
            return False
        
        with open(odis_component, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_elements = [
            "card-header",
            "card-body", 
            "price-display",
            "token-stats",
            "price-chart-container"
        ]
        
        for element in required_elements:
            if element not in content:
                print(f"   ⚠️  Missing component element: {element}")
                return False
        
        return True

if __name__ == "__main__":
    validator = UIValidator()
    success = validator.validate_all()
    
    if success:
        print("\n🎉 All UI validations passed! The dashboard should now display correctly.")
    else:
        print("\n⚠️  Some validations failed. Run the patch script again:")
        print("   python scripts/ui_consistency_patch.py")
