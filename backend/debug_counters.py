#!/usr/bin/env python3
"""Debug Phase 5 - Track counter values"""

from services.validation_service import validate_data

# Test with banking data
result = validate_data('sample_banking.csv', 'banking')

print("\n" + "="*60)
print("DETAILED COUNTER TRACKING")
print("="*60)
print(f"\nCounting Records:")
print(f"  total_records: {result.total_records}")
print(f"  valid_records: {result.valid_records}")
print(f"  invalid_records: {result.invalid_records}")
print(f"  complete_records: {result.complete_records}")
print(f"  consistent_records: {result.consistent_records}")
print(f"  anomaly_count: {result.anomaly_count}")

print(f"\nScores Calculated:")
print(f"  completeness_score: {result.completeness_score}")
print(f"  validity_score: {result.validity_score}")
print(f"  consistency_score: {result.consistency_score}")
print(f"  final_score: {result.final_score}")
print(f"  anomaly_score: {result.anomaly_score}")

print(f"\nScore Calculations (if manual):")
if result.total_records > 0:
    print(f"  complete/total = {result.complete_records}/{result.total_records} = {(result.complete_records / result.total_records * 100):.1f}%")
    print(f"  valid/total = {result.valid_records}/{result.total_records} = {(result.valid_records / result.total_records * 100):.1f}%")
    print(f"  consistent/total = {result.consistent_records}/{result.total_records} = {(result.consistent_records / result.total_records * 100):.1f}%")

print(f"\nErrors Found: {len(result.errors)}")
for error in result.errors[:3]:
    print(f"  • {error}")
if len(result.errors) > 3:
    print(f"  ... and {len(result.errors) - 3} more")
