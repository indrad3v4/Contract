"""
Data Source Agent Controller
Manages all data source agents and orchestrator integration
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from .base_agent import BaseDataSourceAgent
from .ifc_agent import IFCDataSourceAgent
from .blockchain_agent import BlockchainDataSourceAgent
from .api_agent import APIDataSourceAgent

logger = logging.getLogger(__name__)

class DataSourceAgentController:
    """Controller for managing all data source agents"""
    
    def __init__(self):
        self.agents: Dict[str, BaseDataSourceAgent] = {}
        self.orchestrator = None
        self.initialize_agents()
        
    def initialize_agents(self):
        """Initialize all data source agents"""
        try:
            # Create agents
            self.agents["ifc"] = IFCDataSourceAgent()
            self.agents["blockchain"] = BlockchainDataSourceAgent()
            self.agents["api"] = APIDataSourceAgent()
            
            logger.info(f"Initialized {len(self.agents)} data source agents")
            
        except Exception as e:
            logger.error(f"Agent initialization failed: {e}")
            
    def register_orchestrator(self, orchestrator):
        """Register orchestrator with all agents"""
        self.orchestrator = orchestrator
        
        for agent in self.agents.values():
            agent.register_with_orchestrator(orchestrator)
            
        logger.info("Orchestrator registered with all agents")
        
    def process_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process query across relevant agents"""
        results = {}
        
        # Determine which agents should handle the query
        relevant_agents = self._determine_relevant_agents(query)
        
        for agent_id in relevant_agents:
            if agent_id in self.agents:
                try:
                    result = self.agents[agent_id].execute_query(query, context)
                    results[agent_id] = result
                except Exception as e:
                    logger.error(f"Agent {agent_id} failed: {e}")
                    results[agent_id] = {
                        "success": False,
                        "error": str(e)
                    }
                    
        return {
            "success": len(results) > 0,
            "results": results,
            "agents_used": list(results.keys()),
            "timestamp": datetime.now().isoformat()
        }
        
    def _determine_relevant_agents(self, query: str) -> List[str]:
        """Determine which agents should handle the query"""
        relevant = []
        query_lower = query.lower()
        
        # IFC/BIM related
        if any(term in query_lower for term in ["ifc", "bim", "building", "model", "element"]):
            relevant.append("ifc")
            
        # Blockchain related  
        if any(term in query_lower for term in ["blockchain", "token", "validator", "transaction"]):
            relevant.append("blockchain")
            
        # External data related
        if any(term in query_lower for term in ["market", "price", "weather", "cost", "external"]):
            relevant.append("api")
            
        # If no specific match, use all agents for comprehensive analysis
        if not relevant:
            relevant = list(self.agents.keys())
            
        return relevant
        
    def get_all_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents for dashboard"""
        status = {}
        
        for agent_id, agent in self.agents.items():
            status[agent_id] = agent.get_dashboard_data()
            
        return {
            "agents": status,
            "total_agents": len(self.agents),
            "active_agents": sum(1 for agent in self.agents.values() 
                               if agent.status.value != "error"),
            "last_updated": datetime.now().isoformat()
        }
        
    def get_agent_by_id(self, agent_id: str) -> Optional[BaseDataSourceAgent]:
        """Get specific agent by ID"""
        return self.agents.get(agent_id)
        
    def initialize_ifc_gateway(self, ifc_gateway):
        """Initialize IFC agent with gateway"""
        if "ifc" in self.agents:
            self.agents["ifc"].initialize_gateway(ifc_gateway)

# Global controller instance
_controller_instance = None

def get_agent_controller() -> DataSourceAgentController:
    """Get singleton agent controller instance"""
    global _controller_instance
    if _controller_instance is None:
        _controller_instance = DataSourceAgentController()
    return _controller_instance
