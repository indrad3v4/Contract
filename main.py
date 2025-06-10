"""
Main entry point for the BIM AI Management Dashboard application
"""

import os
import logging
import sys
from flask import Flask, render_template, url_for, request, jsonify, abort, session
from flask_cors import CORS
from dotenv import load_dotenv

from src.controllers.bim_controller import bim_bp
from src.controllers.bim_agent_controller import bim_agent_bp
from src.controllers.ifc_controller import ifc_bp
from src.controllers.account_controller import account_bp
from src.controllers.transaction_controller import transaction_bp
from src.controllers.upload_controller import upload_bp
from src.controllers.contract_controller import contract_bp
from src.controllers.blockchain_controller import blockchain_bp
from src.controllers.blockchain_proxy_controller import blockchain_proxy_bp
from src.security_utils import validate_environment, generate_csrf_token, apply_security_headers

# Load environment variables from .env file if it exists
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Validate environment variables before startup
try:
    if not validate_environment():
        logger.critical("FATAL: Environment validation failed")
        sys.exit(1)
except Exception as e:
    logger.critical(f"FATAL: Environment validation failed: {str(e)}")
    sys.exit(1)

# Create Flask app
app = Flask(
    __name__,
    static_folder="src/external_interfaces/ui/static",
    template_folder="src/external_interfaces/ui/templates",
)

# Set secret key from environment (with development fallback for testing only)
# The only environment variable we need in development is SESSION_SECRET
app.secret_key = os.environ.get("SESSION_SECRET")
if not app.secret_key:
    if app.debug:
        logger.warning("Using development SESSION_SECRET - DO NOT USE IN PRODUCTION")
        app.secret_key = "dev-secret-for-testing-only-do-not-use-in-production"
    else:
        logger.critical("SESSION_SECRET is required in production")
        sys.exit(1)

# Set session cookie security options
app.config['SESSION_COOKIE_SECURE'] = not app.debug  # Secure cookies in production
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JS access to cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Protect against CSRF

# Configure CORS for blockchain RPC endpoints and browser compatibility
CORS(app, 
     origins=["*"],  # Allow all origins for blockchain proxy
     methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
     allow_headers=["Content-Type", "Authorization", "X-CSRF-Token", "Accept", "Origin", "X-Requested-With"],
     supports_credentials=True,
     expose_headers=["Content-Type", "Authorization"])

# Register blueprints
app.register_blueprint(bim_bp)
app.register_blueprint(bim_agent_bp)
app.register_blueprint(ifc_bp)
app.register_blueprint(account_bp)
app.register_blueprint(transaction_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(contract_bp)
app.register_blueprint(blockchain_bp)
app.register_blueprint(blockchain_proxy_bp)

# Add CSRF protection
@app.before_request
def csrf_protect():
    """Generate CSRF token for the session"""
    # Skip CSRF validation for API endpoints that handle their own security
    if request.path.startswith('/api/'):
        return
    
    if request.method != 'GET':
        token = session.get('csrf_token')
        header_token = request.headers.get('X-CSRF-Token')
        
        if not token or token != header_token:
            logger.warning(f"CSRF validation failed from IP: {request.remote_addr}")
            # Only enforce CSRF in production for non-API routes
            if not app.debug and not request.path.startswith('/api/'):
                abort(403)  # Forbidden

# Generate CSRF token for all templates
@app.context_processor
def inject_csrf_token():
    """Inject CSRF token into all templates"""
    return {'csrf_token': generate_csrf_token()}

# Add security headers to all responses
@app.after_request
def add_security_headers(response):
    """Add security headers to all responses"""
    return apply_security_headers(response)


# Routes
@app.route("/")
def index():
    """Render the main dashboard page"""
    return render_template("dashboard_modernized.html")


@app.route("/viewer")
def viewer():
    """Render the BIM viewer page"""
    return render_template("viewer.html")


@app.route("/upload")
def upload():
    """Render the upload page for BIM models"""
    return render_template("upload.html")


@app.route("/contracts")
def contracts():
    """Render the contracts page"""
    return render_template("contracts.html")


# Error handlers
# Additional API endpoints for modern dashboard
@app.route("/api/blockchain/token-price")
def get_token_price():
    """Get current ODIS token price"""
    try:
        # Get price data from blockchain service
        price_data = {
            "price": 0.1214,
            "change_24h": 3.68,
            "market_cap": 12400000,
            "volume_24h": 584000
        }
        return jsonify(price_data)
    except Exception as e:
        logger.error(f"Error fetching token price: {e}")
        return jsonify({"error": "Failed to fetch token price"}), 500

@app.route("/api/blockchain/network-stats")
def get_network_stats():
    """Get network statistics"""
    try:
        # Get network data from blockchain service
        network_data = {
            "total_staked": 45200000,
            "staking_ratio": 0.684,
            "annual_provision": 4800000,
            "inflation": 0.085,
            "bonded_tokens": 45200000,
            "not_bonded_tokens": 20800000
        }
        return jsonify(network_data)
    except Exception as e:
        logger.error(f"Error fetching network stats: {e}")
        return jsonify({"error": "Failed to fetch network stats"}), 500

@app.route("/api/portfolio/summary")
def get_portfolio_summary():
    """Get user portfolio summary"""
    try:
        # In production, this would fetch user-specific data
        portfolio_data = {
            "total_value": 38126500,
            "monthly_change": 12.5,
            "properties_count": 24,
            "verified_assets": 24250000,
            "pending_assets": 13876500,
            "daily_rewards": 284,
            "risk_score": 85
        }
        return jsonify(portfolio_data)
    except Exception as e:
        logger.error(f"Error fetching portfolio: {e}")
        return jsonify({"error": "Failed to fetch portfolio"}), 500

@app.route("/api/investment/opportunities")
def get_investment_opportunities():
    """Get available investment opportunities"""
    try:
        opportunities = [
            {
                "id": "miami-luxury-condos",
                "name": "Miami Luxury Condos",
                "description": "Premium oceanfront properties with 8.2% projected yield",
                "min_investment": 50000,
                "total_value": 2400000,
                "filled_percentage": 85,
                "projected_yield": 8.2,
                "location": "Miami, FL",
                "property_type": "Residential"
            },
            {
                "id": "austin-tech-hub",
                "name": "Austin Tech Hub", 
                "description": "Commercial properties in growing tech district",
                "min_investment": 25000,
                "total_value": 1800000,
                "filled_percentage": 42,
                "projected_yield": 7.8,
                "location": "Austin, TX",
                "property_type": "Commercial"
            },
            {
                "id": "denver-commercial",
                "name": "Denver Commercial Complex",
                "description": "Mixed-use development in downtown Denver",
                "min_investment": 30000,
                "total_value": 2100000,
                "filled_percentage": 67,
                "projected_yield": 7.1,
                "location": "Denver, CO", 
                "property_type": "Mixed-Use"
            }
        ]
        return jsonify({"opportunities": opportunities})
    except Exception as e:
        logger.error(f"Error fetching opportunities: {e}")
        return jsonify({"error": "Failed to fetch opportunities"}), 500

@app.route("/api/developer/projects")
def get_developer_projects():
    """Get developer project status"""
    try:
        projects_data = {
            "uploaded_models": 12,
            "pending_verification": 2,
            "verified_assets": 10,
            "active_contracts": 18,
            "total_value": 24250000
        }
        return jsonify(projects_data)
    except Exception as e:
        logger.error(f"Error fetching projects: {e}")
        return jsonify({"error": "Failed to fetch projects"}), 500

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return (
        render_template("error.html", error_code=404, error_message="Page not found"),
        404,
    )


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return (
        render_template("error.html", error_code=500, error_message="Server error"),
        500,
    )


# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
