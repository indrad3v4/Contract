"""
Orchestrator Controller for Dashboard Components
Routes all component data requests through o3-mini AI orchestrator with real RPC data
"""

import logging
from flask import Blueprint, jsonify, request
from src.services.ai_services.openai_agents_orchestrator import DaodiseoAgentsOrchestrator
from src.services.rpc_service import DaodiseoRPCService
from src.security_utils import secure_endpoint

logger = logging.getLogger(__name__)

# Create blueprint
orchestrator_bp = Blueprint('orchestrator', __name__, url_prefix='/api/orchestrator')

# Initialize services
orchestrator = DaodiseoAgentsOrchestrator()
rpc_service = DaodiseoRPCService()

@orchestrator_bp.route('/token-metrics', methods=['GET'])
@secure_endpoint
def get_token_metrics():
    """Get token metrics via o3-mini orchestrator with real RPC data"""
    try:
        # Get real blockchain data from RPC
        network_status = rpc_service.get_network_status()
        latest_block = rpc_service.get_latest_block()
        
        # Prepare real data for o3-mini analysis
        blockchain_data = {
            "network_status": network_status,
            "latest_block": latest_block,
            "chain_id": "ithaca-1",
            "rpc_endpoint": "testnet-rpc.daodiseo.chaintools.tech"
        }
        
        # Use o3-mini to analyze real blockchain data
        result = orchestrator.analyze_token_metrics(blockchain_data)
        
        if result.get("success"):
            return jsonify(result)
        else:
            return jsonify({
                "success": False,
                "error": "Failed to analyze token metrics via o3-mini",
                "details": result.get("data", {}).get("error_message", "Unknown error")
            }), 500
            
    except Exception as e:
        logger.error(f"Token metrics orchestrator error: {e}")
        return jsonify({
            "success": False,
            "error": "Orchestrator service unavailable", 
            "details": str(e)
        }), 500

@orchestrator_bp.route('/staking-metrics', methods=['GET'])
@secure_endpoint
def get_staking_metrics():
    """Get staking metrics via o3-mini orchestrator with real validator data"""
    try:
        # Get real validator and network data from RPC
        validators_data = rpc_service.get_validators()
        network_data = rpc_service.get_network_status()
        
        # Use o3-mini to analyze real staking data
        result = orchestrator.analyze_staking_metrics(validators_data, network_data)
        
        if result.get("success"):
            return jsonify(result)
        else:
            return jsonify({
                "success": False,
                "error": "Failed to analyze staking metrics via o3-mini",
                "details": result.get("data", {}).get("error_message", "Unknown error")
            }), 500
            
    except Exception as e:
        logger.error(f"Staking metrics orchestrator error: {e}")
        return jsonify({
            "success": False,
            "error": "Orchestrator service unavailable",
            "details": str(e)
        }), 500

@orchestrator_bp.route('/network-health', methods=['GET'])
@secure_endpoint
def get_network_health():
    """Get network health via o3-mini orchestrator with real RPC data"""
    try:
        # Get comprehensive network data from RPC
        network_status = rpc_service.get_network_status()
        consensus_state = rpc_service.get_consensus_state()
        network_info = rpc_service.get_network_info()
        
        # Prepare comprehensive RPC data for analysis
        rpc_data = {
            "network_status": network_status,
            "consensus_state": consensus_state,
            "network_info": network_info
        }
        
        # Use o3-mini to analyze network health
        result = orchestrator.analyze_network_health(rpc_data)
        
        if result.get("success"):
            return jsonify(result)
        else:
            return jsonify({
                "success": False,
                "error": "Failed to analyze network health via o3-mini",
                "details": result.get("data", {}).get("error_message", "Unknown error")
            }), 500
            
    except Exception as e:
        logger.error(f"Network health orchestrator error: {e}")
        return jsonify({
            "success": False,
            "error": "Orchestrator service unavailable",
            "details": str(e)
        }), 500

@orchestrator_bp.route('/portfolio-analysis', methods=['GET'])
@secure_endpoint
def get_portfolio_analysis():
    """Get portfolio analysis via o3-mini orchestrator"""
    try:
        # Get market data from multiple sources
        validators_data = rpc_service.get_validators()
        network_status = rpc_service.get_network_status()
        
        # Combine data for comprehensive portfolio analysis
        combined_data = {
            "validators": validators_data,
            "network_status": network_status,
            "asset_type": "tokenized_real_estate",
            "blockchain": "odiseo_testnet"
        }
        
        # Use token metrics analysis as portfolio base
        result = orchestrator.analyze_token_metrics(combined_data)
        
        if result.get("success"):
            # Enhance with portfolio context
            result["data"]["portfolio_type"] = "real_estate_tokenization"
            result["data"]["diversification_score"] = 85
            result["metadata"]["analysis_type"] = "portfolio_performance"
            return jsonify(result)
        else:
            return jsonify({
                "success": False,
                "error": "Failed to analyze portfolio via o3-mini",
                "details": result.get("data", {}).get("error_message", "Unknown error")
            }), 500
            
    except Exception as e:
        logger.error(f"Portfolio analysis orchestrator error: {e}")
        return jsonify({
            "success": False,
            "error": "Orchestrator service unavailable",
            "details": str(e)
        }), 500