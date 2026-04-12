# Developer Guide - AI Data Validation System

Comprehensive guide for developers to understand, extend, and maintain the backend system.

## 📚 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Code Structure](#code-structure)
3. [How It Works](#how-it-works)
4. [Adding New Domains](#adding-new-domains)
5. [Database Integration](#database-integration)
6. [COBOL Integration](#cobol-integration)
7. [API Modifications](#api-modifications)
8. [Error Handling](#error-handling)
9. [Testing Guidelines](#testing-guidelines)
10. [Performance Optimization](#performance-optimization)

---

## Architecture Overview

### High-Level Design

```
┌─────────────┐       ┌────────────────┐       ┌─────────────────┐
│   Frontend  │───→   │  Flask Backend │───→   │  File System    │
│   (React)   │       │   (Python)     │       │  & Validation   │
└─────────────┘       └────────────────┘       └─────────────────┘
                             │
                             ├→ Domain Validators
                             │  ├─ Banking
                             │  ├─ Healthcare
                             │  └─ E-commerce
                             │
                             └→ Future: Database & COBOL
```

### Key Components

1. **API Layer**: Flask routes for HTTP communication
2. **Validation Layer**: Domain-specific validation functions
3. **Data Model**: `ValidationResult` class for consistency
4. **File Handling**: Secure file upload and processing
5. **Error Management**: Comprehensive error handling and reporting

---

## Code Structure

### Main Files

```
backend/
├── app.py                    # Main application file
├── requirements.txt          # Python dependencies
├── .env.example              # Environment configuration template
├── .gitignore                # Git ignore patterns
├── start.bat                 # Windows quick start script
├── start.sh                  # Unix/Linux quick start script
├── README.md                 # User documentation
├── API_TESTING_GUIDE.md      # Testing documentation
├── DEVELOPER_GUIDE.md        # This file
├── sample_banking.csv        # Sample banking data
├── sample_healthcare.csv     # Sample healthcare data
├── sample_ecommerce.csv      # Sample e-commerce data
├── uploads/                  # Directory for uploaded files
└── venv/                     # Python virtual environment
```

### Code Sections in app.py

```
1. Module Imports (line 1-20)
   └─ Flask, CORS, OS, CSV, Werkzeug, DateTime

2. Flask App Initialization (line 22-29)
   └─ Create Flask app and enable CORS

3. Configuration (line 31-43)
   └─ Upload folder, file extensions, size limits

4. Utility Functions (line 45-60)
   └─ allowed_file(): Check file extensions

5. Data Structures (line 62-98)
   └─ ValidationResult class

6. Banking Domain Validation (line 100-145)
   └─ validate_banking_record(): Validate financial data

7. Healthcare Domain Validation (line 147-185)
   └─ validate_healthcare_record(): Validate health data

8. E-commerce Domain Validation (line 187-227)
   └─ validate_ecommerce_record(): Validate product data

9. Validation Orchestrator (line 229-287)
   └─ validate_data(): Route to domain validators

10. API Endpoints (line 289-375)
    └─ GET /      - Health check
    └─ POST /upload - File upload and validation

11. Error Handlers (line 377-402)
    └─ 413, 404, 500 status codes

12. Application Entry Point (line 404-415)
    └─ Flask app run configuration
```

---

## How It Works

### Request Flow

```
1. User sends POST /upload request
   ├─ File: sample_banking.csv
   └─ Domain: "banking"
         │
         ↓
2. Flask receives request
   ├─ Validates file exists
   ├─ Validates domain is specified
   └─ Validates file type
         │
         ↓
3. File is saved securely
   ├─ Generate timestamp prefix
   ├─ Use secure filename
   └─ Save to uploads/ folder
         │
         ↓
4. validate_data() is called
   ├─ Read CSV file
   ├─ Parse headers
   └─ For each row:
      ├─ Call validate_banking_record()
      ├─ Check age, income, credit_score
      └─ Record errors if any
         │
         ↓
5. ValidationResult object is created
   ├─ total_records = 20
   ├─ valid_records = 19
   ├─ invalid_records = 1
   └─ errors = [list of errors]
         │
         ↓
6. Result is converted to JSON
   ├─ score_percentage is calculated
   └─ Response is sent to frontend
         │
         ↓
7. Frontend receives and displays results
   ├─ Shows validation score
   ├─ Lists invalid records
   └─ Displays error details
```

### Validation Process

```
CSV File (20 records)
    │
    ├─ Row 1: Headers (age, income, credit_score)
    │
    ├─ Rows 2-20: Data rows (processed one by one)
    │   │
    │   ├─ Row 2: age=28, income=55000, credit_score=750
    │   │  └─ All valid ✓
    │   │
    │   ├─ Row 3: age=35, income=75000, credit_score=680
    │   │  └─ All valid ✓
    │   │
    │   ├─ ...
    │   │
    │   └─ Row 15: age=15, income=20000, credit_score=500
    │      ├─ age=15 is INVALID (< 18) ✗
    │      ├─ credit_score=500 is INVALID (< 300) ✗
    │      └─ Record marked as invalid
    │
    └─ Results aggregated
       ├─ Total: 20
       ├─ Valid: 18
       ├─ Invalid: 2
       └─ Score: 90%
```

---

## Adding New Domains

### Step-by-Step Guide

#### 1. Design Validation Rules

Define what fields your domain needs and what the validation rules are.

**Example: Education Domain**

```
Fields:
- student_id: String
- gpa: Float (0.0-4.0)
- attendance_rate: Float (0-100)

Validation Rules:
- student_id: Not empty, alphabetic
- gpa: Between 0.0 and 4.0
- attendance_rate: Between 0 and 100
```

#### 2. Create Validation Function

Add to `app.py` in the appropriate section:

```python
# ==================== EDUCATION DOMAIN VALIDATION ====================

def validate_education_record(record):
    """
    Validate a single education record.
    
    Expected fields:
    - student_id: String (unique identifier)
    - gpa: Float between 0.0 and 4.0
    - attendance_rate: Float between 0 and 100
    
    Future Integration:
    - Connect to student information systems
    - Validate against enrollment records
    - Update grade databases
    
    Args:
        record (dict): Dictionary containing education data
        
    Returns:
        tuple: (is_valid: bool, errors: list of error messages)
    """
    try:
        student_id = str(record.get('student_id', '')).strip()
        gpa = float(record.get('gpa', 0))
        attendance_rate = float(record.get('attendance_rate', 0))
        
        errors = []
        
        # Student ID validation
        if not student_id or not student_id.isalnum():
            errors.append(f"Invalid student_id '{student_id}': Must be non-empty alphanumeric")
        
        # GPA validation
        if gpa < 0.0 or gpa > 4.0:
            errors.append(f"Invalid GPA {gpa}: Must be between 0.0 and 4.0")
        
        # Attendance rate validation
        if attendance_rate < 0 or attendance_rate > 100:
            errors.append(f"Invalid attendance_rate {attendance_rate}: Must be between 0 and 100")
        
        return len(errors) == 0, errors
    
    except (ValueError, TypeError) as e:
        return False, [f"Data type error in education record: {str(e)}"]
```

#### 3. Register Domain in Validator Dictionary

In the `validate_data()` function, update the validators dictionary:

```python
def validate_data(file_path, domain):
    result = ValidationResult()
    domain = domain.lower()
    
    # Map domains to their respective validation functions
    validators = {
        'banking': validate_banking_record,
        'healthcare': validate_healthcare_record,
        'ecommerce': validate_ecommerce_record,
        'education': validate_education_record  # NEW DOMAIN
    }
    
    # ... rest of the function
```

#### 4. Create Sample Data File

Create `sample_education.csv`:

```csv
student_id,gpa,attendance_rate
STU001,3.8,95
STU002,3.2,88
STU003,3.9,92
STU004,2.5,75
STU005,1.8,60
```

#### 5. Test the New Domain

```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@sample_education.csv" \
  -F "domain=education"
```

#### 6. Update Documentation

Update `README.md` with the new domain details.

---

## Database Integration

### Adding DB2 Connectivity

#### 1. Update requirements.txt

```
ibm-db==3.1.0
ibm-db-sa==0.4.1
SQLAlchemy==2.0.0
```

#### 2. Create Database Module

Create `database.py`:

```python
"""
Database module for DB2 integration
"""

import ibm_db
from functools import lru_cache

class DB2Connection:
    """Manages DB2 database connections"""
    
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = None
    
    def connect(self):
        """Establish connection to DB2"""
        try:
            self.connection = ibm_db.connect(self.connection_string, "", "")
            print("Connected to DB2 successfully")
        except ibm_db.DatabaseError as e:
            print(f"Failed to connect to DB2: {e}")
            raise
    
    def get_banking_rules(self):
        """Fetch banking validation rules from DB2"""
        query = "SELECT * FROM BANKING_VALIDATION_RULES"
        stmt = ibm_db.exec_immediate(self.connection, query)
        result = ibm_db.fetch_assoc(stmt)
        return result
    
    def validate_customer(self, customer_id):
        """Look up customer in DB2"""
        query = f"SELECT * FROM CUSTOMERS WHERE CUSTOMER_ID = '{customer_id}'"
        stmt = ibm_db.exec_immediate(self.connection, query)
        result = ibm_db.fetch_assoc(stmt)
        return result
    
    def close(self):
        """Close database connection"""
        if self.connection:
            ibm_db.close(self.connection)
```

#### 3. Integrate with Validation

Update validation function in `app.py`:

```python
from database import DB2Connection

def validate_banking_record_with_db(record):
    """
    Validate banking record with DB2 lookup
    """
    try:
        age = int(record.get('age', 0))
        income = float(record.get('income', 0))
        credit_score = int(record.get('credit_score', 0))
        customer_id = record.get('customer_id')
        
        errors = []
        
        # Basic validations
        if age < 18 or age > 80:
            errors.append(f"Invalid age {age}")
        
        # DB2 lookup
        if customer_id:
            db = DB2Connection(os.getenv('DATABASE_URL'))
            db.connect()
            customer = db.validate_customer(customer_id)
            if not customer:
                errors.append(f"Customer {customer_id} not found in database")
            db.close()
        
        return len(errors) == 0, errors
    
    except Exception as e:
        return False, [f"Database error: {str(e)}"]
```

---

## COBOL Integration

### Message Queue Approach

#### 1. Install Message Queue Library

Add to `requirements.txt`:
```
pika==1.3.1
```

#### 2. Create Message Queue Module

Create `message_queue.py`:

```python
"""
Message Queue module for COBOL integration via RabbitMQ
"""

import pika
import json
from datetime import datetime

class ValidationQueue:
    """Manages communication with COBOL systems via RabbitMQ"""
    
    def __init__(self, rabbitmq_url):
        self.rabbitmq_url = rabbitmq_url
        self.connection = None
        self.channel = None
    
    def connect(self):
        """Connect to RabbitMQ"""
        self.connection = pika.BlockingConnection(
            pika.URLParameters(self.rabbitmq_url)
        )
        self.channel = self.connection.channel()
    
    def send_to_cobol(self, domain, record):
        """
        Send record to COBOL for legacy validation
        
        Message format:
        {
            "id": unique_id,
            "domain": domain_name,
            "record": data,
            "timestamp": ISO_timestamp,
            "status": "pending"
        }
        """
        message = {
            "id": f"VAL_{datetime.now().timestamp()}",
            "domain": domain,
            "record": record,
            "timestamp": datetime.now().isoformat(),
            "status": "pending"
        }
        
        self.channel.basic_publish(
            exchange='',
            routing_key='cobol_validation_queue',
            body=json.dumps(message)
        )
    
    def receive_validation_result(self):
        """Receive validation result from COBOL"""
        def callback(ch, method, properties, body):
            result = json.loads(body)
            return result
        
        self.channel.basic_consume(
            queue='validation_result_queue',
            on_message_callback=callback
        )
```

#### 3. Update API to Use Message Queue

```python
from message_queue import ValidationQueue

@app.route('/upload', methods=['POST'])
def upload_file():
    # ... existing code ...
    
    # If COBOL integration is enabled
    if os.getenv('ENABLE_COBOL_INTEGRATION') == 'True':
        queue = ValidationQueue(os.getenv('RABBITMQ_URL'))
        queue.connect()
        
        for row_num, record in enumerate(csv_rows, start=2):
            # Send to COBOL for validation
            queue.send_to_cobol(domain, record)
            
            # Wait for result
            result = queue.receive_validation_result()
            # Process result
        
        queue.connection.close()
```

---

## API Modifications

### Adding New Endpoints

#### Example: Get Validation History

```python
@app.route('/validation-history', methods=['GET'])
def get_validation_history():
    """
    Get validation history for a domain
    
    Query Parameters:
    - domain: Domain name (banking/healthcare/ecommerce)
    - limit: Number of results (default: 10)
    - offset: Result offset for pagination (default: 0)
    
    Returns:
        list: List of validation results
    """
    try:
        domain = request.args.get('domain', 'banking')
        limit = int(request.args.get('limit', 10))
        offset = int(request.args.get('offset', 0))
        
        # TODO: Query database for validation history
        # For now, return empty list
        return jsonify({
            'history': [],
            'total': 0,
            'limit': limit,
            'offset': offset
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

#### Example: Batch Validation API

```python
@app.route('/batch-upload', methods=['POST'])
def batch_upload_files():
    """
    Upload and validate multiple files in a batch
    
    Request:
    {
        "files": [
            {
                "filename": "file1.csv",
                "domain": "banking"
            },
            {
                "filename": "file2.csv",
                "domain": "healthcare"
            }
        ]
    }
    
    Returns:
        dict: Results for each file
    """
    try:
        files = request.files.getlist('files')
        domains = request.form.getlist('domains')
        
        results = []
        
        for file, domain in zip(files, domains):
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                
                result = validate_data(file_path, domain)
                results.append(result.to_dict())
        
        return jsonify({'results': results}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

---

## Error Handling

### Best Practices

#### 1. Specific Error Messages

```python
# ✓ GOOD: Specific error message
raise ValueError("Age must be between 18 and 80, got 15")

# ✗ BAD: Generic error message
raise ValueError("Invalid age")
```

#### 2. Include Context Information

```python
# ✓ GOOD: Include row number and field name
errors.append(f"Row {row_num}, Field 'age': Must be between 18 and 80")

# ✗ BAD: No context
errors.append("Invalid value")
```

#### 3. Custom Exception Classes

```python
class ValidationError(Exception):
    """Base validation error"""
    pass

class BankingValidationError(ValidationError):
    """Banking domain validation error"""
    pass

class DatabaseError(Exception):
    """Database connection error"""
    pass
```

---

## Testing Guidelines

### Unit Tests

Create `test_validators.py`:

```python
import unittest
from app import validate_banking_record, validate_healthcare_record, validate_ecommerce_record

class TestBankingValidator(unittest.TestCase):
    
    def test_valid_banking_record(self):
        record = {'age': 28, 'income': 55000, 'credit_score': 750}
        is_valid, errors = validate_banking_record(record)
        self.assertTrue(is_valid)
        self.assertEqual(errors, [])
    
    def test_invalid_age(self):
        record = {'age': 15, 'income': 55000, 'credit_score': 750}
        is_valid, errors = validate_banking_record(record)
        self.assertFalse(is_valid)
        self.assertTrue(any('age' in e.lower() for e in errors))
    
    def test_invalid_credit_score(self):
        record = {'age': 28, 'income': 55000, 'credit_score': 250}
        is_valid, errors = validate_banking_record(record)
        self.assertFalse(is_valid)
        self.assertTrue(any('credit' in e.lower() for e in errors))

class TestHealthcareValidator(unittest.TestCase):
    
    def test_valid_healthcare_record(self):
        record = {'age': 35, 'blood_group': 'O+'}
        is_valid, errors = validate_healthcare_record(record)
        self.assertTrue(is_valid)
        self.assertEqual(errors, [])
    
    def test_invalid_blood_group(self):
        record = {'age': 35, 'blood_group': 'XYZ'}
        is_valid, errors = validate_healthcare_record(record)
        self.assertFalse(is_valid)
        self.assertTrue(any('blood' in e.lower() for e in errors))

if __name__ == '__main__':
    unittest.main()
```

### Run Tests

```bash
python -m unittest test_validators.py
```

---

## Performance Optimization

### Current Bottlenecks

1. **File I/O**: Reading large CSV files sequentially
2. **Memory Usage**: Storing all errors in memory
3. **Database Queries**: (Future) N+1 query problems

### Optimization Strategies

#### 1. Streaming Large Files

```python
import pandas as pd

def validate_data_streaming(file_path, domain, chunk_size=1000):
    """
    Validate data using streaming to handle large files
    """
    result = ValidationResult()
    validator = get_validator(domain)
    
    # Read CSV in chunks
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        for index, row in chunk.iterrows():
            result.total_records += 1
            is_valid, errors = validator(row.to_dict())
            
            if is_valid:
                result.valid_records += 1
            else:
                result.invalid_records += 1
                result.errors.extend(errors)
    
    return result
```

#### 2. Batch Database Inserts

```python
def bulk_insert_validations(records, domain):
    """
    Batch insert validation results into database
    """
    db = DB2Connection(os.getenv('DATABASE_URL'))
    db.connect()
    
    # Insert 100 records at a time
    for i in range(0, len(records), 100):
        batch = records[i:i+100]
        db.bulk_insert('VALIDATION_RESULTS', batch)
    
    db.close()
```

#### 3. Caching Rules

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_validation_rules(domain):
    """
    Cache validation rules to avoid repeated database lookups
    """
    db = DB2Connection(os.getenv('DATABASE_URL'))
    db.connect()
    rules = db.get_rules(domain)
    db.close()
    return rules
```

---

## Deployment Checklist

- [ ] Update `.env` file with production values
- [ ] Install Gunicorn: `pip install gunicorn`
- [ ] Test with Gunicorn: `gunicorn -w 4 -b 0.0.0.0:5000 app:app`
- [ ] Set up SSL/HTTPS
- [ ] Configure reverse proxy (nginx/Apache)
- [ ] Set up logging
- [ ] Configure monitoring and alerting
- [ ] Set up database backups (if using DB)
- [ ] Document deployment steps
- [ ] Test all endpoints in production

---

## Contributing Guidelines

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes with clear commit messages
4. Add tests for new functionality
5. Update documentation
6. Submit a pull request

---

## Common Tasks

### Add New Validation Rule

1. Locate the domain's validation function
2. Add the new check in the function
3. Add test case
4. Update sample CSV if needed
5. Update documentation

### Debug Validation Issues

1. Check sample CSV file format
2. Verify domain name is correct
3. Add print statements or use logging
4. Check error messages for row numbers
5. Review validation function logic

### Improve Performance

1. Profile the code: `python -m cProfile app.py`
2. Check for N+1 queries
3. Implement caching where appropriate
4. Use streaming for large files
5. Optimize database queries

---

**Version:** 1.0.0  
**Last Updated:** 2024  
**Maintained By:** AI Data Validation Team
