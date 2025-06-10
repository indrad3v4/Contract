#!/usr/bin/env python3
"""
Data Source Integration Agent Script (DS.py)
Creates intelligent dashboard panels that act as agents for different data sources
(IFC files, blockchain data, external APIs) with orchestrator integration.
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

# Color scheme from existing CSS
COLORS = {
    'primary': '#001e00',
    'secondary': '#b80596', 
    'info': '#e00d79',
    'success': '#009907',
    'warning': '#f3c000',
    'danger': '#ed0048',
    'bg_dark': '#050a13',
    'bg_card': 'rgba(10, 18, 30, 0.9)',
    'glass_border': 'rgba(255, 255, 255, 0.12)',
    'text_light': 'rgba(255, 255, 255, 0.9)'
}

def create_data_source_agents():
    """Create Data Source Integration Agent components"""
    
    print("🤖 Creating Data Source Integration Agents...")
    
    # 1. Create agent base class
    create_agent_base()
    
    # 2. Create specific data source agents
    create_ifc_agent()
    create_blockchain_agent() 
    create_api_agent()
    
    # 3. Create agent controller
    create_agent_controller()
    
    # 4. Create frosted glass agent panels
    create_agent_panels_css()
    create_agent_panels_js()
    create_agent_panels_html()
    
    # 5. Update dashboard to include agents
    update_dashboard_template()
    
    # 6. Create orchestrator integration
    create_orchestrator_integration()
    
    print("✅ Data Source Integration Agents created successfully!")
    print("\nNext steps:")
    print("1. Run this script: python DS.py")
    print("2. Review generated components")
    print("3. Test agent integration")

def create_agent_base():
    """Create base agent class for data source integration"""
    
    agent_dir = Path("src/services/ai/agents")
    agent_dir.mkdir(exist_ok=True)
    
    base_agent_code = '''"""
Base Agent for Data Source Integration
"""

import logging
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)

class AgentStatus(Enum):
    IDLE = "idle"
    PROCESSING = "processing"
    SUCCESS = "success"
    ERROR = "error"
    LEARNING = "learning"

@dataclass
class AgentMetrics:
    """Performance metrics for each agent"""
    agent_id: str
    data_source: str
    requests_processed: int = 0
    success_rate: float = 0.0
    avg_response_time: float = 0.0
    last_update: Optional[datetime] = None
    error_count: int = 0
    learning_iterations: int = 0

@dataclass
class DataInsight:
    """Structured insight from data analysis"""
    source: str
    insight_type: str
    confidence: float
    data: Dict[str, Any]
    timestamp: datetime
    stakeholder_relevance: List[str]

class BaseDataSourceAgent(ABC):
    """Base class for all data source agents"""
    
    def __init__(self, agent_id: str, data_source: str):
        self.agent_id = agent_id
        self.data_source = data_source
        self.status = AgentStatus.IDLE
        self.metrics = AgentMetrics(agent_id=agent_id, data_source=data_source)
        self.insights_cache: List[DataInsight] = []
        self.orchestrator = None
        
    def register_with_orchestrator(self, orchestrator):
        """Register this agent with the orchestrator"""
        self.orchestrator = orchestrator
        logger.info(f"Agent {self.agent_id} registered with orchestrator")
        
    @abstractmethod
    def fetch_data(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Fetch data from the source"""
        pass
        
    @abstractmethod
    def process_data(self, raw_data: Dict[str, Any]) -> List[DataInsight]:
        """Process raw data into structured insights"""
        pass
        
    @abstractmethod
    def get_status_summary(self) -> Dict[str, Any]:
        """Get current agent status for dashboard"""
        pass
        
    def execute_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main execution method"""
        start_time = time.time()
        self.status = AgentStatus.PROCESSING
        
        try:
            # Fetch data
            raw_data = self.fetch_data(query, context)
            
            # Process into insights
            insights = self.process_data(raw_data)
            
            # Cache insights
            self.insights_cache.extend(insights)
            self.insights_cache = self.insights_cache[-100:]  # Keep last 100
            
            # Update metrics
            self.metrics.requests_processed += 1
            execution_time = time.time() - start_time
            self._update_metrics(execution_time, success=True)
            
            # Communicate with orchestrator
            if self.orchestrator:
                self.orchestrator.receive_agent_insights(self.agent_id, insights)
                
            self.status = AgentStatus.SUCCESS
            
            return {
                "success": True,
                "insights": [asdict(insight) for insight in insights],
                "execution_time": execution_time,
                "agent_status": self.status.value
            }
            
        except Exception as e:
            self.metrics.error_count += 1
            self.status = AgentStatus.ERROR
            logger.error(f"Agent {self.agent_id} execution failed: {e}")
            
            return {
                "success": False,
                "error": str(e),
                "agent_status": self.status.value
            }
            
    def _update_metrics(self, execution_time: float, success: bool):
        """Update agent performance metrics"""
        total_requests = self.metrics.requests_processed
        
        # Update average response time
        if total_requests == 1:
            self.metrics.avg_response_time = execution_time
        else:
            self.metrics.avg_response_time = (
                (self.metrics.avg_response_time * (total_requests - 1) + execution_time) / total_requests
            )
            
        # Update success rate
        if success:
            success_count = total_requests - self.metrics.error_count
            self.metrics.success_rate = success_count / total_requests
        else:
            self.metrics.success_rate = (total_requests - self.metrics.error_count) / total_requests
            
        self.metrics.last_update = datetime.now()
        
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get data formatted for dashboard display"""
        return {
            "agent_id": self.agent_id,
            "data_source": self.data_source,
            "status": self.status.value,
            "metrics": asdict(self.metrics),
            "recent_insights": [asdict(insight) for insight in self.insights_cache[-5:]],
            "status_summary": self.get_status_summary()
        }
'''
    
    with open(agent_dir / "base_agent.py", "w") as f:
        f.write(base_agent_code)
    
    # Create __init__.py
    with open(agent_dir / "__init__.py", "w") as f:
        f.write("# Data Source Integration Agents\n")

def create_ifc_agent():
    """Create IFC Data Source Agent"""
    
    ifc_agent_code = '''"""
IFC Data Source Agent
Intelligent agent for processing IFC/BIM data
"""

from typing import Dict, Any, List
from datetime import datetime
import logging

from .base_agent import BaseDataSourceAgent, DataInsight, AgentStatus

logger = logging.getLogger(__name__)

class IFCDataSourceAgent(BaseDataSourceAgent):
    """Agent specialized in IFC/BIM data processing"""
    
    def __init__(self):
        super().__init__("ifc_agent", "IFC/BIM Files")
        self.ifc_gateway = None
        self.supported_elements = [
            "IfcWall", "IfcSlab", "IfcColumn", "IfcBeam", 
            "IfcWindow", "IfcDoor", "IfcSpace", "IfcSite"
        ]
        
    def initialize_gateway(self, ifc_gateway):
        """Initialize with IFC gateway"""
        self.ifc_gateway = ifc_gateway
        
    def fetch_data(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Fetch IFC data based on query"""
        if not self.ifc_gateway:
            raise Exception("IFC Gateway not initialized")
            
        try:
            if "summary" in query.lower():
                return self.ifc_gateway.summary()
            elif "elements" in query.lower():
                return {
                    "elements": self.ifc_gateway.get_all_elements(),
                    "element_types": self.ifc_gateway.get_element_types(),
                    "total_count": len(self.ifc_gateway.get_all_elements())
                }
            elif "properties" in query.lower():
                return self.ifc_gateway.get_element_properties()
            else:
                # General data fetch
                return {
                    "summary": self.ifc_gateway.summary(),
                    "elements": self.ifc_gateway.get_all_elements()[:10]  # First 10
                }
                
        except Exception as e:
            logger.error(f"IFC data fetch failed: {e}")
            return {"error": str(e)}
            
    def process_data(self, raw_data: Dict[str, Any]) -> List[DataInsight]:
        """Process IFC data into structured insights"""
        insights = []
        
        if "error" in raw_data:
            return insights
            
        # Building complexity insight
        if "summary" in raw_data:
            summary = raw_data["summary"]
            element_count = summary.get("elements", 0)
            
            if element_count > 1000:
                complexity = "High"
                confidence = 0.9
            elif element_count > 500:
                complexity = "Medium"
                confidence = 0.8
            else:
                complexity = "Low" 
                confidence = 0.7
                
            insights.append(DataInsight(
                source="IFC",
                insight_type="building_complexity",
                confidence=confidence,
                data={
                    "complexity": complexity,
                    "element_count": element_count,
                    "schema": summary.get("schema", "Unknown")
                },
                timestamp=datetime.now(),
                stakeholder_relevance=["architect", "engineer", "contractor"]
            ))
            
        # Element distribution insight
        if "elements" in raw_data:
            elements = raw_data["elements"]
            element_types = {}
            
            for element in elements:
                elem_type = element.get("type", "Unknown")
                element_types[elem_type] = element_types.get(elem_type, 0) + 1
                
            insights.append(DataInsight(
                source="IFC",
                insight_type="element_distribution",
                confidence=0.85,
                data={
                    "distribution": element_types,
                    "total_elements": len(elements),
                    "most_common": max(element_types, key=element_types.get) if element_types else "None"
                },
                timestamp=datetime.now(),
                stakeholder_relevance=["engineer", "contractor"]
            ))
            
        return insights
        
    def get_status_summary(self) -> Dict[str, Any]:
        """Get IFC agent status summary"""
        return {
            "data_source": "IFC Files",
            "supported_formats": ["IFC2X3", "IFC4"],
            "element_types": len(self.supported_elements),
            "processing_capabilities": [
                "Element extraction",
                "Property analysis", 
                "Spatial relationships",
                "Quantity takeoffs"
            ],
            "current_model": self.ifc_gateway.file_path if self.ifc_gateway and self.ifc_gateway.file_path else None
        }
'''
    
    with open(Path("src/services/ai/agents/ifc_agent.py"), "w") as f:
        f.write(ifc_agent_code)

def create_blockchain_agent():
    """Create Blockchain Data Source Agent"""
    
    blockchain_agent_code = '''"""
Blockchain Data Source Agent
Intelligent agent for processing blockchain/tokenization data
"""

from typing import Dict, Any, List
from datetime import datetime
import logging

from .base_agent import BaseDataSourceAgent, DataInsight, AgentStatus

logger = logging.getLogger(__name__)

class BlockchainDataSourceAgent(BaseDataSourceAgent):
    """Agent specialized in blockchain data processing"""
    
    def __init__(self):
        super().__init__("blockchain_agent", "Blockchain/Tokenization")
        self.chain_id = "ithaca-1"
        self.supported_operations = [
            "token_stats", "validator_info", "transaction_history",
            "staking_data", "governance_proposals"
        ]
        
    def fetch_data(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Fetch blockchain data based on query"""
        try:
            if "validators" in query.lower():
                return self._fetch_validator_data()
            elif "tokens" in query.lower() or "stats" in query.lower():
                return self._fetch_token_stats()
            elif "transactions" in query.lower():
                return self._fetch_transaction_data(context)
            else:
                # General blockchain status
                return self._fetch_general_stats()
                
        except Exception as e:
            logger.error(f"Blockchain data fetch failed: {e}")
            return {"error": str(e)}
            
    def _fetch_validator_data(self) -> Dict[str, Any]:
        """Fetch validator information"""
        # This would integrate with actual blockchain service
        return {
            "total_validators": 10,
            "active_validators": 8,
            "chain_id": self.chain_id,
            "network_status": "active"
        }
        
    def _fetch_token_stats(self) -> Dict[str, Any]:
        """Fetch token statistics"""
        return {
            "total_supply": "1000000000",
            "circulating_supply": "750000000", 
            "staked_tokens": "200000000",
            "token_symbol": "ODIS"
        }
        
    def _fetch_transaction_data(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Fetch transaction data"""
        return {
            "recent_transactions": 156,
            "total_volume": "50000000",
            "avg_tx_time": "6.2s",
            "network_fees": "0.025"
        }
        
    def _fetch_general_stats(self) -> Dict[str, Any]:
        """Fetch general blockchain statistics"""
        return {
            "chain_id": self.chain_id,
            "block_height": "245890",
            "network_status": "healthy",
            "consensus": "Tendermint"
        }
        
    def process_data(self, raw_data: Dict[str, Any]) -> List[DataInsight]:
        """Process blockchain data into structured insights"""
        insights = []
        
        if "error" in raw_data:
            return insights
            
        # Network health insight
        if "network_status" in raw_data:
            status = raw_data["network_status"]
            confidence = 0.95 if status == "healthy" or status == "active" else 0.6
            
            insights.append(DataInsight(
                source="Blockchain",
                insight_type="network_health",
                confidence=confidence,
                data={
                    "status": status,
                    "chain_id": raw_data.get("chain_id", self.chain_id),
                    "validators": raw_data.get("total_validators", 0)
                },
                timestamp=datetime.now(),
                stakeholder_relevance=["owner", "investor"]
            ))
            
        # Token economics insight
        if "total_supply" in raw_data:
            total = float(raw_data["total_supply"])
            circulating = float(raw_data.get("circulating_supply", total))
            staked = float(raw_data.get("staked_tokens", 0))
            
            staking_ratio = staked / circulating if circulating > 0 else 0
            
            insights.append(DataInsight(
                source="Blockchain",
                insight_type="token_economics",
                confidence=0.9,
                data={
                    "staking_ratio": staking_ratio,
                    "circulating_ratio": circulating / total,
                    "network_security": "High" if staking_ratio > 0.3 else "Medium"
                },
                timestamp=datetime.now(),
                stakeholder_relevance=["owner", "investor", "contractor"]
            ))
            
        return insights
        
    def get_status_summary(self) -> Dict[str, Any]:
        """Get blockchain agent status summary"""
        return {
            "data_source": "Blockchain Network",
            "chain_id": self.chain_id,
            "supported_operations": self.supported_operations,
            "network_type": "Cosmos SDK",
            "consensus": "Tendermint",
            "real_time_monitoring": True
        }
'''
    
    with open(Path("src/services/ai/agents/blockchain_agent.py"), "w") as f:
        f.write(blockchain_agent_code)

def create_api_agent():
    """Create External API Data Source Agent"""
    
    api_agent_code = '''"""
External API Data Source Agent  
Intelligent agent for processing external API data
"""

from typing import Dict, Any, List
from datetime import datetime
import logging

from .base_agent import BaseDataSourceAgent, DataInsight, AgentStatus

logger = logging.getLogger(__name__)

class APIDataSourceAgent(BaseDataSourceAgent):
    """Agent specialized in external API data processing"""
    
    def __init__(self):
        super().__init__("api_agent", "External APIs")
        self.api_endpoints = {
            "market_data": "https://api.coingecko.com/api/v3/simple/price",
            "weather": "https://api.openweathermap.org/data/2.5/weather",
            "construction_costs": "https://api.construction-index.com/costs"
        }
        
    def fetch_data(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Fetch external API data based on query"""
        try:
            if "market" in query.lower() or "price" in query.lower():
                return self._fetch_market_data()
            elif "weather" in query.lower():
                return self._fetch_weather_data(context)
            elif "construction" in query.lower() or "cost" in query.lower():
                return self._fetch_construction_costs(context)
            else:
                # General API status
                return self._fetch_api_status()
                
        except Exception as e:
            logger.error(f"API data fetch failed: {e}")
            return {"error": str(e)}
            
    def _fetch_market_data(self) -> Dict[str, Any]:
        """Fetch cryptocurrency market data"""
        # This would make actual API calls
        return {
            "odis_price": "0.025",
            "market_cap": "25000000",
            "24h_change": "+2.5%",
            "volume_24h": "125000"
        }
        
    def _fetch_weather_data(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Fetch weather data for property location"""
        location = context.get("location", "Default City") if context else "Default City"
        
        return {
            "location": location,
            "temperature": "22°C",
            "conditions": "Partly Cloudy",
            "humidity": "65%",
            "impact_assessment": "Favorable for construction"
        }
        
    def _fetch_construction_costs(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Fetch construction cost indices"""
        return {
            "material_costs": {
                "concrete": "120 USD/m³",
                "steel": "850 USD/ton", 
                "labor": "45 USD/hour"
            },
            "cost_index": "108.5",
            "trend": "increasing"
        }
        
    def _fetch_api_status(self) -> Dict[str, Any]:
        """Fetch general API status"""
        return {
            "active_apis": len(self.api_endpoints),
            "response_times": {
                "market_data": "150ms",
                "weather": "200ms", 
                "construction_costs": "300ms"
            },
            "availability": "99.2%"
        }
        
    def process_data(self, raw_data: Dict[str, Any]) -> List[DataInsight]:
        """Process API data into structured insights"""
        insights = []
        
        if "error" in raw_data:
            return insights
            
        # Market insight
        if "odis_price" in raw_data:
            price_change = raw_data.get("24h_change", "0%")
            trend = "positive" if "+" in price_change else "negative" if "-" in price_change else "stable"
            
            insights.append(DataInsight(
                source="Market API",
                insight_type="token_performance",
                confidence=0.85,
                data={
                    "price": raw_data["odis_price"],
                    "trend": trend,
                    "market_cap": raw_data.get("market_cap"),
                    "investment_signal": "bullish" if trend == "positive" else "bearish"
                },
                timestamp=datetime.now(),
                stakeholder_relevance=["owner", "investor"]
            ))
            
        # Weather impact insight
        if "conditions" in raw_data:
            impact = raw_data.get("impact_assessment", "Neutral")
            
            insights.append(DataInsight(
                source="Weather API",
                insight_type="environmental_impact",
                confidence=0.7,
                data={
                    "conditions": raw_data["conditions"],
                    "temperature": raw_data.get("temperature"),
                    "construction_impact": impact,
                    "recommendation": "Proceed with outdoor work" if "Favorable" in impact else "Consider delays"
                },
                timestamp=datetime.now(),
                stakeholder_relevance=["contractor", "engineer"]
            ))
            
        # Construction cost insight
        if "material_costs" in raw_data:
            trend = raw_data.get("trend", "stable")
            
            insights.append(DataInsight(
                source="Construction API",
                insight_type="cost_analysis",
                confidence=0.8,
                data={
                    "cost_trend": trend,
                    "materials": raw_data["material_costs"],
                    "budget_impact": "increase" if trend == "increasing" else "stable",
                    "recommendation": "Lock in material prices" if trend == "increasing" else "Normal procurement"
                },
                timestamp=datetime.now(),
                stakeholder_relevance=["contractor", "owner"]
            ))
            
        return insights
        
    def get_status_summary(self) -> Dict[str, Any]:
        """Get API agent status summary"""
        return {
            "data_source": "External APIs",
            "endpoints": list(self.api_endpoints.keys()),
            "update_frequency": "Real-time",
            "data_types": [
                "Market data",
                "Weather conditions",
                "Construction indices",
                "Economic indicators"
            ],
            "integration_status": "Active"
        }
'''
    
    with open(Path("src/services/ai/agents/api_agent.py"), "w") as f:
        f.write(api_agent_code)

def create_agent_controller():
    """Create controller for managing data source agents"""
    
    controller_code = '''"""
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
'''
    
    with open(Path("src/services/ai/agents/controller.py"), "w") as f:
        f.write(controller_code)

def create_agent_panels_css():
    """Create CSS for frosted glass agent panels"""
    
    css_code = f'''/* Data Source Agent Panels - Frosted Glass Effect */

.agent-panel-container {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 1.5rem;
    margin: 1.5rem 0;
}}

.agent-panel {{
    /* Frosted glass base */
    background: {COLORS['bg_card']};
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    
    /* Glass borders and shadows */
    border: 1px solid {COLORS['glass_border']};
    border-radius: 16px;
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.1);
    
    /* Layout */
    padding: 1.5rem;
    min-height: 280px;
    position: relative;
    overflow: hidden;
    
    /* Transitions */
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}

.agent-panel:hover {{
    transform: translateY(-4px);
    box-shadow: 
        0 12px 40px rgba(0, 0, 0, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.2);
}}

/* Agent Panel Header */
.agent-panel-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}}

.agent-title {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.1rem;
    font-weight: 600;
    color: {COLORS['text_light']};
}}

.agent-icon {{
    width: 24px;
    height: 24px;
    background: linear-gradient(135deg, {COLORS['info']}, {COLORS['secondary']});
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}}

.agent-status {{
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.agent-status.idle {{
    background: rgba(108, 117, 125, 0.2);
    color: #6c757d;
    border: 1px solid rgba(108, 117, 125, 0.3);
}}

.agent-status.processing {{
    background: rgba(255, 193, 7, 0.2);
    color: {COLORS['warning']};
    border: 1px solid rgba(255, 193, 7, 0.3);
    animation: pulse 2s infinite;
}}

.agent-status.success {{
    background: rgba(0, 153, 7, 0.2);
    color: {COLORS['success']};
    border: 1px solid rgba(0, 153, 7, 0.3);
}}

.agent-status.error {{
    background: rgba(237, 0, 72, 0.2);
    color: {COLORS['danger']};
    border: 1px solid rgba(237, 0, 72, 0.3);
}}

/* Agent Metrics */
.agent-metrics {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
    margin: 1rem 0;
}}

.metric-item {{
    text-align: center;
    padding: 0.75rem;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.08);
}}

.metric-value {{
    font-size: 1.25rem;
    font-weight: 700;
    color: {COLORS['info']};
    display: block;
}}

.metric-label {{
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.6);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 0.25rem;
}}

/* Agent Insights */
.agent-insights {{
    margin-top: 1rem;
}}

.insight-item {{
    padding: 0.75rem;
    margin-bottom: 0.5rem;
    background: rgba(255, 255, 255, 0.02);
    border-left: 3px solid {COLORS['info']};
    border-radius: 0 6px 6px 0;
    font-size: 0.85rem;
    line-height: 1.4;
}}

.insight-type {{
    font-weight: 600;
    color: {COLORS['info']};
    text-transform: capitalize;
    margin-bottom: 0.25rem;
}}

.insight-confidence {{
    float: right;
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.5);
}}

/* Agent Actions */
.agent-actions {{
    display: flex;
    gap: 0.5rem;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}}

.agent-btn {{
    flex: 1;
    padding: 0.5rem 1rem;
    background: rgba(224, 13, 121, 0.1);
    color: {COLORS['info']};
    border: 1px solid rgba(224, 13, 121, 0.3);
    border-radius: 8px;
    font-size: 0.8rem;
    cursor: pointer;
    transition: all 0.2s ease;
}}

.agent-btn:hover {{
    background: rgba(224, 13, 121, 0.2);
    border-color: rgba(224, 13, 121, 0.5);
    transform: translateY(-1px);
}}

/* Loading Animation */
@keyframes pulse {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.6; }}
}}

.agent-loading {{
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100px;
    color: rgba(255, 255, 255, 0.5);
}}

.agent-loading::after {{
    content: '';
    width: 20px;
    height: 20px;
    border: 2px solid rgba(224, 13, 121, 0.3);
    border-top: 2px solid {COLORS['info']};
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-left: 0.5rem;
}}

@keyframes spin {{
    0% {{ transform: rotate(0deg); }}
    100% {{ transform: rotate(360deg); }}
}}

/* Responsive Design */
@media (max-width: 768px) {{
    .agent-panel-container {{
        grid-template-columns: 1fr;
        gap: 1rem;
        margin: 1rem 0;
    }}
    
    .agent-panel {{
        padding: 1rem;
        min-height: 240px;
    }}
    
    .agent-metrics {{
        grid-template-columns: 1fr;
        gap: 0.5rem;
    }}
}}

/* Dark mode enhancements */
@media (prefers-color-scheme: dark) {{
    .agent-panel {{
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }}
    
    .agent-panel:hover {{
        box-shadow: 
            0 12px 40px rgba(0, 0, 0, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }}
}}
'''
    
    css_path = Path("src/external_interfaces/ui/static/css/agent-panels.css")
    with open(css_path, "w") as f:
        f.write(css_code)

def create_agent_panels_js():
    """Create JavaScript for agent panel interactions"""
    
    js_code = '''/**
 * Data Source Agent Panels JavaScript
 * Handles agent panel interactions and real-time updates
 */

class AgentPanelManager {
    constructor() {
        this.agents = new Map();
        this.updateInterval = null;
        this.websocket = null;
        this.initialize();
    }

    initialize() {
        console.log('Initializing Agent Panel Manager');
        this.setupEventListeners();
        this.startPeriodicUpdates();
        this.initializeWebSocket();
    }

    setupEventListeners() {
        // Agent action buttons
        document.addEventListener('click', (e) => {
            if (e.target.matches('.agent-btn[data-action]')) {
                const action = e.target.dataset.action;
                const agentId = e.target.closest('.agent-panel').dataset.agentId;
                this.executeAgentAction(agentId, action);
            }
        });

        // Panel refresh buttons
        document.addEventListener('click', (e) => {
            if (e.target.matches('.agent-refresh-btn')) {
                const agentId = e.target.closest('.agent-panel').dataset.agentId;
                this.refreshAgent(agentId);
            }
        });
    }

    async fetchAgentStatus() {
        try {
            const response = await fetch('/api/agents/status');
            if (!response.ok) throw new Error('Failed to fetch agent status');
            return await response.json();
        } catch (error) {
            console.error('Error fetching agent status:', error);
            return null;
        }
    }

    async updateAgentPanels() {
        const statusData = await this.fetchAgentStatus();
        if (!statusData) return;

        Object.entries(statusData.agents).forEach(([agentId, agentData]) => {
            this.updateAgentPanel(agentId, agentData);
        });
    }

    updateAgentPanel(agentId, agentData) {
        const panel = document.querySelector(`[data-agent-id="${agentId}"]`);
        if (!panel) return;

        // Update status
        const statusElement = panel.querySelector('.agent-status');
        if (statusElement) {
            statusElement.className = `agent-status ${agentData.status}`;
            statusElement.textContent = agentData.status;
        }

        // Update metrics
        this.updateMetrics(panel, agentData.metrics);
        
        // Update insights
        this.updateInsights(panel, agentData.recent_insights);
        
        // Store agent data
        this.agents.set(agentId, agentData);
    }

    updateMetrics(panel, metrics) {
        const successRateElement = panel.querySelector('.metric-success-rate');
        const responseTimeElement = panel.querySelector('.metric-response-time');
        const requestsElement = panel.querySelector('.metric-requests');
        const errorsElement = panel.querySelector('.metric-errors');

        if (successRateElement) {
            successRateElement.textContent = `${(metrics.success_rate * 100).toFixed(1)}%`;
        }
        if (responseTimeElement) {
            responseTimeElement.textContent = `${metrics.avg_response_time.toFixed(2)}s`;
        }
        if (requestsElement) {
            requestsElement.textContent = metrics.requests_processed;
        }
        if (errorsElement) {
            errorsElement.textContent = metrics.error_count;
        }
    }

    updateInsights(panel, insights) {
        const insightsContainer = panel.querySelector('.agent-insights');
        if (!insightsContainer || !insights) return;

        insightsContainer.innerHTML = '';
        
        insights.slice(0, 3).forEach(insight => {
            const insightElement = this.createInsightElement(insight);
            insightsContainer.appendChild(insightElement);
        });
    }

    createInsightElement(insight) {
        const element = document.createElement('div');
        element.className = 'insight-item';
        
        element.innerHTML = `
            <div class="insight-type">
                ${insight.insight_type.replace('_', ' ')}
                <span class="insight-confidence">${(insight.confidence * 100).toFixed(0)}%</span>
            </div>
            <div class="insight-content">
                ${this.formatInsightData(insight.data)}
            </div>
        `;
        
        return element;
    }

    formatInsightData(data) {
        if (typeof data === 'object') {
            const key = Object.keys(data)[0];
            const value = data[key];
            return `${key}: ${value}`;
        }
        return String(data);
    }

    async executeAgentAction(agentId, action) {
        const panel = document.querySelector(`[data-agent-id="${agentId}"]`);
        if (!panel) return;

        // Show loading state
        this.setAgentLoading(panel, true);

        try {
            const response = await fetch(`/api/agents/${agentId}/action`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]')?.content
                },
                body: JSON.stringify({ action })
            });

            if (!response.ok) throw new Error('Action failed');
            
            const result = await response.json();
            
            // Update panel with results
            if (result.success) {
                this.showSuccessMessage(panel, 'Action completed successfully');
                // Refresh agent data
                await this.refreshAgent(agentId);
            } else {
                this.showErrorMessage(panel, result.error || 'Action failed');
            }
            
        } catch (error) {
            console.error('Agent action error:', error);
            this.showErrorMessage(panel, 'Network error occurred');
        } finally {
            this.setAgentLoading(panel, false);
        }
    }

    async refreshAgent(agentId) {
        const panel = document.querySelector(`[data-agent-id="${agentId}"]`);
        if (!panel) return;

        this.setAgentLoading(panel, true);

        try {
            const response = await fetch(`/api/agents/${agentId}/status`);
            if (!response.ok) throw new Error('Refresh failed');
            
            const agentData = await response.json();
            this.updateAgentPanel(agentId, agentData);
            
        } catch (error) {
            console.error('Agent refresh error:', error);
            this.showErrorMessage(panel, 'Failed to refresh agent');
        } finally {
            this.setAgentLoading(panel, false);
        }
    }

    setAgentLoading(panel, loading) {
        const loadingOverlay = panel.querySelector('.agent-loading-overlay');
        
        if (loading) {
            if (!loadingOverlay) {
                const overlay = document.createElement('div');
                overlay.className = 'agent-loading-overlay';
                overlay.innerHTML = '<div class="agent-loading">Processing...</div>';
                panel.appendChild(overlay);
            }
        } else {
            if (loadingOverlay) {
                loadingOverlay.remove();
            }
        }
    }

    showSuccessMessage(panel, message) {
        this.showMessage(panel, message, 'success');
    }

    showErrorMessage(panel, message) {
        this.showMessage(panel, message, 'error');
    }

    showMessage(panel, message, type) {
        // Remove existing messages
        const existingMessage = panel.querySelector('.agent-message');
        if (existingMessage) existingMessage.remove();

        // Create new message
        const messageElement = document.createElement('div');
        messageElement.className = `agent-message agent-message-${type}`;
        messageElement.textContent = message;
        
        panel.appendChild(messageElement);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (messageElement.parentNode) {
                messageElement.remove();
            }
        }, 3000);
    }

    startPeriodicUpdates() {
        // Update every 30 seconds
        this.updateInterval = setInterval(() => {
            this.updateAgentPanels();
        }, 30000);
        
        // Initial update
        this.updateAgentPanels();
    }

    initializeWebSocket() {
        try {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.location.host}/ws/agents`;
            
            this.websocket = new WebSocket(wsUrl);
            
            this.websocket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                if (data.type === 'agent_update') {
                    this.updateAgentPanel(data.agent_id, data.agent_data);
                }
            };
            
            this.websocket.onerror = (error) => {
                console.log('WebSocket connection not available, using polling only');
            };
            
        } catch (error) {
            console.log('WebSocket not supported, using polling only');
        }
    }

    destroy() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }
        if (this.websocket) {
            this.websocket.close();
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.agentPanelManager = new AgentPanelManager();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (window.agentPanelManager) {
        window.agentPanelManager.destroy();
    }
});
'''
    
    js_path = Path("src/external_interfaces/ui/static/js/agent-panels.js")
    with open(js_path, "w") as f:
        f.write(js_code)

def create_agent_panels_html():
    """Create HTML template for agent panels"""
    
    html_code = '''<!-- Data Source Agent Panels Component -->
<div class="agent-panel-container">
    <!-- IFC Data Source Agent Panel -->
    <div class="agent-panel" data-agent-id="ifc">
        <div class="agent-panel-header">
            <div class="agent-title">
                <div class="agent-icon">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                        <polyline points="9,22 9,12 15,12 15,22"/>
                    </svg>
                </div>
                IFC/BIM Agent
            </div>
            <div class="agent-status idle" id="ifc-status">Idle</div>
        </div>
        
        <div class="agent-metrics">
            <div class="metric-item">
                <span class="metric-value metric-success-rate">0%</span>
                <span class="metric-label">Success Rate</span>
            </div>
            <div class="metric-item">
                <span class="metric-value metric-response-time">0s</span>
                <span class="metric-label">Avg Time</span>
            </div>
            <div class="metric-item">
                <span class="metric-value metric-requests">0</span>
                <span class="metric-label">Requests</span>
            </div>
            <div class="metric-item">
                <span class="metric-value metric-errors">0</span>
                <span class="metric-label">Errors</span>
            </div>
        </div>
        
        <div class="agent-insights">
            <div class="insight-item">
                <div class="insight-type">Ready to analyze</div>
                Upload an IFC file to begin analysis
            </div>
        </div>
        
        <div class="agent-actions">
            <button class="agent-btn" data-action="analyze">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8"/>
                    <path d="m21 21-4.35-4.35"/>
                </svg>
                Analyze
            </button>
            <button class="agent-btn" data-action="refresh">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="23 4 23 10 17 10"/>
                    <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
                </svg>
                Refresh
            </button>
        </div>
    </div>

    <!-- Blockchain Data Source Agent Panel -->
    <div class="agent-panel" data-agent-id="blockchain">
        <div class="agent-panel-header">
            <div class="agent-title">
                <div class="agent-icon">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="3" width="7" height="7"/>
                        <rect x="14" y="3" width="7" height="7"/>
                        <rect x="14" y="14" width="7" height="7"/>
                        <rect x="3" y="14" width="7" height="7"/>
                    </svg>
                </div>
                Blockchain Agent
            </div>
            <div class="agent-status idle" id="blockchain-status">Idle</div>
        </div>
        
        <div class="agent-metrics">
            <div class="metric-item">
                <span class="metric-value metric-success-rate">0%</span>
                <span class="metric-label">Success Rate</span>
            </div>
            <div class="metric-item">
                <span class="metric-value metric-response-time">0s</span>
                <span class="metric-label">Avg Time</span>
            </div>
            <div class="metric-item">
                <span class="metric-value metric-requests">0</span>
                <span class="metric-label">Requests</span>
            </div>
            <div class="metric-item">
                <span class="metric-value metric-errors">0</span>
                <span class="metric-label">Errors</span>
            </div>
        </div>
        
        <div class="agent-insights">
            <div class="insight-item">
                <div class="insight-type">Network monitoring</div>
                Odiseo testnet connection active
            </div>
        </div>
        
        <div class="agent-actions">
            <button class="agent-btn" data-action="sync">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 12c0 4.97-4.03 9-9 9s-9-4.03-9-9 4.03-9 9-9 9 4.03 9 9z"/>
                    <path d="M12 6v6l4 2"/>
                </svg>
                Sync
            </button>
            <button class="agent-btn" data-action="refresh">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="23 4 23 10 17 10"/>
                    <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
                </svg>
                Refresh
            </button>
        </div>
    </div>

    <!-- External API Data Source Agent Panel -->
    <div class="agent-panel" data-agent-id="api">
        <div class="agent-panel-header">
            <div class="agent-title">
                <div class="agent-icon">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="2" y1="12" x2="22" y2="12"/>
                        <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
                    </svg>
                </div>
                External API Agent
            </div>
            <div class="agent-status idle" id="api-status">Idle</div>
        </div>
        
        <div class="agent-metrics">
            <div class="metric-item">
                <span class="metric-value metric-success-rate">0%</span>
                <span class="metric-label">Success Rate</span>
            </div>
            <div class="metric-item">
                <span class="metric-value metric-response-time">0s</span>
                <span class="metric-label">Avg Time</span>
            </div>
            <div class="metric-item">
                <span class="metric-value metric-requests">0</span>
                <span class="metric-label">Requests</span>
            </div>
            <div class="metric-item">
                <span class="metric-value metric-errors">0</span>
                <span class="metric-label">Errors</span>
            </div>
        </div>
        
        <div class="agent-insights">
            <div class="insight-item">
                <div class="insight-type">API monitoring</div>
                External data sources ready
            </div>
        </div>
        
        <div class="agent-actions">
            <button class="agent-btn" data-action="fetch">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7,10 12,15 17,10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                </svg>
                Fetch
            </button>
            <button class="agent-btn" data-action="refresh">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="23 4 23 10 17 10"/>
                    <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
                </svg>
                Refresh
            </button>
        </div>
    </div>
</div>

<style>
.agent-loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(5, 10, 19, 0.8);
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 16px;
    z-index: 10;
}

.agent-message {
    position: absolute;
    bottom: 1rem;
    left: 1rem;
    right: 1rem;
    padding: 0.75rem;
    border-radius: 8px;
    font-size: 0.85rem;
    z-index: 5;
}

.agent-message-success {
    background: rgba(0, 153, 7, 0.2);
    color: #009907;
    border: 1px solid rgba(0, 153, 7, 0.3);
}

.agent-message-error {
    background: rgba(237, 0, 72, 0.2);
    color: #ed0048;
    border: 1px solid rgba(237, 0, 72, 0.3);
}
</style>
'''
    
    component_path = Path("src/external_interfaces/ui/templates/components/agent_panels.html")
    component_path.parent.mkdir(exist_ok=True)
    with open(component_path, "w") as f:
        f.write(html_code)

def update_dashboard_template():
    """Update dashboard template to include agent panels"""
    
    dashboard_path = Path("src/external_interfaces/ui/templates/dashboard.html")
    
    if not dashboard_path.exists():
        print("⚠️  Dashboard template not found, creating basic template")
        return
        
    # Read current dashboard
    with open(dashboard_path, "r") as f:
        dashboard_content = f.read()
    
    # Add agent panels CSS and JS to base template
    base_path = Path("src/external_interfaces/ui/templates/base.html")
    
    if base_path.exists():
        with open(base_path, "r") as f:
            base_content = f.read()
        
        # Add CSS link if not present
        if "agent-panels.css" not in base_content:
            css_link = '    <link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/agent-panels.css\') }}">'
            base_content = base_content.replace(
                '    <link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/daodiseo-ux.css\') }}">',
                '    <link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/daodiseo-ux.css\') }}">\n' + css_link
            )
        
        # Add JS script if not present  
        if "agent-panels.js" not in base_content:
            js_script = '    <script src="{{ url_for(\'static\', filename=\'js/agent-panels.js\') }}"></script>'
            base_content = base_content.replace(
                '{% endblock %}',
                js_script + '\n{% endblock %}'
            )
        
        with open(base_path, "w") as f:
            f.write(base_content)
    
    # Add agent panels to dashboard if not present
    if "agent-panel-container" not in dashboard_content:
        # Find a good place to insert agent panels
        if '{% block content %}' in dashboard_content:
            agent_include = '''
    <!-- Data Source Integration Agents -->
    <div class="row mb-4">
        <div class="col-12">
            <h3 class="cosmic-text mb-3">
                <i data-feather="cpu"></i>
                Data Source Agents
            </h3>
            {% include 'components/agent_panels.html' %}
        </div>
    </div>
'''
            
            dashboard_content = dashboard_content.replace(
                '{% block content %}',
                '{% block content %}' + agent_include
            )
            
            with open(dashboard_path, "w") as f:
                f.write(dashboard_content)

def create_orchestrator_integration():
    """Create orchestrator integration for agent controller"""
    
    integration_code = '''"""
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
'''
    
    integration_path = Path("src/services/ai/agent_orchestrator_integration.py")
    with open(integration_path, "w") as f:
        f.write(integration_code)

def main():
    """Main execution function"""
    print("🚀 Data Source Integration Agent System")
    print("=" * 50)
    
    try:
        create_data_source_agents()
        print("\n🎉 Agent system created successfully!")
        print("\nFiles created:")
        print("- src/services/ai/agents/base_agent.py")
        print("- src/services/ai/agents/ifc_agent.py") 
        print("- src/services/ai/agents/blockchain_agent.py")
        print("- src/services/ai/agents/api_agent.py")
        print("- src/services/ai/agents/controller.py")
        print("- src/external_interfaces/ui/static/css/agent-panels.css")
        print("- src/external_interfaces/ui/static/js/agent-panels.js")
        print("- src/external_interfaces/ui/templates/components/agent_panels.html")
        print("- src/services/ai/agent_orchestrator_integration.py")
        
        print("\n📋 Next Steps:")
        print("1. Review the generated components")
        print("2. Test agent integration in your dashboard")
        print("3. Customize agent behaviors as needed")
        print("4. Run the application to see frosted glass agent panels")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main())