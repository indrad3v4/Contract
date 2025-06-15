"""
Tokenize Property Use Case - Clean Architecture Layer 1
Application business rule for property tokenization on blockchain
"""

from typing import Dict, Any
from datetime import datetime
from src.layer0_entities.property import RealEstateProperty, PropertyStatus
from src.layer2_interface_adapters.gateways.blockchain_gateway import BlockchainGatewayInterface


class TokenizePropertyUseCase:
    """Use case for tokenizing real estate properties on blockchain"""
    
    def __init__(self, blockchain_gateway: BlockchainGatewayInterface = None, property_repository=None):
        from src.layer2_interface_adapters.gateways.blockchain_gateway import BlockchainGateway
        self.blockchain_gateway = blockchain_gateway or BlockchainGateway()
        self.property_repository = property_repository
    
    def execute(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute property tokenization process
        
        Args:
            property_data: Property information for tokenization
            
        Returns:
            Dict containing tokenization results
        """
        try:
            # Validate input data
            validation_result = self._validate_property_data(property_data)
            if not validation_result["valid"]:
                return {
                    "success": False,
                    "error": validation_result["error"],
                    "step": "validation"
                }
            
            # Create property entity from data
            property_entity = self._create_property_entity(property_data)
            
            # Check if property can be tokenized
            if not property_entity.can_be_tokenized():
                return {
                    "success": False,
                    "error": "Property does not meet tokenization requirements",
                    "step": "eligibility_check"
                }
            
            # Generate smart contract parameters
            contract_params = self._generate_contract_parameters(property_entity, property_data)
            
            # Deploy smart contract (if blockchain gateway is available)
            if self.blockchain_gateway:
                deployment_result = self.blockchain_gateway.deploy_smart_contract(contract_params)
                if not deployment_result.get("success"):
                    return {
                        "success": False,
                        "error": f"Contract deployment failed: {deployment_result.get('error')}",
                        "step": "contract_deployment"
                    }
                
                # Update property status
                property_entity.status = PropertyStatus.TOKENIZED
                
                return {
                    "success": True,
                    "property_id": property_entity.id,
                    "contract_address": deployment_result.get("contract_address"),
                    "transaction_hash": deployment_result.get("transaction_hash"),
                    "block_height": deployment_result.get("block_height"),
                    "token_symbol": contract_params["token_symbol"],
                    "total_tokens": contract_params["total_supply"],
                    "token_price": contract_params["initial_price"],
                    "tokenization_timestamp": datetime.now().isoformat(),
                    "step": "completed"
                }
            else:
                # Mock response when blockchain gateway is not available
                return self._mock_tokenization_response(property_entity, contract_params)
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "step": "execution_error"
            }
    
    def _validate_property_data(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate property data for tokenization
        
        Args:
            property_data: Property data to validate
            
        Returns:
            Validation result
        """
        required_fields = [
            "name", "property_type", "address", "city", "state", "zip_code", "country",
            "current_valuation", "total_tokens", "token_price"
        ]
        
        for field in required_fields:
            if field not in property_data or not property_data[field]:
                return {
                    "valid": False,
                    "error": f"Missing required field: {field}"
                }
        
        # Validate financial data
        try:
            valuation = float(property_data["current_valuation"])
            total_tokens = int(property_data["total_tokens"])
            token_price = float(property_data["token_price"])
            
            if valuation <= 0:
                return {"valid": False, "error": "Property valuation must be positive"}
            
            if total_tokens <= 0:
                return {"valid": False, "error": "Total tokens must be positive"}
            
            if token_price <= 0:
                return {"valid": False, "error": "Token price must be positive"}
            
            # Check if token math makes sense
            expected_total = total_tokens * token_price
            if abs(expected_total - valuation) / valuation > 0.1:  # 10% tolerance
                return {
                    "valid": False,
                    "error": f"Token math inconsistent: {total_tokens} × ${token_price} = ${expected_total}, but valuation is ${valuation}"
                }
                
        except (ValueError, TypeError):
            return {"valid": False, "error": "Invalid numeric values in financial data"}
        
        return {"valid": True}
    
    def _create_property_entity(self, property_data: Dict[str, Any]) -> RealEstateProperty:
        """
        Create property entity from input data
        
        Args:
            property_data: Property data
            
        Returns:
            RealEstateProperty entity
        """
        from src.layer0_entities.property import PropertyType, Location, PropertyDetails, FinancialData
        
        # Create location
        location = Location(
            address=property_data["address"],
            city=property_data["city"],
            state=property_data["state"],
            zip_code=property_data["zip_code"],
            country=property_data["country"],
            coordinates=property_data.get("coordinates")
        )
        
        # Create property details
        details = PropertyDetails(
            size_sqft=float(property_data.get("size_sqft", 0)),
            bedrooms=int(property_data.get("bedrooms", 0)),
            bathrooms=float(property_data.get("bathrooms", 0)),
            year_built=property_data.get("year_built"),
            lot_size_sqft=property_data.get("lot_size_sqft"),
            features=property_data.get("features", []),
            amenities=property_data.get("amenities", [])
        )
        
        # Create financial data
        financials = FinancialData(
            purchase_price=float(property_data.get("purchase_price", 0)),
            current_valuation=float(property_data["current_valuation"]),
            token_price=float(property_data["token_price"]),
            total_tokens=int(property_data["total_tokens"]),
            available_tokens=int(property_data.get("available_tokens", property_data["total_tokens"])),
            annual_return=property_data.get("annual_return"),
            rental_income=property_data.get("rental_income"),
            expenses=property_data.get("expenses")
        )
        
        # Create property entity
        property_entity = RealEstateProperty(
            name=property_data["name"],
            property_type=PropertyType(property_data["property_type"]),
            location=location,
            details=details,
            financials=financials,
            bim_data=property_data.get("bim_data"),
            status=PropertyStatus.DRAFT
        )
        
        return property_entity
    
    def _generate_contract_parameters(self, property_entity: RealEstateProperty, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate smart contract deployment parameters
        
        Args:
            property_entity: Property entity
            property_data: Original property data
            
        Returns:
            Contract parameters
        """
        # Generate token symbol from property name
        token_symbol = self._generate_token_symbol(property_entity.name)
        
        return {
            "contract_type": "PropertyToken",
            "token_name": f"{property_entity.name} Token",
            "token_symbol": token_symbol,
            "total_supply": property_entity.financials.total_tokens,
            "initial_price": property_entity.financials.token_price,
            "property_address": property_entity.location.address,
            "property_valuation": property_entity.financials.current_valuation,
            "metadata": {
                "property_type": property_entity.property_type.value,
                "size_sqft": property_entity.details.size_sqft,
                "year_built": property_entity.details.year_built,
                "location": property_entity.location.to_dict(),
                "tokenization_date": datetime.now().isoformat()
            },
            "governance": {
                "voting_enabled": True,
                "proposal_threshold": 0.01,  # 1% of tokens needed to create proposal
                "voting_period": 604800,  # 7 days in seconds
            }
        }
    
    def _generate_token_symbol(self, property_name: str) -> str:
        """
        Generate token symbol from property name
        
        Args:
            property_name: Name of the property
            
        Returns:
            Token symbol (3-5 characters)
        """
        # Clean and extract letters
        import re
        clean_name = re.sub(r'[^A-Za-z\s]', '', property_name)
        words = clean_name.split()
        
        if len(words) >= 2:
            # Use first 2-3 letters of first two words
            symbol = (words[0][:2] + words[1][:2]).upper()
        else:
            # Use first 4 letters of the name
            symbol = clean_name[:4].upper()
        
        # Ensure minimum length
        if len(symbol) < 3:
            symbol = (symbol + "TOK")[:4]
        
        return symbol
    
    def _mock_tokenization_response(self, property_entity: RealEstateProperty, contract_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate mock tokenization response when blockchain is not available
        
        Args:
            property_entity: Property entity
            contract_params: Contract parameters
            
        Returns:
            Mock tokenization response
        """
        import uuid
        
        return {
            "success": True,
            "property_id": property_entity.id,
            "contract_address": f"odiseo1mock{uuid.uuid4().hex[:8]}",
            "transaction_hash": f"mock_tx_{uuid.uuid4().hex[:16]}",
            "block_height": 3483100,
            "token_symbol": contract_params["token_symbol"],
            "total_tokens": contract_params["total_supply"],
            "token_price": contract_params["initial_price"],
            "tokenization_timestamp": datetime.now().isoformat(),
            "step": "completed",
            "note": "Mock tokenization - blockchain gateway not configured"
        }