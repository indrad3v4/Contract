"""
Get Hot Asset Use Case - Clean Architecture Layer 1
Business logic for retrieving hot asset data with IFC viewer integration
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class GetHotAssetUseCase:
    """Use case for retrieving hot asset data with 3D model viewer"""
    
    def __init__(self, bim_repository=None, ifc_viewer_gateway=None):
        self.bim_repository = bim_repository
        self.ifc_viewer_gateway = ifc_viewer_gateway
    
    def execute(self) -> Dict[str, Any]:
        """
        Execute hot asset retrieval with viewer integration
        
        Returns:
            Hot asset data including viewer URL
        """
        try:
            # Get the latest uploaded model
            if self.bim_repository:
                latest_model = self.bim_repository.get_latest_model()
                
                if latest_model and self.ifc_viewer_gateway:
                    # Get model file path
                    model_id = latest_model["model_id"]
                    file_path = latest_model["file_path"]
                    
                    # Prepare viewer data
                    viewer_data = self.ifc_viewer_gateway.prepare_viewer_data(model_id, file_path)
                    
                    # Extract building name from model info
                    building_name = viewer_data["model_info"].get("building_name", "Real Estate Asset")
                    project_name = viewer_data["model_info"].get("project_name", "Property Investment")
                    
                    # Calculate ROI based on model complexity and size
                    element_count = viewer_data["model_info"].get("element_count", 0)
                    file_size = viewer_data["model_info"].get("file_size", 0)
                    
                    # ROI calculation based on model characteristics
                    base_roi = 12.0
                    complexity_bonus = min(element_count / 100, 5.0)  # Up to 5% bonus
                    size_bonus = min(file_size / (1024 * 1024), 3.0)  # Up to 3% bonus for larger models
                    calculated_roi = base_roi + complexity_bonus + size_bonus
                    
                    return {
                        "success": True,
                        "name": building_name,
                        "project_name": project_name,
                        "roi": round(calculated_roi, 1),
                        "viewer_url": viewer_data["viewer_url"],
                        "model_id": model_id,
                        "element_count": element_count,
                        "file_size_mb": round(file_size / (1024 * 1024), 2),
                        "schema": viewer_data["model_info"].get("schema", "IFC2X3"),
                        "bounds": viewer_data["bounds"],
                        "viewer_config": viewer_data["viewer_config"]
                    }
            
            # Fallback for when no IFC model is available
            return {
                "success": False,
                "name": "Ithaca Village",
                "roi": 14.1,
                "viewer_url": None,
                "message": "No 3D model available. Upload an IFC file to view the building model."
            }
            
        except Exception as e:
            logger.error(f"Error in GetHotAssetUseCase: {e}")
            return {
                "success": False,
                "name": "Real Estate Asset",
                "roi": 14.1,
                "viewer_url": None,
                "error": str(e)
            }
    
    def get_asset_details(self, model_id: str) -> Dict[str, Any]:
        """
        Get detailed asset information for a specific model
        
        Args:
            model_id: Model identifier
            
        Returns:
            Detailed asset information
        """
        try:
            if not self.bim_repository:
                raise ValueError("BIM repository not configured")
            
            # Get model metadata
            metadata = self.bim_repository.get_model_metadata(model_id)
            if not metadata:
                raise ValueError(f"Model {model_id} not found")
            
            # Get viewer data
            file_path = metadata["file_path"]
            viewer_data = self.ifc_viewer_gateway.prepare_viewer_data(model_id, file_path)
            
            # Calculate investment metrics
            element_count = viewer_data["model_info"].get("element_count", 0)
            file_size = viewer_data["model_info"].get("file_size", 0)
            
            # Estimated property value based on model complexity
            base_value = 2500000  # Base value in USD
            complexity_multiplier = 1 + (element_count / 1000)  # Increase value with complexity
            estimated_value = int(base_value * complexity_multiplier)
            
            # Token economics
            token_supply = 100000
            token_price = estimated_value / token_supply
            
            return {
                "success": True,
                "model_id": model_id,
                "asset_details": {
                    "name": viewer_data["model_info"].get("building_name", "Real Estate Asset"),
                    "project_name": viewer_data["model_info"].get("project_name", "Property Investment"),
                    "estimated_value": estimated_value,
                    "token_supply": token_supply,
                    "token_price": round(token_price, 2),
                    "element_count": element_count,
                    "file_size_mb": round(file_size / (1024 * 1024), 2),
                    "schema": viewer_data["model_info"].get("schema", "IFC2X3"),
                    "upload_date": metadata.get("upload_timestamp")
                },
                "viewer_data": viewer_data
            }
            
        except Exception as e:
            logger.error(f"Error getting asset details for {model_id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }