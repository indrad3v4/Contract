"""
Chain Brain Orchestrator - Deep o3-mini Integration
Feeds actual blockchain data directly into the AI orchestrator's reasoning engine
"""

import logging
import time
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import requests
from concurrent.futures import ThreadPoolExecutor

from src.services.ai.orchestrator import get_orchestrator
from src.services.blockchain_service import BlockchainService

logger = logging.getLogger(__name__)

@dataclass
class ChainDataPoint:
    """Represents a single data point from the blockchain"""
    timestamp: datetime
    data_type: str
    value: Any
    source_endpoint: str
    context: Dict[str, Any]

class ChainBrainOrchestrator:
    """
    Deep o3-mini orchestrator that continuously feeds actual chain data into AI reasoning
    """
    
    def __init__(self):
        self.rpc_endpoint = "https://testnet-rpc.daodiseo.chaintools.tech"
        self.rest_endpoint = "https://testnet-api.daodiseo.chaintools.tech"
        self.orchestrator = get_orchestrator()
        self.blockchain_service = BlockchainService()
        self.data_cache = {}
        self.learning_memory = []
        self.is_feeding = False
        self.feed_interval = 30  # seconds
        self.max_memory_size = 1000
        
        # Initialize chain data feeds
        self.chain_feeds = {
            'validators': self._feed_validator_data,
            'blocks': self._feed_block_data,
            'transactions': self._feed_transaction_data,
            'consensus': self._feed_consensus_data,
            'network_state': self._feed_network_state,
            'governance': self._feed_governance_data
        }
        
    async def start_chain_brain_feeding(self):
        """Start continuous feeding of chain data into o3-mini brain"""
        if self.is_feeding:
            return
            
        self.is_feeding = True
        logger.info("Starting Chain Brain feeding into o3-mini orchestrator...")
        
        # Initialize with historical context
        await self._initialize_chain_context()
        
        # Start continuous feeding
        while self.is_feeding:
            try:
                await self._feed_all_chain_data()
                await self._process_learning_insights()
                await asyncio.sleep(self.feed_interval)
            except Exception as e:
                logger.error(f"Chain brain feeding error: {e}")
                await asyncio.sleep(5)
    
    def stop_chain_brain_feeding(self):
        """Stop the chain data feeding"""
        self.is_feeding = False
        logger.info("Stopped Chain Brain feeding")
    
    async def _initialize_chain_context(self):
        """Initialize the AI brain with current chain state context"""
        try:
            # Get comprehensive current state
            current_state = await self._get_comprehensive_chain_state()
            
            # Feed initial context to o3-mini
            context_prompt = f"""
            Initialize blockchain analysis brain with current Odiseo testnet state:
            
            Network Status: {current_state['network']['status']}
            Block Height: {current_state['network']['height']}
            Active Validators: {current_state['validators']['count']}
            Total Stake: {current_state['validators']['total_stake']}
            Governance Proposals: {current_state['governance']['active_proposals']}
            
            This is your continuous data feed source. Analyze patterns, detect anomalies,
            and provide intelligent insights for real estate blockchain operations.
            """
            
            result = self.orchestrator.orchestrate_task(
                context_prompt,
                {
                    "mode": "initialization",
                    "data_source": "chain_brain",
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            if result.get("success"):
                logger.info("Chain Brain initialized successfully in o3-mini")
            else:
                logger.warning("Chain Brain initialization had issues")
                
        except Exception as e:
            logger.error(f"Failed to initialize chain context: {e}")
    
    async def _get_comprehensive_chain_state(self) -> Dict[str, Any]:
        """Get comprehensive current blockchain state"""
        try:
            # Parallel fetch of all critical data
            with ThreadPoolExecutor(max_workers=6) as executor:
                futures = {
                    'status': executor.submit(self._fetch_status),
                    'validators': executor.submit(self._fetch_validators),
                    'latest_block': executor.submit(self._fetch_latest_block),
                    'consensus_params': executor.submit(self._fetch_consensus_params),
                    'net_info': executor.submit(self._fetch_net_info),
                    'governance': executor.submit(self._fetch_governance_data)
                }
                
                results = {}
                for key, future in futures.items():
                    try:
                        results[key] = future.result(timeout=10)
                    except Exception as e:
                        logger.warning(f"Failed to fetch {key}: {e}")
                        results[key] = {}
            
            # Process and structure the data
            return {
                'network': {
                    'status': results['status'].get('result', {}).get('sync_info', {}).get('catching_up', True),
                    'height': int(results['status'].get('result', {}).get('sync_info', {}).get('latest_block_height', 0)),
                    'chain_id': results['status'].get('result', {}).get('node_info', {}).get('network', 'unknown'),
                    'peers': results['net_info'].get('result', {}).get('n_peers', 0)
                },
                'validators': {
                    'count': len(results['validators'].get('result', {}).get('validators', [])),
                    'total_stake': self._calculate_total_stake(results['validators']),
                    'active': self._count_active_validators(results['validators'])
                },
                'consensus': {
                    'block_time': results['consensus_params'].get('result', {}).get('consensus_params', {}).get('block', {}).get('time_iota_ms', 0),
                    'max_gas': results['consensus_params'].get('result', {}).get('consensus_params', {}).get('block', {}).get('max_gas', 0)
                },
                'governance': {
                    'active_proposals': 0,  # Would be fetched from governance module
                    'voting_period': 0
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get comprehensive chain state: {e}")
            return {}
    
    async def _feed_all_chain_data(self):
        """Feed all types of chain data to the AI brain"""
        for feed_name, feed_func in self.chain_feeds.items():
            try:
                data_points = await feed_func()
                await self._process_data_points(feed_name, data_points)
            except Exception as e:
                logger.warning(f"Failed to feed {feed_name} data: {e}")
    
    async def _feed_validator_data(self) -> List[ChainDataPoint]:
        """Feed real-time validator data"""
        try:
            validators_data = self._fetch_validators()
            validators = validators_data.get('result', {}).get('validators', [])
            
            data_points = []
            for validator in validators:
                data_points.append(ChainDataPoint(
                    timestamp=datetime.now(),
                    data_type='validator_status',
                    value={
                        'address': validator.get('address'),
                        'voting_power': int(validator.get('voting_power', 0)),
                        'proposer_priority': int(validator.get('proposer_priority', 0))
                    },
                    source_endpoint='/validators',
                    context={'validator_count': len(validators)}
                ))
            
            return data_points
            
        except Exception as e:
            logger.error(f"Failed to feed validator data: {e}")
            return []
    
    async def _feed_block_data(self) -> List[ChainDataPoint]:
        """Feed real-time block data"""
        try:
            status_data = self._fetch_status()
            sync_info = status_data.get('result', {}).get('sync_info', {})
            
            latest_block_height = int(sync_info.get('latest_block_height', 0))
            latest_block_time = sync_info.get('latest_block_time')
            
            # Get specific block data
            block_data = self._fetch_block(latest_block_height)
            
            return [ChainDataPoint(
                timestamp=datetime.now(),
                data_type='block_production',
                value={
                    'height': latest_block_height,
                    'time': latest_block_time,
                    'tx_count': len(block_data.get('result', {}).get('block', {}).get('data', {}).get('txs', [])),
                    'proposer': block_data.get('result', {}).get('block', {}).get('header', {}).get('proposer_address')
                },
                source_endpoint='/status',
                context={'catching_up': sync_info.get('catching_up', False)}
            )]
            
        except Exception as e:
            logger.error(f"Failed to feed block data: {e}")
            return []
    
    async def _feed_transaction_data(self) -> List[ChainDataPoint]:
        """Feed real-time transaction data"""
        try:
            # Get unconfirmed transactions
            unconfirmed = self._fetch_unconfirmed_txs()
            unconfirmed_txs = unconfirmed.get('result', {}).get('txs', [])
            
            # Search for recent transactions
            recent_txs_data = self._fetch_tx_search()
            recent_txs = recent_txs_data.get('result', {}).get('txs', [])
            
            data_points = []
            
            # Process unconfirmed transactions
            data_points.append(ChainDataPoint(
                timestamp=datetime.now(),
                data_type='mempool_status',
                value={
                    'unconfirmed_count': len(unconfirmed_txs),
                    'recent_confirmed': len(recent_txs)
                },
                source_endpoint='/unconfirmed_txs',
                context={'network_activity': 'real_time'}
            ))
            
            return data_points
            
        except Exception as e:
            logger.error(f"Failed to feed transaction data: {e}")
            return []
    
    async def _feed_consensus_data(self) -> List[ChainDataPoint]:
        """Feed consensus state data"""
        try:
            consensus_state = self._fetch_consensus_state()
            
            return [ChainDataPoint(
                timestamp=datetime.now(),
                data_type='consensus_state',
                value=consensus_state.get('result', {}),
                source_endpoint='/consensus_state',
                context={'data_type': 'consensus_monitoring'}
            )]
            
        except Exception as e:
            logger.error(f"Failed to feed consensus data: {e}")
            return []
    
    async def _feed_network_state(self) -> List[ChainDataPoint]:
        """Feed network state data"""
        try:
            net_info = self._fetch_net_info()
            health = self._fetch_health()
            
            return [ChainDataPoint(
                timestamp=datetime.now(),
                data_type='network_health',
                value={
                    'peers': net_info.get('result', {}).get('n_peers', 0),
                    'listening': net_info.get('result', {}).get('listening', False),
                    'health_status': 'healthy' if health else 'unhealthy'
                },
                source_endpoint='/net_info',
                context={'monitoring_type': 'network_health'}
            )]
            
        except Exception as e:
            logger.error(f"Failed to feed network state: {e}")
            return []
    
    async def _feed_governance_data(self) -> List[ChainDataPoint]:
        """Feed governance data"""
        try:
            # This would query governance module for proposals
            # For now, return basic governance state
            return [ChainDataPoint(
                timestamp=datetime.now(),
                data_type='governance_state',
                value={
                    'active_proposals': 0,
                    'voting_period': True
                },
                source_endpoint='/governance',
                context={'governance_active': True}
            )]
            
        except Exception as e:
            logger.error(f"Failed to feed governance data: {e}")
            return []
    
    async def _process_data_points(self, feed_name: str, data_points: List[ChainDataPoint]):
        """Process data points and feed to o3-mini brain"""
        if not data_points:
            return
        
        # Store in memory
        self.learning_memory.extend(data_points)
        
        # Limit memory size
        if len(self.learning_memory) > self.max_memory_size:
            self.learning_memory = self.learning_memory[-self.max_memory_size:]
        
        # Prepare data for AI analysis
        data_summary = self._summarize_data_points(feed_name, data_points)
        
        # Feed to o3-mini if significant data
        if self._is_significant_data(data_points):
            await self._feed_to_orchestrator(feed_name, data_summary, data_points)
    
    def _summarize_data_points(self, feed_name: str, data_points: List[ChainDataPoint]) -> str:
        """Create summary of data points for AI consumption"""
        summary_parts = [f"Chain Data Feed: {feed_name}"]
        
        for dp in data_points:
            summary_parts.append(f"- {dp.data_type}: {dp.value}")
        
        return " | ".join(summary_parts)
    
    def _is_significant_data(self, data_points: List[ChainDataPoint]) -> bool:
        """Determine if data points are significant enough for AI analysis"""
        # Only process every 3rd cycle to avoid overwhelming the AI
        return len(self.learning_memory) % 3 == 0
    
    async def _feed_to_orchestrator(self, feed_name: str, summary: str, data_points: List[ChainDataPoint]):
        """Feed processed data to o3-mini orchestrator"""
        try:
            analysis_prompt = f"""
            Real-time blockchain data update:
            {summary}
            
            Analyze this data for:
            1. Network health indicators
            2. Validator performance patterns  
            3. Transaction flow anomalies
            4. Governance implications
            5. Real estate tokenization insights
            
            Provide brief analysis and any alerts.
            """
            
            result = self.orchestrator.orchestrate_task(
                analysis_prompt,
                {
                    "mode": "real_time_analysis",
                    "data_source": "chain_brain",
                    "feed_type": feed_name,
                    "data_points": len(data_points),
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            if result.get("success"):
                # Store AI insights for later retrieval
                insight = {
                    "timestamp": datetime.now(),
                    "feed_name": feed_name,
                    "ai_response": result.get("response"),
                    "data_summary": summary
                }
                self._store_ai_insight(insight)
            
        except Exception as e:
            logger.error(f"Failed to feed data to orchestrator: {e}")
    
    async def _process_learning_insights(self):
        """Process accumulated learning insights"""
        if len(self.learning_memory) % 100 == 0:  # Every 100 data points
            await self._generate_pattern_analysis()
    
    async def _generate_pattern_analysis(self):
        """Generate pattern analysis from accumulated data"""
        try:
            recent_data = self.learning_memory[-50:]  # Last 50 data points
            
            pattern_prompt = f"""
            Pattern Analysis Request:
            Analyze the last 50 blockchain data points to identify:
            1. Emerging trends in validator behavior
            2. Network performance patterns
            3. Transaction volume patterns
            4. Potential issues or optimizations
            
            Data points span: {len(recent_data)} entries
            Time range: {recent_data[0].timestamp} to {recent_data[-1].timestamp}
            
            Provide strategic insights for real estate blockchain operations.
            """
            
            result = self.orchestrator.orchestrate_task(
                pattern_prompt,
                {
                    "mode": "pattern_analysis",
                    "data_source": "chain_brain_patterns",
                    "analysis_depth": "deep",
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            if result.get("success"):
                logger.info("Pattern analysis completed by o3-mini")
                
        except Exception as e:
            logger.error(f"Failed to generate pattern analysis: {e}")
    
    def _store_ai_insight(self, insight: Dict[str, Any]):
        """Store AI insight for retrieval"""
        cache_key = f"ai_insight_{insight['timestamp'].strftime('%Y%m%d_%H%M%S')}"
        self.data_cache[cache_key] = insight
        
        # Limit cache size
        if len(self.data_cache) > 100:
            oldest_key = min(self.data_cache.keys())
            del self.data_cache[oldest_key]
    
    def get_recent_insights(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent AI insights"""
        insights = list(self.data_cache.values())
        insights.sort(key=lambda x: x['timestamp'], reverse=True)
        return insights[:limit]
    
    async def get_ai_chain_analysis(self, query: str) -> Dict[str, Any]:
        """Get AI analysis of current chain state for specific query"""
        try:
            # Get current state
            current_state = await self._get_comprehensive_chain_state()
            
            # Get recent insights
            recent_insights = self.get_recent_insights(5)
            
            analysis_prompt = f"""
            Query: {query}
            
            Current Chain State:
            {json.dumps(current_state, indent=2)}
            
            Recent AI Insights:
            {json.dumps(recent_insights, indent=2, default=str)}
            
            Provide comprehensive analysis addressing the query with current data.
            """
            
            return self.orchestrator.orchestrate_task(
                analysis_prompt,
                {
                    "mode": "on_demand_analysis",
                    "data_source": "chain_brain_query",
                    "query": query,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Failed to get AI chain analysis: {e}")
            return {"success": False, "error": str(e)}
    
    # Blockchain data fetching methods
    def _fetch_status(self) -> Dict[str, Any]:
        """Fetch network status"""
        try:
            response = requests.get(f"{self.rpc_endpoint}/status", timeout=10)
            return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch status: {e}")
            return {}
    
    def _fetch_validators(self) -> Dict[str, Any]:
        """Fetch validators data"""
        try:
            response = requests.get(f"{self.rpc_endpoint}/validators", timeout=10)
            return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch validators: {e}")
            return {}
    
    def _fetch_latest_block(self) -> Dict[str, Any]:
        """Fetch latest block"""
        try:
            response = requests.get(f"{self.rpc_endpoint}/block", timeout=10)
            return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch latest block: {e}")
            return {}
    
    def _fetch_block(self, height: int) -> Dict[str, Any]:
        """Fetch specific block"""
        try:
            response = requests.get(f"{self.rpc_endpoint}/block?height={height}", timeout=10)
            return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch block {height}: {e}")
            return {}
    
    def _fetch_consensus_params(self) -> Dict[str, Any]:
        """Fetch consensus parameters"""
        try:
            response = requests.get(f"{self.rpc_endpoint}/consensus_params", timeout=10)
            return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch consensus params: {e}")
            return {}
    
    def _fetch_consensus_state(self) -> Dict[str, Any]:
        """Fetch consensus state"""
        try:
            response = requests.get(f"{self.rpc_endpoint}/consensus_state", timeout=10)
            return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch consensus state: {e}")
            return {}
    
    def _fetch_net_info(self) -> Dict[str, Any]:
        """Fetch network info"""
        try:
            response = requests.get(f"{self.rpc_endpoint}/net_info", timeout=10)
            return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch net info: {e}")
            return {}
    
    def _fetch_health(self) -> bool:
        """Check network health"""
        try:
            response = requests.get(f"{self.rpc_endpoint}/health", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def _fetch_unconfirmed_txs(self) -> Dict[str, Any]:
        """Fetch unconfirmed transactions"""
        try:
            response = requests.get(f"{self.rpc_endpoint}/unconfirmed_txs?limit=100", timeout=10)
            return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch unconfirmed txs: {e}")
            return {}
    
    def _fetch_tx_search(self) -> Dict[str, Any]:
        """Search for recent transactions"""
        try:
            response = requests.get(f"{self.rpc_endpoint}/tx_search?query=\"\"&page=1&per_page=20", timeout=10)
            return response.json()
        except Exception as e:
            logger.error(f"Failed to search transactions: {e}")
            return {}
    
    def _fetch_governance_data(self) -> Dict[str, Any]:
        """Fetch governance data"""
        try:
            # This would query governance module
            response = requests.get(f"{self.rest_endpoint}/cosmos/gov/v1/proposals", timeout=10)
            return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch governance data: {e}")
            return {}
    
    def _calculate_total_stake(self, validators_data: Dict[str, Any]) -> int:
        """Calculate total voting power"""
        validators = validators_data.get('result', {}).get('validators', [])
        return sum(int(v.get('voting_power', 0)) for v in validators)
    
    def _count_active_validators(self, validators_data: Dict[str, Any]) -> int:
        """Count active validators"""
        validators = validators_data.get('result', {}).get('validators', [])
        return len([v for v in validators if int(v.get('voting_power', 0)) > 0])


# Global instance
_chain_brain_orchestrator = None

def get_chain_brain_orchestrator() -> ChainBrainOrchestrator:
    """Get the global chain brain orchestrator instance"""
    global _chain_brain_orchestrator
    if _chain_brain_orchestrator is None:
        _chain_brain_orchestrator = ChainBrainOrchestrator()
    return _chain_brain_orchestrator

async def start_chain_brain():
    """Start the chain brain feeding process"""
    orchestrator = get_chain_brain_orchestrator()
    await orchestrator.start_chain_brain_feeding()

def stop_chain_brain():
    """Stop the chain brain feeding process"""
    global _chain_brain_orchestrator
    if _chain_brain_orchestrator:
        _chain_brain_orchestrator.stop_chain_brain_feeding()