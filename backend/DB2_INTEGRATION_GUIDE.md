# DB2 INTEGRATION GUIDE - PHASE 9

**Status**: ✅ Production Ready  
**Version**: 1.0  
**Date**: April 13, 2026

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Installation & Setup](#installation--setup)
4. [Configuration](#configuration)
5. [Core Components](#core-components)
6. [Usage Patterns](#usage-patterns)
7. [Query Examples](#query-examples)
8. [Performance Optimization](#performance-optimization)
9. [Monitoring & Troubleshooting](#monitoring--troubleshooting)
10. [Integration with Existing System](#integration-with-existing-system)

---

## Overview

**Purpose**: Persistent storage of validation results in IBM DB2 database for:
- Historical audit trail
- Regulatory compliance reporting
- Real-time analytics and dashboards
- ML model training data
- Business intelligence queries

**Key Capabilities**:
- ✅ Store validation results with full traceability
- ✅ Batch processing with transaction support
- ✅ Historical analysis and trend detection
- ✅ Error tracking and root cause analysis
- ✅ Anomaly pattern detection
- ✅ Quality metrics calculation
- ✅ Compliance reporting
- ✅ Dashboard data aggregation

**Supported DB2 Variants**:
- IBM DB2 for z/OS (mainframe)
- IBM DB2 for Linux, Unix, Windows (LUW)
- IBM Db2 on Cloud
- IBM Db2 Warehouse

---

## Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│         ENTERPRISE VALIDATION SYSTEM (Python)              │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Validation Orchestrator (orchestrator.py)          │   │
│  │  - Process files                                    │   │
│  │  - Run validations                                  │   │
│  │  - Trigger COBOL                                    │   │
│  └────────────────┬────────────────────────────────────┘   │
│                   │                                         │
│                   ▼                                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  DB2 Service (db2_service.py)                       │   │
│  │  - Connection pooling                              │   │
│  │  - CRUD operations                                 │   │
│  │  - Batch insert/update                             │   │
│  │  - Query operations                                │   │
│  │  - Transaction management                          │   │
│  └────────────────┬────────────────────────────────────┘   │
│                   │                                         │
└───────────────────┼─────────────────────────────────────────┘
                    │
                    ▼
        ┌───────────────────────────┐
        │   IBM DB2 DATABASE        │
        │                           │
        │ ┌─────────────────────┐   │
        │ │ VALIDATION_RESULTS  │   │
        │ │ VALIDATION_RECORDS  │   │
        │ │ VALIDATION_ANOMALIES│   │
        │ │ VALIDATION_ERRORS   │   │
        │ └─────────────────────┘   │
        │                           │
        │ With Indexes & PKs        │
        └───────────────────────────┘
```

### Data Flow

```
CSV File → Validator → Result Object → DB2 Repository → Database
                         │
                         ├─ Validation Result
                         ├─ Individual Records
                         ├─ Anomalies
                         └─ Errors
```

### Table Relationships

```
VALIDATION_RESULTS (Parent)
        │
        ├─ VALIDATION_RECORDS (1:N)
        │  └─ VALIDATION_ANOMALIES (1:N)
        │
        ├─ VALIDATION_ANOMALIES (1:N)
        │
        └─ VALIDATION_ERRORS (1:N)
```

---

## Installation & Setup

### Prerequisites

```
Python 3.8+
IBM DB2 (any variant)
Python DB2 Driver: ibm_db
```

### Step 1: Install Python DB2 Driver

```bash
# For DB2 on Linux/Windows
pip install ibm-db

# For DB2 on z/OS (mainframe)
# Connection string uses DSNAME parameter
```

### Step 2: Update requirements.txt

```
ibm-db>=2.1.1
```

### Step 3: Create Database and Tables

**For DB2 z/OS (CICS):**

```sql
-- Run in DB2 Interactive Shell (SPUFI)

-- Create database
CREATE DATABASE VALIDATION;

-- Create tables (copy from db2_service.py Db2Schema class)
CONNECT TO VALIDATION;

CREATE TABLE VALIDATION_RESULTS (
    VALIDATION_ID       BIGINT NOT NULL GENERATED ALWAYS AS IDENTITY,
    VALIDATION_DATE     DATE NOT NULL,
    VALIDATION_TIME     TIME NOT NULL,
    DOMAIN              VARCHAR(20) NOT NULL,
    FILENAME            VARCHAR(255) NOT NULL,
    TOTAL_RECORDS       INTEGER NOT NULL,
    VALID_RECORDS       INTEGER NOT NULL,
    INVALID_RECORDS     INTEGER NOT NULL,
    COMPLETE_RECORDS    INTEGER NOT NULL,
    CONSISTENT_RECORDS  INTEGER NOT NULL,
    ANOMALY_COUNT       INTEGER NOT NULL,
    COMPLETENESS_SCORE  DECIMAL(5,2) NOT NULL,
    VALIDITY_SCORE      DECIMAL(5,2) NOT NULL,
    CONSISTENCY_SCORE   DECIMAL(5,2) NOT NULL,
    FINAL_SCORE         DECIMAL(5,2) NOT NULL,
    ANOMALY_SCORE       DECIMAL(5,2) NOT NULL,
    QUALITY_RATING      VARCHAR(20) NOT NULL,
    STATUS              VARCHAR(20) NOT NULL,
    PROCESSING_TIME_MS  INTEGER,
    COBOL_PROCESSED     CHAR(1) DEFAULT 'N',
    MAINFRAME_STATUS    VARCHAR(20),
    CREATED_BY          VARCHAR(50) DEFAULT USER,
    CREATED_TS          TIMESTAMP DEFAULT CURRENT TIMESTAMP,
    UPDATED_TS          TIMESTAMP,
    PRIMARY KEY (VALIDATION_ID)
);

-- Create indexes for performance
CREATE INDEX IDX_VALIDATION_DOMAIN 
    ON VALIDATION_RESULTS (DOMAIN, VALIDATION_DATE);
CREATE INDEX IDX_VALIDATION_STATUS 
    ON VALIDATION_RESULTS (STATUS, FINAL_SCORE);

-- Repeat for VALIDATION_RECORDS, VALIDATION_ANOMALIES, VALIDATION_ERRORS
```

**For DB2 LUW:**

```bash
# Using db2 CLI
db2 create database VALIDATION
db2 connect to VALIDATION
db2 -f create_tables.sql  # Run DDL from Db2Schema
```

---

## Configuration

### Environment Variables

```bash
# Connection Settings
DB2_HOST=localhost           # Host name or IP
DB2_PORT=50000              # Default DB2 port
DB2_DATABASE=VALIDATION     # Database name
DB2_USER=db2admin           # User ID
DB2_PASSWORD=secure_pwd     # Password

# Connection Pool
DB2_CONNECTION_TIMEOUT=30   # Seconds
DB2_MAX_CONNECTIONS=10      # Pool size

# Mainframe (z/OS) Settings
DB2_DSNAME_VALIDATION=VALIDATION.DB
DB2_DSNAME_AUDIT=AUDIT.DB

# Batch Processing
DB2_BATCH_SIZE=1000         # Records per batch
DB2_COMMIT_INTERVAL=100     # Commit frequency
```

### .env File Example

```
# backend/.env

# DB2 Connection
DB2_HOST=dbserver.company.com
DB2_PORT=50000
DB2_DATABASE=VALIDATION
DB2_USER=validation_user
DB2_PASSWORD=${DB2_PASSWORD_SECURE}

# Connection Pool
DB2_CONNECTION_TIMEOUT=30
DB2_MAX_CONNECTIONS=20

# Batch
DB2_BATCH_SIZE=1000
DB2_COMMIT_INTERVAL=100

# For mainframe
DB2_DSNAME_VALIDATION=validation.db.z.os
DB2_DSNAME_AUDIT=audit.db.z.os
```

### Python Configuration in Code

```python
from services.db2_service import Db2Config

# Auto-loads from environment
print(f"Host: {Db2Config.DB2_HOST}")
print(f"Port: {Db2Config.DB2_PORT}")
print(f"Max Connections: {Db2Config.MAX_CONNECTIONS}")
```

---

## Core Components

### 1. Connection Pool (Db2ConnectionPool)

**Purpose**: Manage database connections efficiently

**Features**:
- Connection reuse
- Automatic reconnection
- Health checks
- Thread-safe pooling

**Usage**:

```python
from services.db2_service import Db2ConnectionPool

pool = Db2ConnectionPool(max_connections=10)
conn = pool.get_connection()

# Use connection...

pool.return_connection(conn)
pool.close_all()
```

### 2. Repository (Db2Repository)

**Purpose**: Data access layer with CRUD operations

**Key Methods**:

```python
from services.db2_service import Db2Repository

repo = Db2Repository()

# CREATE
validation_id = repo.store_validation_result(result_dict, filename)
repo.store_validation_records(validation_id, records_list)
repo.store_anomalies(validation_id, anomalies_list)
repo.store_errors(validation_id, errors_list)

# READ
result = repo.get_validation_result(validation_id)
results = repo.get_validation_results_by_domain('banking', limit=100)
stats = repo.get_quality_statistics('banking', days=30)

# UPDATE
repo.update_validation_status(validation_id, 'ARCHIVED')

# UTILITY
fields = repo.get_high_error_fields('banking', limit=10)
anomalies = repo.get_anomaly_trends('banking', days=30)

repo.close()
```

### 3. Schema (Db2Schema)

**Purpose**: DDL for table creation

**Includes**:
- VALIDATION_RESULTS (main table)
- VALIDATION_RECORDS (child records)
- VALIDATION_ANOMALIES (anomaly tracking)
- VALIDATION_ERRORS (error log)

---

## Usage Patterns

### Pattern 1: Simple Store and Retrieve

```python
from services.enterprise_validation import validate_data_comprehensive
from services.db2_service import Db2Repository

# Validate
result = validate_data_comprehensive('data.csv', 'banking')

# Store to DB2
repo = Db2Repository()
val_id = repo.store_validation_result(
    result.to_dict(),
    'data.csv'
)

# Retrieve
stored_result = repo.get_validation_result(val_id)
print(f"Score: {stored_result['final_score']}%")

repo.close()
```

### Pattern 2: Batch Processing

```python
from services.db2_service import store_validation_to_db2

# Process multiple files
for csv_file in csv_files:
    result = validate_data_comprehensive(csv_file, domain)
    
    val_id = store_validation_to_db2(
        validation_result=result.to_dict(),
        filename=csv_file,
        records=result.records,
        enable_batch=True
    )
    
    print(f"Stored: {val_id}")
```

### Pattern 3: Historical Analysis

```python
from services.db2_service import Db2Repository

repo = Db2Repository()

# Get last 30 days
results = repo.get_validation_results_by_domain(
    'banking',
    start_date='2026-03-14',
    end_date='2026-04-13',
    limit=100
)

# Calculate trends
scores = [r['final_score'] for r in results]
avg = sum(scores) / len(scores)
print(f"Average Score: {avg:.1f}%")

repo.close()
```

### Pattern 4: Error Analysis

```python
from services.db2_service import Db2Repository

repo = Db2Repository()

# Find problematic fields
error_fields = repo.get_high_error_fields('banking', limit=5)

for field, count in error_fields:
    print(f"{field}: {count} errors")

repo.close()
```

### Pattern 5: Anomaly Trends

```python
from services.db2_service import Db2Repository

repo = Db2Repository()

# Get anomaly patterns
anomalies = repo.get_anomaly_trends('banking', days=30)

for anomaly, count in sorted(anomalies.items(), key=lambda x: x[1], reverse=True):
    print(f"{anomaly}: {count} occurrences")

repo.close()
```

---

## Query Examples

### Query 1: Top 10 Lowest Scoring Validations

```sql
SELECT VALIDATION_ID, DOMAIN, FILENAME, FINAL_SCORE, VALIDATION_DATE
FROM VALIDATION_RESULTS
WHERE FINAL_SCORE < 80
ORDER BY FINAL_SCORE ASC
LIMIT 10;
```

### Query 2: Daily Average Score by Domain

```sql
SELECT 
    VALIDATION_DATE,
    DOMAIN,
    AVG(FINAL_SCORE) as daily_avg,
    COUNT(*) as count
FROM VALIDATION_RESULTS
WHERE VALIDATION_DATE >= CURRENT DATE - 30 DAYS
GROUP BY VALIDATION_DATE, DOMAIN
ORDER BY VALIDATION_DATE DESC, DOMAIN;
```

### Query 3: Records with Most Errors

```sql
SELECT 
    r.VALIDATION_ID,
    r.RECORD_NUMBER,
    COUNT(e.ERROR_ID) as error_count,
    COUNT(a.ANOMALY_ID) as anomaly_count
FROM VALIDATION_RECORDS r
LEFT JOIN VALIDATION_ERRORS e ON r.RECORD_ID = e.RECORD_ID
LEFT JOIN VALIDATION_ANOMALIES a ON r.RECORD_ID = a.RECORD_ID
GROUP BY r.VALIDATION_ID, r.RECORD_NUMBER
ORDER BY error_count DESC
LIMIT 20;
```

### Query 4: Compliance Status

```sql
SELECT 
    DOMAIN,
    COUNT(*) as total,
    SUM(CASE WHEN STATUS = 'APPROVED' THEN 1 ELSE 0 END) as approved,
    ROUND(SUM(CASE WHEN STATUS = 'APPROVED' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as compliance_pct
FROM VALIDATION_RESULTS
WHERE VALIDATION_DATE >= CURRENT DATE - 30 DAYS
GROUP BY DOMAIN;
```

### Query 5: Validation Trend

```sql
SELECT 
    DOMAIN,
    VALIDATION_DATE,
    AVG(FINAL_SCORE) as avg_score,
    AVG(PROCESSING_TIME_MS) as avg_time_ms,
    COUNT(*) as count
FROM VALIDATION_RESULTS
WHERE VALIDATION_DATE >= CURRENT DATE - 60 DAYS
GROUP BY DOMAIN, VALIDATION_DATE
ORDER BY DOMAIN, VALIDATION_DATE;
```

---

## Performance Optimization

### Indexing Strategy

```sql
-- Query Speed Indexes
CREATE INDEX IDX_VALIDATION_DOMAIN 
    ON VALIDATION_RESULTS (DOMAIN, VALIDATION_DATE DESC);

CREATE INDEX IDX_VALIDATION_STATUS 
    ON VALIDATION_RESULTS (STATUS, FINAL_SCORE DESC);

CREATE INDEX IDX_RECORDS_VALIDATION 
    ON VALIDATION_RECORDS (VALIDATION_ID);

CREATE INDEX IDX_ANOMALIES_SEVERITY 
    ON VALIDATION_ANOMALIES (SEVERITY DESC);

-- Covering Indexes for common queries
CREATE INDEX IDX_RESULTS_COVER
    ON VALIDATION_RESULTS (DOMAIN, VALIDATION_DATE)
    INCLUDE (FINAL_SCORE, STATUS);
```

### Batch Insert Optimization

```python
# Use batch processing
repo.store_validation_records(
    validation_id,
    records,  # Pass all at once
    batch_size=1000  # Insert in chunks
)

# Commit strategy
# - Small batches: Commit every 100 records
# - Large batches: Commit every 1000 records
```

### Query Performance Tips

```python
# GOOD: Single query with joins
results = repo.get_validation_results_by_domain('banking', limit=50)

# AVOID: N+1 queries in loop
for result in results:
    details = repo.get_validation_details(result['id'])  # Avoid!

# GOOD: Aggregate in database
stats = repo.get_quality_statistics('banking')

# AVOID: Aggregate in Python after fetching all rows
```

---

## Monitoring & Troubleshooting

### Enable Debug Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('db2_service')
logger.setLevel(logging.DEBUG)
```

### Common Issues

**Issue 1: Connection Refused**

```
Error: "Connection refused at xx.xx.xx.xx:50000"

Solution:
- Check DB2 server is running
- Verify host and port in config
- Check firewall rules
```

**Issue 2: Authentication Failed**

```
Error: "Authentication failed for user db2admin"

Solution:
- Verify DB2_USER and DB2_PASSWORD
- Check user permissions in DB2
- Use sqlplus or db2 CLI to test manually
```

**Issue 3: Table Not Found**

```
Error: "Table VALIDATION_RESULTS does not exist"

Solution:
- Run schema DDL from Db2Schema class
- Verify database name (VALIDATION)
- Check user has schema creation privileges
```

**Issue 4: Connection Pool Exhausted**

```
Error: "Connection pool exhausted"

Solution:
- Increase DB2_MAX_CONNECTIONS
- Check for connection leaks (ensure close() is called)
- Reduce concurrent operations
- Monitor active connections: SELECT * FROM SYSCAT.CONNECTIONS
```

### Health Check

```python
from services.db2_service import Db2Repository

repo = Db2Repository()

# Test connection
try:
    result = repo.get_validation_result(1000001)
    print("✓ DB2 connection healthy")
except Exception as e:
    print(f"✗ DB2 connection failed: {e}")
finally:
    repo.close()
```

---

## Integration with Existing System

### Integration with Orchestrator

**File**: `backend/orchestrator.py`

```python
from services.db2_service import store_validation_to_db2
import time

def validate_with_complete_workflow(csv_file: str, domain: str):
    """
    Enhanced workflow with DB2 storage.
    """
    
    # ... existing validation steps ...
    
    # Step 9: Store to DB2
    print("\n[Step 9] Storing to DB2...")
    start_time = time.time()
    
    validation_id = store_validation_to_db2(
        validation_result=result.to_dict(),
        filename=csv_file,
        records=result.records,
        enable_batch=True
    )
    
    if validation_id:
        elapsed = (time.time() - start_time) * 1000
        print(f"✓ Stored to DB2 (ID: {validation_id}) in {elapsed:.0f}ms")
    else:
        print("✗ DB2 storage failed")
    
    # ... rest of workflow ...
```

### Integration with Flask API

**File**: `backend/app.py`

```python
from services.db2_service import (
    Db2Repository,
    get_validation_dashboard_data,
    retrieve_validation_history
)

@app.route('/api/validations/<int:validation_id>', methods=['GET'])
def get_validation(validation_id):
    """Get validation result from DB2."""
    repo = Db2Repository()
    result = repo.get_validation_result(validation_id)
    repo.close()
    return jsonify(result)

@app.route('/api/history/<domain>', methods=['GET'])
def get_history(domain):
    """Get validation history."""
    limit = request.args.get('limit', 100, type=int)
    results = retrieve_validation_history(domain, limit=limit)
    return jsonify(results)

@app.route('/api/dashboard/<domain>', methods=['GET'])
def get_dashboard(domain):
    """Get dashboard data."""
    dashboard = get_validation_dashboard_data(domain)
    return jsonify(dashboard)
```

### Running Examples

```bash
# Run all DB2 examples
python backend/db2_examples.py

# Run specific example
python backend/db2_examples.py 1  # Basic storage
python backend/db2_examples.py 2  # Batch processing
python backend/db2_examples.py 7  # Dashboard data
```

---

## Summary

**DB2 Integration Phase (Phase 9) Delivers**:

✅ Complete DB2 service layer (700+ lines)  
✅ Connection pooling and pool management  
✅ CRUD operations for all table types  
✅ Batch insert/update functionality  
✅ Comprehensive query operations  
✅ Error handling and logging  
✅ 8 complete working examples  
✅ Performance optimization patterns  
✅ Compliance reporting capabilities  
✅ Dashboard data aggregation  
✅ Full documentation and integration guides

**Status**: Production Ready

**Next Phase**: Phase 10 - Message Queue Integration (RabbitMQ/IBM MQ)

