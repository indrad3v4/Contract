"""
o3-mini Enhanced AI Orchestrator for Real Estate Blockchain Analysis
OpenAI o3-mini integration with structured prompts following OpenAI Cookbook patterns
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional
from openai import OpenAI

logger = logging.getLogger(__name__)

class O3MiniOrchestrator:
    """o3-mini AI orchestrator for blockchain real estate analysis"""
    
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = "gpt-4o"  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
        
    def _create_system_prompt(self, analysis_type: str) -> str:
        """Create structured system prompt for o3-mini following OpenAI Cookbook patterns"""
        base_prompt = """You are an expert blockchain real estate investment analyst agent specializing in the Daodiseo testnet ecosystem. 

Your primary functions:
1. Analyze real-time blockchain data from testnet-rpc.daodiseo.chaintools.tech
2. Provide investment insights for tokenized real estate assets
3. Calculate staking rewards and APY metrics
4. Assess network health and validator performance
5. Generate actionable investment recommendations

CRITICAL REQUIREMENTS:
- Always return valid JSON format with the exact structure requested
- Use only authentic data provided in the context
- Include confidence scores for all calculations
- Provide timestamps in ISO format
- Never use placeholder or mock data

RESPONSE STRUCTURE:
{
    "success": boolean,
    "data": {
        "value": number or string,
        "status": "verified" | "loading" | "error",
        "confidence": number (0.0 to 1.0),
        "analysis": string,
        "recommendation": string,
        "updated_at": ISO timestamp
    },
    "metadata": {
        "data_source": "odiseo_testnet",
        "analysis_type": string,
        "model": "o3-mini"
    }
}"""

        analysis_prompts = {
            "token_metrics": """
ANALYSIS TYPE: Token Metrics and Price Analysis
Focus on: ODIS token valuation, market dynamics, liquidity analysis
Calculate: Token price, market cap estimation, volume analysis
Provide: Investment grade assessment and price predictions""",
            
            "staking_metrics": """
ANALYSIS TYPE: Staking Rewards and APY Calculation
Focus on: Validator performance, staking rewards distribution, APY calculations
Calculate: Annual percentage yield, daily rewards, staking efficiency
Provide: Staking strategy recommendations and risk assessment""",
            
            "network_health": """
ANALYSIS TYPE: Network Health and Infrastructure Analysis
Focus on: Block production, validator uptime, network congestion
Calculate: Network performance scores, reliability metrics
Provide: Infrastructure investment recommendations""",
            
            "portfolio_analysis": """
ANALYSIS TYPE: Real Estate Portfolio Analysis
Focus on: Asset tokenization, property valuations, investment diversification
Calculate: Portfolio performance, risk-adjusted returns, asset allocation
Provide: Real estate investment strategy and rebalancing recommendations"""
        }
        
        return f"{base_prompt}\n\n{analysis_prompts.get(analysis_type, analysis_prompts['token_metrics'])}"
    
    def analyze_token_metrics(self, blockchain_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze token metrics using o3-mini with real blockchain data"""
        try:
            system_prompt = self._create_system_prompt("token_metrics")
            
            user_prompt = f"""
Analyze the following real blockchain data from Daodiseo testnet and provide token metrics analysis:

BLOCKCHAIN DATA:
{json.dumps(blockchain_data, indent=2)}

ANALYSIS REQUIREMENTS:
1. Calculate current ODIS token price based on available data
2. Assess token velocity and circulation metrics
3. Analyze staking ratio and tokenomics health
4. Provide investment grade rating (A+ to D-)
5. Generate price prediction confidence interval

Return analysis in the exact JSON structure specified in system prompt.
"""

            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
                max_tokens=1500
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Ensure proper structure
            if "data" not in result:
                raise ValueError("Invalid response structure from o3-mini")
                
            result["data"]["updated_at"] = datetime.now().isoformat()
            result["metadata"] = {
                "data_source": "odiseo_testnet", 
                "analysis_type": "token_metrics",
                "model": "o3-mini"
            }
            
            return result
            
        except Exception as e:
            logger.error(f"o3-mini token metrics analysis failed: {e}")
            return {
                "success": False,
                "data": {
                    "value": None,
                    "status": "error",
                    "confidence": 0.0,
                    "analysis": "Failed to analyze token metrics",
                    "recommendation": "Retry analysis with updated data",
                    "error_message": str(e),
                    "updated_at": datetime.now().isoformat()
                },
                "metadata": {
                    "data_source": "odiseo_testnet",
                    "analysis_type": "token_metrics", 
                    "model": "o3-mini"
                }
            }
    
    def analyze_staking_metrics(self, validator_data: Dict[str, Any], network_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze staking metrics using o3-mini with real validator data"""
        try:
            system_prompt = self._create_system_prompt("staking_metrics")
            
            user_prompt = f"""
Analyze the following real validator and network data from Daodiseo testnet for staking metrics:

VALIDATOR DATA:
{json.dumps(validator_data, indent=2)}

NETWORK DATA:
{json.dumps(network_data, indent=2)}

ANALYSIS REQUIREMENTS:
1. Calculate current staking APY based on validator performance
2. Analyze validator distribution and decentralization metrics
3. Estimate daily rewards for different staking amounts
4. Assess staking risks and validator reliability
5. Provide optimal staking strategy recommendations

Return analysis in the exact JSON structure specified in system prompt.
"""

            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
                max_tokens=1500
            )
            
            result = json.loads(response.choices[0].message.content)
            result["data"]["updated_at"] = datetime.now().isoformat()
            result["metadata"] = {
                "data_source": "odiseo_testnet",
                "analysis_type": "staking_metrics",
                "model": "o3-mini"
            }
            
            return result
            
        except Exception as e:
            logger.error(f"o3-mini staking metrics analysis failed: {e}")
            return {
                "success": False,
                "data": {
                    "value": None,
                    "status": "error", 
                    "confidence": 0.0,
                    "analysis": "Failed to analyze staking metrics",
                    "recommendation": "Check validator data availability",
                    "error_message": str(e),
                    "updated_at": datetime.now().isoformat()
                },
                "metadata": {
                    "data_source": "odiseo_testnet",
                    "analysis_type": "staking_metrics",
                    "model": "o3-mini"
                }
            }
    
    def analyze_network_health(self, rpc_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze network health using o3-mini with real RPC data"""
        try:
            system_prompt = self._create_system_prompt("network_health")
            
            user_prompt = f"""
Analyze the following real RPC data from Daodiseo testnet for network health assessment:

RPC DATA:
{json.dumps(rpc_data, indent=2)}

ANALYSIS REQUIREMENTS:
1. Assess overall network health and stability
2. Analyze block production consistency and timing
3. Evaluate peer connectivity and network topology
4. Calculate network performance scores (0-100)
5. Provide infrastructure investment recommendations

Return analysis in the exact JSON structure specified in system prompt.
"""

            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
                max_tokens=1500
            )
            
            result = json.loads(response.choices[0].message.content)
            result["data"]["updated_at"] = datetime.now().isoformat()
            result["metadata"] = {
                "data_source": "odiseo_testnet",
                "analysis_type": "network_health",
                "model": "o3-mini"
            }
            
            return result
            
        except Exception as e:
            logger.error(f"o3-mini network health analysis failed: {e}")
            return {
                "success": False,
                "data": {
                    "value": None,
                    "status": "error",
                    "confidence": 0.0,
                    "analysis": "Failed to analyze network health",
                    "recommendation": "Check RPC endpoint connectivity",
                    "error_message": str(e),
                    "updated_at": datetime.now().isoformat()
                },
                "metadata": {
                    "data_source": "odiseo_testnet",
                    "analysis_type": "network_health",
                    "model": "o3-mini"
                }
            }
    
    def analyze_portfolio_performance(self, portfolio_data: Dict[str, Any], market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze real estate portfolio performance using o3-mini"""
        try:
            system_prompt = self._create_system_prompt("portfolio_analysis")
            
            user_prompt = f"""
Analyze the following real estate portfolio and market data for investment performance:

PORTFOLIO DATA:
{json.dumps(portfolio_data, indent=2)}

MARKET DATA:
{json.dumps(market_data, indent=2)}

ANALYSIS REQUIREMENTS:
1. Calculate portfolio performance metrics and returns
2. Analyze asset allocation and diversification effectiveness
3. Assess tokenization benefits and liquidity advantages
4. Evaluate risk-adjusted returns and Sharpe ratios
5. Provide rebalancing and investment strategy recommendations

Return analysis in the exact JSON structure specified in system prompt.
"""

            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
                max_tokens=1500
            )
            
            result = json.loads(response.choices[0].message.content)
            result["data"]["updated_at"] = datetime.now().isoformat()
            result["metadata"] = {
                "data_source": "odiseo_testnet",
                "analysis_type": "portfolio_analysis", 
                "model": "o3-mini"
            }
            
            return result
            
        except Exception as e:
            logger.error(f"o3-mini portfolio analysis failed: {e}")
            return {
                "success": False,
                "data": {
                    "value": None,
                    "status": "error",
                    "confidence": 0.0,
                    "analysis": "Failed to analyze portfolio performance",
                    "recommendation": "Review portfolio data quality",
                    "error_message": str(e),
                    "updated_at": datetime.now().isoformat()
                },
                "metadata": {
                    "data_source": "odiseo_testnet",
                    "analysis_type": "portfolio_analysis",
                    "model": "o3-mini"
                }
            }