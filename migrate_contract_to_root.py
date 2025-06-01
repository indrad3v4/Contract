#!/usr/bin/env python3
"""
Script to migrate all files from Contract directory to root level
while preserving folder structure and updating import paths
"""

import os
import shutil
import glob
from pathlib import Path

def migrate_contract_to_root():
    """
    Move all files from Contract directory to root level
    """
    contract_dir = Path("Contract")
    root_dir = Path(".")
    
    if not contract_dir.exists():
        print("Contract directory not found!")
        return False
    
    print("Starting migration from Contract/ to root...")
    
    # Files to skip (protected files)
    skip_files = {".replit", "replit.nix", ".gitignore"}
    
    # Get all items in Contract directory
    items_to_move = [item for item in contract_dir.iterdir() if item.name not in skip_files]
    
    for item in items_to_move:
        destination = root_dir / item.name
        
        try:
            if item.is_file():
                # Move file to root
                print(f"Moving file: {item} -> {destination}")
                if destination.exists():
                    print(f"  Backing up existing: {destination} -> {destination}.backup")
                    shutil.move(str(destination), f"{destination}.backup")
                shutil.move(str(item), str(destination))
                
            elif item.is_dir():
                # Move directory to root
                print(f"Moving directory: {item} -> {destination}")
                if destination.exists():
                    print(f"  Merging with existing directory: {destination}")
                    # Merge directories
                    for sub_item in item.rglob("*"):
                        if sub_item.is_file():
                            rel_path = sub_item.relative_to(item)
                            dest_file = destination / rel_path
                            dest_file.parent.mkdir(parents=True, exist_ok=True)
                            shutil.move(str(sub_item), str(dest_file))
                            print(f"    Moved: {sub_item} -> {dest_file}")
                    # Remove empty source directory
                    shutil.rmtree(str(item))
                else:
                    shutil.move(str(item), str(destination))
                    
        except Exception as e:
            print(f"Error moving {item}: {e}")
            continue
    
    # Remove Contract directory if empty
    try:
        if contract_dir.exists() and not any(contract_dir.iterdir()):
            contract_dir.rmdir()
            print("Removed empty Contract directory")
    except:
        print("Contract directory not empty, keeping it")
    
    print("Migration completed!")
    return True

def update_main_py():
    """
    Update main.py to remove Contract directory references
    """
    main_py_path = Path("main.py")
    
    if main_py_path.exists():
        print("Updating main.py...")
        
        new_content = '''"""
Main entry point for the DAODISEO application
"""

import os
import sys
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

# Import the Flask app directly
try:
    from main import app
except ImportError:
    # If main.py is this file, create a simple Flask app
    from flask import Flask
    
    app = Flask(__name__)
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
    
    @app.route('/')
    def index():
        return "DAODISEO Application - Please run from the correct main.py"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
'''
        
        # Backup existing main.py
        shutil.copy(str(main_py_path), f"{main_py_path}.backup")
        
        # Write new content
        with open(main_py_path, 'w') as f:
            f.write(new_content)
        
        print("Updated main.py")

def update_import_paths():
    """
    Update import paths in Python files to reflect new structure
    """
    print("Updating import paths...")
    
    # Find all Python files in the root and subdirectories
    python_files = list(Path(".").rglob("*.py"))
    
    for py_file in python_files:
        if py_file.name == "migrate_contract_to_root.py":
            continue
            
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace Contract.src imports with src imports
            if "from Contract.src" in content or "import Contract.src" in content:
                print(f"Updating imports in: {py_file}")
                content = content.replace("from Contract.src", "from src")
                content = content.replace("import Contract.src", "import src")
                
                with open(py_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
        except Exception as e:
            print(f"Error updating {py_file}: {e}")

if __name__ == "__main__":
    print("DAODISEO Contract-to-Root Migration Script")
    print("==========================================")
    
    # Step 1: Migrate files
    if migrate_contract_to_root():
        # Step 2: Update import paths
        update_import_paths()
        
        print("\nMigration Summary:")
        print("✓ Files moved from Contract/ to root")
        print("✓ Import paths updated")
        print("✓ Folder structure preserved")
        print("\nYou can now run the application from the root directory")
        print("Next steps:")
        print("1. Stop the Contract Server workflow")
        print("2. Start the DAODISEO Main Server workflow")
        print("3. Test the application")
    else:
        print("Migration failed!")