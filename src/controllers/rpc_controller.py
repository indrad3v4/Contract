"""
RPC Controller for Direct Testnet Access
Exposes direct RPC endpoints from testnet-rpc.daodiseo.chaintools.tech
"""

import logging
from flask import Blueprint, jsonify, request
from src.services.rpc_service import DaodiseoRPCService
from src.security_utils import secure_endpoint

logger = logging.getLogger(__name__)

# Create blueprint
rpc_bp = Blueprint('rpc', __name__, url_prefix='/api/rpc')

# Initialize RPC service
rpc_service = DaodiseoRPCService()

@rpc_bp.route('/network-status', methods=['GET'])
@secure_endpoint
def get_network_status():
    """Get current network status and health from RPC"""
    try:
        result = rpc_service.get_network_status()
        return jsonify(result)
    except Exception as e:
        logger.error(f"RPC network status error: {e}")
        return jsonify({
            "success": False,
            "error": "Failed to fetch network status from RPC",
            "details": str(e)
        }), 500

@rpc_bp.route('/validators', methods=['GET'])
@secure_endpoint
def get_validators():
    """Get current validators from RPC"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 100, type=int)
        
        result = rpc_service.get_validators(page=page, per_page=per_page)
        return jsonify(result)
    except Exception as e:
        logger.error(f"RPC validators error: {e}")
        return jsonify({
            "success": False,
            "error": "Failed to fetch validators from RPC",
            "details": str(e)
        }), 500

@rpc_bp.route('/latest-block', methods=['GET'])
@secure_endpoint
def get_latest_block():
    """Get latest block information from RPC"""
    try:
        result = rpc_service.get_latest_block()
        return jsonify(result)
    except Exception as e:
        logger.error(f"RPC latest block error: {e}")
        return jsonify({
            "success": False,
            "error": "Failed to fetch latest block from RPC",
            "details": str(e)
        }), 500

@rpc_bp.route('/transactions', methods=['GET'])
@secure_endpoint
def search_transactions():
    """Search transactions from RPC"""
    try:
        query = request.args.get('query', 'tx.height>0')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 30, type=int)
        
        result = rpc_service.search_transactions(query=query, page=page, per_page=per_page)
        return jsonify(result)
    except Exception as e:
        logger.error(f"RPC transactions error: {e}")
        return jsonify({
            "success": False,
            "error": "Failed to fetch transactions from RPC",
            "details": str(e)
        }), 500

@rpc_bp.route('/network-info', methods=['GET'])
@secure_endpoint
def get_network_info():
    """Get network peer information from RPC"""
    try:
        result = rpc_service.get_network_info()
        return jsonify(result)
    except Exception as e:
        logger.error(f"RPC network info error: {e}")
        return jsonify({
            "success": False,
            "error": "Failed to fetch network info from RPC",
            "details": str(e)
        }), 500

@rpc_bp.route('/consensus-state', methods=['GET'])
@secure_endpoint
def get_consensus_state():
    """Get consensus state from RPC"""
    try:
        result = rpc_service.get_consensus_state()
        return jsonify(result)
    except Exception as e:
        logger.error(f"RPC consensus state error: {e}")
        return jsonify({
            "success": False,
            "error": "Failed to fetch consensus state from RPC",
            "details": str(e)
        }), 500

def register_rpc_routes(app):
    """Register RPC routes with the Flask app"""
    app.register_blueprint(rpc_bp)
    logger.info("RPC routes registered successfully")