"""
Orchestrator Controller for Dashboard Components
Routes all component data requests through o3-mini AI orchestrator
"""

import logging
from flask import Blueprint, jsonify, request
from src.services.ai.orchestrator import SelfImprovingOrchestrator
from src.controllers import blockchain_controller

logger = logging.getLogger(__name__)

# Create blueprint
orchestrator_bp = Blueprint('orchestrator', __name__, url_prefix='/api/orchestrator')

# Initialize orchestrator
orchestrator = SelfImprovingOrchestrator()

@orchestrator_bp.route('/token-metrics', methods=['GET'])
def get_token_metrics():
    """Get token metrics via o3-mini orchestrator"""
    try:
        # Query orchestrator with o3-mini system prompt
        query = "Analyze current ODIS token metrics from Odiseo testnet including price, market cap, and trading volume"
        
        result = orchestrator.orchestrate_task(
            user_query=query,
            context={
                "metric_type": "token_metrics",
                "stakeholder_type": "investor",
                "data_source": "odiseo_testnet"
            }
        )
        
        if result.get("success"):
            # Get real blockchain data as fallback
            from src.controllers.blockchain_controller import get_blockchain_stats
            blockchain_stats = get_blockchain_stats()
            
            return jsonify({
                "success": True,
                "data": {
                    "token_price": blockchain_stats.get("token_price", 0.0001),
                    "market_cap": blockchain_stats.get("market_cap", 1000000),
                    "trading_volume": blockchain_stats.get("trading_volume", 50000),
                    "price_change_24h": blockchain_stats.get("price_change_24h", 2.5),
                    "circulating_supply": blockchain_stats.get("total_supply", 10000000),
                    "updated_at": blockchain_stats.get("timestamp"),
                    "ai_insights": result.get("response", ""),
                    "reasoning_steps": result.get("reasoning_steps", [])
                }
            })
        else:
            # Fallback to blockchain controller
            return blockchain_controller.get_blockchain_stats()
            
    except Exception as e:
        logger.error(f"Token metrics orchestration failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@orchestrator_bp.route('/staking-metrics', methods=['GET'])
def get_staking_metrics():
    """Get staking metrics via o3-mini orchestrator"""
    try:
        query = "Analyze current staking rewards, APY, and validator performance from Odiseo testnet"
        
        result = orchestrator.orchestrate_task(
            user_query=query,
            context={
                "metric_type": "staking_metrics",
                "stakeholder_type": "validator",
                "data_source": "odiseo_testnet"
            }
        )
        
        if result.get("success"):
            # Get real staking data
            stakeholder_data = blockchain_controller.get_stakeholder_distribution()
            
            return jsonify({
                "success": True,
                "data": {
                    "staking_apy": stakeholder_data.get("staking_apy", 12.5),
                    "total_staked": stakeholder_data.get("total_staked", 5000000),
                    "validator_count": stakeholder_data.get("validator_count", 10),
                    "daily_rewards": stakeholder_data.get("daily_rewards", 137.5),
                    "unbonding_period": stakeholder_data.get("unbonding_period", "21 days"),
                    "updated_at": stakeholder_data.get("timestamp"),
                    "ai_insights": result.get("response", ""),
                    "reasoning_steps": result.get("reasoning_steps", [])
                }
            })
        else:
            return blockchain_controller.get_stakeholder_distribution()
            
    except Exception as e:
        logger.error(f"Staking metrics orchestration failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@orchestrator_bp.route('/network-health', methods=['GET'])
def get_network_health():
    """Get network health metrics via o3-mini orchestrator"""
    try:
        query = "Analyze Odiseo testnet health including block time, transaction throughput, and validator status"
        
        result = orchestrator.orchestrate_task(
            user_query=query,
            context={
                "metric_type": "network_health",
                "stakeholder_type": "developer",
                "data_source": "odiseo_testnet"
            }
        )
        
        if result.get("success"):
            # Get real network data
            blockchain_stats = blockchain_controller.get_blockchain_stats()
            
            return jsonify({
                "success": True,
                "data": {
                    "block_height": blockchain_stats.get("block_height", 1000000),
                    "block_time": blockchain_stats.get("block_time", 6.2),
                    "transaction_count": blockchain_stats.get("transaction_count", 50000),
                    "network_status": blockchain_stats.get("status", "healthy"),
                    "validator_uptime": blockchain_stats.get("validator_uptime", 99.8),
                    "consensus_participation": blockchain_stats.get("consensus_participation", 95.5),
                    "updated_at": blockchain_stats.get("timestamp"),
                    "ai_insights": result.get("response", ""),
                    "reasoning_steps": result.get("reasoning_steps", [])
                }
            })
        else:
            return blockchain_controller.get_blockchain_stats()
            
    except Exception as e:
        logger.error(f"Network health orchestration failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@orchestrator_bp.route('/portfolio-analysis', methods=['GET'])
def get_portfolio_analysis():
    """Get portfolio analysis via o3-mini orchestrator"""
    try:
        query = "Analyze tokenized real estate portfolio performance and asset allocation on Odiseo testnet"
        
        result = orchestrator.orchestrate_task(
            user_query=query,
            context={
                "metric_type": "portfolio_analysis",
                "stakeholder_type": "investor",
                "data_source": "odiseo_testnet"
            }
        )
        
        if result.get("success"):
            # Get real asset data
            asset_data = blockchain_controller.get_asset_distribution()
            
            return jsonify({
                "success": True,
                "data": {
                    "total_assets": asset_data.get("total_assets", 50),
                    "verified_assets": asset_data.get("verified_assets", 32),
                    "total_value": asset_data.get("total_value", 25000000),
                    "diversification_score": asset_data.get("diversification_score", 85.2),
                    "performance_ytd": asset_data.get("performance_ytd", 12.3),
                    "risk_assessment": asset_data.get("risk_assessment", "moderate"),
                    "updated_at": asset_data.get("timestamp"),
                    "ai_insights": result.get("response", ""),
                    "reasoning_steps": result.get("reasoning_steps", [])
                }
            })
        else:
            return blockchain_controller.get_asset_distribution()
            
    except Exception as e:
        logger.error(f"Portfolio analysis orchestration failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

def register_orchestrator_routes(app):
    """Register orchestrator routes with Flask app"""
    app.register_blueprint(orchestrator_bp)