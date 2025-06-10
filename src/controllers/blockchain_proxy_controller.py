"""
Blockchain Proxy Controller for DAODISEO Platform
Handles RPC proxy requests to bypass CORS limitations
"""

import logging
import requests
import json
from flask import Blueprint, request, jsonify
from src.security_utils import secure_endpoint

logger = logging.getLogger(__name__)

blockchain_proxy_bp = Blueprint('blockchain_proxy', __name__, url_prefix='/api/blockchain-proxy')

@blockchain_proxy_bp.route('/rpc', methods=['POST', 'OPTIONS'])
@secure_endpoint
def rpc_proxy():
    """
    Proxy blockchain RPC requests to bypass CORS restrictions
    This allows frontend applications to interact with blockchain nodes
    """
    if request.method == 'OPTIONS':
        # Handle preflight CORS request
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response
    
    try:
        # Get the RPC request data
        rpc_data = request.get_json()
        if not rpc_data:
            return jsonify({"error": "No RPC data provided"}), 400
        
        # Validate RPC request structure
        required_fields = ["jsonrpc", "method", "id"]
        for field in required_fields:
            if field not in rpc_data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Blockchain RPC endpoints
        rpc_endpoints = [
            "https://testnet-rpc.daodiseo.chaintools.tech",
            "https://rpc.odiseotestnet.chaintools.tech",
            "https://testnet-rpc.odiseo.nodeshub.online"
        ]
        
        logger.debug(f"Proxying RPC request: {rpc_data.get('method')}")
        
        # Try each RPC endpoint until one succeeds
        last_error = None
        for rpc_url in rpc_endpoints:
            try:
                logger.debug(f"Attempting RPC call to: {rpc_url}")
                
                # Make the RPC request
                response = requests.post(
                    rpc_url,
                    json=rpc_data,
                    headers={
                        'Content-Type': 'application/json',
                        'User-Agent': 'DAODISEO-Platform/1.0'
                    },
                    timeout=30
                )
                
                # Check if request was successful
                if response.status_code == 200:
                    result = response.json()
                    logger.debug(f"Successful RPC response from {rpc_url}")
                    
                    # Add CORS headers to response
                    json_response = jsonify(result)
                    json_response.headers.add('Access-Control-Allow-Origin', '*')
                    return json_response
                
                else:
                    logger.warning(f"RPC endpoint {rpc_url} returned {response.status_code}")
                    last_error = f"HTTP {response.status_code}: {response.text}"
                    
            except requests.RequestException as e:
                logger.warning(f"RPC endpoint {rpc_url} failed: {str(e)}")
                last_error = str(e)
                continue
        
        # All endpoints failed
        logger.error(f"All RPC endpoints failed. Last error: {last_error}")
        return jsonify({
            "error": "All blockchain RPC endpoints are currently unavailable",
            "details": last_error
        }), 503
        
    except Exception as e:
        logger.error(f"RPC proxy error: {str(e)}", exc_info=True)
        return jsonify({"error": f"Proxy error: {str(e)}"}), 500

@blockchain_proxy_bp.route('/broadcast', methods=['POST', 'OPTIONS'])
@secure_endpoint
def broadcast_proxy():
    """
    Proxy transaction broadcast requests with proper format handling
    """
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response
    
    try:
        # Get transaction data
        tx_data = request.get_json()
        if not tx_data:
            return jsonify({"error": "No transaction data provided"}), 400
        
        logger.debug(f"Proxying transaction broadcast: {json.dumps(tx_data, indent=2)}")
        
        # Try REST API endpoints first (more reliable for transactions)
        rest_endpoints = [
            "https://testnet-api.daodiseo.chaintools.tech/txs",
            "https://api.odiseotestnet.chaintools.tech/txs",
            "https://testnet-api.odiseo.nodeshub.online/txs"
        ]
        
        # Try RPC endpoints as fallback
        rpc_endpoints = [
            "https://testnet-rpc.daodiseo.chaintools.tech/broadcast_tx_sync",
            "https://rpc.odiseotestnet.chaintools.tech/broadcast_tx_sync",
            "https://testnet-rpc.odiseo.nodeshub.online/broadcast_tx_sync"
        ]
        
        # First try REST API endpoints
        for endpoint in rest_endpoints:
            try:
                logger.debug(f"Attempting broadcast to REST endpoint: {endpoint}")
                
                response = requests.post(
                    endpoint,
                    json=tx_data,
                    headers={
                        'Content-Type': 'application/json',
                        'User-Agent': 'DAODISEO-Platform/1.0'
                    },
                    timeout=30
                )
                
                if response.status_code in [200, 201]:
                    result = response.json()
                    logger.info(f"Transaction broadcast successful via {endpoint}")
                    
                    json_response = jsonify(result)
                    json_response.headers.add('Access-Control-Allow-Origin', '*')
                    return json_response
                
                else:
                    logger.warning(f"REST endpoint {endpoint} returned {response.status_code}: {response.text}")
                    
            except requests.RequestException as e:
                logger.warning(f"REST endpoint {endpoint} failed: {str(e)}")
                continue
        
        # Try RPC endpoints as fallback
        for endpoint in rpc_endpoints:
            try:
                logger.debug(f"Attempting broadcast to RPC endpoint: {endpoint}")
                
                # Convert transaction to RPC format if needed
                rpc_data = {
                    "jsonrpc": "2.0",
                    "method": "broadcast_tx_sync",
                    "params": {
                        "tx": tx_data.get("tx", tx_data)
                    },
                    "id": 1
                }
                
                response = requests.post(
                    endpoint,
                    json=rpc_data,
                    headers={
                        'Content-Type': 'application/json',
                        'User-Agent': 'DAODISEO-Platform/1.0'
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"Transaction broadcast successful via RPC {endpoint}")
                    
                    json_response = jsonify(result)
                    json_response.headers.add('Access-Control-Allow-Origin', '*')
                    return json_response
                
                else:
                    logger.warning(f"RPC endpoint {endpoint} returned {response.status_code}: {response.text}")
                    
            except requests.RequestException as e:
                logger.warning(f"RPC endpoint {endpoint} failed: {str(e)}")
                continue
        
        # All endpoints failed
        return jsonify({
            "error": "All blockchain endpoints are currently unavailable for transaction broadcasting",
            "suggestion": "Please try again in a few moments or contact support"
        }), 503
        
    except Exception as e:
        logger.error(f"Broadcast proxy error: {str(e)}", exc_info=True)
        return jsonify({"error": f"Broadcast proxy error: {str(e)}"}), 500

@blockchain_proxy_bp.route('/query', methods=['POST', 'OPTIONS'])
@secure_endpoint
def query_proxy():
    """
    Proxy blockchain query requests (account info, balances, etc.)
    """
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response
    
    try:
        query_data = request.get_json()
        if not query_data:
            return jsonify({"error": "No query data provided"}), 400
        
        # Extract query parameters
        query_path = query_data.get("path", "")
        query_params = query_data.get("params", {})
        
        logger.debug(f"Proxying blockchain query: {query_path}")
        
        # REST API endpoints for queries
        api_endpoints = [
            "https://testnet-api.daodiseo.chaintools.tech",
            "https://api.odiseotestnet.chaintools.tech",
            "https://testnet-api.odiseo.nodeshub.online"
        ]
        
        for base_url in api_endpoints:
            try:
                full_url = f"{base_url}/{query_path.lstrip('/')}"
                logger.debug(f"Querying: {full_url}")
                
                response = requests.get(
                    full_url,
                    params=query_params,
                    headers={
                        'Content-Type': 'application/json',
                        'User-Agent': 'DAODISEO-Platform/1.0'
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.debug(f"Query successful via {base_url}")
                    
                    json_response = jsonify(result)
                    json_response.headers.add('Access-Control-Allow-Origin', '*')
                    return json_response
                
                else:
                    logger.warning(f"Query endpoint {base_url} returned {response.status_code}")
                    
            except requests.RequestException as e:
                logger.warning(f"Query endpoint {base_url} failed: {str(e)}")
                continue
        
        return jsonify({
            "error": "All blockchain query endpoints are currently unavailable"
        }), 503
        
    except Exception as e:
        logger.error(f"Query proxy error: {str(e)}", exc_info=True)
        return jsonify({"error": f"Query proxy error: {str(e)}"}), 500

# Health check for proxy service
@blockchain_proxy_bp.route('/health', methods=['GET'])
def proxy_health():
    """Check the health of blockchain proxy service"""
    try:
        # Test connectivity to at least one endpoint
        test_url = "https://testnet-api.daodiseo.chaintools.tech/cosmos/base/tendermint/v1beta1/node_info"
        response = requests.get(test_url, timeout=10)
        
        if response.status_code == 200:
            return jsonify({
                "status": "healthy",
                "message": "Blockchain proxy service is operational",
                "endpoints_available": True
            })
        else:
            return jsonify({
                "status": "degraded", 
                "message": "Some blockchain endpoints may be unavailable",
                "endpoints_available": False
            }), 503
            
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "message": f"Blockchain proxy service error: {str(e)}",
            "endpoints_available": False
        }), 503