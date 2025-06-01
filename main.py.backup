"""
Main entry point for deployment - imports the app from Contract directory
"""

import sys
import os

# Add the Contract directory to the Python path
contract_path = os.path.join(os.path.dirname(__file__), 'Contract')
sys.path.insert(0, contract_path)

# Import the Flask app from the Contract directory
# Use importlib to avoid circular import issues
import importlib.util
spec = importlib.util.spec_from_file_location("contract_main", os.path.join(contract_path, "main.py"))
contract_main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contract_main)

# Get the Flask app instance
app = contract_main.app

# This is what gunicorn will look for
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)