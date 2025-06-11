"""Combined blockchain controllers"""

# ==== File: src/controllers/account_controller.py ====
import logging
from flask import Blueprint, jsonify, request
from src.gateways.blockchain_gateways import KeplerGateway
from src.gateways.blockchain_gateways import PingPubGateway

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create blueprint
account_bp = Blueprint("account", __name__, url_prefix="/api")

# Initialize kepler gateway with network configuration
network_config = {
    "chain_id": "ithaca-1",  # Updated to match the testnet chain ID
    "rpc_url": "https://odiseo.test.rpc.nodeshub.online",
    "api_url": "https://odiseo.test.api.nodeshub.online"
}
kepler_gateway = KeplerGateway(network_config)

# Initialize the PingPub gateway for blockchain interactions
pingpub_gateway = PingPubGateway()


@account_bp.route("/account", methods=["GET"])
def get_account():
    """Get current user account information"""
    # Get wallet address from query parameters
    wallet_address = request.args.get("address", "")
    
    if not wallet_address:
        return jsonify({"error": "Wallet address is required"}), 400
    
    try:
        # Get real account information from the blockchain
        account_info = pingpub_gateway.get_account_info(wallet_address)
        
        # Add additional user information
        # TODO(DDS_TEAM): Replace with real database lookup for user profile
        account_info.update({
            "username": f"user_{wallet_address[:8]}",  # Generated username based on address
            "role": "user",
            "permissions": ["upload", "view"],
        })
        
        logger.debug(f"Returning account info for {wallet_address}: {account_info}")
        return jsonify(account_info)
    except Exception as e:
        logger.error(f"Error retrieving account info: {str(e)}")
        return jsonify({"error": f"Failed to retrieve account info: {str(e)}"}), 500


@account_bp.route("/account/wallet", methods=["POST"])
def connect_wallet():
    """Connect a wallet address to the user account"""
    try:
        data = request.json

        if not data or "address" not in data:
            return jsonify({"error": "Wallet address is required"}), 400

        address = data["address"]

        # Store the connected address locally (async cannot be used in Flask routes directly)
        kepler_gateway.connected_address = address
        logger.info(f"Wallet connected: {address}")

        # Get account info from blockchain
        try:
            # Get real account information from the blockchain
            account_info = pingpub_gateway.get_account_info(address)
            logger.debug(f"Retrieved account info: {account_info}")
        except Exception as account_error:
            logger.warning(f"Error retrieving account info: {str(account_error)}")
            account_info = {"address": address}
            
        # TODO(DDS_TEAM): Store connection in database with user profile

        return jsonify(
            {
                "success": True,
                "message": "Wallet connected successfully",
                "address": address,
                "account_info": account_info
            }
        )
    except Exception as e:
        logger.error(f"Error connecting wallet: {str(e)}")
        return jsonify({"error": str(e)}), 500


@account_bp.route("/network-config", methods=["GET"])
def get_network_config():
    """Get Cosmos network configuration for Keplr wallet integration"""
    try:
        # Get network configuration from the gateway
        config = kepler_gateway.get_network_config()
        logger.debug(f"Returning network config: {config}")
        return jsonify(config)
    except Exception as e:
        logger.error(f"Error getting network config: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ==== File: src/controllers/contract_controller.py ====
import logging
import json
from flask import Blueprint, jsonify, request
import os
from src.gateways.blockchain_gateways import MultiSigBlockchainGateway

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create blueprint
contract_bp = Blueprint("contract", __name__, url_prefix="/api")

# Path to JSON file storing contract data
CONTRACTS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "contracts.json"
)

# Ensure contracts file exists
if not os.path.exists(CONTRACTS_FILE):
    with open(CONTRACTS_FILE, "w") as f:
        json.dump([], f)


@contract_bp.route("/contracts", methods=["GET"])
def get_contracts():
    """Retrieve all contracts"""
    logger.debug("Fetching contracts")
    try:
        with open(CONTRACTS_FILE, "r") as f:
            contracts = json.load(f)
        return jsonify(contracts)
    except Exception as e:
        logger.error(f"Error fetching contracts: {str(e)}")
        return jsonify({"error": str(e)}), 500


@contract_bp.route("/contracts/<contract_id>", methods=["GET"])
def get_contract(contract_id):
    """Retrieve a specific contract by ID"""
    try:
        with open(CONTRACTS_FILE, "r") as f:
            contracts = json.load(f)

        contract = next((c for c in contracts if c.get("id") == contract_id), None)

        if not contract:
            return jsonify({"error": "Contract not found"}), 404

        return jsonify(contract)
    except Exception as e:
        logger.error(f"Error fetching contract {contract_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500


@contract_bp.route("/transactions/<transaction_id>/status", methods=["GET"])
def view_transaction_status(transaction_id):
    """Retrieve the status of a specific transaction"""
    try:
        # Initialize the gateway with test mode for now
        # In production, this would be properly configured
        gateway = MultiSigBlockchainGateway(test_mode=True)
        
        # Get the transaction status
        try:
            status = gateway.get_transaction_status(transaction_id)
            return jsonify(status)
        except ValueError as e:
            logger.error(f"Transaction not found: {str(e)}")
            return jsonify({"error": f"Transaction not found: {str(e)}"}), 404
        except Exception as e:
            logger.error(f"Error getting transaction status: {str(e)}")
            return jsonify({"error": f"Error getting transaction status: {str(e)}"}), 500
            
    except Exception as e:
        logger.error(f"Error initializing blockchain gateway: {str(e)}")
        return jsonify({"error": str(e)}), 500


@contract_bp.route("/contracts", methods=["POST"])
def create_contract():
    """Create a new contract"""
    try:
        contract_data = request.json

        if not contract_data:
            return jsonify({"error": "No contract data provided"}), 400

        with open(CONTRACTS_FILE, "r") as f:
            contracts = json.load(f)

        # Generate simple ID
        contract_id = str(len(contracts) + 1)
        contract_data["id"] = contract_id

        contracts.append(contract_data)

        with open(CONTRACTS_FILE, "w") as f:
            json.dump(contracts, f, indent=2)

        logger.debug(f"Contract created with ID: {contract_id}")
        return jsonify(contract_data), 201
    except Exception as e:
        logger.error(f"Error creating contract: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ==== File: src/controllers/blockchain_controller.py ====
"""
Blockchain Controller for handling blockchain-related API endpoints
"""

import os
import json
import logging
import hashlib
import time
from flask import Blueprint, request, jsonify, current_app, session, abort

from src.services.blockchain_service import BlockchainService
from src.security_utils import secure_endpoint, verify_wallet_ownership

# Set up logging
logger = logging.getLogger(__name__)

# Create blueprint
blockchain_bp = Blueprint('blockchain', __name__, url_prefix='/api/blockchain')

# Initialize services
blockchain_service = BlockchainService()

@blockchain_bp.route('/account', methods=['GET'])
@secure_endpoint
def get_account():
    """Get account information for a wallet address"""
    try:
        address = request.args.get('address')
        if not address:
            return jsonify({'error': 'Address parameter is required'}), 400
        
        # Security: Verify wallet ownership if not in debug mode
        # In production, this will reject requests for addresses not owned by the user
        if not current_app.debug:
            try:
                verify_wallet_ownership(address)
            except Exception as auth_error:
                logger.warning(f"Unauthorized wallet access attempt for address: {address}")
                return jsonify({'error': 'Unauthorized access to wallet data'}), 403
        
        # Get account information from the blockchain
        account_info = blockchain_service.pingpub_gateway.get_account_info(address)
        
        # Security: Log access timestamp
        logger.info(f"Account information retrieved for: {address} at {time.time()}")
        
        return jsonify(account_info), 200
    
    except Exception as e:
        logger.error(f"Error in get_account: {str(e)}")
        # Security: Don't expose detailed error message in production
        if current_app.debug:
            return jsonify({'error': str(e)}), 500
        else:
            return jsonify({'error': 'Failed to retrieve account information'}), 500

@blockchain_bp.route('/broadcast', methods=['POST'])
@secure_endpoint
def broadcast_transaction():
    """Broadcast a signed transaction to the blockchain"""
    try:
        # Security: Get and validate request data
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Security: Validate transaction format
        if not isinstance(data, dict):
            return jsonify({'error': 'Transaction data must be a JSON object'}), 400
            
        # Security: Basic transaction validation
        if 'tx' not in data:
            return jsonify({'error': 'Missing tx field in transaction data'}), 400
            
        tx_data = data.get('tx', {})
        if not tx_data.get('signatures'):
            return jsonify({'error': 'Missing signatures in transaction data'}), 400
        
        # Security: Check for valid sender address if available
        from_address = None
        try:
            # Try to extract sender address from transaction
            msgs = tx_data.get('msg', [])
            if msgs and len(msgs) > 0:
                from_address = msgs[0].get('value', {}).get('fromAddress') or msgs[0].get('value', {}).get('from_address')
                
                # Verify wallet ownership in production
                if from_address and not current_app.debug:
                    try:
                        verify_wallet_ownership(from_address)
                    except Exception:
                        logger.warning(f"Unauthorized transaction broadcast attempt for address: {from_address}")
                        return jsonify({'error': 'Unauthorized transaction broadcast'}), 403
        except Exception as e:
            logger.warning(f"Failed to extract sender address: {str(e)}")
            # Continue processing as this is just an additional security check
            
        # Security: Rate limiting for transaction broadcasts
        # Implemented via @secure_endpoint decorator
        
        # Broadcast the transaction
        result = blockchain_service.broadcast_signed_transaction(data)
        
        # Security: Enhanced logging
        tx_hash = result.get('transaction_hash')
        logger.info(f"Transaction broadcast: {tx_hash} by {from_address or 'unknown'} at {time.time()}")
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error in broadcast_transaction: {str(e)}")
        # Security: Don't expose internal errors in production
        if current_app.debug:
            return jsonify({'error': str(e)}), 500
        else:
            return jsonify({'error': 'Failed to broadcast transaction'}), 500

@blockchain_bp.route('/verify/<tx_hash>', methods=['GET'])
@secure_endpoint
def verify_transaction(tx_hash):
    """Verify a transaction on the blockchain with enhanced security"""
    try:
        # Security: Validate transaction hash format
        if not tx_hash or len(tx_hash) < 10:
            return jsonify({'error': 'Invalid transaction hash'}), 400
            
        # Get expected content hash if available
        content_hash = request.args.get('content_hash')
        user_address = request.args.get('address')
        
        # Create complete transaction data for enhanced verification
        transaction_data = {
            'transaction_hash': tx_hash,
            'content_hash': content_hash,
            'user_address': user_address
        }
        
        # Basic transaction verification
        result = blockchain_service.verify_transaction(tx_hash)
        
        # Enhanced security verification if content hash provided
        if content_hash:
            # Verify content hash matches transaction memo
            memo = result.get('status', {}).get('memo', '')
            
            # Try to extract memo data
            memo_data = {}
            try:
                # Try parsing as JSON
                memo_data = json.loads(memo)
            except:
                # Try legacy format (key:value|key:value)
                if '|' in memo and ':' in memo:
                    pairs = memo.split('|')
                    for pair in pairs:
                        if ':' in pair:
                            key, value = pair.split(':', 1)
                            memo_data[key.strip()] = value.strip()
                # Try simple format (id:hash:role)
                elif ':' in memo:
                    parts = memo.split(':')
                    if len(parts) >= 2:
                        memo_data['hash'] = parts[1]
            
            # Verify hash if found in memo data
            memo_hash = memo_data.get('hash')
            if memo_hash and memo_hash != content_hash:
                logger.warning(f"Content hash mismatch: {memo_hash} != {content_hash}")
                result['hash_verified'] = False
                result['security_warning'] = 'Content hash mismatch'
            else:
                result['hash_verified'] = bool(memo_hash and memo_hash == content_hash)
        
        # Security: Add verification timestamp
        result['verification_timestamp'] = time.time()
        
        # Security: Enhanced logging
        logger.info(f"Transaction verification: {tx_hash} at {time.time()}")
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error in verify_transaction: {str(e)}")
        # Security: Don't expose internal errors in production
        if current_app.debug:
            return jsonify({'error': str(e)}), 500
        else:
            return jsonify({'error': 'Failed to verify transaction'}, {'verified': False}), 500

@blockchain_bp.route('/stats', methods=['GET'])
@secure_endpoint
def get_blockchain_stats():
    """Get blockchain statistics for the dashboard"""
    try:
        # Get stats from blockchain service or use cached data
        stats = blockchain_service.get_dashboard_stats()
        
        # Security: Add timestamp for freshness verification
        stats['timestamp'] = time.time()
        
        return jsonify(stats), 200
        
    except Exception as e:
        logger.error(f"Error in get_blockchain_stats: {str(e)}")
        # Security: Don't expose internal errors in production
        if current_app.debug:
            return jsonify({'error': str(e)}), 500
        else:
            return jsonify({'error': 'Failed to retrieve blockchain statistics'}), 500

@blockchain_bp.route('/asset-distribution', methods=['GET'])
@secure_endpoint
def get_asset_distribution():
    """Get asset distribution data for dashboard charts"""
    try:
        # Get asset distribution from blockchain service
        distribution = blockchain_service.get_asset_distribution()
        
        # Security: Add timestamp for freshness verification
        distribution['timestamp'] = time.time()
        
        return jsonify(distribution), 200
        
    except Exception as e:
        logger.error(f"Error in get_asset_distribution: {str(e)}")
        # Security: Don't expose internal errors in production
        if current_app.debug:
            return jsonify({'error': str(e)}), 500
        else:
            return jsonify({'error': 'Failed to retrieve asset distribution data'}), 500

@blockchain_bp.route('/stakeholder-distribution', methods=['GET'])
@secure_endpoint
def get_stakeholder_distribution():
    """Get stakeholder distribution data for dashboard charts"""
    try:
        # Get stakeholder distribution from blockchain service
        distribution = blockchain_service.get_stakeholder_distribution()
        
        # Security: Add timestamp for freshness verification
        distribution['timestamp'] = time.time()
        
        return jsonify(distribution), 200
        
    except Exception as e:
        logger.error(f"Error in get_stakeholder_distribution: {str(e)}")
        # Security: Don't expose internal errors in production
        if current_app.debug:
            return jsonify({'error': str(e)}), 500
        else:
            return jsonify({'error': 'Failed to retrieve stakeholder distribution data'}), 500

@blockchain_bp.route('/validators', methods=['GET'])
@secure_endpoint
def get_validators():
    """Get list of active validators"""
    try:
        # Get validators with caching for rate limiting
        validators = blockchain_service.get_validators()
        
        # Security: Add timestamp for freshness verification
        response_data = {
            'validators': validators,
            'timestamp': time.time(),
            'count': len(validators)
        }
        
        return jsonify(response_data), 200
    
    except Exception as e:
        logger.error(f"Error in get_validators: {str(e)}")
        # Security: Don't expose internal errors in production
        if current_app.debug:
            return jsonify({'error': str(e)}), 500
        else:
            return jsonify({'error': 'Failed to retrieve validators'}), 500

@blockchain_bp.route('/prepare-upload', methods=['POST'])
@secure_endpoint
def prepare_upload():
    """Prepare a transaction for uploading an IFC file hash"""
    try:
        # Check if file and address are provided
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        user_address = request.form.get('address')
        if not user_address:
            return jsonify({'error': 'User address is required'}), 400
        
        # Security: Verify wallet ownership if not in debug mode
        if not current_app.debug:
            try:
                verify_wallet_ownership(user_address)
            except Exception as auth_error:
                logger.warning(f"Unauthorized file upload attempt for address: {user_address}")
                return jsonify({'error': 'Unauthorized wallet access'}), 403
        
        # Get file data
        file = request.files['file']
        
        # Security: Validate file extension
        if not file.filename or '.' not in file.filename:
            return jsonify({'error': 'Invalid filename'}), 400
            
        extension = file.filename.rsplit('.', 1)[1].lower()
        if extension not in ['ifc']:
            return jsonify({'error': 'Only IFC files are allowed'}), 400
        
        # Security: Limit file size (100MB)
        file_data = file.read()
        if len(file_data) > 100 * 1024 * 1024:  # 100MB
            return jsonify({'error': 'File too large (max 100MB)'}), 400
            
        # Security: Validate IFC file format
        try:
            from src.security_utils import validate_ifc_file
            validate_ifc_file(file_data)
        except ValueError as validation_error:
            logger.warning(f"Invalid IFC file uploaded: {str(validation_error)}")
            return jsonify({'error': f'Invalid IFC file: {str(validation_error)}'}), 400
        
        # Get metadata if provided
        metadata = {}
        if 'metadata' in request.form:
            try:
                metadata_str = request.form.get('metadata')
                # Security: Limit metadata size
                if len(metadata_str) > 10 * 1024:  # 10KB
                    return jsonify({'error': 'Metadata too large'}), 400
                    
                metadata = json.loads(metadata_str)
                
                # Security: Validate metadata structure
                if not isinstance(metadata, dict):
                    return jsonify({'error': 'Metadata must be a JSON object'}), 400
                    
            except json.JSONDecodeError:
                return jsonify({'error': 'Invalid metadata format'}), 400
        
        # Add filename and timestamp to metadata
        metadata['filename'] = file.filename
        metadata['upload_timestamp'] = time.time()
        metadata['file_size'] = len(file_data)
        
        # Security: Add hash verification to metadata
        from src.security_utils import secure_hash_file
        file_hash = secure_hash_file(file_data)
        metadata['file_hash'] = file_hash
        
        # Process the file upload
        result = blockchain_service.process_ifc_upload(file_data, user_address, metadata)
        
        # Security: Verify the returned content hash matches our calculated hash
        if result.get('content_hash') != file_hash:
            logger.error(f"Hash mismatch: {result.get('content_hash')} != {file_hash}")
            return jsonify({'error': 'Security validation failed: hash mismatch'}), 500
        
        # Security: Log the upload
        logger.info(f"IFC file uploaded: {file.filename} by {user_address} at {time.time()}")
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error in prepare_upload: {str(e)}")
        # Security: Don't expose detailed error message in production
        if current_app.debug:
            return jsonify({'error': str(e)}), 500
        else:
            return jsonify({'error': 'Failed to process upload'}), 500

# Additional blockchain endpoints for enhanced dashboard
@blockchain_bp.route("/network-stats", methods=["GET"])
def get_network_stats():
    """Get comprehensive network statistics"""
    try:
        # This would be implemented with real RPC calls
        network_stats = {
            "block_height": 12345,
            "block_time": "6.2s",
            "tx_throughput": "45 TPS",
            "active_validators": 10,
            "network_version": "v0.47.0",
            "consensus_state": "active"
        }
        
        return jsonify({
            "success": True,
            "data": network_stats
        })
    except Exception as e:
        logger.error(f"Error fetching network stats: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@blockchain_bp.route("/token-price", methods=["GET"])  
def get_token_price():
    """Get current ODIS token price and market data"""
    try:
        # This would integrate with actual price feeds
        price_data = {
            "price_usd": 0.42,
            "price_change_24h": 5.7,
            "market_cap": 15811040,
            "volume_24h": 234567,
            "circulating_supply": 37650000
        }
        
        return jsonify({
            "success": True,
            "price": price_data["price_usd"],
            "change_24h": price_data["price_change_24h"],
            "volume": price_data["volume_24h"],
            "data": price_data
        })
    except Exception as e:
        logger.error(f"Error fetching token price: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@blockchain_bp.route("/recent-transactions", methods=["GET"])
def get_recent_transactions():
    """Get recent blockchain transactions"""
    try:
        from datetime import datetime
        from src.gateways.blockchain_gateways import PingPubGateway
        
        # Initialize gateway for this request
        gateway = PingPubGateway()
        
        # Get real validator data to create meaningful transaction data
        validators_data = gateway.get_validators()
        
        transactions = []
        if validators_data and isinstance(validators_data, dict) and 'validators' in validators_data:
            validators = validators_data['validators']
            
            for i, validator in enumerate(validators[:5] if isinstance(validators, list) else []):
                if isinstance(validator, dict):
                    transactions.append({
                        'hash': f"0x{hash(str(validator.get('address', '')))%1000000:06x}...",
                        'type': 'stake' if i % 2 == 0 else 'delegate',
                        'amount': str(int(float(validator.get('voting_power', 1000)) / 1000)),
                        'timestamp': datetime.now().isoformat(),
                        'status': 'confirmed',
                        'validator': str(validator.get('address', ''))[:12] + '...'
                    })
        else:
            # Fallback with minimal data structure
            transactions = [
                {
                    'hash': "0xa1b2c3...",
                    'type': 'stake',
                    'amount': "1000",
                    'timestamp': datetime.now().isoformat(),
                    'status': 'confirmed'
                }
            ]
        
        return jsonify({
            'success': True,
            'transactions': transactions
        })
        
    except Exception as e:
        logger.error(f"Error fetching recent transactions: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==== File: src/controllers/blockchain_proxy_controller.py ====
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
# ==== File: src/controllers/rpc_controller.py ====
"""
RPC Controller for Direct Testnet Access
Exposes direct RPC endpoints from testnet-rpc.daodiseo.chaintools.tech
"""

import logging
from flask import Blueprint, jsonify, request
from src.services.rpc_service import DaodiseoRPCService
from src.security_utils import secure_endpoint

logger = logging.getLogger(__name__)

# Create blueprint
rpc_bp = Blueprint('rpc', __name__, url_prefix='/api/rpc')

# Initialize RPC service
rpc_service = DaodiseoRPCService()

@rpc_bp.route('/network-status', methods=['GET'])
@secure_endpoint
def get_network_status():
    """Get current network status and health from RPC"""
    try:
        result = rpc_service.get_network_status()
        return jsonify(result)
    except Exception as e:
        logger.error(f"RPC network status error: {e}")
        return jsonify({
            "success": False,
            "error": "Failed to fetch network status from RPC",
            "details": str(e)
        }), 500

@rpc_bp.route('/validators', methods=['GET'])
@secure_endpoint
def get_validators():
    """Get current validators from RPC"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 100, type=int)
        
        result = rpc_service.get_validators(page=page, per_page=per_page)
        return jsonify(result)
    except Exception as e:
        logger.error(f"RPC validators error: {e}")
        return jsonify({
            "success": False,
            "error": "Failed to fetch validators from RPC",
            "details": str(e)
        }), 500

@rpc_bp.route('/latest-block', methods=['GET'])
@secure_endpoint
def get_latest_block():
    """Get latest block information from RPC"""
    try:
        result = rpc_service.get_latest_block()
        return jsonify(result)
    except Exception as e:
        logger.error(f"RPC latest block error: {e}")
        return jsonify({
            "success": False,
            "error": "Failed to fetch latest block from RPC",
            "details": str(e)
        }), 500

@rpc_bp.route('/transactions', methods=['GET'])
@secure_endpoint
def search_transactions():
    """Search transactions from RPC"""
    try:
        query = request.args.get('query', 'tx.height>0')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 30, type=int)
        
        result = rpc_service.search_transactions(query=query, page=page, per_page=per_page)
        return jsonify(result)
    except Exception as e:
        logger.error(f"RPC transactions error: {e}")
        return jsonify({
            "success": False,
            "error": "Failed to fetch transactions from RPC",
            "details": str(e)
        }), 500

@rpc_bp.route('/network-info', methods=['GET'])
@secure_endpoint
def get_network_info():
    """Get network peer information from RPC"""
    try:
        result = rpc_service.get_network_info()
        return jsonify(result)
    except Exception as e:
        logger.error(f"RPC network info error: {e}")
        return jsonify({
            "success": False,
            "error": "Failed to fetch network info from RPC",
            "details": str(e)
        }), 500

@rpc_bp.route('/consensus-state', methods=['GET'])
@secure_endpoint
def get_consensus_state():
    """Get consensus state from RPC"""
    try:
        result = rpc_service.get_consensus_state()
        return jsonify(result)
    except Exception as e:
        logger.error(f"RPC consensus state error: {e}")
        return jsonify({
            "success": False,
            "error": "Failed to fetch consensus state from RPC",
            "details": str(e)
        }), 500

def register_rpc_routes(app):
    """Register RPC routes with the Flask app"""
    app.register_blueprint(rpc_bp)
    logger.info("RPC routes registered successfully")
# ==== File: src/controllers/transaction_controller.py ====
import logging
import uuid
import json
from flask import Blueprint, jsonify, request
from src.services.transaction_service import TransactionService
from src.gateways.blockchain_gateways import KeplerGateway, KeplerSignatureRole

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create blueprint
transaction_bp = Blueprint("transaction", __name__, url_prefix="/api")

# Initialize service
transaction_service = TransactionService()
network_config = {
    "chain_id": "ithaca-1",  # Updated to match the testnet chain ID
    "rpc_url": "https://odiseo.test.rpc.nodeshub.online",
    "api_url": "https://odiseo.test.api.nodeshub.online"
}
kepler_gateway = KeplerGateway(network_config)


@transaction_bp.route("/transactions", methods=["GET"])
def get_transactions():
    """Retrieve blockchain transactions"""
    # Get from blockchain or return test data if no address is provided
    address = request.args.get("address")
    
    # ------------------------------------------------------------
    # TODO(DDS_TEAM): Replace mock transaction data with real blockchain queries
    # TODO(DDS_TEAM): Implement proper pagination for transaction results
    # TODO(DDS_TEAM): Add caching layer to reduce blockchain API calls
    # TODO(DDS_TEAM): Add proper error handling for blockchain query failures
    # ------------------------------------------------------------
    if address:
        # Try to get real transaction data for the address
        try:
            # This would be replaced with actual blockchain query
            logger.debug(f"Querying transactions for address: {address}")
            # Placeholder - real implementation would query blockchain
            return jsonify([
                {
                    "id": f"tx-{uuid.uuid4().hex[:8]}",
                    "type": "Property Tokenization",
                    "hash": f"0x{uuid.uuid4().hex}",
                    "timestamp": "2025-04-04T12:34:56Z",
                    "status": "confirmed",
                    "address": address,
                }
            ])
        except Exception as e:
            logger.error(f"Error querying transactions: {str(e)}")
            # Fall back to sample data
    
    # Sample transactions for display
    transactions = [
        {
            "id": "tx1",
            "type": "Property Tokenization",
            "hash": "0x7a3bc8e4f82b5d98f3c8bd71904a31c9e4d77d18e76d9b4d60bb598af3c9a8b2",
            "block": 10245678,
            "timestamp": "2025-04-04T12:34:56Z",
            "status": "confirmed",
            "value": "1500000",
            "currency": "ODIS",
        },
        {
            "id": "tx2",
            "type": "Document Upload",
            "hash": "0x9d2e7c6b45a3f2e89d364c5f7e8b9a1c2d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a",
            "block": 10245621,
            "timestamp": "2025-04-03T09:12:34Z",
            "status": "confirmed",
            "document": "Property Deed.pdf",
        },
        {
            "id": "tx3",
            "type": "Multi-sig Approval",
            "hash": "0x3f8e2d9c15b7a6f4d8e2c9b1a7d6f5e4d3c2b1a9f8e7d6c5b4a3f2e1d9c8b7a6",
            "block": 10245589,
            "timestamp": "2025-04-02T15:45:30Z",
            "status": "confirmed",
            "signatures": "3/4",
        },
    ]

    return jsonify(transactions)


@transaction_bp.route("/transactions/<tx_id>", methods=["GET"])
def get_transaction(tx_id):
    """Retrieve a specific transaction by ID"""
    # ------------------------------------------------------------
    # TODO(DDS_TEAM): Implement real blockchain query to fetch transaction details
    # TODO(DDS_TEAM): Add error handling for non-existent transaction IDs
    # TODO(DDS_TEAM): Add transaction verification using blockchain API
    # ------------------------------------------------------------
    logger.debug(f"Getting transaction details for: {tx_id}")

    mock_transactions = {
        "tx1": {
            "id": "tx1",
            "type": "Property Tokenization",
            "hash": "0x7a3bc8e4f82b5d98f3c8bd71904a31c9e4d77d18e76d9b4d60bb598af3c9a8b2",
            "block": 10245678,
            "timestamp": "2025-04-04T12:34:56Z",
            "status": "confirmed",
            "value": "1500000",
            "currency": "ODIS",
            "sender": "odiseo1a2b3c4d5e6f7g8h9i0j",
            "receiver": "odiseo0j9i8h7g6f5e4d3c2b1a",
            "gas_used": 21000,
            "gas_price": "0.000000001",
            "fees": "0.000021",
            "details": {
                "property_id": "prop123",
                "property_name": "Cosmic Tower",
                "token_count": 1500000,
                "token_price": "1.00",
                "total_value": "1500000.00",
            },
        }
    }

    if tx_id not in mock_transactions:
        return jsonify({"error": "Transaction not found"}), 404

    return jsonify(mock_transactions[tx_id])


@transaction_bp.route("/transactions/sign", methods=["POST"])
def sign_transaction():
    """Sign a transaction with a wallet"""
    try:
        data = request.json
        logger.debug(f"Received data for signing: {data}")

        if not data:
            return jsonify({"error": "Transaction data is required"}), 400

        if "wallet_address" not in data:
            return jsonify({"error": "Wallet address is required"}), 400
        
        # Extract transaction parameters
        wallet_address = data.get("wallet_address")
        transaction_id = data.get("transaction_id", f"tx-{uuid.uuid4().hex[:8]}")
        content_hash = data.get("content_hash", "")
        role = data.get("role", "owner")
        
        # Create transaction parameters
        tx_data = {
            "from_address": wallet_address,
            "to_address": data.get("to_address", "odiseo1qg5ega6dykkxc307y25pecuv380qje7zp9qpxt"),
            "amount": data.get("amount", [{"denom": "uodis", "amount": "1000"}]),
            "transaction_id": transaction_id,
            "content_hash": content_hash,
            "role": role
        }
        
        # Try to get account info from blockchain
        try:
            # Get real account information for transaction parameters
            from src.gateways.blockchain_gateways import PingPubGateway
            pingpub_gateway = PingPubGateway()
            account_info = pingpub_gateway.get_account_info(wallet_address)
            
            # Add account info to transaction data
            tx_data["account_number"] = account_info.get("account_number", "0")
            tx_data["sequence"] = account_info.get("sequence", "0")
            
            logger.debug(f"Using account info from blockchain: {account_info}")
        except Exception as acc_error:
            logger.warning(f"Error retrieving account info: {str(acc_error)}")
            # Continue without account info, will use defaults
        
        # Create sign doc for Keplr wallet using Kepler gateway
        sign_doc = kepler_gateway.sign_transaction(tx_data)
        
        return jsonify({
            "success": True,
            "sign_doc": sign_doc,
            "transaction_id": transaction_id,
            "broadcast_url": "/api/transactions/broadcast"
        })
    except Exception as e:
        logger.error(f"Error preparing transaction for signing: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@transaction_bp.route("/transactions/broadcast", methods=["POST"])
def broadcast_transaction():
    """Broadcast a signed transaction to the blockchain"""
    try:
        data = request.json
        logger.debug(f"Received data for broadcasting: {data}")

        # Validate input data
        if not data:
            return jsonify({"error": "Transaction data is required"}), 400
            
        if "signature" not in data:
            return jsonify({"error": "Signature is required"}), 400
            
        if "transaction" not in data:
            return jsonify({"error": "Transaction data is required"}), 400
            
        # Extract signature and transaction data
        signature = data["signature"]
        transaction = data["transaction"]
        
        # Get signature components
        signature_value = signature.get("signature")
        pub_key = signature.get("pub_key")
        
        # Get signed transaction details for formatting
        signed_tx = signature.get("signed", {})
        
        # Validate signature components
        if not signature_value or not pub_key:
            return jsonify({"error": "Invalid signature format"}), 400
            
        # Convert Amino messages to Proto format
        amino_msgs = signed_tx.get("msgs", [])
        proto_msgs = []
        
        for msg in amino_msgs:
            proto_msg = kepler_gateway.convert_amino_to_proto(msg)
            proto_msgs.append(proto_msg)
            
        logger.debug(f"Converted messages to Proto format: {proto_msgs}")
        
        # Prepare broadcast data
        broadcast_tx = {
            "tx": {
                "msg": proto_msgs,
                "fee": signed_tx.get("fee", {"amount": [{"denom": "uodis", "amount": "2500"}], "gas": "100000"}),
                "signatures": [{
                    "pub_key": pub_key,
                    "signature": signature_value
                }],
                "memo": signed_tx.get("memo", "")
            },
            "mode": "block"  # Wait for confirmation
        }
        
        # Broadcast the transaction
        result = transaction_service.broadcast_transaction(broadcast_tx)
        
        # Format response with transaction hash
        tx_hash = result.get("txhash", "")
        explorer_url = f"https://testnet.explorer.nodeshub.online/odiseo/tx/{tx_hash}"
        
        return jsonify({
            "success": True,
            "message": "Transaction broadcasted successfully",
            "txhash": tx_hash,
            "explorer_url": explorer_url,
            "result": result
        })
    except Exception as e:
        logger.error(f"Error broadcasting transaction: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@transaction_bp.route("/transactions/create", methods=["POST"])
def create_transaction():
    """Create a transaction for tokenizing a property"""
    try:
        data = request.json
        logger.debug(f"Received data for creating transaction: {data}")

        # ------------------------------------------------------------
        # TODO(DDS_TEAM): Implement proper property validation
        # TODO(DDS_TEAM): Add token distribution calculations
        # TODO(DDS_TEAM): Connect to smart contract for token creation
        # TODO(DDS_TEAM): Implement multi-signature requirements
        # ------------------------------------------------------------

        if not data or "property_id" not in data:
            return jsonify({"error": "Property ID is required"}), 400

        property_id = data["property_id"]
        property_value = data.get("property_value", "1000000")
        token_count = data.get("token_count", "1000000")
        
        # Generate transaction ID
        transaction_id = f"tx-{uuid.uuid4().hex[:8]}"
        
        # Create a message with proper structure for Cosmos SDK
        msg = {
            "type": "cosmos-sdk/MsgSend",
            "property_id": property_id,
            "property_value": property_value,
            "token_count": token_count,
            "transaction_id": transaction_id
        }
        
        # Return the transaction data
        return jsonify({
            "success": True,
            "transaction_id": transaction_id,
            "msg": msg,
            "next_steps": {
                "sign": f"/api/transactions/sign",
                "broadcast": f"/api/transactions/broadcast"
            }
        })
    except Exception as e:
        logger.error(f"Error creating transaction: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500
