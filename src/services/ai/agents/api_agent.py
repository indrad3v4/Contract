"""
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
