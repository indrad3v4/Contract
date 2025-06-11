"""Combined Python test stubs for JavaScript modules"""

# ==== File: __init__.py ====
"""
Package for JavaScript test stubs.
This package creates Python module representations of JS files for testing.
"""

# ==== File: main.py ====
"""
Python module representation of main.js for testing purposes.
This simulates the JavaScript functions and objects from the main.js file.
"""
import json

# Create a browser-like window object for accessing globals like keplr
class Window:
    """Mock browser window object."""
    def __init__(self):
        self.keplr = None
        self.document = None
        self.localStorage = {}
        self.sessionStorage = {}

# Global window instance
window = Window()

# Mock Keplr wallet integration functions
async def convert_amino_to_proto(msg):
    """
    Convert Amino message format to Proto format.
    This is a Python simulation of the JavaScript function.
    
    Args:
        msg (dict): Message in Amino format
    
    Returns:
        dict: Message in Proto format
    """
    if msg.get("type") == "cosmos-sdk/MsgSend":
        # Convert MsgSend from Amino to Proto format
        return {
            "@type": "/cosmos.bank.v1beta1.MsgSend",
            "from_address": msg["value"]["from_address"],
            "to_address": msg["value"]["to_address"],
            "amount": msg["value"]["amount"],
        }
    
    # For other message types
    return msg

# Mock fetch API for tests
async def fetch(url, options=None):
    """Mock fetch implementation for tests"""
    response = {
        "ok": True,
        "status": 200,
        "json": lambda: {"result": "success", "data": {"test": "value"}}
    }
    return response

def mock_js_convert_amino_to_proto(msg):
    """Non-async version for tests"""
    if msg.get("type") == "cosmos-sdk/MsgSend":
        return {
            "@type": "/cosmos.bank.v1beta1.MsgSend", 
            "fromAddress": msg["value"]["from_address"],
            "toAddress": msg["value"]["to_address"],
            "amount": msg["value"]["amount"]
        }
    return msg

def parse_memo_data(memo):
    """Parse the transaction memo to extract data"""
    parts = memo.split('|')
    result = {}
    
    for part in parts:
        if ':' in part:
            key, value = part.split(':', 1)
            result[key] = value
    
    return result

class TransactionHelper:
    """Helper class for transaction related functions"""
    
    @staticmethod
    def create_sign_doc(account_info, tx_data):
        """Create a sign doc for Keplr"""
        return {
            "chain_id": "odiseotestnet_1234-1",
            "account_number": account_info.get("account_number", "0"),
            "sequence": account_info.get("sequence", "0"),
            "fee": {"amount": [{"denom": "uodis", "amount": "2500"}], "gas": "100000"},
            "msgs": [
                {
                    "type": "cosmos-sdk/MsgSend",
                    "value": {
                        "from_address": account_info.get("address", ""),
                        "to_address": "odiseo1qg5ega6dykkxc307y25pecuv380qje7zp9qpxt",
                        "amount": [{"denom": "uodis", "amount": "1000"}],
                    },
                }
            ],
            "memo": f"tx:{tx_data.get('tx_id', '')}|hash:{tx_data.get('content_hash', '')}|role:{tx_data.get('role', 'user')}",
        }

async def signContract(tx_id, role="owner"):
    """
    Sign a contract transaction using Keplr wallet.
    
    Args:
        tx_id (str): Transaction ID to sign
        role (str): Signer role (owner, validator, etc.)
        
    Returns:
        dict: Result of the signing operation
    """
    if not window.keplr:
        raise Exception("Keplr wallet extension not found")
    
    # Enable the chain
    chain_id = "odiseotestnet_1234-1"
    await window.keplr.enable(chain_id)
    
    # Get the offline signer
    offlineSigner = window.keplr.getOfflineSigner(chain_id)
    
    # Get accounts
    accounts = await offlineSigner.getAccounts()
    if not accounts or len(accounts) == 0:
        raise Exception("No accounts found in Keplr wallet")
    
    # Get the first account
    user_address = accounts[0]["address"]
    
    # 1. Get transaction details
    transaction_response = await fetch(f"/api/transaction/{tx_id}")
    transaction = await transaction_response.json()
    
    # 2. Get account information
    account_response = await fetch(f"/api/account?address={user_address}")
    account_info = await account_response.json()
    
    # 3. Create transaction data
    tx_data = {
        "tx_id": tx_id, 
        "content_hash": transaction["content_hash"],
        "role": role
    }
    
    # 4. Create sign doc
    sign_doc = TransactionHelper.create_sign_doc(account_info, tx_data)
    
    # 5. Sign with Keplr (Amino format)
    signature = await window.keplr.signAmino(
        chain_id, 
        user_address, 
        sign_doc, 
        {"preferNoSetFee": True}
    )
    
    # 6. Send signature to backend
    sign_payload = {
        "transaction_id": tx_id,
        "signature": signature.signature,
        "public_key": signature.pub_key.value,
        "role": role
    }
    
    sign_response = await fetch("/api/sign", {
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(sign_payload)
    })
    
    sign_result = await sign_response.json()
    
    return {
        "success": sign_response.ok,
        "result": sign_result,
        "transaction_id": tx_id,
        "signer": user_address
    }
# ==== File: transaction.py ====
"""
Python module representation of transaction.js for testing purposes.
This simulates the JavaScript functions and objects from the transaction.js file.
"""
import json

# A mock window object for Keplr wallet integration tests
class MockWindow:
    """Mock browser window object with Keplr wallet instance."""
    
    def __init__(self):
        self.keplr = None


# Create a window instance for tests to access
window = MockWindow()

# Mock transaction functions
async def signAmino(chain_id, signer, sign_doc, sign_options=None):
    """
    Mock Keplr signAmino function.
    
    Args:
        chain_id (str): Chain ID
        signer (str): Signer address
        sign_doc (dict): Document to sign
        sign_options (dict): Options for signing
        
    Returns:
        dict: Mock signature response
    """
    if not window.keplr:
        raise Exception("Keplr not available")
    
    # Enable the chain first (if not already enabled)
    if not hasattr(window.keplr, "enabled_chains") or chain_id not in window.keplr.enabled_chains:
        await window.keplr.enable(chain_id)
    
    # Call the signAmino method of the Keplr wallet
    return await window.keplr.signAmino(chain_id, signer, sign_doc, sign_options)

def validateSignDoc(sign_doc):
    """
    Validate a sign doc format.
    
    Args:
        sign_doc (dict): Document to validate
        
    Returns:
        bool: True if valid
    """
    required_fields = [
        "chain_id", "account_number", "sequence",
        "fee", "msgs", "memo"
    ]
    
    # Check required fields
    for field in required_fields:
        if field not in sign_doc:
            return False
    
    # Check messages format
    for msg in sign_doc["msgs"]:
        if "type" not in msg or "value" not in msg:
            return False
    
    return True

def parse_memo_format(memo):
    """
    Parse structured memo format like "tx:123|hash:abc|role:owner"
    
    Args:
        memo (str): Memo string to parse
        
    Returns:
        dict: Parsed memo fields
    """
    parts = memo.split('|')
    result = {}
    
    for part in parts:
        if ':' in part:
            key, value = part.split(':', 1)
            result[key] = value
            
    return result

def create_amino_sign_doc(account_data, tx_id, content_hash, role="owner"):
    """
    Create a sign doc in Amino format for Keplr
    
    Args:
        account_data (dict): User account data
        tx_id (str): Transaction ID
        content_hash (str): Content hash
        role (str): Signer role
        
    Returns:
        dict: Amino format sign document
    """
    return {
        "chain_id": "odiseotestnet_1234-1",
        "account_number": account_data.get("account_number", "0"),
        "sequence": account_data.get("sequence", "0"),
        "fee": {"amount": [{"denom": "uodis", "amount": "2500"}], "gas": "100000"},
        "msgs": [
            {
                "type": "cosmos-sdk/MsgSend",
                "value": {
                    "from_address": account_data.get("address", ""),
                    "to_address": "odiseo1qg5ega6dykkxc307y25pecuv380qje7zp9qpxt",
                    "amount": [{"denom": "uodis", "amount": "1000"}],
                },
            }
        ],
        "memo": f"tx:{tx_id}|hash:{content_hash}|role:{role}",
    }