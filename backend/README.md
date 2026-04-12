# AI Data Validation System - Backend

A Flask-based REST API for multi-domain data validation supporting Banking, Healthcare, and E-commerce domains.

## 📋 Overview

This backend service provides APIs to validate data across multiple domains with domain-specific validation rules:

- **Banking**: Validate customer financial profiles (age, income, credit score)
- **Healthcare**: Validate patient health records (age, blood group)
- **E-commerce**: Validate product inventory data (price, stock)

### Future Integration Points
- COBOL Mainframe Systems (message queue integration)
- DB2 Database (regulatory compliance and historical data)
- Microservices Architecture

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

**GET** `/`

Returns a simple status message to verify the backend is running.

#### Example Request
```bash
curl http://localhost:5000/
```

#### Example Response
```json
{
  "message": "Backend Running"
}
```

---

### 2. File Upload and Validation Endpoint

**POST** `/upload`

Uploads a CSV file and validates the data according to domain-specific rules.

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

#### Response Format
```json
{
  "total_records": integer,
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

## 🔒 Security Considerations

### Current Features
- File extension validation (CSV/TXT only)
- File size limit (16MB)
- Secure filename handling (prevents path traversal)
- CORS enabled for frontend communication
- Input sanitization and error handling

### Recommended for Production
- Implement authentication (JWT tokens)
- Add rate limiting
- Use HTTPS only
- Implement request logging
- Add data encryption for sensitive information
- Deploy with production WSGI server (Gunicorn)
- Implement input validation for CSV headers
- Add database transactions for atomicity
- Implement audit logging

---

## 🔄 Modular Architecture

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

**Version:** 1.0.0  
**Last Updated:** 2024  
**Author:** AI Data Validation Team
