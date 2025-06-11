"""
Enhanced Rate Limiter for DAODISEO API Endpoints
Implements sliding window and circuit breaker patterns
"""
import time
import threading
from collections import defaultdict, deque
from functools import wraps
from flask import request, jsonify
import logging

class SlidingWindowRateLimiter:
    def __init__(self):
        self.requests = defaultdict(deque)
        self.blocked_ips = defaultdict(float)
        self.lock = threading.Lock()
        
        # Rate limits per endpoint type
        self.limits = {
            'orchestrator': {'requests': 10, 'window': 60},  # 10 requests per minute
            'rpc': {'requests': 20, 'window': 60},           # 20 requests per minute
            'blockchain': {'requests': 15, 'window': 60},    # 15 requests per minute
            'default': {'requests': 30, 'window': 60}        # 30 requests per minute
        }
        
        # Circuit breaker thresholds
        self.circuit_breaker = {
            'failure_threshold': 5,
            'recovery_time': 300  # 5 minutes
        }

    def get_endpoint_type(self, endpoint):
        """Determine rate limit category based on endpoint"""
        if '/api/orchestrator/' in endpoint:
            return 'orchestrator'
        elif '/api/rpc/' in endpoint:
            return 'rpc'
        elif '/api/blockchain/' in endpoint:
            return 'blockchain'
        return 'default'

    def is_rate_limited(self, client_id, endpoint):
        """Check if client is rate limited for specific endpoint"""
        endpoint_type = self.get_endpoint_type(endpoint)
        limit_config = self.limits[endpoint_type]
        
        with self.lock:
            now = time.time()
            key = f"{client_id}:{endpoint_type}"
            
            # Check if client is temporarily blocked
            if key in self.blocked_ips:
                if now < self.blocked_ips[key]:
                    return True, f"Blocked until {self.blocked_ips[key] - now:.0f}s"
                else:
                    del self.blocked_ips[key]
            
            # Clean old requests outside the window
            requests = self.requests[key]
            while requests and requests[0] <= now - limit_config['window']:
                requests.popleft()
            
            # Check if limit exceeded
            if len(requests) >= limit_config['requests']:
                # Block client for progressive timeout
                block_duration = min(300, 30 * (len(requests) - limit_config['requests'] + 1))
                self.blocked_ips[key] = now + block_duration
                return True, f"Rate limit exceeded. Blocked for {block_duration}s"
            
            # Add current request
            requests.append(now)
            return False, None

    def record_failure(self, client_id, endpoint):
        """Record API failure for circuit breaker"""
        endpoint_type = self.get_endpoint_type(endpoint)
        key = f"{client_id}:{endpoint_type}:failures"
        
        with self.lock:
            now = time.time()
            failures = self.requests[key]
            
            # Clean old failures (last 5 minutes)
            while failures and failures[0] <= now - 300:
                failures.popleft()
            
            failures.append(now)
            
            # Check if circuit should open
            if len(failures) >= self.circuit_breaker['failure_threshold']:
                block_key = f"{client_id}:{endpoint_type}"
                self.blocked_ips[block_key] = now + self.circuit_breaker['recovery_time']
                logging.warning(f"Circuit breaker opened for {client_id} on {endpoint_type}")

# Global rate limiter instance
rate_limiter = SlidingWindowRateLimiter()

def rate_limit(f):
    """Decorator to apply rate limiting to Flask routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_id = request.environ.get('REMOTE_ADDR', 'unknown')
        endpoint = request.path
        
        is_limited, message = rate_limiter.is_rate_limited(client_id, endpoint)
        
        if is_limited:
            logging.warning(f"Rate limit hit: {client_id} on {endpoint} - {message}")
            return jsonify({
                'error': 'Rate limit exceeded',
                'message': message,
                'retry_after': 60
            }), 429
        
        try:
            response = f(*args, **kwargs)
            return response
        except Exception as e:
            # Record failure for circuit breaker
            rate_limiter.record_failure(client_id, endpoint)
            raise
    
    return decorated_function

def smart_rate_limit(requests_per_minute=None):
    """Configurable rate limiter decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_id = request.environ.get('REMOTE_ADDR', 'unknown')
            endpoint = request.path
            
            # Override default limit if specified
            if requests_per_minute:
                endpoint_type = rate_limiter.get_endpoint_type(endpoint)
                original_limit = rate_limiter.limits[endpoint_type]['requests']
                rate_limiter.limits[endpoint_type]['requests'] = requests_per_minute
            
            is_limited, message = rate_limiter.is_rate_limited(client_id, endpoint)
            
            # Restore original limit
            if requests_per_minute:
                rate_limiter.limits[endpoint_type]['requests'] = original_limit
            
            if is_limited:
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'message': message,
                    'retry_after': 60
                }), 429
            
            try:
                return f(*args, **kwargs)
            except Exception as e:
                rate_limiter.record_failure(client_id, endpoint)
                raise
        
        return decorated_function
    return decorator