"""
Main entry point for deployment - imports the app from Contract directory
"""

import sys
import os

# Add the Contract directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Contract'))

# Import the Flask app from the Contract/main.py
from main import app

# This is what gunicorn will look for
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)