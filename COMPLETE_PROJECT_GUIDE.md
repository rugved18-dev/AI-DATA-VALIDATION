# 🎯 AI DATA VALIDATION SYSTEM - COMPLETE PROJECT GUIDE

**Version:** 2.0.0 (Phase 7 - Security & COBOL Integration)  
**Status:** ✅ Production Ready  
**Updated:** April 12, 2026  
**Purpose:** Enterprise-grade multi-domain data validation system with security, anomaly detection, and mainframe integration

---

## 📑 TABLE OF CONTENTS

1. [What This Project Does](#what-this-project-does)
2. [Key Features (All 7 Phases)](#key-features-all-7-phases)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Complete Architecture](#complete-architecture)
6. [Backend Details](#backend-details)
7. [Frontend Details](#frontend-details)
8. [Validation Domains](#validation-domains)
9. [API Endpoints](#api-endpoints)
10. [Database Schema](#database-schema)
11. [Setup & Installation](#setup--installation)
12. [Running the Application](#running-the-application)
13. [Deployment Instructions](#deployment-instructions)
14. [Important Files Reference](#important-files-reference)

---

## WHAT THIS PROJECT DOES

This is an **enterprise-grade data validation system** that:

1. **Validates data** across three business domains (Banking, Healthcare, E-commerce)
2. **Detects anomalies** in validated data using statistical analysis
3. **Provides a dashboard** for visualizing validation results with interactive charts
4. **Ensures security** with rate limiting, input validation, and sanitization
5. **Integrates with mainframes** via COBOL/RabbitMQ message queue pattern

Users upload CSV files → System validates against domain rules → Returns results with quality scores, anomalies, and errors → Dashboard visualizes results.

---

## KEY FEATURES (ALL 7 PHASES)

### ✅ Phase 1-4: Core Validation System
- Multi-domain validation (Banking, Healthcare, E-commerce)
- Domain-specific business rules and constraints
- Real-time error detection and comprehensive reporting
- Modular, extensible architecture
- Record-by-record validation with detailed error messages
- CSV file processing with proper error handling

### ✅ Phase 5: Anomaly Detection & Quality Scoring
- **3-Dimensional Quality Scoring:**
  - `completeness`: % of non-null fields (40% weight)
  - `validity`: % matching business rules (40% weight)
  - `consistency`: % without logical conflicts (20% weight)
- Statistical outlier detection (domain-specific rules)
- Anomaly severity classification (HIGH/MEDIUM/LOW/INFO)
- Domain-specific anomaly thresholds
- Non-blocking anomaly flags (validation continues)
- Anomaly storage and historical tracking

Example: If banking data has age=150, it flags as HIGH severity anomaly but validation succeeds

### ✅ Phase 6: Interactive React Dashboard
- Professional React-based UI (React 19.2.4)
- Real-time data visualization (Recharts 2.12.7)
- 6+ interactive components:
  - Domain selector with color coding
  - File upload with drag-and-drop
  - Validation results cards
  - Quality metrics gauge charts
  - Anomaly severity display
  - Error detail tables
- Live error tracking and filtering
- Responsive design for desktop/tablet
- Real-time update from backend API

### ✅ Phase 7: Enterprise Security & Mainframe Integration

**Security Features:**
- Input validation (filename, domain, file type checks)
- CSV sanitization (removes formulas, special characters)
- Rate limiting (10 uploads/hour per IP address)
- Security headers (XSS protection, clickjacking prevention, MIME-sniffing blocking)
- Comprehensive audit logging (all requests logged)
- SQL injection prevention (parameterized queries)
- CORS security headers
- Error handling without information leakage

**Mainframe Integration:**
- COBOL integration framework (RabbitMQ ready)
- 3 COBOL program interfaces:
  1. Validation data transmission
  2. Historical record retrieval
  3. Updated record sync
- Message queue pattern for asynchronous processing
- DB2 database integration placeholder
- Production deployment support with message headers

---

## TECHNOLOGY STACK

### Backend
- **Framework:** Flask 2.3.3 (Python web framework)
- **Python Version:** 3.8+
- **Database:** SQLite3 (validation result persistence)
- **Cache:** Python dict-based (in-memory)
- **Server:** Gunicorn 21.2.0 (production deployment)
- **CORS:** Flask-CORS 4.0.0
- **File Handling:** Werkzeug 2.3.7
- **Rate Limiting:** Custom Flask middleware
- **Logging:** Python logging module

### Frontend
- **Library:** React 19.2.4
- **Package Manager:** npm
- **Build Tool:** React Scripts 5.0.1
- **HTTP Client:** Axios 1.14.0
- **Data Visualization:** Recharts 2.12.7
- **Styling:** CSS3 (500+ lines custom CSS)
- **Testing:** Jest + React Testing Library

### Infrastructure & Deployment
- **Environment Config:** python-dotenv 1.0.0
- **Data Format:** CSV (comma-separated values)
- **API Protocol:** RESTful HTTP/HTTPS with JSON
- **Message Queue (Optional):** RabbitMQ (for mainframe)
- **Mainframe DB (Optional):** DB2
- **Deployment:** Docker-ready, Gunicorn WSGI

---

## PROJECT STRUCTURE

```
AI-DATA-VALIDATION/
│
├── README.md                           # Quick start guide
├── PROJECT_DOCUMENTATION.md            # Full documentation (v2.0.0)
├── COMPLETE_PROJECT_GUIDE.md          # THIS FILE - Comprehensive guide
│
├── backend/                            # Flask API (Python)
│   ├── app.py                          # Main Flask application (Phase 7 enhanced)
│   ├── requirements.txt                # Python dependencies
│   │
│   ├── models/
│   │   └── validation_result.py        # ValidationResult class (Phases 1-5)
│   │       ├── id, timestamp, filename
│   │       ├── domain, record_number, data
│   │       ├── is_valid, errors[]
│   │       ├── quality_scores (completeness/validity/consistency)
│   │       ├── anomaly_count, anomaly_score
│   │       ├── anomalies[] list
│   │       └── to_dict() method
│   │
│   ├── services/
│   │   ├── validation_service.py       # Core validators (Phases 1-4)
│   │   │   ├── BankingValidator
│   │   │   ├── HealthcareValidator
│   │   │   └── EcommerceValidator
│   │   │
│   │   ├── anomaly_detection.py        # Phase 5: Anomaly detection
│   │   │   ├── detect_anomalies()
│   │   │   ├── banking_anomalies()
│   │   │   ├── healthcare_anomalies()
│   │   │   ├── ecommerce_anomalies()
│   │   │   └── calculate_quality_score()
│   │   │
│   │   ├── database_service.py         # Phase 3/6: Database operations
│   │   │   ├── save_validation()
│   │   │   ├── get_all_validations()
│   │   │   └── stats_by_domain()
│   │   │
│   │   ├── security_utils.py           # Phase 7: Security
│   │   │   ├── validate_input()
│   │   │   ├── sanitize_csv()
│   │   │   ├── rate_limit_check()
│   │   │   └── audit_log()
│   │   │
│   │   └── mainframe_service.py        # Phase 7: COBOL Integration
│   │       ├── send_validation_data()
│   │       ├── retrieve_historical()
│   │       ├── sync_updated_records()
│   │       └── queue_message()
│   │
│   ├── routes/
│   │   ├── health_routes.py            # GET /health endpoint
│   │   └── upload_routes.py            # POST /upload endpoint
│   │
│   ├── uploads/                        # Uploaded CSV files storage
│   │   ├── sample_banking.csv
│   │   ├── sample_healthcare.csv
│   │   └── sample_ecommerce.csv
│   │
│   ├── validation_results.db           # SQLite3 database (Phase 6)
│   │
│   ├── DEVELOPER_GUIDE.md              # Developer documentation
│   ├── API_TESTING_GUIDE.md            # API testing instructions
│   └── QUICK_REFERENCE.md              # Quick reference
│
├── frontend/                           # React Dashboard (Phase 6)
│   ├── package.json                    # NPM dependencies
│   ├── public/
│   │   ├── index.html                  # HTML entry point
│   │   ├── manifest.json               # PWA manifest
│   │   └── robots.txt                  # SEO
│   │
│   └── src/
│       ├── index.js                    # React entry point
│       ├── App.js                      # Main App component
│       ├── App.css                     # Main styles (500+ lines)
│       ├── components/
│       │   ├── DomainSelector.js       # Domain selection dropdown
│       │   ├── FileUpload.js           # Drag-drop file upload
│       │   ├── ValidationResults.js    # Results display
│       │   ├── QualityMetrics.js       # Quality gauge charts
│       │   ├── AnomalySeverity.js      # Anomaly display
│       │   └── ErrorDetails.js         # Error table
│       │
│       ├── setupTests.js               # Test configuration
│       ├── reportWebVitals.js          # Performance monitoring
│       └── index.css                   # Global styles
│
└── Sample Data Files
    ├── backend/sample_banking.csv       # Sample banking domain data
    ├── backend/sample_healthcare.csv    # Sample healthcare domain data
    └── backend/sample_ecommerce.csv     # Sample e-commerce domain data
```

---

## COMPLETE ARCHITECTURE

### System Architecture Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                    USER BROWSER / CLIENT                        │
│         (Desktop, Tablet, or Mobile Device)                     │
└────────────────────┬─────────────────────────────────────────┬──┘
                     │                                           │
        ┌────────────▼──────────────┐              ┌─────────────▼──────┐
        │  REACT FRONTEND (Phase 6) │              │ Static Files (.css) │
        ├──────────────────────────┤              └───────────────────┘
        │ ✅ Domain Selector       │
        │ ✅ File Upload (DnD)     │              Runs on: localhost:3000
        │ ✅ Results Display       │
        │ ✅ Quality Charts        │
        │ ✅ Anomaly Display       │
        │ ✅ Error Details         │
        └────────────┬─────────────┘
                     │
        HTTP Client-Request (TLS in Prod)
        ├─ Authorization (if needed)
        ├─ CORS Headers
        └─ JSON Payloads
                     │
        ┌────────────▼──────────────────────────┐
        │  FLASK SECURITY LAYER (Phase 7)      │
        ├──────────────────────────┬────────────┤
        │ ✅ Rate Limiter         │ IPAddress  │
        │ ✅ Input Validator      │            │
        │ ✅ Request Logger       │            │
        │ ✅ Security Headers     │            │
        │ ✅ CORS Handler         │            │
        └────────────┬─────────────┴────────────┘
                     │
        ┌────────────▼──────────────────────────┐
        │  FLASK BACKEND API SERVER             │
        ├──────────────────────────────────────┤
        │                                       │
        │  Route: GET /health                  │
        │  └─ Health check                    │
        │                                      │
        │  Route: POST /upload                │
        │  ├─ Parse multipart form            │
        │  ├─ Route to validator              │
        │  └─ Return validation results       │
        │                                      │
        │  Service Layer:                     │
        │  ├─ ValidationService (Phase 1-4)  │
        │  ├─ AnomalyDetection (Phase 5)     │
        │  ├─ DatabaseService (Phase 3/6)   │
        │  ├─ SecurityUtils (Phase 7)        │
        │  └─ MainframeService (Phase 7)     │
        │                                      │
        └────────────┬──────────────────────────┘
                     │
        ┌────────────┴──────────────────────────┐
        │        DATA STORAGE LAYERS             │
        │                                        │
        ├─ File Storage: uploads/ directory     │
        │   └─ Uploaded CSV files               │
        │                                        │
        ├─ SQLite3 Database: validation_results.db (Phase 3/6)
        │   └─ Validation history & persistence│
        │                                        │
        ├─ Optional: RabbitMQ (Phase 7)         │
        │   └─ Message queue for mainframe      │
        │                                        │
        └─ Optional: DB2 Database (Phase 7)     │
            └─ Mainframe historical data         │
```

### Complete Data Flow (All Phases)

```
STEP 1: User Input
├─ Opens dashboard (localhost:3000)
├─ Selects domain (Banking/Healthcare/E-commerce)
├─ Selects CSV file (drag-drop or browse)
└─ Clicks "Validate"

STEP 2: Security Layer (Phase 7)
├─ Check rate limit (10/hour per IP) ✓
├─ Validate input (filename, domain) ✓
├─ Sanitize CSV (remove formulas) ✓
└─ Log request for audit ✓

STEP 3: Validation (Phases 1-4)
├─ Parse CSV file
├─ For each record:
│  ├─ Route to domain validator
│  ├─ Apply business rules
│  ├─ Check field constraints
│  └─ Collect errors if invalid

STEP 4: Quality Scoring (Phase 5)
├─ Calculate completeness (non-null %)
├─ Calculate validity (rules match %)
├─ Calculate consistency (no conflicts %)
└─ Weighted average = quality_score

STEP 5: Anomaly Detection (Phase 5)
├─ Check domain-specific thresholds
├─ Identify outliers (e.g., age > 150)
├─ Classify by severity (HIGH/MEDIUM/LOW/INFO)
├─ Store anomaly details
└─ Do NOT block validation (non-blocking)

STEP 6: Database Storage (Phase 3/6)
├─ Save ValidationResult to SQLite3
│  ├─ timestamp, filename, domain
│  ├─ record data, validation errors
│  ├─ quality scores
│  └─ anomalies list
└─ Generate record_id

STEP 7: Optional Mainframe Sync (Phase 7)
├─ Queue message to RabbitMQ
├─ Send validation data to COBOL programs
│  ├─ Program 1: NEW_VALIDATION (transmission)
│  ├─ Program 2: GET_HISTORY (retrieve)
│  └─ Program 3: SYNC_UPDATES (synchronize)
└─ Update DB2 if connected

STEP 8: API Response
├─ Return JSON with:
│  ├─ summary (total, valid, invalid, errors)
│  ├─ records[] (with validation, errors, quality)
│  ├─ quality metrics (overall scores)
│  ├─ anomalies list (with severity)
│  └─ record_id (database reference)
└─ HTTP 200 success or 4xx/5xx error

STEP 9: Frontend Display (Phase 6)
├─ Parse API response
├─ Update Dashboard:
│  ├─ Show summary cards (valid/invalid counts)
│  ├─ Display quality gauge charts
│  ├─ Highlight anomalies by severity
│  ├─ List detailed errors
│  └─ Enable drill-down by record
└─ Real-time visualization
```

---

## BACKEND DETAILS

### Backend Technologies
- **Framework:** Flask 2.3.3 (lightweight Python web framework)
- **Python Version:** 3.8+ (required)
- **Database:** SQLite3 (file-based relational database)
- **Server:** Gunicorn 21.2.0 (production WSGI server)

### Core Files

**app.py - Main Application (500+ lines, Phase 7 Enhanced)**
- Flask app initialization
- CORS configuration
- Security headers middleware
- Rate limiting middleware
- Request/response logging
- Error handlers (40x, 50x)
- Route registration
- SQLite database initialization
- Query parameter validation

**models/validation_result.py - Data Model**
```python
class ValidationResult:
    def __init__(self):
        self.id                 # Database record ID
        self.timestamp          # When validated
        self.filename           # Uploaded file name
        self.domain             # 'banking', 'healthcare', or 'ecommerce'
        self.record_number      # Row number in CSV
        self.data              # Original record data (dict)
        self.is_valid          # Boolean validation result
        self.errors            # List of error messages
        self.quality_scores    # Dict: {completeness, validity, consistency}
        self.anomaly_count     # Number of anomalies detected
        self.anomaly_score     # Average severity (0-100)
        self.anomalies         # List of anomaly objects
```

**services/validation_service.py - Validators (Phase 1-4)**

Banking Domain Validation:
```
Required Fields: account_holder_name, age, income, credit_score, ssn, account_type
Rules:
├─ age: 18-100 (must be numeric)
├─ income: >= 0 (must be numeric)
├─ credit_score: 300-850 (must be numeric)
├─ ssn: Format XXX-XX-XXXX (must match regex)
├─ account_type: Checking, Savings, or Money Market
└─ account_holder_name: Not empty, 2-100 chars
```

Healthcare Domain Validation:
```
Required Fields: patient_name, age, blood_group, heart_rate, cholesterol_level, medication
Rules:
├─ age: 0-150 (must be numeric)
├─ blood_group: A, B, AB, or O (with +/-)
├─ heart_rate: 40-200 (must be numeric, in BPM)
├─ cholesterol_level: 0-300 (must be numeric, in mg/dL)
├─ medication: Not empty, must be from approved list
└─ patient_name: Not empty, 2-100 chars
```

E-commerce Domain Validation:
```
Required Fields: product_name, price, stock, rating, category
Rules:
├─ price: > 0 (must be numeric, in USD)
├─ stock: >= 0 (must be integer)
├─ rating: 1-5 (must be numeric)
├─ category: Electronics, Clothing, Books, etc.
└─ product_name: Not empty, 2-200 chars
```

**services/anomaly_detection.py - Phase 5 (180+ lines)**

Anomaly Detection Thresholds:
```
Banking:
├─ age > 150 or < 0 → HIGH
├─ income > 10M → MEDIUM
└─ credit_score < 300 → MEDIUM

Healthcare:
├─ age > 120 or < 0 → HIGH
├─ heart_rate > 150 or < 50 → MEDIUM
├─ cholesterol > 300 → LOW
└─ medication not in list → MEDIUM

E-commerce:
├─ price < 0 or > 1M → HIGH
├─ stock > 100K → MEDIUM
├─ rating < 1 or > 5 → HIGH
└─ category not recognized → LOW
```

Quality Score Formula:
```
quality_score = (completeness × 0.40) + (validity × 0.40) + (consistency × 0.20)

Where:
- completeness = (non_null_fields / total_fields) × 100
- validity = (fields_matching_rules / total_fields) × 100
- consistency = (fields_without_conflicts / total_fields) × 100
```

**services/database_service.py - Phase 3/6**
```python
def save_validation(result) → record_id
def get_all_validations() → List[ValidationResult]
def get_validations_by_domain(domain) → List[ValidationResult]
def stats_by_domain() → {domain: {total, valid, invalid, avg_quality}}
def delete_old_records(days=30) → affected_count
```

**services/security_utils.py - Phase 7 (450+ lines)**
```python
def validate_input(file, domain):
    ├─ Check file exists
    ├─ Check domain in valid list
    ├─ Validate filename (alphanum, dash, underscore only)
    └─ Check file size (max 10MB)

def sanitize_csv(data):
    ├─ Remove formula prefixes (=, +, -, @)
    ├─ Remove null bytes
    ├─ Escape quotes and backslashes
    └─ Trim whitespace

def rate_limit_check(ip_address):
    ├─ Get request count for IP in last hour
    ├─ If >= 10: reject with 429
    └─ Otherwise: increment counter

def audit_log(method, path, ip, user_agent, status):
    └─ Log to file: timestamp | method | path | ip | status
```

**services/mainframe_service.py - Phase 7 (500+ lines)**
```python
def send_validation_data(validation_result):
    ├─ Create message envelope
    ├─ Queue to RabbitMQ
    └─ Log message_id

def retrieve_historical(domain, start_date, end_date):
    ├─ Query DB2 for records
    ├─ Filter by date range
    └─ Return aggregated results

def sync_updated_records(validation_id):
    ├─ Get validation from SQLite
    ├─ Mark as synced in DB2
    └─ Update sync_timestamp

# COBOL Program Interfaces
├─ NEW_VALIDATION: Send new validation record
├─ GET_HISTORY: Retrieve historical data
└─ SYNC_UPDATES: Synchronize updated records
```

---

## FRONTEND DETAILS

### Frontend Technologies
- **Library:** React 19.2.4 (JavaScript UI framework)
- **Package Manager:** npm
- **Build Tool:** React Scripts 5.0.1 (Create React App)
- **HTTP Client:** Axios 1.14.0
- **Charts:** Recharts 2.12.7 (React charting library)
- **Styling:** CSS3 (500+ lines custom)

### React Components (Phase 6)

**App.js - Main Component (200+ lines)**
```javascript
function App() {
  // State:
  // - selectedDomain (banking/healthcare/ecommerce)
  // - uploadedFile
  // - validationResults
  // - isLoading
  // - error

  // Renders:
  // ├─ DomainSelector (dropdown)
  // ├─ FileUpload (drag-drop)
  // ├─ ValidationResults (cards + charts)
  // ├─ AnomalySeverity (severity breakdown)
  // └─ ErrorDetails (error table)
}
```

**DomainSelector.js**
- Dropdown with Banking, Healthcare, E-commerce options
- Color-coded (blue, green, orange)
- Updates App state on change

**FileUpload.js**
- Drag-and-drop zone
- File browse button
- File size validation
- Submit button to POST /upload

**ValidationResults.js**
- Summary cards: Total, Valid, Invalid, Record ID
- Quality metrics display
- Record-by-record results list
- Expandable error details

**QualityMetrics.js**
- Gauge charts for Completeness, Validity, Consistency
- Overall quality score
- Color-coded by percentage (green/yellow/red)

**AnomalySeverity.js**
- List of anomalies with severity badges
- Color-coded (red=HIGH, orange=MEDIUM, yellow=LOW, blue=INFO)
- Sortable by severity

**ErrorDetails.js**
- Table showing errors by record
- Error message, field name, reason
- Searchable and filterable

### Styling (App.css - 500+ lines)
- Responsive grid layout
- Card components with shadows
- Color scheme (primary blue, success green, warning orange, danger red)
- Chart tooltips and animations
- Mobile-friendly design (768px+ breakpoints)

---

## VALIDATION DOMAINS

### 🏦 Banking Domain

**Sample CSV:**
```
account_holder_name,age,income,credit_score,ssn,account_type
John Doe,35,75000,720,123-45-6789,Checking
Jane Smith,28,95000,750,987-65-4321,Savings
```

**Validation Rules:**
- `account_holder_name`: Required, 2-100 characters
- `age`: Must be 18-100 (numeric)
- `income`: Must be >= 0 (numeric)
- `credit_score`: Must be 300-850 (numeric)
- `ssn`: Must match format XXX-XX-XXXX
- `account_type`: Must be "Checking", "Savings", or "Money Market"

**Anomalies (Phase 5):**
- age > 150 → HIGH severity
- income > $10M → MEDIUM severity
- credit_score < 300 → MEDIUM severity
- Missing required field → blocks validation

---

### 🏥 Healthcare Domain

**Sample CSV:**
```
patient_name,age,blood_group,heart_rate,cholesterol_level,medication
Alice Johnson,45,O+,72,180,Aspirin
Bob Williams,52,A-,88,220,Metformin
```

**Validation Rules:**
- `patient_name`: Required, 2-100 characters
- `age`: Must be 0-150 (numeric)
- `blood_group`: Must be A, B, AB, or O (with +/-)
- `heart_rate`: Must be 40-200 (numeric, BPM)
- `cholesterol_level`: Must be 0-300 (numeric, mg/dL)
- `medication`: Required, must be from approved list

**Anomalies (Phase 5):**
- age > 120 → HIGH severity
- heart_rate > 150 or < 50 → MEDIUM severity
- cholesterol > 300 → LOW severity
- age inconsistent with medications → LOW severity

---

### 🛒 E-commerce Domain

**Sample CSV:**
```
product_name,price,stock,rating,category
Laptop,1200.50,45,4.8,Electronics
T-Shirt,25.99,150,4.2,Clothing
```

**Validation Rules:**
- `product_name`: Required, 2-200 characters
- `price`: Must be > 0 (numeric, USD)
- `stock`: Must be >= 0 (integer)
- `rating`: Must be 1-5 (numeric)
- `category`: Required, must match predefined list

**Anomalies (Phase 5):**
- price < 0 or > $1M → HIGH severity
- stock > 100K → MEDIUM severity
- rating < 1 or > 5 → HIGH severity
- Inconsistent pricing with category → LOW severity

---

## API ENDPOINTS

### Endpoint 1: Health Check

**GET** `/health`

Check system health and version.

**Response (200):**
```json
{
  "status": "healthy",
  "timestamp": "2026-04-12T10:30:45.123456",
  "version": "2.0.0"
}
```

---

### Endpoint 2: File Upload & Validation

**POST** `/upload`

Upload CSV and validate against domain rules.

**Request:**
```
Content-Type: multipart/form-data

Parameters:
- file: (required) CSV file
- domain: (required) "banking", "healthcare", or "ecommerce"
```

**Response (200):**
```json
{
  "summary": {
    "total_records": 5,
    "valid_records": 4,
    "invalid_records": 1,
    "total_errors": 3,
    "overall_quality_score": 78.5
  },
  "records": [
    {
      "record_number": 1,
      "data": {
        "name": "John Doe",
        "age": 35,
        "account_type": "Checking"
      },
      "is_valid": true,
      "errors": [],
      "quality_scores": {
        "completeness": 100,
        "validity": 100,
        "consistency": 100
      },
      "anomaly_count": 0,
      "anomaly_score": 0,
      "anomalies": []
    },
    {
      "record_number": 2,
      "data": {
        "name": "Jane Smith",
        "age": 150,
        "account_type": "Savings"
      },
      "is_valid": true,
      "errors": [],
      "quality_scores": {
        "completeness": 100,
        "validity": 100,
        "consistency": 100
      },
      "anomaly_count": 1,
      "anomaly_score": 95,
      "anomalies": [
        {
          "field": "age",
          "value": 150,
          "reason": "Age exceeds expected range for banking",
          "severity": "HIGH"
        }
      ]
    },
    {
      "record_number": 3,
      "data": {
        "name": "Bob Wilson",
        "age": null,
        "account_type": "Invalid"
      },
      "is_valid": false,
      "errors": [
        "Field 'age' is required",
        "Field 'account_type' must be one of: Checking, Savings, Money Market"
      ],
      "quality_scores": {
        "completeness": 67,
        "validity": 50,
        "consistency": 80
      },
      "anomaly_count": 0,
      "anomaly_score": 0,
      "anomalies": []
    }
  ],
  "quality_metrics": {
    "average_completeness": 89.0,
    "average_validity": 83.3,
    "average_consistency": 93.3
  },
  "database_record_id": "validation_2026_04_12_1030_xyz123"
}
```

**Error Response (400):**
```json
{
  "error": "Invalid domain. Must be: banking, healthcare, or ecommerce"
}
```

**Error Response (429):**
```json
{
  "error": "Rate limit exceeded. Maximum 10 uploads per hour"
}
```

---

## DATABASE SCHEMA

### SQLite3 Database: validation_results.db

**Table: validation_results**

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Auto-increment record ID |
| timestamp | TEXT | ISO 8601 format (YYYY-MM-DDTHH:MM:SS) |
| filename | TEXT | Original uploaded filename |
| domain | TEXT | 'banking', 'healthcare', or 'ecommerce' |
| record_number | INTEGER | Row number in CSV |
| data_json | TEXT | Original record data (JSON) |
| is_valid | BOOLEAN | 1=valid, 0=invalid |
| errors_json | TEXT | Error messages (JSON array) |
| completeness_score | REAL | 0-100 percent |
| validity_score | REAL | 0-100 percent |
| consistency_score | REAL | 0-100 percent |
| quality_score | REAL | Weighted average 0-100 |
| anomaly_count | INTEGER | Number of anomalies detected |
| anomaly_score | REAL | 0-100 severity average |
| anomalies_json | TEXT | Anomaly details (JSON array) |

**Indexes:**
- `idx_timestamp`: For time-range queries
- `idx_domain`: For domain filtering
- `idx_is_valid`: For valid/invalid filtering

**Queries:**
```sql
-- Get all validations
SELECT * FROM validation_results ORDER BY timestamp DESC;

-- Get statistics by domain
SELECT domain, COUNT(*) as total, 
       SUM(CASE WHEN is_valid=1 THEN 1 ELSE 0 END) as valid,
       AVG(quality_score) as avg_quality
FROM validation_results GROUP BY domain;

-- Get anomalies detected in last 7 days
SELECT * FROM validation_results 
WHERE anomaly_count > 0 
AND timestamp > datetime('now', '-7 days')
ORDER BY anomaly_score DESC;
```

---

## SETUP & INSTALLATION

### Prerequisites
- **Python:** 3.8 or higher (check: `python --version`)
- **Node.js:** 14 or higher (check: `node --version`)
- **npm:** (check: `npm --version`)
- **Git:** (optional, for version control)

### Step 1: Clone or Download Project

```bash
cd "d:\New folder (4)\AI-DATA-VALIDATION"
```

### Step 2: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from app import init_db; init_db()"
```

### Step 3: Frontend Setup

```bash
# Navigate to frontend (in new terminal)
cd frontend

# Install dependencies
npm install

# (Do NOT run npm start yet - wait for backend)
```

### Step 4: Verify Installation

**Backend (in backend terminal):**
```bash
python app.py
# Should output: Running on http://127.0.0.1:5000
```

**Frontend (in frontend terminal):**
```bash
npm start
# Should open http://localhost:3000 in browser
```

---

## RUNNING THE APPLICATION

### Quick Start

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python app.py
```

Expected output:
```
 * Flask app.py running
 * Running on http://127.0.0.1:5000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

Expected output:
```
Compiled successfully!
You can now view app in the browser.
Open http://localhost:3000 to view it.
```

### Testing with Sample Data

**Option 1: Using Dashboard**
1. Open http://localhost:3000
2. Select domain (Banking, Healthcare, or E-commerce)
3. Click upload or drag sample CSV from `backend/sample_*.csv`
4. View results in dashboard

**Option 2: Using cURL**
```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@backend/sample_banking.csv" \
  -F "domain=banking"
```

### Stopping the Application

- **Backend:** Press Ctrl+C in terminal
- **Frontend:** Press Ctrl+C in terminal
- Or close both terminal windows

---

## DEPLOYMENT INSTRUCTIONS

### Production Deployment (Linux/Docker)

**Step 1: Install Dependencies**
```bash
sudo apt-get update
sudo apt-get install python3.10 python3-pip nodejs npm

# Or use Docker:
docker pull python:3.10-slim
docker pull node:18-slim
```

**Step 2: Deploy Backend**
```bash
cd backend
pip install -r requirements.txt
# Use Gunicorn instead of Flask dev server
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Step 3: Deploy Frontend**
```bash
cd frontend
npm run build  # Creates optimized production build
npm install -g serve
serve -s build -l 3000
```

**Step 4: Setup Reverse Proxy (nginx)**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:5000;
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
    }
}
```

**Step 5: Enable HTTPS (Let's Encrypt)**
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com
```

### Environment Variables (.env file)

Create `backend/.env`:
```
FLASK_ENV=production
DATABASE_URL=sqlite:///validation_results.db
RATE_LIMIT_ENABLED=true
AUDIT_LOG_PATH=/var/log/validation/audit.log
MAINFRAME_QUEUE_URL=amqp://rabbitmq:5672/
DB2_CONNECTION_STRING=DB2_HOST:DB2_PORT/VALIDATION_DB
```

### Database Backup (Production)

```bash
# Daily backup
sqlite3 validation_results.db ".backup backup_$(date +%Y%m%d).db"

# Or with cron job:
0 2 * * * cd /app/backend && sqlite3 validation_results.db \
  ".backup backup_$(date +\%Y\%m\%d).db"
```

---

## IMPORTANT FILES REFERENCE

### Configuration Files
- `backend/requirements.txt` - Python dependencies
- `frontend/package.json` - NPM dependencies
- `backend/.env` - Environment variables (create manually)
- `.gitignore` - Git ignore patterns

### Core Application Files
- `backend/app.py` - Flask application entry point (500+ lines)
- `frontend/src/index.js` - React application entry point
- `frontend/src/App.js` - Main React component

### Business Logic
- `backend/services/validation_service.py` - Validators (Phases 1-4)
- `backend/services/anomaly_detection.py` - Anomaly detection (Phase 5)
- `backend/services/database_service.py` - Database operations (Phase 3/6)
- `backend/services/security_utils.py` - Security & rate limiting (Phase 7)
- `backend/services/mainframe_service.py` - COBOL integration (Phase 7)

### Data Models
- `backend/models/validation_result.py` - ValidationResult class

### Routes (API Endpoints)
- `backend/routes/health_routes.py` - GET /health
- `backend/routes/upload_routes.py` - POST /upload

### Frontend Components
- `frontend/src/App.js` - Main component
- `frontend/src/components/DomainSelector.js` - Domain selection
- `frontend/src/components/FileUpload.js` - File upload
- `frontend/src/components/ValidationResults.js` - Results display
- `frontend/src/components/QualityMetrics.js` - Quality charts
- `frontend/src/components/AnomalySeverity.js` - Anomaly display
- `frontend/src/components/ErrorDetails.js` - Error table

### Sample Data
- `backend/sample_banking.csv` - Banking test data
- `backend/sample_healthcare.csv` - Healthcare test data
- `backend/sample_ecommerce.csv` - E-commerce test data

### Database
- `backend/validation_results.db` - SQLite3 database (auto-created on first run)

---

## QUICK REFERENCE COMMANDS

```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python app.py

# Frontend
cd frontend
npm install
npm start

# Test API
curl http://localhost:5000/health
curl -X POST http://localhost:5000/upload -F "file=@sample_banking.csv" -F "domain=banking"

# Database
sqlite3 backend/validation_results.db "SELECT COUNT(*) FROM validation_results;"

# Production
gunicorn -w 4 -b 0.0.0.0:5000 app:app
npm run build && serve -s build -l 3000
```

---

## PHASE SUMMARY

| Phase | Name | Status | Key Components |
|-------|------|--------|-----------------|
| 1-4 | Core Validation | ✅ Complete | BankingValidator, HealthcareValidator, EcommerceValidator |
| 5 | Anomaly Detection | ✅ Complete | anomaly_detection.py, quality_scoring, anomaly_severity |
| 6 | Dashboard | ✅ Complete | React components, Recharts, interactive visualization |
| 7 | Security & Mainframe | ✅ Complete | security_utils.py, mainframe_service.py, rate limiting |

---

**Created:** April 12, 2026  
**Last Updated:** April 12, 2026  
**Maintained By:** AI Data Validation Team
