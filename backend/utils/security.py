import time
from flask import request

_request_history = {}

def rate_limit_middleware():
    client_ip = request.remote_addr or "127.0.0.1"
    now = time.time()
    
    # Simple window rate limit: max 60 requests per minute
    if client_ip not in _request_history:
        _request_history[client_ip] = []
    
    _request_history[client_ip] = [t for t in _request_history[client_ip] if now - t < 60]
    
    if len(_request_history[client_ip]) >= 60:
        return {"success": False, "error": "Rate limit exceeded (60 req/min)"}, 429
        
    _request_history[client_ip].append(now)

def apply_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
