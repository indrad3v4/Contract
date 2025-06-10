"""
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
