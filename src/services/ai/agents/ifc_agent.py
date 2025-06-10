"""
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
