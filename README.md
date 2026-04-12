# 🎯 AI Data Validation System

**Version:** 2.0.0 (Phase 7 - Security & COBOL Integration)  
**Status:** ✅ Production Ready  
**Updated:** April 12, 2026

A comprehensive **enterprise-grade data validation system** with multi-domain support, anomaly detection, interactive dashboard, and mainframe integration capabilities.

## ✨ Key Features

### Core Validation (Phases 1-4)
- ✅ Multi-domain validation (Banking, Healthcare, E-commerce)
- ✅ Domain-specific business rules
- ✅ Real-time error detection and reporting
- ✅ Modular, extensible architecture

### Advanced Analytics (Phase 5)
- ✅ Anomaly detection with statistical analysis
- ✅ 3-dimensional quality scoring
  - **Completeness**: % of non-null fields (40% weight)
  - **Validity**: % matching business rules (40% weight)
  - **Consistency**: % without conflicts (20% weight)
- ✅ Domain-specific outlier detection
- ✅ Anomaly severity classification

### Interactive Dashboard (Phase 6)
- ✅ Professional React-based UI
- ✅ Real-time data visualization (Recharts)
- ✅ 6+ interactive components
- ✅ Domain selector with color coding
- ✅ Drag-and-drop file upload
- ✅ Anomaly display with severity indicators

### Enterprise Security (Phase 7)
- ✅ Input validation and CSV sanitization
- ✅ Rate limiting (10 uploads/hour per IP)
- ✅ Security headers (XSS, clickjacking, MIME-sniffing protection)
- ✅ Comprehensive audit logging
- ✅ SQL injection prevention
- ✅ Formula injection blocking

### Mainframe Integration (Phase 7)
- ✅ COBOL integration framework
- ✅ Message queue pattern (RabbitMQ ready)
- ✅ 3 COBOL program interfaces
- ✅ DB2 database integration ready
- ✅ Production deployment support

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup (Flask API)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
python app.py
```

Server runs at: `http://localhost:5000`

### Frontend Setup (React Dashboard)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Dashboard runs at: `http://localhost:3000`

### Sample CSV Upload

```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@backend/sample_banking.csv" \
  -F "domain=banking"
```

## 📊 Validation Domains

### 🏦 Banking Domain
- Validates customer financial profiles
- Rules: Age (18-80), Income (>0), Credit Score (300-850)
- Anomalies: Extreme income, age patterns, credit extremes

### 🏥 Healthcare Domain
- Validates patient health records
- Rules: Age (0-120), Blood Group (valid types)
- Anomalies: Age extremes, unusual blood group patterns

### 🛒 E-commerce Domain
- Validates product inventory data
- Rules: Price (>0), Stock (≥0)
- Anomalies: Extreme prices, stock inconsistencies

## 📡 API Response Format

All validations return comprehensive metrics:

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
  "anomalies": [...],
  
  "errors": [...],
  "stored": true,
  "timestamp": "2026-04-12T10:30:45.123456"
}
```

## 🔒 Security Features (Phase 7)

### Input Validation
- ✅ Filename validation (prevent path traversal)
- ✅ File size limits (100MB max)
- ✅ MIME type detection (CSV/text only)
- ✅ UTF-8 encoding validation

### Attack Prevention
- ✅ Formula injection blocking (`=`, `@`, `+`, `-`)
- ✅ Script injection prevention (`<script>`, `javascript:`)
- ✅ SQL injection detection (dangerous keywords)
- ✅ Null byte removal
- ✅ Path traversal prevention

### Security Headers
- ✅ X-Content-Type-Options: nosniff
- ✅ X-Frame-Options: DENY
- ✅ Content-Security-Policy: strict
- ✅ Referrer-Policy: strict-origin-when-cross-origin
- ✅ Permissions-Policy: disabled device APIs

### Rate Limiting
- ✅ 10 requests per hour per IP
- ✅ Automatic cleanup
- ✅ 429 response on limit
- ✅ Extensible configuration

## 📚 Documentation

### Getting Started
- **Backend**: [backend/README.md](backend/README.md)
- **Frontend**: [frontend/README.md](frontend/README.md)
- **Project Overview**: [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)

### Technical Guides
- **API Testing**: [backend/API_TESTING_GUIDE.md](backend/API_TESTING_GUIDE.md)
- **Developer Guide**: [backend/DEVELOPER_GUIDE.md](backend/DEVELOPER_GUIDE.md)
- **Implementation Summary**: [backend/IMPLEMENTATION_SUMMARY.md](backend/IMPLEMENTATION_SUMMARY.md)
- **Quick Reference**: [backend/QUICK_REFERENCE.md](backend/QUICK_REFERENCE.md)

### Phase-Specific Documentation
- **Phase 5** (Anomaly Detection): [backend/PHASE5_IMPLEMENTATION.md](backend/PHASE5_IMPLEMENTATION.md)
- **Phase 6** (Frontend Dashboard): [frontend/PHASE6_IMPLEMENTATION.md](frontend/PHASE6_IMPLEMENTATION.md)
- **Phase 7** (Security & COBOL):
  - [backend/PHASE7_IMPLEMENTATION.md](backend/PHASE7_IMPLEMENTATION.md) - Full technical guide
  - [backend/PHASE7_QUICK_REFERENCE.md](backend/PHASE7_QUICK_REFERENCE.md) - Quick start
  - [backend/PHASE7_STATUS.md](backend/PHASE7_STATUS.md) - Completion status

## 🏗️ Architecture

### Technology Stack

**Backend**
- Flask 2.3.3 (Python web framework)
- SQLite3 (persistent database)
- RabbitMQ ready (message queue)
- Python 3.8+

**Frontend**
- React 19.2.4
- Recharts 2.12.7 (data visualization)
- Axios 1.14.0 (HTTP client)
- Modern CSS3 (500+ lines)

### System Architecture

```
Frontend (React)
    ↓ HTTP/CORS (Secured)
API Server (Flask)
    ├─ Validation Service
    ├─ Anomaly Detection
    ├─ Security Layer
    └─ Mainframe Interface
    ↓
Database (SQLite3)
    + Optional: RabbitMQ, DB2, COBOL
```

## 🧪 Testing

### Unit Tests
```bash
# Backend
cd backend
python -m pytest tests/

# Frontend
cd frontend
npm test
```

### Manual Testing
```bash
# Test with sample files
curl -X POST http://localhost:5000/upload \
  -F "file=@backend/sample_banking.csv" \
  -F "domain=banking"
```

## 📊 Directory Structure

```
AI-DATA-VALIDATION/
├── backend/                          # Python Flask API
│   ├── services/                    # Business logic
│   │   ├── validation_service.py   # Domain validators
│   │   ├── anomaly_detection.py    # Phase 5
│   │   ├── security_utils.py       # Phase 7
│   │   ├── mainframe_service.py    # Phase 7
│   │   └── database_service.py     # Phase 3
│   ├── models/validation_result.py # Data model
│   ├── routes/upload_routes.py     # API endpoints
│   └── app.py                       # Main app
│
├── frontend/                         # React Dashboard
│   ├── src/
│   │   ├── components/             # 6+ React components
│   │   └── App.js                  # Main component
│   └── package.json
│
├── PROJECT_DOCUMENTATION.md         # Project overview
├── PHASE*.md                        # Phase documentation
├── sample_*.csv                     # Sample data
└── start.bat / start.sh            # Startup scripts
```

## 🚀 Deployment

### Development
```bash
# Terminal 1: Backend
cd backend
python app.py

# Terminal 2: Frontend
cd frontend
npm start
```

### Production
```bash
# Backend
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Frontend
npm run build
# Serve from static file server or CDN
```

### Docker (Optional)
```bash
docker build -t validation-app .
docker run -p 5000:5000 validation-app
```

## 📋 Validation Rules

### Banking
| Field | Rules | Anomaly Threshold |
|-------|-------|-------------------|
| Age | 18-80 | Extreme values |
| Income | > 0 | > $10M |
| Credit Score | 300-850 | Extremes |

### Healthcare
| Field | Rules | Anomaly Threshold |
|-------|-------|-------------------|
| Age | 0-120 | > 110 |
| Blood Group | A, B, O, AB (±/−) | Invalid types |

### E-commerce
| Field | Rules | Anomaly Threshold |
|-------|-------|-------------------|
| Price | > 0 | > $100K |
| Stock | ≥ 0 | Extremes |

## 🔄 Integration Points

### Phase 7: Mainframe Integration
- **Framework**: RabbitMQ message queue
- **Format**: JSON COBOL records
- **Programs**:
  1. CREDIT.RISK.CALC (Banking)
  2. COMPLIANCE.VALIDATE (All domains)
  3. DATA.ENRICH (All domains)
- **Database**: DB2 integration ready

## 🐛 Common Issues

### Backend Connection Errors
```bash
# Check if backend is running
curl http://localhost:5000/health

# Expected response
{"status": "healthy", "version": "2.0.0"}
```

### CORS Errors
- Frontend and backend must be on same origin or backend CORS configured
- Backend CORS configured for http://localhost:3000

### File Upload Fails
- Check file format (CSV/TXT only)
- Check file size (max 100MB)
- Verify domain parameter (banking/healthcare/ecommerce)

## 📞 Support

### Documentation
1. Check [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)
2. Review backend/README.md for API details
3. Check frontend/README.md for UI guide
4. Review phase-specific documentation

### Troubleshooting
1. Check console for error messages
2. Verify file format and domain
3. Review API_TESTING_GUIDE.md
4. Check security logs for validation failures

## 🎯 Roadmap

### Phase 8 (Planned)
- [ ] API authentication (JWT/OAuth2)
- [ ] Role-based access control
- [ ] Advanced analytics dashboard
- [ ] PDF/Excel export

### Phase 9 (Planned)
- [ ] Real-time monitoring
- [ ] Performance metrics
- [ ] Security threat detection
- [ ] Automated alerting

### Phase 10 (Planned)
- [ ] Multi-tenant support
- [ ] Webhook integrations
- [ ] Custom validation rules
- [ ] Advanced reporting

## 📄 License

This project is part of the AI Data Validation System.

## 👨‍💻 Authors

**AI Data Validation Team**

## 📞 Contact

For questions or issues:
1. Review comprehensive documentation
2. Check API testing guide
3. Verify sample data format
4. Review error logs

---

**Project Status**: ✅ Production Ready (Phase 7 Complete)  
**Last Updated**: April 12, 2026  
**Support**: Comprehensive documentation included
