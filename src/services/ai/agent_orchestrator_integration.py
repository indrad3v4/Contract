"""
Orchestrator Integration for Data Source Agents
Updates the orchestrator to work with data source agents
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

def integrate_agents_with_orchestrator():
    """Integrate data source agents with the orchestrator"""
    
    try:
        # Import orchestrator and agent controller
        from src.services.ai.orchestrator import get_orchestrator
        from src.services.ai.agents.controller import get_agent_controller
        
        orchestrator = get_orchestrator()
        agent_controller = get_agent_controller()
        
        # Register agent controller with orchestrator
        agent_controller.register_orchestrator(orchestrator)
        
        # Add agent communication methods to orchestrator
        orchestrator.agent_controller = agent_controller
        orchestrator.receive_agent_insights = _receive_agent_insights
        orchestrator.query_agents = _query_agents
        
        logger.info("Successfully integrated agents with orchestrator")
        return True
        
    except Exception as e:
        logger.error(f"Failed to integrate agents with orchestrator: {e}")
        return False

def _receive_agent_insights(self, agent_id: str, insights: List[Dict[str, Any]]):
    """Receive insights from agents"""
    logger.info(f"Received {len(insights)} insights from agent {agent_id}")
    
    # Process insights for orchestrator decision making
    for insight in insights:
        self._process_agent_insight(insight)

def _query_agents(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """Query all relevant agents"""
    return self.agent_controller.process_query(query, context)

def _process_agent_insight(self, insight: Dict[str, Any]):
    """Process individual agent insight"""
    # Add insight to orchestrator's knowledge base
    insight_type = insight.get('insight_type')
    confidence = insight.get('confidence', 0.0)
    
    if confidence > 0.8:
        # High confidence insights influence future decisions
        logger.info(f"High confidence insight: {insight_type}")

# Initialize integration when module is imported
integrate_agents_with_orchestrator()
