# Phase 7: Security & COBOL Integration Implementation Guide

## 📋 Overview

Phase 7 represents a major production-readiness upgrade with two primary focuses:

1. **Security Enhancements** - Input validation, sanitization, rate limiting, and security headers
2. **COBOL Mainframe Integration** - Placeholder architecture for legacy system connectivity

This phase transforms the application from a development system into an enterprise-grade solution suitable for production deployment.

**Version**: 2.0.0 (Phase 7)  
**Completion Status**: ✅ Complete (All 5 tasks implemented)

---

## 🔒 Security Enhancements

### 1. Input Sanitization (`security_utils.py`)

**Purpose**: Prevent injection attacks and malformed data from compromising the system.

**File**: `backend/services/security_utils.py` (450+ lines)

#### CSV Security Validator
```python
# Core Features:
- Filename validation (prevent path traversal)
- File size validation (0-100MB)
- MIME type validation
- Cell value sanitization
- Row structure validation
- Dangerous pattern detection (formulas, scripts, SQL)
- CSV content sanitization with error handling
```

#### Key Protections:
- **Formula Injection**: Detects and removes leading `=`, `@`, `+`, `-`
- **Script Injection**: Blocks `<script>` tags and JavaScript URLs
- **Path Traversal**: Prevents `../` and null bytes in filenames
- **Buffer Overflow**: Enforces max length limits on cell values
- **SQL Injection**: Detects dangerous keywords and patterns

#### Input Validator
```python
# General input validation:
- Domain parameter validation (banking/healthcare/ecommerce)
- JSON structure validation
- String sanitization with length limits
- UTF-8 encoding validation
```

#### SQL Injection Prevention
```python
# Additional protections:
- Detects dangerous SQL keywords
- Removes SQL comment patterns
- Sanitizes quotes for database insertion
```

#### Usage Example:
```python
from services.security_utils import CSVSecurityValidator

# Validate file name
if CSVSecurityValidator.validate_filename(filename):
    print("Filename is safe")

# Validate file size
if CSVSecurityValidator.validate_file_size(file_size):
    print("File size within limits")

# Sanitize CSV data
sanitized_lines, errors = CSVSecurityValidator.sanitize_csv_data(file_content)
```

---

### 2. Rate Limiting (in `app.py`)

**Purpose**: Prevent API abuse and ensure fair resource utilization.

#### Implementation Details:
```python
# Configuration:
- Max requests: 10 per IP address
- Time window: 1 hour (3600 seconds)
- Storage: In-memory (Redis recommended for production)

# Response on limit exceeded:
- Status Code: 429 (Too Many Requests)
- Error Message: "Rate limit exceeded. Maximum 10 uploads per hour."
- Retry-After header included
```

#### Rate Limiting Class:
```python
class RateLimitStore:
    def __init__(self):
        self.requests = defaultdict(list)  # Track requests per IP
    
    def is_rate_limited(self, key: str, max_requests: int, 
                       time_window: int) -> bool:
        # Cleans old requests outside time window
        # Returns True if limit exceeded
        # Otherwise records request and returns False
```

#### Decorator Pattern:
```python
@app.route('/upload', methods=['POST'])
def upload_file():
    # Rate limiting check integrated into upload handler
    client_ip = request.remote_addr or 'unknown'
    if rate_limit_store.is_rate_limited(client_ip, 10, 3600):
        return jsonify({
            'error': 'Rate limit exceeded',
            'retry_after': 3600
        }), 429
```

#### Production Considerations:
- Replace in-memory store with Redis for distributed systems
- Monitor rate limit hits for security anomalies
- Configure limits based on your deployment requirements
- Use CloudFront/CDN rate limiting for additional protection

---

### 3. Security Headers (in `app.py`)

**Purpose**: Enhance browser-level security to prevent common web vulnerabilities.

#### Headers Implemented:

1. **X-Content-Type-Options: nosniff**
   - Prevents MIME-type sniffing attacks
   - Browsers must respect Content-Type headers

2. **X-Frame-Options: DENY**
   - Prevents clickjacking attacks
   - Blocks embedding in iframes

3. **X-XSS-Protection: 1; mode=block**
   - Legacy browser XSS protection
   - Stops reflected XSS attempts

4. **Content-Security-Policy (Strict Policy)**
   ```
   default-src 'self'                          # Only same-origin
   script-src 'self'                           # Scripts only from self
   style-src 'self' 'unsafe-inline'            # Styles with inline
   img-src 'self' data:                        # Images from self/data
   connect-src 'self' http://localhost:5000   # API connections
   frame-ancestors 'none'                      # No framing
   object-src 'none'                           # No plugins
   ```

5. **Referrer-Policy: strict-origin-when-cross-origin**
   - Controls referrer information leakage
   - Enhances privacy

6. **Permissions-Policy**
   - Disables microphone, camera, geolocation, payment APIs
   - Prevents unauthorized device access

#### Implementation:
```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Content-Security-Policy'] = "default-src 'self'; ..."
    # ... more headers
    return response
```

#### Production Recommendations:
- Enable `Strict-Transport-Security` for HTTPS-only access
- Update CSP policy based on your frontend resources
- Monitor CSP violations in browser console
- Use security header validator tools (Mozilla Observatory)

---

### 4. CORS Configuration (in `app.py`)

**Purpose**: Control cross-origin requests for frontend-backend communication.

#### Restrictive Configuration:
```python
CORS(app, resources={
    r"/upload": {
        "origins": [
            "http://localhost:3000",      # React frontend
            "http://localhost:5000"       # Fallback
        ],
        "methods": ["POST", "OPTIONS"],  # Only POST for security
        "allow_headers": ["Content-Type"],
        "max_age": 3600                   # Cache preflight 1 hour
    }
})
```

#### Production Updates:
- Replace `localhost` with your actual domain
- Use HTTPS URLs
- Remove unnecessary origins
- Monitor CORS errors in browser console

---

### 5. Request/Response Logging (in `app.py`)

**Purpose**: Create audit trails for security monitoring and debugging.

#### Logging Features:
```python
@app.before_request
def log_request():
    # Logs: Method, Path, IP, Content-Type
    logger.info(f"REQUEST - Method: {request.method}, "
                f"Path: {request.path}, IP: {request.remote_addr}")

@app.after_request
def log_response(response):
    # Logs: Status code
    logger.info(f"RESPONSE - Status: {response.status_code}")
```

#### Security Event Logging:
```python
SecurityLogger.log_validation_attempt(
    filename=filename,
    domain=domain,
    status='success'/'blocked'/'error',
    reason='optional reason'
)

SecurityLogger.log_security_event(
    event_type='RATE_LIMIT_EXCEEDED',
    details='IP: 192.168.1.1',
    severity='INFO'/'WARNING'/'CRITICAL'
)
```

#### Audit Trail Features:
- All validation attempts logged
- Rate limit violations tracked
- File sanitization warnings recorded
- Error conditions documented
- IP addresses captured for analysis

---

### 6. Error Handling (in `app.py`)

**Purpose**: Secure error responses without revealing system details.

#### Error Handlers:
```python
@app.errorhandler(413)  # File too large
@app.errorhandler(404)  # Not found
@app.errorhandler(500)  # Internal error
```

#### Features:
- No stack traces in responses (prevent information leakage)
- Consistent JSON error format
- Meaningful user messages
- Security logging for monitoring

---

## 🏗️ COBOL Mainframe Integration

### Architecture Overview

**File**: `backend/services/mainframe_service.py` (500+ lines)

**Design Pattern**: Message Queue with COBOL Bridge

```
┌─────────────────────────┐
│   Data Validation       │
│   System (Flask)        │
└───────────┬─────────────┘
            │
            ├─→ ValidationResult
            │
            ├─→ mainframe_service.py
            │   (Format conversion)
            │
            ├─→ RabbitMQ
            │   (VALIDATION_QUEUE)
            │
            ├─→ Message Consumer
            │   (On mainframe)
            │
            ├─→ COBOL Programs
            │   - CREDIT.RISK.CALC
            │   - COMPLIANCE.VALIDATE
            │   - DATA.ENRICH
            │
            ├─→ DB2 Database
            │   (Optional)
            │
            └─→ Response Queue
                (For status/results)
```

### Components

#### 1. MainframeConfig
```python
# Message Queue Settings
RABBITMQ_HOST = "localhost"
RABBITMQ_PORT = 5672
RABBITMQ_USER = "guest"
RABBITMQ_PASSWORD = "guest"

# Queue Names
VALIDATION_QUEUE = "validation.results"
MAINFRAME_QUEUE = "mainframe.requests"
RESPONSE_QUEUE = "mainframe.responses"

# COBOL Program Names (mappings to mainframe)
CREDIT_RISK_PROGRAM = "COBOL.CREDIT.RISK.CALC"
COMPLIANCE_CHECK_PROGRAM = "COBOL.COMPLIANCE.VALIDATE"
DATA_ENRICHMENT_PROGRAM = "COBOL.DATA.ENRICH"

# DB2 Configuration
DB2_DSNAME = "PROD.VALIDATION.DB"
DB2_TABLE = "VALIDATION_RESULTS"
```

#### 2. MainframeMessage
```python
class MainframeMessage:
    @staticmethod
    def create_validation_message(validation_result, domain):
        # Converts Flask validation_result to COBOL record format
        # Includes all: scores, anomalies, timestamps
        # Returns JSON-compatible COBOL record
```

**COBOL Record Structure**:
```cobol
01 VALIDATION-RECORD.
   05 VALIDATION-ID PIC 9(10).
   05 VALIDATION-DATE PIC 9(8).
   05 VALIDATION-TIME PIC 9(6).
   05 DOMAIN PIC X(20).
   05 TOTAL-RECORDS PIC 9(10).
   05 VALID-RECORDS PIC 9(10).
   05 INVALID-RECORDS PIC 9(10).
   05 QUALITY-SCORE PIC 999V99.
   05 ANOMALY-COUNT PIC 9(5).
   05 STATUS PIC X(10).
```

#### 3. MainframeService
```python
class MainframeService:
    
    def connect():
        # Establishes RabbitMQ connection
        # Returns connection status
    
    def disconnect():
        # Gracefully closes connection
    
    def send_validation_to_mainframe(validation_result, domain):
        # Publishes ValidationMessage to RABBITMQ
        # Mainframe consumer processes asynchronously
    
    def call_credit_risk_program(banking_record):
        # Calls COBOL program via transaction server
        # Returns risk assessment (HIGH/MEDIUM/LOW)
        # Domain: Banking only
    
    def call_compliance_check_program(validation_result):
        # Calls COBOL compliance validation
        # Returns compliance status (PASS/FAIL/REVIEW)
        # All domains
    
    def call_data_enrichment_program(record, domain):
        # Calls COBOL data enrichment
        # Enriches with mainframe historical data
        # All domains
```

#### 4. Integration Decorators
```python
@with_mainframe_processing
def validate_and_enrich(data, domain):
    # Decorator automatically:
    # 1. Runs standard validation
    # 2. Sends to mainframe
    # 3. Calls COBOL programs
    # 4. Returns enriched result
```

#### 5. Main Entry Points
```python
def process_with_mainframe(validation_result, domain):
    # Primary integration function
    # 1. Connect to RabbitMQ
    # 2. Send validation result
    # 3. Call domain-specific COBOL programs
    # 4. Attach mainframe results to response
    # 5. Return combined result

def store_to_db2(validation_result):
    # Future: Store to DB2 mainframe database
    # Uses pyodbc for connectivity
```

---

### Integration Steps

#### Phase 1: Setup (Prerequisites)
1. Install RabbitMQ on mainframe or separate message queue server
2. Configure queue names to match MainframeConfig
3. Deploy COBOL programs on mainframe
4. Create DB2 tables for validation history
5. Set up transaction server (CICS/IMS) for COBOL calls

#### Phase 2: Python Implementation
1. Install pika library: `pip install pika`
2. Update MainframeConfig with actual RabbitMQ details
3. Implement actual RabbitMQ connection in `connect()` method
4. Replace placeholder COBOL program calls with real logic

#### Phase 3: COBOL Integration
1. Create COBOL programs for each function
2. Map COBOL records to JSON for transport
3. Implement transaction server handlers
4. Test end-to-end message flow

#### Phase 4: Production Deployment
1. Enable mainframe_service in upload_routes.py
2. Deploy message queue infrastructure
3. Configure monitoring and alerting
4. Create fallback logic if mainframe is unavailable
5. Implement message queue persistence

---

### Current Status

**Implementation**: ✅ Placeholder complete with full architecture
**Testing**: ⏳ Awaiting RabbitMQ infrastructure setup
**Production**: ⏳ Ready once prerequisites are met

**Enable in Production**:
```python
# In upload_routes.py, uncomment:
from services.mainframe_service import process_with_mainframe
result = process_with_mainframe(result.to_dict(), domain)
```

---

## 📊 Phase 7 File Structure

```
backend/
├── app.py
│   ├── Security headers middleware
│   ├── Rate limiting system
│   ├── CORS configuration
│   ├── Request/response logging
│   └── Error handlers
│
├── services/
│   ├── security_utils.py (NEW)
│   │   ├── CSVSecurityValidator
│   │   ├── InputValidator
│   │   ├── SQLInjectionPrevention
│   │   └── SecurityLogger
│   │
│   ├── mainframe_service.py (NEW)
│   │   ├── MainframeConfig
│   │   ├── MainframeMessage
│   │   ├── MainframeService
│   │   ├── @with_mainframe_processing
│   │   └── Integration functions
│   │
│   ├── validation_service.py (Enhanced)
│   ├── anomaly_detection.py (Phase 5)
│   └── ...other services...
│
├── routes/
│   └── upload_routes.py (Enhanced)
│       └── /upload with security integration
│
└── PHASE7_IMPLEMENTATION.md (THIS FILE)
```

---

## 🧪 Testing & Validation

### Security Tests

#### 1. Filename Validation
```python
# Valid filenames
✓ sample_data.csv
✓ banking_records.txt
✓ healthcare-data_2024.csv

# Blocked filenames
✗ ../../../etc/passwd (path traversal)
✗ data\x00.csv (null byte)
✗ file.exe (invalid extension)
```

#### 2. SQL Injection Prevention
```python
# Dangerous inputs blocked
✗ '; DROP TABLE users; --
✗ " OR 1=1 --
✗ UNION SELECT * FROM passwords

# Clean inputs allowed
✓ Normal customer name
✓ Valid email address
✓ Numeric values
```

#### 3. Formula Injection Prevention
```python
# Blocked
✗ =1+1 (formula)
✗ @SUM(A:A) (command)
✗ +2*5 (hidden formula)

# Allowed
✓ 2+5 (regular text)
✓ Text with numbers like 15000
```

#### 4. Rate Limiting Test
```bash
# First 10 requests within window: ✓ 200 OK
# 11th request: ✗ 429 Too Many Requests
# After 1 hour: ✓ Counter resets
```

#### 5. Security Headers Verification
```bash
# Check headers in response
curl -I http://localhost:5000/upload

# Should include:
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'; ...
```

### Integration Tests

#### 1. File Upload with Sanitization
```bash
# Upload file with dangerous content
curl -F "file=@malicious.csv" \
     -F "domain=banking" \
     http://localhost:5000/upload

# File is sanitized before processing
# Response includes sanitization warnings
```

#### 2. Rate Limit Enforcement
```bash
# Simulate 11 uploads
for i in {1..11}; do
    curl -F "file=@test.csv" -F "domain=banking" \
         http://localhost:5000/upload
done

# Last one returns 429
```

#### 3. Input Validation
```bash
# Missing file: ✗ 400 Bad Request
# Invalid domain: ✗ 400 Bad Request
# Unsafe filename: ✗ 400 Bad Request
```

---

## 📋 Deployment Checklist

### Pre-Deployment

- [ ] Update CORS origins with production domain
- [ ] Configure rate limiting based on requirements
- [ ] Set up logging infrastructure (CloudWatch, ELK, etc.)
- [ ] Enable HTTPS/TLS
- [ ] Set `debug=False` in production
- [ ] Configure environment variables for secrets
- [ ] Test all security features
- [ ] Review security headers with Mozilla Observatory
- [ ] Set up RabbitMQ for mainframe integration (optional)

### Deployment

- [ ] Deploy to production server
- [ ] Verify security headers in response
- [ ] Test rate limiting functionality
- [ ] Monitor application logs
- [ ] Set up alerts for suspicious activity
- [ ] Configure backup and disaster recovery
- [ ] Document security procedures

### Post-Deployment

- [ ] Monitor rate limit violations
- [ ] Review security logs regularly
- [ ] Keep dependencies updated
- [ ] Test mainframe integration if enabled
- [ ] Conduct security audit
- [ ] Update documentation with production URLs

---

## 🔧 Configuration Reference

### Environment Variables (Recommended)

```bash
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here

# CORS Configuration
ALLOWED_ORIGINS=https://yourdomain.com

# Rate Limiting
RATE_LIMIT_MAX_REQUESTS=10
RATE_LIMIT_WINDOW=3600

# RabbitMQ Configuration
RABBITMQ_HOST=rabbitmq.example.com
RABBITMQ_PORT=5672
RABBITMQ_USER=your_username
RABBITMQ_PASSWORD=your_password

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/app.log
```

### Production Deployment Options

#### Option 1: Docker Container
```dockerfile
FROM python:3.8
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

#### Option 2: WSGI Server (Gunicorn)
```bash
# Install
pip install gunicorn

# Run
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Option 3: Azure App Service
```bash
# Deploy with Azure CLI
az webapp deployment source config-zip \
  --resource-group myResourceGroup \
  --name myAppService \
  --src-path myapp.zip
```

---

## 📚 Future Enhancements

### Phase 8+ Roadmap

1. **API Authentication**
   - JWT token-based authentication
   - OAuth2 social login
   - API key management

2. **Advanced Monitoring**
   - Real-time dashboard
   - Performance metrics
   - Security threat detection

3. **Enhanced Reporting**
   - PDF export
   - Excel exports
   - Scheduled reports

4. **Machine Learning**
   - Anomaly detection improvements
   - Pattern recognition
   - Predictive analytics

5. **Database Security**
   - Encryption at rest
   - Encryption in transit
   - Audit logging

---

## 🐛 Troubleshooting

### Issue: Rate Limit Enforcement Not Working

**Cause**: In-memory rate limit store reset on app restart  
**Solution**: Use Redis for persistent rate limiting  
```python
import redis
cache = redis.Redis(host='localhost', port=6379)
```

### Issue: CSP Blocking Resources

**Cause**: Content-Security-Policy too strict  
**Solution**: Update CSP directive to allow necessary sources  
```python
response.headers['Content-Security-Policy'] = (
    "default-src 'self'; script-src 'self' cdnjs.cloudflare.com; ..."
)
```

### Issue: CORS Errors in Frontend

**Cause**: Frontend origin not in whitelist  
**Solution**: Add domain to CORS configuration in app.py

### Issue: File Sanitization Too Aggressive

**Cause**: Legitimate data being removed  
**Solution**: Review dangerous patterns in security_utils.py

---

## 📞 Support

For issues or questions:
1. Check this documentation
2. Review security_utils.py comments
3. Review mainframe_service.py architecture
4. Check application logs
5. Contact development team

---

## Version History

- **v2.0.0** (Phase 7) - Security & COBOL Integration ✅
- **v1.5.0** (Phase 6) - Frontend Dashboard 
- **v1.3.0** (Phase 5) - Anomaly Detection
- **v1.2.0** (Phase 3-4) - Database Integration
- **v1.0.0** (Phase 1-2) - Initial System

---

**Last Updated**: 2026-04-12  
**Maintained By**: AI Data Validation Team  
**Status**: ✅ Production Ready (with prerequisites)
