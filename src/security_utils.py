"""
Security utilities for DAODISEO Platform
Provides security functions, CSRF protection, and environment validation
"""

import os
import secrets
import time
import hashlib
import logging
from functools import wraps
from flask import request, jsonify, session, current_app, g
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Rate limiting storage (in production, use Redis)
_rate_limit_storage = {}

def validate_environment() -> bool:
    """Validate required environment variables"""
    required_vars = [
        'OPENAI_API_KEY',
        'SESSION_SECRET'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        return False
    
    return True

def generate_csrf_token() -> str:
    """Generate CSRF token for the session"""
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
    return session['csrf_token']

def verify_csrf_token(token: str) -> bool:
    """Verify CSRF token"""
    session_token = session.get('csrf_token')
    if not session_token or not token:
        return False
    return secrets.compare_digest(session_token, token)

def apply_security_headers(response):
    """Apply security headers to response"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = (
        'max-age=31536000; includeSubDomains'
    )
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
        "style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; "
        "font-src 'self' data:; connect-src 'self'"
    )
    return response


def get_client_ip() -> str:
    """Get client IP address"""
    forwarded = request.headers.get('X-Forwarded-For')
    if forwarded:
        return forwarded.split(',')[0].strip()
    real_ip = request.headers.get('X-Real-IP')
    if real_ip:
        return real_ip
    return request.remote_addr or 'unknown'


def is_rate_limited(identifier: str, limit: int = 100, window: int = 3600) -> bool:
    """Check if request is rate limited"""
    current_time = time.time()
    window_start = current_time - window
    
    if identifier not in _rate_limit_storage:
        _rate_limit_storage[identifier] = []
    
    # Remove old requests outside the window
    _rate_limit_storage[identifier] = [
        req_time for req_time in _rate_limit_storage[identifier] 
        if req_time > window_start
    ]
    
    # Check if limit exceeded
    if len(_rate_limit_storage[identifier]) >= limit:
        return True
    
    # Add current request
    _rate_limit_storage[identifier].append(current_time)
    return False

def secure_endpoint(f):
    """Decorator for securing API endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get client identifier
        client_ip = get_client_ip()
        
        # Rate limiting
        if is_rate_limited(client_ip, limit=100, window=3600):
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return jsonify({
                'error': 'Rate limit exceeded',
                'retry_after': 3600
            }), 429
        
        # CSRF protection for state-changing requests
        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            csrf_token = request.headers.get('X-CSRF-Token') or request.form.get('csrf_token')
            if not csrf_token or not verify_csrf_token(csrf_token):
                if not current_app.debug:  # Skip CSRF in debug mode for API testing
                    logger.warning(f"CSRF token validation failed for IP: {client_ip}")
                    return jsonify({'error': 'CSRF token validation failed'}), 403
        
        # Content type validation for JSON endpoints
        if request.method in ['POST', 'PUT', 'PATCH']:
            if request.content_type and 'application/json' in request.content_type:
                try:
                    request.get_json(force=True)
                except Exception:
                    return jsonify({'error': 'Invalid JSON payload'}), 400
        
        # Execute the original function
        response = f(*args, **kwargs)
        
        # Apply security headers if response is a Flask Response object
        if hasattr(response, 'headers'):
            apply_security_headers(response)
        
        return response
    
    return decorated_function

def verify_wallet_ownership(wallet_address: str) -> bool:
    """Verify wallet ownership (placeholder implementation)"""
    # In production, this would verify cryptographic proof of wallet ownership
    # For now, we'll do basic validation
    if not wallet_address:
        raise ValueError("Wallet address is required")
    
    if len(wallet_address) < 10:
        raise ValueError("Invalid wallet address format")
    
    # Additional validation logic would go here
    # For example, signature verification, session checks, etc.
    
    return True

def hash_sensitive_data(data: str) -> str:
    """Hash sensitive data for logging/storage"""
    if not data:
        return "empty"
    
    salt = os.environ.get('HASH_SALT', 'default_salt')
    return hashlib.sha256(f"{data}{salt}".encode()).hexdigest()[:16]

def sanitize_input(input_str: str, max_length: int = 1000) -> str:
    """Sanitize user input"""
    if not input_str:
        return ""
    
    # Remove potential XSS characters
    dangerous_chars = ['<', '>', '"', "'", '&', 'javascript:', 'data:']
    sanitized = input_str
    
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    # Truncate to max length
    return sanitized[:max_length]

def validate_api_request(required_fields: list, data: dict) -> Optional[str]:
    """Validate API request data"""
    if not data:
        return "Request data is required"
    
    missing_fields = []
    for field in required_fields:
        if field not in data or data[field] is None:
            missing_fields.append(field)
    
    if missing_fields:
        return f"Missing required fields: {', '.join(missing_fields)}"
    
    return None

def log_security_event(event_type: str, details: Dict[str, Any]):
    """Log security-related events"""
    client_ip = get_client_ip()
    timestamp = time.time()
    
    log_entry = {
        'timestamp': timestamp,
        'event_type': event_type,
        'client_ip': hash_sensitive_data(client_ip),
        'details': details,
        'user_agent': request.headers.get('User-Agent', 'unknown')[:100]
    }
    
    logger.info(f"Security event: {event_type} from {hash_sensitive_data(client_ip)}")
    logger.debug(f"Security event details: {log_entry}")

class SecurityMiddleware:
    """Security middleware for Flask application"""
    
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize security middleware with Flask app"""
        app.before_request(self._before_request)
        app.after_request(self._after_request)
    
    def _before_request(self):
        """Process request before handling"""
        # Set security context
        g.client_ip = get_client_ip()
        g.request_start_time = time.time()
        
        # Log suspicious requests
        if self._is_suspicious_request():
            log_security_event('suspicious_request', {
                'method': request.method,
                'path': request.path,
                'user_agent': request.headers.get('User-Agent', 'unknown')
            })
    
    def _after_request(self, response):
        """Process response after handling"""
        # Apply security headers
        apply_security_headers(response)
        
        # Log response time for monitoring
        if hasattr(g, 'request_start_time'):
            response_time = time.time() - g.request_start_time
            if response_time > 5.0:  # Log slow requests
                logger.warning(f"Slow request: {request.path} took {response_time:.2f}s")
        
        return response
    
    def _is_suspicious_request(self) -> bool:
        """Check if request looks suspicious"""
        suspicious_patterns = [
            'admin', 'login', 'wp-admin', '.php', '.asp', '.jsp',
            'eval(', '<script', 'javascript:', 'data:text/html'
        ]
        
        path = request.path.lower()
        for pattern in suspicious_patterns:
            if pattern in path:
                return True
        
        # Check for unusual headers
        unusual_headers = ['X-Forwarded-Host', 'X-Originating-IP', 'X-Remote-IP']
        for header in unusual_headers:
            if request.headers.get(header):
                return True
        
        return False