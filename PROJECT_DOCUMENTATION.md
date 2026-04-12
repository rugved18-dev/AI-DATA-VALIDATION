# AI DATA VALIDATION SYSTEM - COMPREHENSIVE PROJECT DOCUMENTATION

**Project Name:** AI Data Validation System
**Version:** 2.0.0 (Phase 7 - Security & COBOL Integration)
**Last Updated:** April 12, 2026
**Author:** AI Data Validation Team
**Status:** ✅ Production Ready
**Purpose:** Enterprise-grade multi-domain data validation system with security, mainframe integration, and advanced anomaly detection

---

## TABLE OF CONTENTS
1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Project Architecture](#project-architecture)
4. [Directory Structure](#directory-structure)
5. [Backend Details](#backend-details)
6. [Frontend Details](#frontend-details)
7. [Dependencies](#dependencies)
8. [API Documentation](#api-documentation)
9. [Validation Rules](#validation-rules)
10. [Setup and Installation](#setup-and-installation)
11. [Running the Application](#running-the-application)
12. [Future Integration Points](#future-integration-points)
13. [Key Files Reference](#key-files-reference)

---

## PROJECT OVERVIEW

### What Does This Project Do?
This is a **multi-domain data validation system** that helps validate data across three different business domains:
1. **Banking Domain** - Validates customer financial profiles
2. **Healthcare Domain** - Validates patient health records
3. **E-commerce Domain** - Validates product inventory data

### High-Level Purpose
Users can upload CSV files containing data records and the system validates each record against domain-specific business rules. The system returns validation results showing which records are valid/invalid and any errors found.

### Target Users
- Data managers who need to validate bulk data
- Business analysts working with different data types
- Enterprise systems that need to integrate validation as a service

---

## TECHNOLOGY STACK

### Backend
- **Framework:** Flask 2.3.3 (Python web framework) with CORS 4.0.0
- **Python Version:** 3.8+
- **Database:** SQLite3 (persistent validation result storage)
- **Server:** Gunicorn 21.2.0 (production deployment)
- **File Handling:** Werkzeug 2.3.7

**Phase 5-7 Additions:**
- Anomaly detection system (statistical outlier detection)
- Security utilities module (input validation, sanitization)
- Rate limiting system (10 requests/hour per IP)
- COBOL mainframe integration framework (RabbitMQ ready)
- Security headers and comprehensive logging

### Frontend
- **Library:** React 19.2.4
- **Node Package Manager:** npm
- **Build Tool:** React Scripts 5.0.1
- **HTTP Client:** Axios 1.14.0
- **Data Visualization:** Recharts 2.12.7 (Phase 6 - Dashboard charts)
- **Testing:** Jest with React Testing Library

**Phase 6 Frontend Enhancements:**
- Professional dashboard with 6+ React components
- Interactive data visualization (bar, pie, gauge charts)
- Real-time anomaly display
- Domain selector with color coding
- Drag-and-drop file upload

### Deployment & Infrastructure
- **Environment Variables:** python-dotenv 1.0.0
- **Data Format:** CSV (comma-separated values)
- **Communication:** RESTful APIs (JSON format)
- **Message Queue Ready:** RabbitMQ (for mainframe integration)
- **Database Ready:** DB2 (mainframe historical data)

---

## PROJECT ARCHITECTURE

### Architecture Pattern: Enterprise-Grade Client-Server with Security & Mainframe Integration

```
┌──────────────────────────────────────────────────────────┐
│    USER BROWSER (Frontend - React 19.2.4)                │
│  ✅ Domain Selector (Banking/Healthcare/E-commerce)      │
│  ✅ Drag-Drop File Upload                                │
│  ✅ Interactive Dashboard with Charts                   │
│  ✅ Anomaly Visualization                               │
│  ✅ Error Display with Severity Indicators              │
└────────────────┬─────────────────────────────────────────┘
                 │
         HTTP/CORS Requests (TLS in Production)
         Security Headers: X-Frame-Options, CSP, etc.
                 │
    ┌────────────▼──────────────────────────┐
    │   FLASK SECURITY LAYER (Phase 7)      │
    │  ✅ Rate Limiting (10 req/hour)       │
    │  ✅ Input Sanitization                │
    │  ✅ Request/Response Logging          │
    │  ✅ Security Headers                  │
    │  ✅ Error Handlers                    │
    └────────────┬──────────────────────────┘
                 │
    ┌────────────▼──────────────────────────┐
    │   BACKEND API SERVER (Flask Python)   │
    │  ✅ File Upload Handling              │
    │  ✅ CSV Parsing                       │
    │  ✅ Domain Validation                 │
    │  ✅ Quality Scoring (3 dimensions)    │
    │  ✅ Anomaly Detection (Phase 5)       │
    │  ✅ Database Persistence              │
    └────────────┬──────────────────────────┘
                 │
    ┌────────────┴──────────────────────────┐
    │         THREE STORAGE LAYERS           │
    │                                        │
    ├─ File Storage (uploads/)               │
    ├─ SQLite3 Database (validation_results) │
    └─ Optional: DB2 (mainframe data)       │
```

**Phase 5-7 Integration Points:**
```
Anomaly Detection (Phase 5) ──┐
Quality Dimensions ──────────┤
                             └──→ Validation Result ──→ Database (SQLite3)
Domain Validators ───────────┐                                ↓
                             │                         Mainframe (Phase 7)
                             └──→ API Response (JSON) ──→ Frontend Dashboard
                                                              (React + Recharts)

Security Layer (Phase 7):
Input Validation → CSV Sanitization → Rate Limiting → Security Headers → Logging
```

### Data Flow with All Phases

1. **Frontend** - User uploads CSV, selects domain
2. **Security** (Phase 7) - Rate limit check, input validation, filename validation
3. **Backend** - Parse CSV, route to domain validator
4. **Validation** (Phases 1-4) - Apply domain-specific business rules
5. **Anomaly Detection** (Phase 5) - Identify statistical outliers
6. **Scoring** - Calculate 3 quality dimensions (completeness, validity, consistency)  
7. **Storage** - Save results to SQLite3 database
8. **Mainframe** (Phase 7 optional) - Send to COBOL programs via RabbitMQ
9. **Response** - Return JSON with all metrics, anomalies, errors
10. **Frontend Dashboard** (Phase 6) - Display interactive charts and metrics

---

## DIRECTORY STRUCTURE

```
AI-DATA-VALIDATION/
│
├── backend/                                  # Python Flask backend (MODULAR ARCHITECTURE)
│   ├── app.py                               # Main Flask entry point with security (Phase 7)
│   │                                         # Features: Security headers, rate limiting, logging
│   ├── models/                              # Data models package
│   │   └── validation_result.py             # ValidationResult with Phase 5 anomaly fields
│   │
│   ├── services/                            # Business logic services package
│   │   ├── validation_service.py            # Domain validators + Phase 5 anomaly detection
│   │   ├── file_service.py                  # File upload validation
│   │   ├── scoring_service.py               # Quality scoring (3 dimensions)
│   │   ├── database_service.py              # SQLite3 persistence (Phase 3)
│   │   ├── anomaly_detection.py             # Phase 5 - Statistical outlier detection
│   │   ├── mainframe_service.py             # Phase 7 - COBOL integration (RabbitMQ ready)
│   │   └── security_utils.py                # Phase 7 - Input validation & sanitization
│   │
│   ├── routes/                              # API routes package
│   │   └── upload_routes.py                 # POST /upload with security (Phase 7)
│   │
│   ├── uploads/                             # Temporary CSV file storage
│   ├── validation_results.db                # SQLite3 database (Phase 3+)
│   ├── requirements.txt                     # Python dependencies
│   │
│   ├── 📚 DOCUMENTATION FILES               # Comprehensive developer documentation
│   ├── README.md                            # Backend quick start
│   ├── DEVELOPER_GUIDE.md                   # Development guidelines
│   ├── API_TESTING_GUIDE.md                 # API testing procedures
│   ├── QUICK_REFERENCE.md                   # Developer quick reference
│   ├── IMPLEMENTATION_SUMMARY.md            # System architecture details
│   │
│   ├── 🎯 PHASE-SPECIFIC DOCUMENTATION
│   ├── PHASE5_IMPLEMENTATION.md             # Anomaly detection details
│   ├── PHASE5_SUMMARY.md                    # Phase 5 overview
│   ├── PHASE7_IMPLEMENTATION.md             # Security & COBOL integration full guide
│   ├── PHASE7_QUICK_REFERENCE.md            # Phase 7 quick reference
│   └── PHASE7_STATUS.md                     # Phase 7 completion status
│
├── frontend/                                # React frontend (Phase 6 improvements)
│   ├── package.json                         # Node dependencies (+ Recharts 2.12.7)
│   ├── src/                                 # React source code
│   │   ├── App.js                          # Main component + state management
│   │   ├── App.css                         # Modern styling (500+ lines)
│   │   ├── index.js                        # React entry point
│   │   ├── components/                     # Phase 6 - 6 New Components
│   │   │   ├── DomainSelector.js           # Domain selection with color coding
│   │   │   ├── FileUpload.js               # Drag-drop file upload
│   │   │   ├── DashboardCards.js           # 5 metric cards
│   │   │   ├── DataQualityChart.js         # 4 Recharts visualizations
│   │   │   ├── ErrorTable.js               # Error display with severity
│   │   │   └── AnomalyList.js              # Anomaly display with color coding
│   │   ├── App.test.js                     # Unit tests
│   │   └── setupTests.js                   # Test configuration
│   │
│   ├── public/
│   │   ├── index.html                      # Main HTML entry
│   │   ├── manifest.json                   # PWA manifest
│   │   └── robots.txt                      # SEO robots file
│   │
│   ├── 📚 DOCUMENTATION FILES
│   ├── README.md                            # Frontend setup instructions
│   └── PHASE6_IMPLEMENTATION.md             # Frontend upgrade details
│
├── 🎯 PROJECT-LEVEL DOCUMENTATION
├── PROJECT_DOCUMENTATION.md                 # THIS FILE - Complete overview
├── PHASE3_IMPLEMENTATION_COMPLETE.md        # Database integration (Phase 3)
├── PHASE3_QUICK_REFERENCE.md               # Database quick reference
├── PHASE6_STATUS.md                        # Frontend completion (Phase 6)
├── PHASE6_QUICK_START.md                   # Frontend quick start (Phase 6)
│
├── 🚀 STARTUP SCRIPTS
├── start.bat                                # Windows startup script
├── start.sh                                 # Linux/Mac startup script
│
└── sample_*.csv                             # Sample data files (3 domains)
    ├── sample_banking.csv
    ├── sample_healthcare.csv
    └── sample_ecommerce.csv
```

### File Organization Benefits
- **Phase Documentation**: Each phase has dedicated implementation guides
- **Modular Backend**: Easy to extend with new domains or services
- **Component-Based Frontend**: Reusable React components
- **Clear Separation**: Models, Services, Routes in backend
- **Easy Navigation**: Sample data and quick reference guides

---

## BACKEND DETAILS

### Architecture: Modular Design Pattern

The backend follows a **modular, layered architecture** for better maintainability and scalability:

```
Request → Routes Layer → Services Layer → Models Layer → Response
   ↓
(Flask receives HTTP request)
   ↓
upload_routes.py (Route handlers)
   ↓
validation_service.py (Business logic)
file_service.py (File operations)
scoring_service.py (Calculations)
   ↓
validation_result.py (Data model)
   ↓
(JSON response returned)
```

### Core Framework: Flask
Flask is a lightweight Python web framework for building REST APIs.

### Backend Modules:

#### 1. **app.py** - Application Entry Point
**Location:** `backend/app.py`
**Purpose:** Main Flask initialization and configuration
**Responsibilities:**
- Create Flask application instance
- Enable CORS for frontend communication
- Configure upload folder and file size limits
- Register all routes from `routes/upload_routes.py`

**Code Example:**
```python
from flask import Flask
from flask_cors import CORS
from routes.upload_routes import register_routes

app = Flask(__name__)
CORS(app)
register_routes(app)
```

#### 2. **models/validation_result.py** - Data Models
**Location:** `backend/models/validation_result.py`
**Purpose:** Define data structures for validation results
**Contains:**
- `ValidationResult` class: Stores validation statistics and errors
- `to_dict()` method: Converts results to JSON format

**Key Attributes:**
- `total_records`: Count of all records processed
- `valid_records`: Count of valid records
- `invalid_records`: Count of invalid records
- `errors`: List of validation error messages
- `score_percentage`: Calculated success rate

#### 3. **services/validation_service.py** - Validation Logic
**Location:** `backend/services/validation_service.py`
**Purpose:** Contains all domain-specific validation rules
**Functions:**

| Function | Domain | Purpose |
|----------|--------|---------|
| `validate_banking_record(record)` | Banking | Validate age, income, credit_score |
| `validate_healthcare_record(record)` | Healthcare | Validate age, blood_group |
| `validate_ecommerce_record(record)` | E-commerce | Validate price, stock |
| `validate_data(file_path, domain)` | All | Main orchestrator function |

**Validation Flow:**
1. Parses CSV file row by row
2. Routes each record to correct domain validator
3. Collects errors and validates counts
4. Returns aggregated `ValidationResult`

#### 4. **services/file_service.py** - File Operations
**Location:** `backend/services/file_service.py`
**Purpose:** Handle file upload validation
**Functions:**
- `allowed_file(filename)`: Check if file extension is allowed (csv, txt)
- `get_allowed_extensions()`: Return set of allowed extensions

#### 5. **services/scoring_service.py** - Scoring Calculations
**Location:** `backend/services/scoring_service.py`
**Purpose:** Calculate validation metrics
**Functions:**
- `calculate_score_percentage(valid_records, total_records)`: Compute success percentage

#### 6. **routes/upload_routes.py** - API Endpoints
**Location:** `backend/routes/upload_routes.py`
**Purpose:** Define all HTTP endpoints and error handlers
**Function:** `register_routes(app)`: Registers all routes with Flask app

**Endpoints:**
- `GET /`: Health check
- `POST /upload`: File upload and validation
- Error handlers: 404, 413, 500

### Backend Port
- **Development:** http://localhost:5000
- **Production:** Deployed via Gunicorn

### Module Dependencies

```
app.py
  ↓
routes/upload_routes.py
  ├── models/validation_result.py
  ├── services/validation_service.py
  │   └── models/validation_result.py
  ├── services/file_service.py
  └── services/scoring_service.py
```

### How to Add a New Validation Domain

1. **Open** `services/validation_service.py`
2. **Add** new validation function:
   ```python
   def validate_mydomain_record(record):
       errors = []
       # validation logic here
       return len(errors) == 0, errors
   ```
3. **Update** `validate_data()` function to include new domain in validators dict
4. **Test** with sample CSV file

### File Upload Handling

**Process:**
1. Receives multipart/form-data requests
2. Validates file type before processing
3. Stores files temporarily in `uploads/` folder
4. Parses CSV content line by line
5. Validates each row against domain rules
6. Returns results as JSON

---

## FRONTEND DETAILS

### Framework: React 19.2.4
React is a JavaScript library for building user interfaces with reusable components.

### Key Files:

**1. public/index.html**
- Main HTML file served to browser
- Contains `<div id="root"></div>` where React mounts

**2. src/index.js**
- React entry point
- Renders App component to DOM

**3. src/App.js**
- Main React component
- Handles:
  - File input/selection UI
  - Domain selection dropdown
  - API call to backend via Axios
  - Results display
  - Error handling

**4. src/App.css**
- Styling for the user interface
- Form styling, upload button, results display

**5. src/index.css**
- Global CSS styles

**6. src/setupTests.js**
- Test configuration for Jest

### Frontend Port
- **Development:** http://localhost:3000
- Automatically opens when you run `npm start`
- Hot reload enabled (changes refresh automatically)

### User Interface Components
1. **File Input** - Users select CSV file to upload
2. **Domain Selector** - Dropdown to choose domain (Banking/Healthcare/E-commerce)
3. **Upload Button** - Triggers file upload to backend
4. **Results Section** - Displays:
   - Total records processed
   - Valid records count
   - Invalid records count
   - Success percentage
   - Error messages

### API Communication
- **Library:** Axios
- **Method:** Sends POST request to `http://localhost:5000/upload`
- **Format:** multipart/form-data (for file upload)
- **Response:** JSON results displayed in UI

---

## DEPENDENCIES

### Backend Dependencies (requirements.txt)
```
Flask==2.3.3              # Web framework
Flask-CORS==4.0.0         # CORS support
Werkzeug==2.3.7           # WSGI utilities
gunicorn==21.2.0          # Production server
python-dotenv==1.0.0      # Environment variables

# Future Dependencies (commented out)
# PyMySQL==1.1.0           # MySQL support
# psycopg2==2.9.7          # PostgreSQL support
# cx_Oracle==8.3.0         # Oracle DB2 support
# pika==1.3.1              # RabbitMQ for message queues
# celery==5.3.1            # Task queue for async jobs
```

### Frontend Dependencies (package.json)
```
react@19.2.4                      # React library
react-dom@19.2.4                  # React DOM rendering
react-scripts@5.0.1               # Build scripts
axios@1.14.0                      # HTTP client
@testing-library/react@16.3.2     # React testing
@testing-library/jest-dom@6.9.1   # Jest testing utilities
web-vitals@2.1.4                  # Performance monitoring
```

---

## API DOCUMENTATION

### Endpoint 1: Health Check
**Method:** GET
**URL:** `http://localhost:5000/`
**Purpose:** Verify backend is running

**Request:**
```
GET http://localhost:5000/
```

**Response (200 OK):**
```json
{
  "message": "Backend Running"
}
```

---

### Endpoint 2: File Upload & Validation
**Method:** POST
**URL:** `http://localhost:5000/upload`
**Purpose:** Upload CSV file and validate based on domain

**Request Headers:**
```
Content-Type: multipart/form-data
```

**Request Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | File | Yes | CSV or TXT file containing data |
| domain | String | Yes | One of: `banking`, `healthcare`, `ecommerce` |

**Request Example:**
```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@sample_banking.csv" \
  -F "domain=banking"
```

**Success Response (200 OK):**
```json
{
  "total_records": 100,
  "valid_records": 95,
  "invalid_records": 5,
  "score_percentage": 95.0,
  "errors": [
    "Record 5: Invalid age -5: Must be between 18 and 80",
    "Record 12: Invalid credit score 900: Must be between 300 and 850"
  ],
  "timestamp": "2026-04-12T10:30:45.123456"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "No file part in request"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "No selected file"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "File type not allowed. Allowed: csv, txt"
}
```

---

## VALIDATION RULES

### BANKING DOMAIN VALIDATION

**Expected CSV Columns:**
```
age, income, credit_score
```

**Validation Rules:**

| Field | Type | Valid Range | Rules |
|-------|------|-------------|-------|
| age | Integer | 18-80 | Must be valid working age |
| income | Float | > 0 | Must be positive number |
| credit_score | Integer | 300-850 | Standard FICO score range |

**Error Messages Example:**
- "Invalid age 15: Must be between 18 and 80"
- "Invalid income -50000: Must be greater than 0"
- "Invalid credit score 200: Must be between 300 and 850"

**Sample Data:** `sample_banking.csv`

**Future Integration:**
- Validate against DB2 regulatory compliance rules
- Call COBOL mainframe services for legacy credit scoring
- Integrate fraud detection services

---

### HEALTHCARE DOMAIN VALIDATION

**Expected CSV Columns:**
```
age, blood_group
```

**Validation Rules:**

| Field | Type | Valid Values | Rules |
|-------|------|--------------|-------|
| age | Integer | 0-150 | Valid human age range |
| blood_group | String | A, B, AB, O | Standard blood type groups |

**Error Messages Example:**
- "Invalid age 200: Must be between 0 and 150"
- "Invalid blood group XY: Must be A, B, AB, or O"

**Sample Data:** `sample_healthcare.csv`

**Future Integration:**
- Validate against medical compliance standards
- Connect to patient history database
- Check allergies and medication interactions

---

### E-COMMERCE DOMAIN VALIDATION

**Expected CSV Columns:**
```
product_name, price, stock
```

**Validation Rules:**

| Field | Type | Valid Range | Rules |
|-------|------|-------------|-------|
| product_name | String | Non-empty | Product must have name |
| price | Float | > 0 | Price must be positive |
| stock | Integer | >= 0 | Stock cannot be negative |

**Error Messages Example:**
- "Invalid product name: Cannot be empty"
- "Invalid price -99.99: Must be greater than 0"
- "Invalid stock -10: Cannot be negative"

**Sample Data:** `sample_ecommerce.csv`

**Future Integration:**
- Integrate with inventory management system
- Price validation against market rates
- Stock level alerts and predictions

---

## SETUP AND INSTALLATION

### System Requirements
- Windows, macOS, or Linux
- Python 3.8+ (for backend)
- Node.js 14+ and npm (for frontend)
- Git (optional, for version control)

### Backend Setup

**Step 1: Navigate to backend directory**
```bash
cd backend
```

**Step 2: Create Python virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**Step 3: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Verify Flask installation**
```bash
python -c "import flask; print(flask.__version__)"
```

### Frontend Setup

**Step 1: Navigate to frontend directory**
```bash
cd frontend
```

**Step 2: Install npm dependencies**
```bash
npm install
```

**Step 3: Verify React installation**
```bash
npm list react
```

---

## RUNNING THE APPLICATION

### Option 1: Manual Start (Both Components)

**Terminal 1 - Backend:**
```bash
cd backend
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
# Run Flask
python app.py
# Output: Running on http://localhost:5000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
# Output: Compiled successfully! Open http://localhost:3000
```

**Access:** Open browser to http://localhost:3000

### Option 2: Quick Start Scripts

**Windows:**
```bash
start.bat
```

**macOS/Linux:**
```bash
chmod +x start.sh
./start.sh
```

### Testing API Endpoints

**Using curl:**
```bash
# Test health check
curl http://localhost:5000/

# Test validation (with sample file)
curl -X POST http://localhost:5000/upload \
  -F "file=@backend/sample_banking.csv" \
  -F "domain=banking"
```

**Using Postman:**
1. Set method to POST
2. URL: http://localhost:5000/upload
3. Body → form-data
4. Key: "file" (type: File) → select sample_banking.csv
5. Key: "domain" (type: Text) → "banking"
6. Click Send

---

## FUTURE INTEGRATION POINTS

### 1. COBOL Mainframe Integration
**Purpose:** Connect with legacy mainframe systems
**Implementation:** Message queue (RabbitMQ/Celery)
**Benefits:** 
- Reuse legacy credit scoring algorithms
- Business rule engine integration
- Batch processing support

**Dependencies to uncomment:**
```python
pika==1.3.1        # RabbitMQ
celery==5.3.1      # Task queue
```

### 2. DB2 Database Integration
**Purpose:** Store validation results and historical data
**Implementation:** Connect to DB2 using cx_Oracle or ODBC
**Use Cases:**
- Audit trail of all validations
- Regulatory compliance tracking
- Historical data analysis
- Business rule repository

**Dependencies to uncomment:**
```python
cx_Oracle==8.3.0   # Oracle DB2
```

### 3. MySQL/PostgreSQL Integration
**Purpose:** Store user accounts and configuration
**Implementation:** ORM (SQLAlchemy) with PyMySQL/psycopg2
**Use Cases:**
- User authentication
- Custom validation rules per user
- Domain customization

**Dependencies to uncomment:**
```python
PyMySQL==1.1.0     # MySQL
psycopg2==2.9.7    # PostgreSQL
```

### 4. Microservices Architecture
**Purpose:** Scale validation domain by domain
**Implementation:** Separate service per domain (Banking, Healthcare, E-commerce)
**Benefits:**
- Independent scaling
- Team autonomy
- Simplified testing
- Easier deployment

### 5. API Authentication
**Purpose:** Secure API endpoints
**Implementation:** JWT tokens or OAuth2
**Libraries:** PyJWT, flask-jwt-extended

### 6. Advanced Logging & Monitoring
**Purpose:** Track system behavior and performance
**Implementation:** ELK stack (Elasticsearch, Logstash, Kibana)
**Libraries:** python-logging-loki or DataDog integration

### 7. GraphQL API
**Purpose:** Alternative to REST API for flexible queries
**Implementation:** Graphene-Python
**Benefits:**
- Client specifies exact data needed
- Reduce over-fetching
- Better for complex domain rules

---

## KEY FILES REFERENCE

### Core Application Files (Modular Backend)

| File | Purpose | Type | Key Content |
|------|---------|------|-------------|
| backend/app.py | Main Flask entry point | Python | Flask initialization, CORS, route registration |
| backend/models/validation_result.py | Data model | Python | ValidationResult class, to_dict() method |
| backend/services/validation_service.py | Validation logic | Python | Domain validators (banking, healthcare, ecommerce), validate_data() |
| backend/services/file_service.py | File utilities | Python | allowed_file(), get_allowed_extensions() |
| backend/services/scoring_service.py | Scoring logic | Python | calculate_score_percentage() |
| backend/routes/upload_routes.py | API endpoints | Python | register_routes(), endpoint handlers, error handlers |
| frontend/src/App.js | Main frontend component | React/JS | UI, file upload, API calls |
| backend/requirements.txt | Python dependencies | Text | All pip packages needed |
| frontend/package.json | Node dependencies | JSON | npm packages and scripts |

### Package Initialization Files

| File | Purpose |
|------|---------|
| backend/models/__init__.py | Exports ValidationResult for imports |
| backend/services/__init__.py | Exports all service functions for imports |
| backend/routes/__init__.py | Exports register_routes function |

### Configuration Files

| File | Purpose | Type |
|------|---------|------|
| public/index.html | React root HTML | HTML |
| public/manifest.json | PWA configuration | JSON |
| frontend/src/setupTests.js | Jest configuration | JavaScript |

### Sample Data Files (Testing)

| File | Domain | Purpose |
|------|--------|---------|
| backend/sample_banking.csv | Banking | Test data for banking validation |
| backend/sample_healthcare.csv | Healthcare | Test data for healthcare validation |
| backend/sample_ecommerce.csv | E-commerce | Test data for e-commerce validation |

### Documentation Files

| File | Purpose |
|------|---------|
| backend/README.md | Backend setup guide |
| frontend/README.md | Frontend setup guide |
| backend/API_TESTING_GUIDE.md | How to test API |
| backend/DEVELOPER_GUIDE.md | Development guidelines |
| backend/IMPLEMENTATION_SUMMARY.md | Implementation details |
| backend/QUICK_REFERENCE.md | Quick commands |
| PROJECT_DOCUMENTATION.md | THIS FILE - Complete overview |

### Startup Scripts

| File | Purpose | OS |
|------|---------|-----|
| start.bat | Automated startup | Windows |
| start.sh | Automated startup | Linux/macOS |

### Import Hierarchy

**Access Pattern from app.py:**
```python
# Main app entry point simply registers routes
from routes.upload_routes import register_routes
register_routes(app)

# Inside upload_routes.py:
from services.validation_service import validate_data
from services.file_service import allowed_file
from models.validation_result import ValidationResult

# Templates for imports in your code:
from models import ValidationResult
from services import validate_data, validate_banking_record, allowed_file
from routes import register_routes
```

---

## ENVIRONMENT & PORTS

### Development Ports
- **Frontend:** http://localhost:3000 (React)
- **Backend:** http://localhost:5000 (Flask/Python)

### Folder Permissions
- `backend/uploads/` - Must be writable (temporary file storage)

### Environment Variables (Optional)
Create `.env` file in backend folder:
```
FLASK_ENV=development
FLASK_DEBUG=True
MAX_FILE_SIZE=16777216
```

---

## TESTING WORKFLOW

### Backend Testing
1. Start backend: `python app.py`
2. Test endpoints:
   ```bash
   # Health check
   curl http://localhost:5000/
   
   # Upload validation
   curl -X POST http://localhost:5000/upload \
     -F "file=@sample_banking.csv" \
     -F "domain=banking"
   ```

### Frontend Testing
1. Start frontend: `npm start`
2. Manual UI testing:
   - Select file via upload input
   - Choose domain from dropdown
   - Click upload button
   - Verify results display
3. Run automated tests: `npm test`

### Integrated Testing
1. Both backend and frontend running
2. Use frontenduploaded to test full flow
3. Verify data flows correctly end-to-end

---

## DEPLOYMENT CONSIDERATIONS

### Backend Deployment (Production)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```
- Uses Gunicorn WSGI server
- 4 worker processes
- Listens on all interfaces

### Frontend Deployment (Production)
```bash
npm run build
# Creates optimized build in frontend/build/ folder
```
- Deploy `build/` folder to static hosting
- CDN for better performance
- Environment variables for API URL

### Docker Containerization (Future)
```dockerfile
# Backend Dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]

# Frontend Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html
```

---

## TROUBLESHOOTING GUIDE

### Backend Issues
1. **Port 5000 already in use:**
   - Kill process: `lsof -ti:5000 | xargs kill -9` (macOS/Linux)
   - Or change Flask port in app.py

2. **Module not found error:**
   - Ensure virtual environment is activated
   - Run: `pip install -r requirements.txt`

3. **CORS errors:**
   - Ensure Flask-CORS is installed
   - Check frontend URL matches CORS config

### Frontend Issues
1. **Port 3000 already in use:**
   - Kill process or change: `PORT=3001 npm start`

2. **API connection refused:**
   - Ensure backend is running on port 5000
   - Check firewall settings
   - Verify baseURL in Axios config

3. **Module not found:**
   - Delete node_modules: `rm -rf node_modules`
   - Reinstall: `npm install`

---

## PROJECT STATISTICS

- **Total Lines of Code:** ~500+ (backend app.py)
- **React Components:** 1 Main (App.js)
- **API Endpoints:** 2 (health check, upload)
- **Supported Domains:** 3 (Banking, Healthcare, E-commerce)
- **Total Dependencies:** ~20 (backend + frontend combined)
- **Max File Upload:** 16MB
- **Allowed File Types:** CSV, TXT

---

## 🚀 PHASE 3 UPGRADE: DATA QUALITY ASSESSMENT SYSTEM

### What's New (Major Upgrade)

Your project has been upgraded from a simple "data validator" to a "Data Quality Assessment System" with industry-standard metrics!

#### 1. THREE DATA QUALITY DIMENSIONS

Instead of just a pass/fail score, you now get:

**A) Completeness Score (40% weight)**
- Measures: % of records with ALL required fields populated
- Calculation: `complete_records / total_records * 100`
- Why Important: Missing data is unusable data
- Example: If 1 record is missing the "income" field out of 100, completeness = 99%

**B) Validity Score (40% weight)**
- Measures: % of records that pass domain validation rules
- Calculation: `valid_records / total_records * 100`
- Why Important: Incorrect data causes wrong business decisions
- Example: Age values outside 18-80 are invalid

**C) Consistency Score (20% weight)**
- Measures: % of records following established data patterns
- Calculation: `consistent_records / total_records * 100`
- Why Important: Anomalies indicate potential issues or outliers
- Example: Age value > 150 is unrealistic, stock > 1,000,000 is suspicious

#### 2. WEIGHTED FINAL SCORE (Industry Standard)

```
final_score = (
    0.4 * completeness_score +
    0.4 * validity_score +
    0.2 * consistency_score
)
```

**Quality Ratings:**
- **Score >= 95%:** EXCELLENT - Production ready
- **Score >= 85%:** GOOD - Minor issues, use with caution
- **Score >= 75%:** ACCEPTABLE - Needs review before use
- **Score < 75%:** POOR - Significant remediation required

#### 3. EXAMPLE RESPONSE (Before vs After)

**BEFORE (Phase 1-2):**
```json
{
  "total_records": 100,
  "valid_records": 95,
  "invalid_records": 5,
  "score_percentage": 95.0,
  "errors": [...]
}
```

**AFTER (Phase 3 - NEW):**
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
  "score_percentage": 95.0,
  "stored": true,
  "timestamp": "2026-04-12T10:30:45.123456",
  "errors": [...]
}
```

#### 4. DATABASE STORAGE (No Longer "Future")

**NEW: Persistent Storage with SQLite**

All validation results are now automatically stored in a database (`validation_results.db`) with:
- Timestamp of validation
- Domain used
- Filename
- All metrics (completeness, validity, consistency, final scores)
- Error messages
- Query capabilities for historical analysis

**Database File Location:**
```
backend/validation_results.db
```

---

## NEW API ENDPOINTS (PHASE 3)

### 1. Upload & Validate (Enhanced)
**POST** `/upload`
- Returns data quality dimensions + record_id
- Automatically stores results in database
- Response includes `"stored": true` and `record_id`

### 2. Retrieve Stored Result (NEW)
**GET** `/results/<record_id>`
```bash
curl http://localhost:5000/results/42
```
Returns the complete validation result from database.

### 3. Domain Statistics (NEW)
**GET** `/stats/<domain>`
```bash
curl http://localhost:5000/stats/banking
```
Returns aggregated metrics:
```json
{
  "total_validations": 25,
  "avg_final_score": 92.5,
  "avg_completeness": 98.0,
  "avg_validity": 92.0,
  "avg_consistency": 90.0,
  "best_score": 99.5,
  "worst_score": 78.3
}
```

### 4. Validation History (NEW)
**GET** `/history?limit=10`
```bash
curl http://localhost:5000/history?limit=10
```
Returns 10 most recent validations (sortable, filterable).

### 5. Export Data (NEW)
**GET** `/export?domain=banking&format=json`
```bash
curl http://localhost:5000/export?domain=banking&format=csv > results.csv
```
Export validation data as JSON or CSV for reporting.

### 6. Database Stats (NEW)
**GET** `/db-stats`
```bash
curl http://localhost:5000/db-stats
```
Returns database health metrics.

---

## NEW SERVICE MODULES

### 1. database_service.py (NEW - PHASE 3)
**Purpose:** Handle all database operations with SQLite

**Key Functions:**
- `init_database()` - Creates schema on startup
- `store_validation_result(result, domain, filename)` - Saves validation to DB
- `get_validation_result(record_id)` - Retrieves stored result
- `get_domain_statistics(domain)` - Gets aggregated stats
- `get_recent_validations(limit)` - Gets history
- `export_validation_data(domain, format)` - Exports for reporting
- `get_database_stats()` - Database health metrics

**Database Schema:**
```sql
CREATE TABLE validation_results (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    domain TEXT,
    filename TEXT,
    total_records INTEGER,
    valid_records INTEGER,
    invalid_records INTEGER,
    completeness_score REAL,
    validity_score REAL,
    consistency_score REAL,
    final_score REAL,
    errors TEXT (JSON array),
    created_at DATETIME
)
```

### 2. Enhanced scoring_service.py
**New Functions:**
- `calculate_completeness_score()` - Data presence metric
- `calculate_validity_score()` - Data correctness metric
- `calculate_consistency_score()` - Data pattern metric
- `calculate_weighted_score()` - Industry-standard formula
- `get_quality_rating()` - Human-readable ratings
- `get_score_breakdown()` - Detailed analysis

### 3. Enhanced validation_service.py
**New Functions:**
- `is_record_complete()` - Checks completeness
- `is_record_consistent()` - Checks patterns
- Updated `validate_data()` - Calculates all 3 dimensions

---

## DATABASE CONFIGURATION

### Default: SQLite (Built-in, No Setup Required)
```
backend/validation_results.db
```

### Optional: MySQL
Uncomment in `requirements.txt`:
```python
PyMySQL==1.1.0
```

Connection: Modify `database_service.py` to use MySQL driver

### Optional: PostgreSQL
Uncomment in `requirements.txt`:
```python
psycopg2-binary==2.9.7
```

Connection: Modify `database_service.py` to use PostgreSQL driver

---

## PROJECT STATISTICS

- **Total Lines of Code:** ~500+ (backend app.py)
- **React Components:** 1 Main (App.js)
- **API Endpoints:** 8 (6 new in Phase 3)
- **Supported Domains:** 3 (Banking, Healthcare, E-commerce)
- **Total Dependencies:** ~20 (backend + frontend combined)
- **Max File Upload:** 16MB
- **Allowed File Types:** CSV, TXT
- **Database:** SQLite with automatic schema initialization
- **Storage:** Unlimited validation history in database

---

## SUCCESS METRICS

The project is working correctly when:
- ✅ Backend server starts without errors
- ✅ Frontend loads at http://localhost:3000
- ✅ File upload form is functional
- ✅ Sample CSV files validate correctly
- ✅ Results display with correct scoring
- ✅ Error messages are helpful and accurate
- ✅ No console errors in browser
- ✅ No Python errors in terminal

---

## MODIFICATION GUIDE FOR AI ASSISTANTS

When working with this project, AI assistants should:

1. **Understand the modular architecture:** Code is organized by concern (models, services, routes)
2. **Respect module boundaries:** Don't mix business logic with routing
3. **Maintain JSON responses:** API contracts must stay consistent
4. **Test changes:** Always verify with sample CSV files
5. **Check dependencies:** Changes in one module might affect imports in others
6. **Update docs:** Keep this file in sync with code changes
7. **Version carefully:** Track what changed and why

### Common Modification Tasks

#### Adding a New Validation Domain

**Step 1:** Create validation function in `services/validation_service.py`
```python
def validate_mydomain_record(record):
    """Validate a single mydomain record."""
    errors = []
    # validation logic
    return len(errors) == 0, errors
```

**Step 2:** Register domain in `validate_data()` function
```python
validators = {
    'banking': validate_banking_record,
    'healthcare': validate_healthcare_record,
    'ecommerce': validate_ecommerce_record,
    'mydomain': validate_mydomain_record  # Add here
}
```

**Step 3:** Test with sample CSV file

#### Changing File Upload Limits

**Modify:** `backend/app.py`
```python
MAX_FILE_SIZE = 32 * 1024 * 1024  # Change from 16MB to 32MB
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
```

#### Adding New Calculation Service

**Create:** `services/mynewservice.py`
```python
def my_calculation_function(param1, param2):
    """New calculation logic."""
    return result
```

**Update:** `services/__init__.py`
```python
from .mynewservice import my_calculation_function
__all__ = [..., 'my_calculation_function']
```

**Use in routes:**
```python
from services import my_calculation_function
result = my_calculation_function(value1, value2)
```

#### Customizing Validation Rules

**Modify:** `services/validation_service.py`
- Edit the validation function for the domain
- Change min/max values, allowed values, etc.
- Test with sample data

#### Adding Database Support

**When ready to add database:**

1. **Create new service:** `services/database_service.py`
2. **Use dependency injection:** Pass DB connection to services
3. **Keep validation logic separate:** DB operations in DB service only
4. **Example:**
   ```python
   # services/database_service.py
   def save_validation_result(result):
       """Save result to database."""
       db.insert(...)
   
   # routes/upload_routes.py
   from services.database_service import save_validation_result
   result = validate_data(file_path, domain)
   save_validation_result(result)  # Optional: save to DB
   ```

### Project Modification Checklist

When upgrading or modifying the project:

- [ ] Identify which module(s) need changes (models/services/routes)
- [ ] Make code changes in the appropriate module
- [ ] Update `__init__.py` if adding new functions
- [ ] Test changes with sample data
- [ ] Update PROJECT_DOCUMENTATION.md with changes
- [ ] Test full integration (frontend + backend)
- [ ] Check for import errors
- [ ] Verify error handling works

### Common Upgrade Tasks

| Task | Files to Modify | Complexity |
|------|-----------------|------------|
| Add new validation domain | `services/validation_service.py` | Low |
| Change validation rules | `services/validation_service.py` | Low |
| Add new calculation | `services/mynewservice.py` + `__init__.py` | Medium |
| Add database support | Create new service + ORM setup | High |
| Add authentication | `routes/upload_routes.py` + middleware | High |
| Add logging | Insert in individual services | Medium |
| Scale to microservices | Separate each domain into own Flask app | Very High |

---

## QUICK COMMANDS REFERENCE

```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
python app.py
pip install -r requirements.txt

# Frontend
cd frontend
npm install
npm start
npm run build
npm test

# Testing
curl http://localhost:5000/
curl -X POST http://localhost:5000/upload \
  -F "file=@backend/sample_banking.csv" \
  -F "domain=banking"
```

---

## CONTACT & SUPPORT

- **Project Type:** Full-stack web application
- **Architecture:** Client-Server (Frontend + REST API)
- **Best For:** Understanding system design, API documentation, integration planning
- **AI Capability:** Can be used with ChatGPT, Claude, GitHub Copilot for upgrades

---

**END OF PROJECT DOCUMENTATION**

This file contains comprehensive information about the project structure, functionality, technologies, and APIs. Use this as a complete reference when discussing the project with AI assistants.
