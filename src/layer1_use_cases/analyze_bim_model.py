"""
Analyze BIM Model Use Case - Clean Architecture Layer 1
Application business rule for AI-powered BIM model analysis
"""

from typing import Dict, Any, List
from datetime import datetime
from src.layer0_entities.bim_model import AIAnalysis
from src.layer2_interface_adapters.gateways.ai_gateway import AIGatewayInterface

class AnalyzeBIMModelUseCase:
    """Use case for AI analysis of BIM models"""
    
    def __init__(self, ai_gateway: AIGatewayInterface = None, bim_repository=None):
        # In full implementation, these would be injected
        from src.layer2_interface_adapters.gateways.ai_gateway import OpenAIGateway
        self.ai_gateway = ai_gateway or OpenAIGateway()
        self.bim_repository = bim_repository
    
    def execute(self, model_id: str) -> Dict[str, Any]:
        """
        Execute AI analysis of a BIM model
        
        Args:
            model_id: Unique identifier of the BIM model
            
        Returns:
            Dict containing analysis results and insights
        """
        # Get model data from repository
        model_data = self._get_model_data(model_id)
        
        if not model_data:
            raise ValueError(f"BIM model {model_id} not found")
        
        # Perform AI analysis
        analysis_result = self.ai_gateway.analyze_bim_model(model_data)
        
        # Create AI analysis entity
        ai_analysis = self._create_ai_analysis(analysis_result)
        
        # Store analysis results
        self._store_analysis(model_id, ai_analysis)
        
        # Return formatted results
        return self._format_analysis_results(model_id, ai_analysis, analysis_result)
    
    def _get_model_data(self, model_id: str) -> Dict[str, Any]:
        """Get BIM model data from repository"""
        # In real implementation, this would query the database
        # For now, return mock data based on model_id
        
        mock_models = {
            "bim_001": {
                "id": "bim_001",
                "filename": "residential_complex.ifc",
                "schema_version": "IFC4",
                "element_count": 1245,
                "file_size": "15.2 MB",
                "elements_by_type": {
                    "walls": 245,
                    "doors": 48,
                    "windows": 96,
                    "slabs": 12,
                    "columns": 32,
                    "beams": 78,
                    "spaces": 24,
                    "other": 710
                },
                "site_name": "Ithaca Village",
                "building_name": "Residential Complex A"
            },
            "bim_002": {
                "id": "bim_002", 
                "filename": "office_building.ifc",
                "schema_version": "IFC4",
                "element_count": 2890,
                "file_size": "28.7 MB",
                "elements_by_type": {
                    "walls": 456,
                    "doors": 89,
                    "windows": 178,
                    "slabs": 25,
                    "columns": 67,
                    "beams": 123,
                    "spaces": 45,
                    "other": 1907
                },
                "site_name": "Downtown Plaza",
                "building_name": "Office Tower"
            }
        }
        
        return mock_models.get(model_id, mock_models["bim_001"])
    
    def _create_ai_analysis(self, analysis_result: Dict[str, Any]) -> AIAnalysis:
        """Create AI analysis entity from analysis results"""
        return AIAnalysis(
            timestamp=datetime.now(),
            analysis_text=self._generate_analysis_summary(analysis_result),
            complexity_score=analysis_result.get("complexity_score", 0),
            quality_score=analysis_result.get("quality_score", 0),
            sustainability_score=analysis_result.get("sustainability_score", 0),
            cost_efficiency_score=analysis_result.get("cost_efficiency_score", 0),
            detected_issues=analysis_result.get("detected_issues", []),
            recommendations=analysis_result.get("recommendations", [])
        )
    
    def _generate_analysis_summary(self, analysis_result: Dict[str, Any]) -> str:
        """Generate a comprehensive analysis summary"""
        complexity = analysis_result.get("complexity_score", 0)
        quality = analysis_result.get("quality_score", 0)
        sustainability = analysis_result.get("sustainability_score", 0)
        cost_efficiency = analysis_result.get("cost_efficiency_score", 0)
        
        # Calculate overall score
        overall_score = (complexity + quality + sustainability + cost_efficiency) / 4
        
        # Generate summary based on scores
        summary_parts = []
        
        # Overall assessment
        if overall_score >= 8:
            summary_parts.append("This BIM model demonstrates excellent architectural design and documentation quality.")
        elif overall_score >= 6:
            summary_parts.append("This BIM model shows good architectural design with some areas for improvement.")
        else:
            summary_parts.append("This BIM model requires significant improvements in design and documentation.")
        
        # Specific insights
        if complexity > 8:
            summary_parts.append("The design exhibits high complexity with sophisticated architectural elements.")
        elif complexity < 5:
            summary_parts.append("The design is relatively simple and straightforward.")
        
        if quality > 8:
            summary_parts.append("Model quality is excellent with comprehensive element definitions.")
        elif quality < 6:
            summary_parts.append("Model quality could be improved with more detailed element specifications.")
        
        if sustainability > 7:
            summary_parts.append("The design incorporates good sustainability principles.")
        elif sustainability < 5:
            summary_parts.append("Consider implementing more sustainable design features.")
        
        if cost_efficiency > 7:
            summary_parts.append("The design demonstrates good cost efficiency.")
        elif cost_efficiency < 5:
            summary_parts.append("Review design for potential cost optimization opportunities.")
        
        return " ".join(summary_parts)
    
    def _store_analysis(self, model_id: str, ai_analysis: AIAnalysis) -> None:
        """Store analysis results in repository"""
        # In real implementation, this would save to database
        # For now, just log the storage
        pass
    
    def _format_analysis_results(self, model_id: str, ai_analysis: AIAnalysis, raw_results: Dict[str, Any]) -> Dict[str, Any]:
        """Format analysis results for API response"""
        return {
            "model_id": model_id,
            "analysis_status": "completed",
            "timestamp": ai_analysis.timestamp.isoformat(),
            "overall_score": round((
                ai_analysis.complexity_score + 
                ai_analysis.quality_score + 
                ai_analysis.sustainability_score + 
                ai_analysis.cost_efficiency_score
            ) / 4, 1),
            "scores": {
                "complexity": ai_analysis.complexity_score,
                "quality": ai_analysis.quality_score,
                "sustainability": ai_analysis.sustainability_score,
                "cost_efficiency": ai_analysis.cost_efficiency_score
            },
            "analysis_summary": ai_analysis.analysis_text,
            "recommendations": ai_analysis.recommendations,
            "detected_issues": ai_analysis.detected_issues,
            "confidence_level": raw_results.get("analysis_confidence", 0.85),
            "detailed_insights": self._generate_detailed_insights(ai_analysis),
            "next_steps": self._suggest_next_steps(ai_analysis)
        }
    
    def _generate_detailed_insights(self, ai_analysis: AIAnalysis) -> Dict[str, Any]:
        """Generate detailed insights from analysis"""
        return {
            "design_complexity": {
                "score": ai_analysis.complexity_score,
                "interpretation": self._interpret_complexity_score(ai_analysis.complexity_score),
                "impact": "Higher complexity may increase construction costs but can provide better functionality"
            },
            "model_quality": {
                "score": ai_analysis.quality_score,
                "interpretation": self._interpret_quality_score(ai_analysis.quality_score),
                "impact": "Higher quality models reduce construction errors and improve coordination"
            },
            "sustainability": {
                "score": ai_analysis.sustainability_score,
                "interpretation": self._interpret_sustainability_score(ai_analysis.sustainability_score),
                "impact": "Better sustainability scores can reduce operating costs and increase property value"
            },
            "cost_efficiency": {
                "score": ai_analysis.cost_efficiency_score,
                "interpretation": self._interpret_cost_efficiency_score(ai_analysis.cost_efficiency_score),
                "impact": "Higher cost efficiency improves investment returns and market competitiveness"
            }
        }
    
    def _suggest_next_steps(self, ai_analysis: AIAnalysis) -> List[str]:
        """Suggest next steps based on analysis"""
        next_steps = []
        
        if ai_analysis.quality_score < 7:
            next_steps.append("Review and enhance model completeness")
        
        if ai_analysis.sustainability_score < 6:
            next_steps.append("Incorporate additional sustainable design features")
        
        if ai_analysis.cost_efficiency_score < 6:
            next_steps.append("Evaluate design for cost optimization opportunities")
        
        if len(ai_analysis.detected_issues) > 3:
            next_steps.append("Address identified model issues before construction")
        
        if not next_steps:
            next_steps.append("Proceed with detailed design development")
            next_steps.append("Begin construction documentation phase")
        
        return next_steps
    
    def _interpret_complexity_score(self, score: float) -> str:
        """Interpret complexity score"""
        if score >= 8:
            return "Highly complex architectural design"
        elif score >= 6:
            return "Moderately complex design"
        elif score >= 4:
            return "Simple to moderate complexity"
        else:
            return "Low complexity design"
    
    def _interpret_quality_score(self, score: float) -> str:
        """Interpret quality score"""
        if score >= 8:
            return "Excellent model quality and completeness"
        elif score >= 6:
            return "Good model quality with minor gaps"
        elif score >= 4:
            return "Adequate quality, improvements needed"
        else:
            return "Poor quality, significant improvements required"
    
    def _interpret_sustainability_score(self, score: float) -> str:
        """Interpret sustainability score"""
        if score >= 8:
            return "Excellent sustainability features"
        elif score >= 6:
            return "Good sustainability considerations"
        elif score >= 4:
            return "Basic sustainability features"
        else:
            return "Limited sustainability considerations"
    
    def _interpret_cost_efficiency_score(self, score: float) -> str:
        """Interpret cost efficiency score"""
        if score >= 8:
            return "Highly cost-efficient design"
        elif score >= 6:
            return "Good cost efficiency"
        elif score >= 4:
            return "Moderate cost efficiency"
        else:
            return "Poor cost efficiency, optimization needed"