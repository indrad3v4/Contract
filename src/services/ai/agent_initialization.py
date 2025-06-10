"""
Agent Initialization Service
Properly initializes all agents with their required dependencies
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)

def initialize_agents_with_dependencies():
    """Initialize all agents with their required dependencies"""
    
    try:
        # Initialize agent controller
        from src.services.ai.agents.controller import get_agent_controller
        agent_controller = get_agent_controller()
        
        # Initialize IFC gateway for IFC agent
        try:
            from src.gateways.ifc.ifc_gateway import IFCGateway
            ifc_gateway = IFCGateway()
            agent_controller.initialize_ifc_gateway(ifc_gateway)
            logger.info("IFC gateway initialized for IFC agent")
        except Exception as e:
            logger.warning(f"Could not initialize IFC gateway: {e}")
        
        # Initialize orchestrator integration
        try:
            from src.services.ai.orchestrator import get_orchestrator
            orchestrator = get_orchestrator()
            agent_controller.register_orchestrator(orchestrator)
            logger.info("Orchestrator registered with agent controller")
        except Exception as e:
            logger.warning(f"Could not register orchestrator: {e}")
        
        return agent_controller
        
    except Exception as e:
        logger.error(f"Agent initialization failed: {e}")
        return None

# Initialize agents when module is imported
_initialized_controller = initialize_agents_with_dependencies()

def get_initialized_agent_controller():
    """Get the initialized agent controller"""
    return _initialized_controller