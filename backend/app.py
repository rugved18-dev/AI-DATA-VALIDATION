"""
Flask Backend for Multi-Domain AI Data Validation System - PHASE 7 ENHANCED

This backend provides APIs for data validation across different domains with
production-grade security and mainframe integration support:
- Banking: Validate customer financial profiles
- Healthcare: Validate patient health records
- E-commerce: Validate product inventory data

PHASE 7 ENHANCEMENTS:
- Input sanitization and validation
- Rate limiting on API endpoints
- Security headers for XSS/CSRF/Clickjacking prevention
- COBOL Mainframe integration placeholder (mainframe_service.py)

Future Integration Points:
- COBOL Mainframe Systems: Message queue integration for legacy system compatibility
- DB2 Database: Enhanced validation against regulatory rules and historical data
- Microservices: RESTful APIs for scalable validation

Author: AI Data Validation Team
Version: 2.0.0 (Phase 7 - Security & COBOL Integration)

Project Structure (Modular Design):
backend/
├── app.py                       # Main Flask application entry point
├── models/
│   └── validation_result.py
├── services/
│   ├── validation_service.py    # Domain validation logic
│   ├── file_service.py          # File handling utilities
│   ├── scoring_service.py       # Scoring calculations
│   ├── anomaly_detection.py     # Anomaly detection (Phase 5)
│   ├── mainframe_service.py     # COBOL integration (Phase 7)
│   └── security_utils.py        # Security utilities (Phase 7)
├── routes/
│   └── upload_routes.py         # API endpoints
├── uploads/                     # Temporary file storage
└── requirements.txt             # Dependencies
"""

from flask import Flask
from flask_cors import CORS
from functools import wraps
import os
import logging
from datetime import datetime, timedelta
from collections import defaultdict

# Import security utilities
from services.security_utils import CSVSecurityValidator, InputValidator, SecurityLogger

# ==================== LOGGING CONFIGURATION ====================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== FLASK APP INITIALIZATION ====================

app = Flask(__name__)

# CORS Configuration (Phase 7 Security - Restrictive)
CORS(app, resources={
    r"/upload": {
        "origins": ["http://localhost:3000", "http://localhost:5000"],
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "max_age": 3600
    }
})

# ==================== CONFIGURATION ====================

UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB limit (for Phase 7 security)

# Create uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# ==================== SECURITY HEADERS MIDDLEWARE ====================

@app.after_request
def set_security_headers(response):
    """
    Add security headers to all responses.
    
    Headers prevent common web vulnerabilities:
    - X-Content-Type-Options: Prevent MIME-type sniffing
    - X-Frame-Options: Prevent clickjacking (deny iframes)
    - X-XSS-Protection: Legacy XSS protection (browsers)
    - Content-Security-Policy: Strict CSP policy
    - Strict-Transport-Security: Force HTTPS
    - Referrer-Policy: Control referrer information
    """
    
    # Prevent MIME-type sniffing attacks
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # Prevent clickjacking by denying iframe embedding
    response.headers['X-Frame-Options'] = 'DENY'
    
    # Enable XSS protection in legacy browsers
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Content Security Policy - Strict policy
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "font-src 'self'; "
        "connect-src 'self' http://localhost:5000; "
        "frame-ancestors 'none'; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "form-action 'self'"
    )
    
    # Force HTTPS (only in production)
    # response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    # Control referrer information
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # Prevent feature policies
    response.headers['Permissions-Policy'] = (
        'microphone=(), '
        'camera=(), '
        'geolocation=(), '
        'usb=(), '
        'payment=(), '
        'vr=(), '
        'xr-spatial-tracking=()'
    )
    
    return response


# ==================== RATE LIMITING ====================

class RateLimitStore:
    """In-memory rate limit tracking (use Redis in production)."""
    
    def __init__(self):
        self.requests = defaultdict(list)
    
    def is_rate_limited(self, key: str, max_requests: int, time_window: int) -> bool:
        """
        Check if request is rate limited.
        
        Args:
            key (str): Client identifier (IP address)
            max_requests (int): Maximum requests allowed
            time_window (int): Time window in seconds
            
        Returns:
            bool: True if rate limited
        """
        now = datetime.now()
        cutoff_time = now - timedelta(seconds=time_window)
        
        # Clean old requests
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if req_time > cutoff_time
        ]
        
        # Check if over limit
        if len(self.requests[key]) >= max_requests:
            return True
        
        # Add current request
        self.requests[key].append(now)
        return False


rate_limit_store = RateLimitStore()


def rate_limit(max_requests: int = 10, time_window: int = 3600):
    """
    Rate limiting decorator.
    
    Args:
        max_requests (int): Max requests per time window
        time_window (int): Time window in seconds
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request
            
            # Get client IP
            client_ip = request.remote_addr or 'unknown'
            
            # Check rate limit
            if rate_limit_store.is_rate_limited(client_ip, max_requests, time_window):
                logger.warning(f"Rate limit exceeded for IP: {client_ip}")
                SecurityLogger.log_security_event(
                    'RATE_LIMIT_EXCEEDED',
                    f'IP: {client_ip}, Endpoint: {request.path}',
                    'WARNING'
                )
                
                from flask import jsonify
                response = jsonify({
                    'status': 'error',
                    'message': 'Rate limit exceeded. Maximum 10 uploads per hour.',
                    'retry_after': time_window
                })
                response.status_code = 429
                return response
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator


# ==================== REQUEST VALIDATION ====================

def require_content_type(content_type: str):
    """Decorator to validate Content-Type header."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request
            
            if request.content_type != content_type:
                SecurityLogger.log_security_event(
                    'INVALID_CONTENT_TYPE',
                    f'Expected: {content_type}, Got: {request.content_type}',
                    'WARNING'
                )
                
                from flask import jsonify
                return jsonify({
                    'status': 'error',
                    'message': f'Content-Type must be {content_type}'
                }), 400
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator


# ==================== REQUEST LOGGING ====================

@app.before_request
def log_request():
    """Log all incoming requests for security audit trail."""
    from flask import request
    
    logger.info(
        f"REQUEST - Method: {request.method}, "
        f"Path: {request.path}, "
        f"IP: {request.remote_addr}, "
        f"Content-Type: {request.content_type}"
    )


@app.after_request
def log_response(response):
    """Log all outgoing responses."""
    logger.info(f"RESPONSE - Status: {response.status_code}")
    return response


# ==================== ERROR HANDLERS ====================

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error."""
    SecurityLogger.log_security_event(
        'FILE_TOO_LARGE',
        f'File exceeds max size of {MAX_FILE_SIZE} bytes',
        'WARNING'
    )
    
    from flask import jsonify
    return jsonify({
        'status': 'error',
        'message': 'File too large. Maximum upload size is 100MB.',
        'max_size': MAX_FILE_SIZE
    }), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    from flask import jsonify
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal error: {str(error)}")
    
    from flask import jsonify
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500


# ==================== ROUTE REGISTRATION ====================

from routes.upload_routes import register_routes

register_routes(app)


# ==================== HEALTH CHECK ENDPOINT ====================

@app.route('/health', methods=['GET'])
def health_check():
    """Basic health check endpoint."""
    from flask import jsonify
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0'
    }), 200


# ==================== APPLICATION ENTRY POINT ====================

if __name__ == '__main__':
    """
    Main application entry point.
    
    Configuration:
    - debug=True: Enables auto-reload and detailed error messages
    - host='0.0.0.0': Accept connections from any IP
    - port=5000: Default Flask development port
    
    Production Deployment:
    - Use production WSGI server (Gunicorn, uWSGI)
    - Set debug=False
    - Use environment variables for sensitive config
    - Use Redis for rate limiting instead of in-memory store
    - Enable HTTPS/TLS
    - Use proper logging (ELK stack, CloudWatch)
    - Deploy behind reverse proxy (nginx, CloudFront)
    - Monitor security headers with tools like Immunicity
    
    Phase 7 Enhancements:
    - Security headers configured
    - Rate limiting implemented
    - Input validation in place
    - Request/response logging enabled
    - COBOL mainframe integration ready (mainframe_service.py)
    
    Future Enhancements:
    - Add logging and monitoring
    - Implement message queue for COBOL integration
    - Add database connection pools for DB2
    - Implement request tracing for debugging
    - Add API authentication (JWT, OAuth2)
    - Database audit logging for compliance
    """
    
    logger.info("Starting AI Data Validation Backend - Phase 7")
    logger.info("Security features: Headers, Rate Limiting, Input Validation, Logging")
    logger.info("COBOL Integration: Available via mainframe_service.py")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
