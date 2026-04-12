#!/usr/bin/env python3
"""Direct test with captured output"""

import sys
from services.validation_service import validate_data

print("Starting validation...")
sys.stdout.flush()

result = validate_data('sample_banking.csv', 'banking')

print("\nValidation complete.")
print("  total_records:", result.total_records)
print("  complete_records:", result.complete_records)
print("  valid_records:", result.valid_records)
