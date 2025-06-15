"""
Get Network Status Use Case - Clean Architecture Layer 1
Application business rule for retrieving blockchain network status
"""

from typing import Dict, Any
from src.layer2_interface_adapters.gateways.blockchain_gateway import BlockchainGatewayInterface

class GetNetworkStatusUseCase:
    """Use case for getting current network status and health"""
    
    def __init__(self, blockchain_gateway: BlockchainGatewayInterface = None):
        from src.layer2_interface_adapters.gateways.blockchain_gateway import BlockchainGateway
        self.blockchain_gateway = blockchain_gateway or BlockchainGateway()
    
    def execute(self) -> Dict[str, Any]:
        """
        Execute the use case to get network status
        
        Returns:
            Dict containing network health and status information
        """
        # Get network health from blockchain gateway
        network_data = self.blockchain_gateway.get_network_health()
        
        # Apply business rules for status interpretation
        status = self._interpret_network_status(network_data)
        
        return {
            "network_name": network_data.get("network_name", "Unknown"),
            "block_height": network_data.get("block_height", 0),
            "health_status": status,
            "validator_count": network_data.get("validator_count", 0),
            "active_validators": network_data.get("active_validators", 0),
            "catching_up": network_data.get("catching_up", False),
            "last_update": network_data.get("block_time", ""),
            "network_healthy": status == "healthy"
        }
    
    def _interpret_network_status(self, network_data: Dict[str, Any]) -> str:
        """Apply business logic to interpret network status"""
        catching_up = network_data.get("catching_up", False)
        block_height = network_data.get("block_height", 0)
        
        if catching_up:
            return "syncing"
        elif block_height == 0:
            return "offline"
        else:
            return "healthy"