# AI Data Validation System - Backend

A Flask-based REST API for enterprise-grade multi-domain data validation with anomaly detection, database persistence, and security features.

## 📋 Overview

**Version:** 2.0.0 (Phase 7 - Security & COBOL Integration)  
**Status:** ✅ Production Ready

This backend service provides APIs to validate data across multiple domains with comprehensive quality metrics:

- **Banking**: Customer financial profiles (age, income, credit score, SSN)
- **Healthcare**: Patient health records (age, blood group, heart rate, cholesterol)
- **E-commerce**: Product inventory data (price, stock, rating)

### Key Features

**✅ Phase 1-4: Core Validation**
- Domain-specific validation rules
- Quality scoring (3 dimensions: completeness, validity, consistency)
- Modular architecture
- Error tracking and reporting

**✅ Phase 5: Anomaly Detection**
- Statistical outlier detection
- Domain-specific anomaly rules
- Separate anomaly tracking (non-blocking)
- Anomaly severity classification (HIGH/MEDIUM/LOW/INFO)

**✅ Phase 6: Dashboard Persistence**
- SQLite3 database for result persistence
- Historical data retrieval
- Aggregated statistics and domain stats

**✅ Phase 7: Enterprise Security & Mainframe**
- Input validation and CSV sanitization
- Rate limiting (10 uploads/hour per IP)
- Security headers (XSS, clickjacking, MIME-sniffing protection)
- Comprehensive audit logging
- COBOL mainframe integration framework (RabbitMQ ready)
- DB2 database integration placeholder

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Navigate to the backend directory**
```bash
cd backend
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

The server will start at `http://localhost:5000`

## 📡 API Endpoints

### 1. Health Check Endpoint

**GET** `/health`

Returns system health status and version information.

#### Example Response
```json
{
  "status": "healthy",
  "timestamp": "2026-04-12T10:30:45.123456",
  "version": "2.0.0"
}
```

---

### 2. File Upload and Validation Endpoint

**POST** `/upload`

Uploads a CSV file and validates the data according to domain-specific rules with quality metrics and anomaly detection.

#### Request Format
```
Content-Type: multipart/form-data

file: <CSV file>
domain: banking | healthcare | ecommerce
```

#### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file` | File | Yes | CSV/TXT file containing data to validate |
| `domain` | String | Yes | Validation domain: `banking`, `healthcare`, or `ecommerce` |

#### Response Format (Complete with Phase 5-7 Data)
```json
{
  "record_id": 42,
  "total_records": 100,
  "valid_records": 95,
  "invalid_records": 5,
  
  "completeness_score": 98.0,
  "validity_score": 95.0,
  "consistency_score": 92.0,
  "final_score": 95.2,
  "quality_rating": "Good",
  
  "anomaly_count": 3,
  "anomaly_score": 3.0,
  "anomalies": [
    {
      "row": 12,
      "field": "income",
      "value": 15000000,
      "reason": "Extreme income value",
      "severity": "HIGH"
    }
  ],
  
  "stored": true,
  "timestamp": "2026-04-12T10:30:45.123456",
  "errors": [
    "Row 5: Invalid age 15: Must be between 18 and 80",
    "Row 12: Income exceeds reasonable range"
  ]
}
```

#### Quality Metrics Explained

**Completeness Score** (0-100%): Percentage of non-null fields  
**Validity Score** (0-100%): Percentage of values matching domain rules  
**Consistency Score** (0-100%): Percentage of records without conflicts  
**Final Score** (Weighted): 40% Completeness + 40% Validity + 20% Consistency  

**Quality Rating**:
- 🟢 **Excellent**: Final Score ≥ 95%
- 🔵 **Good**: Final Score 85-94%
- 🟡 **Acceptable**: Final Score 70-84%
- 🔴 **Poor**: Final Score < 70%

#### Anomaly Detection

Automatically identifies statistical outliers using domain-specific rules:

**Banking**: 
- Income > $10,000,000
- Age patterns analysis
- Credit score extremes

**Healthcare**:
- Age > 110 years
- Unusual blood group combinations
- Heart rate outliers

**E-commerce**:
- Price > $100,000
- Stock anomalies
- Rating inconsistencies
  "valid_records": integer,
  "invalid_records": integer,
  "score_percentage": float,
  "errors": [
    "Row X: error message"
  ]
}
```

#### Response Fields
| Field | Type | Description |
|-------|------|-------------|
| `total_records` | int | Total number of records processed |
| `valid_records` | int | Number of records that passed validation |
| `invalid_records` | int | Number of records that failed validation |
| `score_percentage` | float | Percentage of valid records (0-100) |
| `errors` | array | List of validation error messages with row numbers |

#### Response Codes
| Code | Description |
|------|-------------|
| 200 | Validation completed successfully |
| 400 | Missing/invalid file or domain parameter |
| 413 | File size exceeds 16MB limit |
| 500 | Server error |

---

## 🎯 Domain-Specific Validation Rules

### Banking Domain

**Expected CSV Headers:** `age`, `income`, `credit_score`

**Validation Rules:**
- **Age**: Must be between 18 and 80 (legal working age)
- **Income**: Must be greater than 0
- **Credit Score**: Must be between 300 and 850 (FICO range)

**Example CSV:**
```csv
age,income,credit_score
28,55000,750
35,75000,680
42,95000,720
```

**Example Request:**
```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@sample_banking.csv" \
  -F "domain=banking"
```

**Example Response:**
```json
{
  "total_records": 20,
  "valid_records": 19,
  "invalid_records": 1,
  "score_percentage": 95.0,
  "errors": [
    "Row 15: Invalid age 15: Must be between 18 and 80"
  ]
}
```

---

### Healthcare Domain

**Expected CSV Headers:** `age`, `blood_group`

**Validation Rules:**
- **Age**: Must be between 0 and 120 (realistic human age range)
- **Blood Group**: Must be one of [A+, A-, B+, B-, O+, O-, AB+, AB-]

**Example CSV:**
```csv
age,blood_group
28,O+
35,A+
42,B+
55,AB+
```

**Example Request:**
```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@sample_healthcare.csv" \
  -F "domain=healthcare"
```

**Example Response:**
```json
{
  "total_records": 20,
  "valid_records": 19,
  "invalid_records": 1,
  "score_percentage": 95.0,
  "errors": [
    "Row 15: Invalid age 150: Must be between 0 and 120"
  ]
}
```

---

### E-commerce Domain

**Expected CSV Headers:** `price`, `stock`

**Validation Rules:**
- **Price**: Must be greater than 0 and less than 9,999,999
- **Stock**: Must be greater than or equal to 0

**Example CSV:**
```csv
price,stock
29.99,150
49.99,200
99.99,50
```

**Example Request:**
```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@sample_ecommerce.csv" \
  -F "domain=ecommerce"
```

**Example Response:**
```json
{
  "total_records": 20,
  "valid_records": 18,
  "invalid_records": 2,
  "score_percentage": 90.0,
  "errors": [
    "Row 11: Invalid price -10.5: Must be greater than 0",
    "Row 20: Invalid price -5.0: Must be greater than 0",
    "Row 20: Invalid stock -50: Cannot be negative"
  ]
}
```

---

## 📁 Project Structure

```
backend/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── sample_banking.csv          # Sample banking data
├── sample_healthcare.csv       # Sample healthcare data
├── sample_ecommerce.csv        # Sample e-commerce data
├── uploads/                    # Directory where uploaded files are stored
└── venv/                       # Virtual environment (auto-created)
```

---

## 🧪 Testing

### Test with Sample Files

```bash
# Banking validation
curl -X POST http://localhost:5000/upload \
  -F "file=@sample_banking.csv" \
  -F "domain=banking"

# Healthcare validation
curl -X POST http://localhost:5000/upload \
  -F "file=@sample_healthcare.csv" \
  -F "domain=healthcare"

# E-commerce validation
curl -X POST http://localhost:5000/upload \
  -F "file=@sample_ecommerce.csv" \
  -F "domain=ecommerce"
```

### Using Python Requests Library

```python
import requests

# Upload file
files = {'file': open('sample_banking.csv', 'rb')}
data = {'domain': 'banking'}
response = requests.post('http://localhost:5000/upload', files=files, data=data)

# Print results
print(response.json())
```

### Using Postman

1. Open Postman
2. Create new POST request to `http://localhost:5000/upload`
3. Go to "Body" tab → Select "form-data"
4. Add fields:
   - `file`: Select your CSV file
   - `domain`: Enter domain name (banking/healthcare/ecommerce)
5. Click "Send"

---

## 🔒 Phase 7: Security Features

### Security Layer (app.py)
- ✅ **Security Headers**: XSS, clickjacking, MIME-sniffing protection
- ✅ **Rate Limiting**: 10 uploads per hour per IP address
- ✅ **Input Validation**: Domain, filename, and file size validation
- ✅ **CSV Sanitization**: Remove dangerous patterns (formulas, scripts, SQL)
- ✅ **Comprehensive Logging**: Audit trail of all operations
- ✅ **Error Handling**: Secure error responses without stack traces

### Input Validation (security_utils.py)
- Filename validation (prevent path traversal)
- File size validation (0-100MB)
- MIME type detection (CSV/text only)
- CSV content sanitization
- Dangerous pattern blocking:
  - Formula injection (=, @, +, -)
  - Script injection (<script>, javascript:)
  - SQL injection keywords
  - Null bytes and special characters

### Rate Limiting
```
Limit: 10 requests/hour per IP
Response: 429 (Too Many Requests)
Cleanup: Automatic request cleanup
```

### Request Validation Flow
1. Check rate limit → 2. Validate domain → 3. Validate filename → 4. Validate file size 
→ 5. Validate file type → 6. Sanitize content → 7. Process validation → 8. Store result

### Production Deployment
- ✅ Update CORS origins with your domain
- ✅ Set `debug=False`
- ✅ Use HTTPS/TLS
- ✅ Deploy with Gunicorn
- ✅ Monitor security logs
- ✅ Keep dependencies updated

---

## 🏗️ Phase 7: Mainframe Integration

### COBOL Integration Framework (mainframe_service.py)
- Message queue pattern (RabbitMQ ready)
- COBOL record format conversion
- 3 COBOL programs supported:
  1. **CREDIT.RISK.CALC** - Banking risk assessment
  2. **COMPLIANCE.VALIDATE** - Regulatory compliance
  3. **DATA.ENRICH** - Data enrichment from mainframe

### Message Flow
```
Validation Result → COBOL Record Format → RabbitMQ Queue 
  → Mainframe COBOL Programs → DB2 Database → Response Queue
```

### Enable Mainframe Integration
1. Set up RabbitMQ server
2. Deploy COBOL programs
3. Update MainframeConfig in mainframe_service.py
4. Uncomment integration code in upload_routes.py

---

## 📚 Documentation

### Backend Documentation
- **API_TESTING_GUIDE.md** - How to test all endpoints
- **DEVELOPER_GUIDE.md** - Development guidelines and architecture
- **IMPLEMENTATION_SUMMARY.md** - System architecture details
- **QUICK_REFERENCE.md** - Quick command reference

### Phase-Specific Documentation  
- **PHASE5_IMPLEMENTATION.md** - Anomaly detection details
- **PHASE7_IMPLEMENTATION.md** - Complete security & COBOL guide
- **PHASE7_QUICK_REFERENCE.md** - Phase 7 quick start

---

## 🧪 Testing

The code is designed with modularity in mind for future integration:

### Domain Separations
Each domain has its own validation function:
- `validate_banking_record()` - Banking rules
- `validate_healthcare_record()` - Healthcare rules
- `validate_ecommerce_record()` - E-commerce rules

### Extensibility Points
1. **Add New Domain**: Create new validation function and add to `validators` dictionary
2. **Enhance Validation**: Update validation functions without affecting other domains
3. **Database Integration**: Connect to DB2 in validation functions
4. **COBOL Integration**: Use `ValidationResult` structure as COBOL record interface
5. **Message Queue**: Route validation requests through message brokers

---

## 🚀 Future Integration Examples

### COBOL Mainframe Integration
```python
# Future pseudo-code for COBOL integration
from message_queue import publish_event

def validate_with_cobol(record, domain):
    # Send to COBOL via message queue
    publish_event('validation_request', {
        'record': record,
        'domain': domain
    })
    # Wait for response
    result = wait_for_validation_result()
    return result
```

### DB2 Database Integration
```python
# Future pseudo-code for DB2 integration
from db2_connector import DB2Connection

def validate_against_database(record, domain):
    db = DB2Connection()
    
    # Banking example
    if domain == 'banking':
        regulatory_rules = db.fetch_rules('BANKING_RULES')
        return apply_regulatory_validation(record, regulatory_rules)
```

---

## 🐛 Troubleshooting

### File Upload Errors

**Error: "No file provided"**
- Ensure `file` field is included in multipart form-data

**Error: "File type not allowed"**
- Only CSV and TXT files are allowed
- Rename your file with correct extension

**Error: "File too large"**
- Maximum file size is 16MB
- Split large files into smaller chunks

### Validation Errors

**Error: "Unknown domain"**
- Check domain spelling: must be `banking`, `healthcare`, or `ecommerce`
- Domain is case-insensitive

**Error: "Data type error"**
- Check CSV headers match expected fields
- Ensure numeric fields contain valid numbers
- Check for special characters or encoding issues

### Server Errors

**Error: "Internal server error"**
- Check console for detailed error messages
- Verify CSV file is properly formatted
- Check file permissions in uploads directory

---

## 📊 Performance Considerations

- Current implementation processes files sequentially
- For large files (>100k records), consider batch processing
- Recommended file size: <5MB for optimal performance
- Database integration will significantly improve performance for repeated validations

---

## 📝 Configuration

### Environment Variables (Future)
Create `.env` file in backend directory:
```
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=db2://connection_string
COBOL_QUEUE_URL=amqp://broker_url
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 2.3.3 | Web framework |
| Flask-CORS | 4.0.0 | Cross-Origin Resource Sharing |
| Werkzeug | 2.3.7 | WSGI utilities |
| Gunicorn | 21.2.0 | Production WSGI server |
| python-dotenv | 1.0.0 | Environment variables |

---

## 🤝 Contributing

When adding new domains or features:

1. Follow the existing code structure
2. Add comprehensive comments
3. Create validation function for new domain
4. Add to `validators` dictionary in `validate_data()`
5. Create sample CSV file
6. Update documentation
7. Test thoroughly

---

## 📄 License

This project is part of the AI Data Validation System.

---

## 👨‍💻 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the sample CSV files
3. Check console error messages
4. Verify file format and domain names

---

## 🎯 Roadmap

- [ ] Database integration (DB2)
- [ ] COBOL mainframe connectivity
- [ ] Advanced analytics dashboard
- [ ] Machine learning-based anomaly detection
- [ ] Real-time validation streaming
- [ ] Webhook support for async processing
- [ ] Advanced reporting and export features
- [ ] Multi-user authentication and role-based access

---

**Version:** 2.0.0 (Phase 7)  
**Last Updated:** April 12, 2026  
**Status:** ✅ Production Ready  
**Author:** AI Data Validation Team
