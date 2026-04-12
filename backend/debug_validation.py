#!/usr/bin/env python3
"""Debug Phase 5 - Check validation functions"""

from services.validation_service import is_record_complete, is_record_consistent, validate_banking_record
from services.anomaly_detection import detect_anomalies_banking
import csv

# Read sample data
with open('sample_banking.csv', 'r') as f:
    reader = csv.DictReader(f)
    records = list(reader)

if not records:
    print("No records found!")
    exit(1)

record = records[0]
print(f"Testing record: {record}\n")

# Test is_record_complete
print("1. Testing is_record_complete():")
result = is_record_complete(record, 'banking')
print(f"   Result: {result}")
print(f"   Expected: True (all fields present)")

# Test is_record_consistent
print("\n2. Testing is_record_consistent():")
result = is_record_consistent(record, 'banking')
print(f"   Result: {result}")
print(f"   Expected: True (values consistent)")

# Test validate_banking_record
print("\n3. Testing validate_banking_record():")
is_valid, errors = validate_banking_record(record)
print(f"   Valid: {is_valid}")
print(f"   Errors: {errors}")
print(f"   Expected: Valid=True, No errors")

# Test anomaly detection
print("\n4. Testing detect_anomalies_banking():")
anomalies = detect_anomalies_banking(record)
print(f"   Anomalies: {anomalies}")
print(f"   Expected: [] (no anomalies for normal data)")

print("\n" + "="*60)
print("Debug complete - check each function's result above")
