#!/usr/bin/env python3
"""Trace why complete_records is not incrementing"""

from services.validation_service import validate_data
import csv

# Add some instrumentation
result = validate_data('sample_banking.csv', 'banking')

# Print raw attributes
print('Raw validation check:')
print('  total_records from loop:', result.total_records)
print('  complete_records:', result.complete_records)
print('  valid_records:', result.valid_records)

# Try calling individual record
with open('sample_banking.csv') as f:
    reader = csv.DictReader(f)
    records = list(reader)
    
from services.validation_service import is_record_complete, validate_banking_record
rec = records[0]
print('\nTesting single record:', rec)
print('is_record_complete=', is_record_complete(rec, 'banking'))
is_valid, errs = validate_banking_record(rec)
print('validate_banking_record=', is_valid)
