"""
Get Asset Metrics Use Case - Clean Architecture Layer 1
Application business rule for retrieving and calculating asset performance metrics
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
import random


class GetAssetMetricsUseCase:
    """Use case for retrieving asset performance metrics and portfolio analytics"""
    
    def __init__(self, asset_repository=None, blockchain_gateway=None):
        self.asset_repository = asset_repository
        self.blockchain_gateway = blockchain_gateway
    
    def execute(self) -> Dict[str, Any]:
        """
        Execute asset metrics calculation
        
        Returns:
            Dict containing comprehensive asset metrics
        """
        try:
            # Get portfolio data
            portfolio_data = self._get_portfolio_data()
            
            # Calculate performance metrics
            performance_metrics = self._calculate_performance_metrics(portfolio_data)
            
            # Get market trends
            market_trends = self._analyze_market_trends()
            
            # Calculate risk assessment
            risk_assessment = self._calculate_risk_assessment(portfolio_data)
            
            # Get top performing assets
            top_performers = self._get_top_performing_assets(portfolio_data)
            
            return {
                "success": True,
                "timestamp": datetime.now().isoformat(),
                "portfolio": {
                    "total_value": performance_metrics["total_value"],
                    "total_invested": performance_metrics["total_invested"],
                    "total_return": performance_metrics["total_return"],
                    "roi_percentage": performance_metrics["roi_percentage"],
                    "asset_count": performance_metrics["asset_count"],
                    "diversification_score": performance_metrics["diversification_score"]
                },
                "performance": {
                    "daily_change": performance_metrics["daily_change"],
                    "weekly_change": performance_metrics["weekly_change"],
                    "monthly_change": performance_metrics["monthly_change"],
                    "ytd_change": performance_metrics["ytd_change"],
                    "annualized_return": performance_metrics["annualized_return"]
                },
                "market_trends": market_trends,
                "risk_assessment": risk_assessment,
                "top_performers": top_performers,
                "analytics": {
                    "income_generating": performance_metrics["income_generating"],
                    "appreciation_assets": performance_metrics["appreciation_assets"],
                    "liquid_assets": performance_metrics["liquid_assets"],
                    "average_hold_period": performance_metrics["average_hold_period"]
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _get_portfolio_data(self) -> List[Dict[str, Any]]:
        """
        Get portfolio data from repository or generate sample data
        
        Returns:
            List of asset data
        """
        if self.asset_repository:
            # In production, this would query the actual repository
            return self.asset_repository.get_all_assets()
        else:
            # Generate sample portfolio data for demonstration
            return self._generate_sample_portfolio()
    
    def _generate_sample_portfolio(self) -> List[Dict[str, Any]]:
        """
        Generate sample portfolio data for demonstration
        
        Returns:
            Sample asset portfolio
        """
        sample_assets = [
            {
                "id": "asset_001",
                "name": "Ithaca Village Apartments",
                "type": "residential",
                "location": "Ithaca, NY",
                "purchase_price": 2500000,
                "current_value": 2850000,
                "tokens_owned": 750,
                "total_tokens": 1000,
                "purchase_date": "2024-01-15",
                "annual_income": 180000,
                "expenses": 45000,
                "roi": 14.1
            },
            {
                "id": "asset_002", 
                "name": "Tech Campus Office Building",
                "type": "commercial",
                "location": "Austin, TX",
                "purchase_price": 5200000,
                "current_value": 5720000,
                "tokens_owned": 320,
                "total_tokens": 2000,
                "purchase_date": "2024-03-22",
                "annual_income": 415000,
                "expenses": 85000,
                "roi": 16.3
            },
            {
                "id": "asset_003",
                "name": "Riverside Retail Plaza",
                "type": "commercial",
                "location": "Portland, OR",
                "purchase_price": 3800000,
                "current_value": 3990000,
                "tokens_owned": 150,
                "total_tokens": 1500,
                "purchase_date": "2024-02-10",
                "annual_income": 285000,
                "expenses": 58000,
                "roi": 11.0
            },
            {
                "id": "asset_004",
                "name": "Mountain View Condos",
                "type": "residential",
                "location": "Denver, CO",
                "purchase_price": 1800000,
                "current_value": 1950000,
                "tokens_owned": 425,
                "total_tokens": 800,
                "purchase_date": "2024-04-05",
                "annual_income": 144000,
                "expenses": 32000,
                "roi": 14.5
            },
            {
                "id": "asset_005",
                "name": "Industrial Warehouse Complex",
                "type": "industrial",
                "location": "Phoenix, AZ",
                "purchase_price": 4500000,
                "current_value": 4725000,
                "tokens_owned": 200,
                "total_tokens": 1800,
                "purchase_date": "2024-01-30",
                "annual_income": 360000,
                "expenses": 72000,
                "roi": 11.4
            }
        ]
        
        return sample_assets
    
    def _calculate_performance_metrics(self, portfolio_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate comprehensive performance metrics
        
        Args:
            portfolio_data: List of asset data
            
        Returns:
            Performance metrics
        """
        if not portfolio_data:
            return self._empty_metrics()
        
        total_invested = sum(asset["purchase_price"] * (asset["tokens_owned"] / asset["total_tokens"]) 
                           for asset in portfolio_data)
        total_value = sum(asset["current_value"] * (asset["tokens_owned"] / asset["total_tokens"]) 
                         for asset in portfolio_data)
        total_return = total_value - total_invested
        roi_percentage = (total_return / total_invested * 100) if total_invested > 0 else 0
        
        # Calculate income metrics
        annual_income = sum(asset["annual_income"] * (asset["tokens_owned"] / asset["total_tokens"]) 
                          for asset in portfolio_data)
        annual_expenses = sum(asset["expenses"] * (asset["tokens_owned"] / asset["total_tokens"]) 
                            for asset in portfolio_data)
        net_income = annual_income - annual_expenses
        
        # Diversification score (simple calculation based on asset types)
        asset_types = set(asset["type"] for asset in portfolio_data)
        diversification_score = min(100, len(asset_types) * 25)
        
        # Performance changes (simulated for demo)
        daily_change = random.uniform(-2.5, 3.0)
        weekly_change = random.uniform(-8.0, 12.0)
        monthly_change = random.uniform(-15.0, 25.0)
        ytd_change = random.uniform(-20.0, 40.0)
        
        return {
            "total_value": total_value,
            "total_invested": total_invested,
            "total_return": total_return,
            "roi_percentage": roi_percentage,
            "asset_count": len(portfolio_data),
            "diversification_score": diversification_score,
            "annual_income": annual_income,
            "annual_expenses": annual_expenses,
            "net_income": net_income,
            "daily_change": daily_change,
            "weekly_change": weekly_change,
            "monthly_change": monthly_change,
            "ytd_change": ytd_change,
            "annualized_return": roi_percentage,
            "income_generating": len([a for a in portfolio_data if a["annual_income"] > 0]),
            "appreciation_assets": len([a for a in portfolio_data if a["current_value"] > a["purchase_price"]]),
            "liquid_assets": len([a for a in portfolio_data if a["tokens_owned"] / a["total_tokens"] < 0.5]),
            "average_hold_period": self._calculate_average_hold_period(portfolio_data)
        }
    
    def _analyze_market_trends(self) -> Dict[str, Any]:
        """
        Analyze market trends for real estate tokenization
        
        Returns:
            Market trend analysis
        """
        # In production, this would analyze real market data
        return {
            "overall_sentiment": "bullish",
            "tokenization_growth": 23.5,  # % growth in tokenization market
            "average_roi": 12.8,  # Average ROI across all tokenized properties
            "liquidity_index": 78.2,  # Liquidity index (0-100)
            "demand_score": 85.4,  # Demand score (0-100)
            "supply_score": 72.1,  # Supply score (0-100)
            "trends": [
                {
                    "category": "Residential",
                    "trend": "up",
                    "change": 8.3,
                    "confidence": 87
                },
                {
                    "category": "Commercial",
                    "trend": "up",
                    "change": 12.1,
                    "confidence": 92
                },
                {
                    "category": "Industrial",
                    "trend": "stable",
                    "change": 2.4,
                    "confidence": 78
                }
            ]
        }
    
    def _calculate_risk_assessment(self, portfolio_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate risk assessment for the portfolio
        
        Args:
            portfolio_data: List of asset data
            
        Returns:
            Risk assessment metrics
        """
        if not portfolio_data:
            return {"risk_score": 0, "risk_level": "unknown"}
        
        # Calculate risk based on diversification, asset types, and concentration
        asset_type_count = len(set(asset["type"] for asset in portfolio_data))
        concentration_risk = max(asset["tokens_owned"] / asset["total_tokens"] for asset in portfolio_data)
        
        # Simple risk scoring algorithm
        diversification_score = min(100, asset_type_count * 20)
        concentration_penalty = concentration_risk * 30
        
        risk_score = max(0, min(100, 50 + diversification_score - concentration_penalty))
        
        if risk_score >= 80:
            risk_level = "low"
        elif risk_score >= 60:
            risk_level = "moderate"
        elif risk_score >= 40:
            risk_level = "high"
        else:
            risk_level = "very_high"
        
        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "diversification_score": diversification_score,
            "concentration_risk": concentration_risk,
            "factors": [
                f"Portfolio spread across {asset_type_count} property types",
                f"Highest single asset exposure: {concentration_risk:.1%}",
                f"Geographic diversification: {len(set(asset['location'] for asset in portfolio_data))} markets"
            ],
            "recommendations": self._generate_risk_recommendations(risk_level, portfolio_data)
        }
    
    def _get_top_performing_assets(self, portfolio_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Get top performing assets from portfolio
        
        Args:
            portfolio_data: List of asset data
            
        Returns:
            Top performing assets
        """
        # Sort by ROI and return top 3
        sorted_assets = sorted(portfolio_data, key=lambda x: x["roi"], reverse=True)
        
        return [
            {
                "id": asset["id"],
                "name": asset["name"],
                "type": asset["type"],
                "location": asset["location"],
                "roi": asset["roi"],
                "current_value": asset["current_value"],
                "ownership_percentage": (asset["tokens_owned"] / asset["total_tokens"]) * 100
            }
            for asset in sorted_assets[:3]
        ]
    
    def _calculate_average_hold_period(self, portfolio_data: List[Dict[str, Any]]) -> float:
        """
        Calculate average holding period for assets
        
        Args:
            portfolio_data: List of asset data
            
        Returns:
            Average hold period in days
        """
        total_days = 0
        current_date = datetime.now()
        
        for asset in portfolio_data:
            purchase_date = datetime.fromisoformat(asset["purchase_date"])
            hold_period = (current_date - purchase_date).days
            total_days += hold_period
        
        return total_days / len(portfolio_data) if portfolio_data else 0
    
    def _generate_risk_recommendations(self, risk_level: str, portfolio_data: List[Dict[str, Any]]) -> List[str]:
        """
        Generate risk management recommendations
        
        Args:
            risk_level: Current risk level
            portfolio_data: Portfolio data
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        if risk_level in ["high", "very_high"]:
            recommendations.append("Consider diversifying across more property types")
            recommendations.append("Reduce concentration in single assets")
            
        asset_types = set(asset["type"] for asset in portfolio_data)
        if len(asset_types) < 3:
            recommendations.append("Add exposure to different property sectors")
        
        locations = set(asset["location"] for asset in portfolio_data)
        if len(locations) < 3:
            recommendations.append("Consider geographic diversification")
        
        if not recommendations:
            recommendations.append("Maintain current diversification strategy")
            recommendations.append("Monitor market conditions for opportunities")
        
        return recommendations
    
    def _empty_metrics(self) -> Dict[str, Any]:
        """Return empty metrics when no data is available"""
        return {
            "total_value": 0,
            "total_invested": 0,
            "total_return": 0,
            "roi_percentage": 0,
            "asset_count": 0,
            "diversification_score": 0,
            "daily_change": 0,
            "weekly_change": 0,
            "monthly_change": 0,
            "ytd_change": 0,
            "annualized_return": 0,
            "income_generating": 0,
            "appreciation_assets": 0,
            "liquid_assets": 0,
            "average_hold_period": 0
        }