"""
Data Source Agents Controller for Flask API endpoints
"""

import logging
from flask import Blueprint, jsonify, request
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

# Create Flask Blueprint
agents_bp = Blueprint("agents", __name__, url_prefix="/api/agents")

try:
    from src.services.ai_services.agent_initialization import get_initialized_agent_controller
    agent_controller = get_initialized_agent_controller()
    logger.info("Agent controller initialized successfully")
except ImportError as e:
    logger.warning(f"Agent controller not available: {e}")
    agent_controller = None

@agents_bp.route("/status", methods=["GET"])
def get_agents_status():
    """Get status of all data source agents"""
    try:
        if not agent_controller:
            return jsonify({
                "success": False,
                "error": "Agent controller not available"
            }), 503
            
        status = agent_controller.get_all_agent_status()
        return jsonify({
            "success": True,
            "data": status
        })
        
    except Exception as e:
        logger.error(f"Error getting agent status: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@agents_bp.route("/<agent_id>/status", methods=["GET"])
def get_agent_status(agent_id):
    """Get status of specific agent"""
    try:
        if not agent_controller:
            return jsonify({
                "success": False,
                "error": "Agent controller not available"
            }), 503
            
        agent = agent_controller.get_agent_by_id(agent_id)
        if not agent:
            return jsonify({
                "success": False,
                "error": f"Agent {agent_id} not found"
            }), 404
            
        return jsonify({
            "success": True,
            "data": agent.get_dashboard_data()
        })
        
    except Exception as e:
        logger.error(f"Error getting agent {agent_id} status: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@agents_bp.route("/<agent_id>/action", methods=["POST"])
def execute_agent_action(agent_id):
    """Execute action on specific agent"""
    try:
        if not agent_controller:
            return jsonify({
                "success": False,
                "error": "Agent controller not available"
            }), 503
            
        data = request.get_json()
        action = data.get("action")
        
        if not action:
            return jsonify({
                "success": False,
                "error": "Action parameter required"
            }), 400
            
        agent = agent_controller.get_agent_by_id(agent_id)
        if not agent:
            return jsonify({
                "success": False,
                "error": f"Agent {agent_id} not found"
            }), 404
            
        # Execute agent action based on type
        if action == "analyze":
            result = agent.execute_query("analyze current data")
        elif action == "refresh":
            result = agent.execute_query("refresh status")
        elif action == "sync":
            result = agent.execute_query("sync data")
        elif action == "fetch":
            result = agent.execute_query("fetch latest data")
        else:
            return jsonify({
                "success": False,
                "error": f"Unknown action: {action}"
            }), 400
            
        return jsonify({
            "success": True,
            "data": result
        })
        
    except Exception as e:
        logger.error(f"Error executing action on agent {agent_id}: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@agents_bp.route("/query", methods=["POST"])
def query_agents():
    """Query multiple agents with a user question"""
    try:
        if not agent_controller:
            return jsonify({
                "success": False,
                "error": "Agent controller not available"
            }), 503
            
        data = request.get_json()
        query = data.get("query")
        context = data.get("context", {})
        
        if not query:
            return jsonify({
                "success": False,
                "error": "Query parameter required"
            }), 400
            
        result = agent_controller.process_query(query, context)
        return jsonify({
            "success": True,
            "data": result
        })
        
    except Exception as e:
        logger.error(f"Error processing agent query: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@agents_bp.route("/orchestrator/status", methods=["GET"])
def get_orchestrator_status():
    """Get orchestrator performance analytics"""
    try:
        from src.services.ai_services.orchestrator import get_orchestrator
        orchestrator = get_orchestrator()
        
        analytics = orchestrator.get_performance_analytics()
        return jsonify({
            "success": True,
            "data": analytics
        })
        
    except Exception as e:
        logger.error(f"Error getting orchestrator status: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@agents_bp.route("/orchestrator/task", methods=["POST"])
def orchestrate_task():
    """Execute task through orchestrator"""
    try:
        from src.services.ai_services.orchestrator import get_orchestrator
        orchestrator = get_orchestrator()
        
        data = request.get_json()
        query = data.get("query")
        context = data.get("context", {})
        
        if not query:
            return jsonify({
                "success": False,
                "error": "Query parameter required"
            }), 400
            
        result = orchestrator.orchestrate_task(query, context)
        return jsonify({
            "success": True,
            "data": result
        })
        
    except Exception as e:
        logger.error(f"Error orchestrating task: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500