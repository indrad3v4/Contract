"""
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
