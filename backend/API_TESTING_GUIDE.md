# API Testing Guide

Complete guide to test the Flask backend with various tools and methods.

## 📌 Prerequisites

1. Backend is running on `http://localhost:5000`
2. Sample CSV files are available in the backend directory
3. You have one of the following tools installed:
   - cURL (command line)
   - Postman (GUI)
   - Python with requests library
   - VS Code REST Client extension

---

## 🔵 Method 1: cURL (Command Line)

### 1. Health Check Test

```bash
curl -X GET http://localhost:5000/
```

**Expected Response:**
```json
{
  "message": "Backend Running"
}
```

---

### 2. Banking Domain Validation

```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@sample_banking.csv" \
  -F "domain=banking"
```

**Expected Response:**
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

### 3. Healthcare Domain Validation

```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@sample_healthcare.csv" \
  -F "domain=healthcare"
```

**Expected Response:**
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

### 4. E-commerce Domain Validation

```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@sample_ecommerce.csv" \
  -F "domain=ecommerce"
```

**Expected Response:**
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

### 5. Error Testing - Missing Domain Parameter

```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@sample_banking.csv"
```

**Expected Response (400):**
```json
{
  "error": "No domain specified"
}
```

---

### 6. Error Testing - Invalid Domain

```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@sample_banking.csv" \
  -F "domain=invalid_domain"
```

**Expected Response (200 with errors):**
```json
{
  "total_records": 0,
  "valid_records": 0,
  "invalid_records": 0,
  "score_percentage": 0,
  "errors": [
    "Unknown domain 'invalid_domain'. Must be one of: ['banking', 'healthcare', 'ecommerce']"
  ]
}
```

---

### 7. Error Testing - No File Provided

```bash
curl -X POST http://localhost:5000/upload \
  -F "domain=banking"
```

**Expected Response (400):**
```json
{
  "error": "No file provided"
}
```

---

## 🟣 Method 2: Postman

### Setup

1. **Open Postman** (or download from https://www.postman.com)
2. **Create New Request**

### Testing Health Check

1. **Request Type**: GET
2. **URL**: `http://localhost:5000/`
3. **Click Send**

### Testing File Upload - Banking

1. **Request Type**: POST
2. **URL**: `http://localhost:5000/upload`
3. **Go to "Body" tab**
4. **Select "form-data"**
5. **Add fields**:
   - Key: `file` | Type: File | Value: Select `sample_banking.csv`
   - Key: `domain` | Type: Text | Value: `banking`
6. **Click Send**

### Testing File Upload - Healthcare

1. **Request Type**: POST
2. **URL**: `http://localhost:5000/upload`
3. **Body** (form-data):
   - Key: `file` | Type: File | Value: Select `sample_healthcare.csv`
   - Key: `domain` | Type: Text | Value: `healthcare`
4. **Click Send**

### Testing File Upload - E-commerce

1. **Request Type**: POST
2. **URL**: `http://localhost:5000/upload`
3. **Body** (form-data):
   - Key: `file` | Type: File | Value: Select `sample_ecommerce.csv`
   - Key: `domain` | Type: Text | Value: `ecommerce`
4. **Click Send**

---

## 🐍 Method 3: Python with Requests Library

### Setup

```bash
pip install requests
```

### Test Script

Create a file named `test_api.py`:

```python
import requests
import json

BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test health check endpoint"""
    print("Testing Health Check...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_banking_validation():
    """Test banking domain validation"""
    print("Testing Banking Validation...")
    files = {'file': open('sample_banking.csv', 'rb')}
    data = {'domain': 'banking'}
    response = requests.post(f"{BASE_URL}/upload", files=files, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_healthcare_validation():
    """Test healthcare domain validation"""
    print("Testing Healthcare Validation...")
    files = {'file': open('sample_healthcare.csv', 'rb')}
    data = {'domain': 'healthcare'}
    response = requests.post(f"{BASE_URL}/upload", files=files, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_ecommerce_validation():
    """Test e-commerce domain validation"""
    print("Testing E-commerce Validation...")
    files = {'file': open('sample_ecommerce.csv', 'rb')}
    data = {'domain': 'ecommerce'}
    response = requests.post(f"{BASE_URL}/upload", files=files, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_error_scenarios():
    """Test error scenarios"""
    print("Testing Error Scenarios...")
    
    # Test 1: Missing domain
    print("1. Missing domain parameter:")
    files = {'file': open('sample_banking.csv', 'rb')}
    response = requests.post(f"{BASE_URL}/upload", files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    
    # Test 2: Invalid domain
    print("2. Invalid domain:")
    files = {'file': open('sample_banking.csv', 'rb')}
    data = {'domain': 'invalid'}
    response = requests.post(f"{BASE_URL}/upload", files=files, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    
    # Test 3: No file provided
    print("3. No file provided:")
    data = {'domain': 'banking'}
    response = requests.post(f"{BASE_URL}/upload", data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

if __name__ == '__main__':
    print("=" * 60)
    print("API Testing Suite")
    print("=" * 60 + "\n")
    
    test_health_check()
    test_banking_validation()
    test_healthcare_validation()
    test_ecommerce_validation()
    test_error_scenarios()
    
    print("=" * 60)
    print("Testing Complete!")
    print("=" * 60)
```

### Run the Test Script

```bash
python test_api.py
```

---

## 📄 Method 4: VS Code REST Client Extension

### Setup

1. Install "REST Client" extension by Huachao Mao
2. Create a file named `test_api.http` in the backend directory

### Test File Content

```http
### Health Check
GET http://localhost:5000/

### Banking Validation
POST http://localhost:5000/upload
Content-Type: multipart/form-data; boundary=----FormBoundary

------FormBoundary
Content-Disposition: form-data; name="file"; filename="sample_banking.csv"
Content-Type: text/csv

< ./sample_banking.csv
------FormBoundary
Content-Disposition: form-data; name="domain"

banking
------FormBoundary--

### Healthcare Validation
POST http://localhost:5000/upload
Content-Type: multipart/form-data; boundary=----FormBoundary

------FormBoundary
Content-Disposition: form-data; name="file"; filename="sample_healthcare.csv"
Content-Type: text/csv

< ./sample_healthcare.csv
------FormBoundary
Content-Disposition: form-data; name="domain"

healthcare
------FormBoundary--

### E-commerce Validation
POST http://localhost:5000/upload
Content-Type: multipart/form-data; boundary=----FormBoundary

------FormBoundary
Content-Disposition: form-data; name="file"; filename="sample_ecommerce.csv"
Content-Type: text/csv

< ./sample_ecommerce.csv
------FormBoundary
Content-Disposition: form-data; name="domain"

ecommerce
------FormBoundary--

### Missing Domain Error
POST http://localhost:5000/upload
Content-Type: multipart/form-data; boundary=----FormBoundary

------FormBoundary
Content-Disposition: form-data; name="file"; filename="sample_banking.csv"
Content-Type: text/csv

< ./sample_banking.csv
------FormBoundary--

### Invalid Domain Error
POST http://localhost:5000/upload
Content-Type: multipart/form-data; boundary=----FormBoundary

------FormBoundary
Content-Disposition: form-data; name="file"; filename="sample_banking.csv"
Content-Type: text/csv

< ./sample_banking.csv
------FormBoundary
Content-Disposition: form-data; name="domain"

invalid
------FormBoundary--
```

### Using the REST Client

1. Click "Send Request" link above each test
2. Results will appear in the right panel
3. View response status and body

---

## 📊 Expected Results Summary

| Test | Status | Key Values |
|------|--------|-----------|
| Health Check | 200 | message: "Backend Running" |
| Banking | 200 | total_records: 20, valid_records: 19, score: 95% |
| Healthcare | 200 | total_records: 20, valid_records: 19, score: 95% |
| E-commerce | 200 | total_records: 20, valid_records: 18, score: 90% |
| Missing Domain | 400 | error: "No domain specified" |
| Invalid Domain | 200 | errors: ["Unknown domain..."] |
| No File | 400 | error: "No file provided" |

---

## 🧪 Creating Custom Test Files

### Banking Test File

Create `test_banking.csv`:
```csv
age,income,credit_score
30,60000,750
```

### Healthcare Test File

Create `test_healthcare.csv`:
```csv
age,blood_group
35,O+
```

### E-commerce Test File

Create `test_ecommerce.csv`:
```csv
price,stock
49.99,100
```

### Test Upload

```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@test_banking.csv" \
  -F "domain=banking"
```

---

## 🔍 Validation Checklist

- [ ] Health check returns 200 with "Backend Running" message
- [ ] Banking CSV validates correctly (95% score with 1 invalid age)
- [ ] Healthcare CSV validates correctly (95% score with 1 invalid age)
- [ ] E-commerce CSV validates correctly (90% score with 2 price/stock errors)
- [ ] Missing domain parameter returns 400 error
- [ ] Invalid domain parameter returns 200 with error in response
- [ ] Missing file returns 400 error
- [ ] Invalid file type returns 400 error
- [ ] Upload folder is created and files are saved
- [ ] Error messages include row numbers
- [ ] Score percentage calculation is correct

---

## 📝 Notes

- All tested endpoints should work without authentication in development mode
- Files are saved with timestamps to prevent conflicts
- Ensure sample CSV files are in the backend directory
- Check that uploads directory has write permissions
- Use correct domain names (case-insensitive)

---

**Testing Version:** 1.0.0  
**Last Updated:** 2024
