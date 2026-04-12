# Quick Reference Card

## 🚀 Startup (Choose One)

### Windows
```bash
cd backend
start.bat
```

### Linux/Mac
```bash
cd backend
./start.sh
```

### Manual
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
python app.py
```

---

## 📡 API Endpoints

### Health Check
```bash
GET http://localhost:5000/
Response: {"message": "Backend Running"}
```

### Upload & Validate
```bash
POST http://localhost:5000/upload
Body: multipart/form-data
  - file: <CSV file>
  - domain: banking | healthcare | ecommerce
```

---

## 📊 Validation Rules

### Banking
```
age:          18 - 80
income:       > 0
credit_score: 300 - 850
```

### Healthcare
```
age:          0 - 120
blood_group:  A+, A-, B+, B-, O+, O-, AB+, AB-
```

### E-commerce
```
price:        > 0 and < 9,999,999
stock:        ≥ 0
```

---

## 🧪 Test Commands

### Health Check
```bash
curl http://localhost:5000/
```

### Banking
```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@sample_banking.csv" \
  -F "domain=banking"
```

### Healthcare
```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@sample_healthcare.csv" \
  -F "domain=healthcare"
```

### E-commerce
```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@sample_ecommerce.csv" \
  -F "domain=ecommerce"
```

---

## 📋 Response Format

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

## 📁 File Structure

```
backend/
├── app.py                    ← Main application
├── requirements.txt          ← Dependencies
├── sample_banking.csv        ← Test data
├── sample_healthcare.csv     ← Test data
├── sample_ecommerce.csv      ← Test data
├── uploads/                  ← Uploaded files
├── README.md                 ← Full documentation
├── API_TESTING_GUIDE.md      ← Testing guide
└── DEVELOPER_GUIDE.md        ← Development guide
```

---

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| Python not found | Install Python 3.8+ |
| Module not found | Run `pip install -r requirements.txt` |
| Port already in use | Change port in app.py (line 412) |
| File not uploading | Check file format (must be CSV or TXT) |
| Invalid domain error | Check domain name (banking/healthcare/ecommerce) |

---

## 📚 Documentation

- **README.md** - Complete user guide
- **API_TESTING_GUIDE.md** - How to test the API
- **DEVELOPER_GUIDE.md** - How to extend the system
- **IMPLEMENTATION_SUMMARY.md** - What was built

---

## 🎯 Key Features

✓ Flask REST API
✓ CORS enabled
✓ File upload & parsing
✓ 3 domain validators
✓ Error handling
✓ JSON responses
✓ Modular code
✓ Ready for DB & COBOL integration

---

## 💻 CSV Format Required

### Banking
```csv
age,income,credit_score
28,55000,750
35,75000,680
```

### Healthcare
```csv
age,blood_group
28,O+
35,A+
```

### E-commerce
```csv
price,stock
29.99,150
49.99,200
```

---

## ⚙️ Configuration

Create `.env` from `.env.example`:
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```
FLASK_ENV=development
DATABASE_URL=db2://your_connection
RABBITMQ_URL=amqp://your_broker
```

---

## 🚀 Production Deployment

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# With SSL (production)
gunicorn --certfile=cert.pem --keyfile=key.pem -b 0.0.0.0:5000 app:app
```

---

## 🔗 Integration Points (Future)

### Database (DB2)
```python
from database import DB2Connection
db = DB2Connection(os.getenv('DATABASE_URL'))
```

### Message Queue (COBOL)
```python
from message_queue import ValidationQueue
queue = ValidationQueue(os.getenv('RABBITMQ_URL'))
queue.send_to_cobol(domain, record)
```

---

## 📞 Quick Help

- Start the app with `start.bat` (Windows) or `./start.sh` (Linux/Mac)
- Server runs at `http://localhost:5000`
- Test with `curl` or Postman
- Check logs in console output
- See README.md for detailed documentation

---

## 🎓 Adding New Domain

1. Create validation function (see DEVELOPER_GUIDE.md)
2. Add to validators dictionary
3. Create sample CSV file
4. Test with curl
5. Update documentation

Example:
```python
def validate_custom_record(record):
    errors = []
    # Add validation rules
    return len(errors) == 0, errors

# Add to validators in validate_data()
validators = {
    'banking': validate_banking_record,
    'healthcare': validate_healthcare_record,
    'ecommerce': validate_ecommerce_record,
    'custom': validate_custom_record  # ← Your new domain
}
```

---

**Version**: 1.0.0 | **Status**: Complete | **Server**: http://localhost:5000
