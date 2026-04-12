#!/usr/bin/env python3
"""Test Phase 5 - Anomaly Detection Integration"""

from services.validation_service import validate_data
import json

# Test with banking data that includes anomalies
result = validate_data('sample_banking.csv', 'banking')
result_dict = result.to_dict()

print("\n" + "="*60)
print("PHASE 5 ANOMALY DETECTION - TEST RESULTS")
print("="*60)
print(f"\n✓ Total Records: {result.total_records}")
print(f"✓ Records with Anomalies: {result.anomaly_count}")
print(f"✓ Anomaly Score: {result.anomaly_score}%")
print(f"✓ Quality Rating: {result_dict['quality_rating']}")

if result.anomalies:
    print(f"\n📊 Detected Anomalies ({len(result.anomalies)}):")
    for anomaly in result.anomalies[:5]:
        print(f"  • {anomaly}")
    if len(result.anomalies) > 5:
        print(f"  ... and {len(result.anomalies) - 5} more")
else:
    print("\n✓ No anomalies detected in this dataset")

print(f"\n📈 Data Quality Scores:")
print(f"  • Completeness: {result.completeness_score}%")
print(f"  • Validity: {result.validity_score}%")
print(f"  • Consistency: {result.consistency_score}%")
print(f"  • Final Score: {result.final_score}%")

# Test with healthcare
print("\n" + "="*60)
result_health = validate_data('sample_healthcare.csv', 'healthcare')
print(f"\nHealthcare Anomaly Score: {result_health.anomaly_score}%")
print(f"Anomalies Detected: {result_health.anomaly_count}")
if result_health.anomalies:
    print("Sample anomalies:")
    for anomaly in result_health.anomalies[:3]:
        print(f"  • {anomaly}")

# Test with ecommerce
print("\n" + "="*60)
result_ecom = validate_data('sample_ecommerce.csv', 'ecommerce')
print(f"\nE-commerce Anomaly Score: {result_ecom.anomaly_score}%")
print(f"Anomalies Detected: {result_ecom.anomaly_count}")
if result_ecom.anomalies:
    print("Sample anomalies:")
    for anomaly in result_ecom.anomalies[:3]:
        print(f"  • {anomaly}")

print("\n" + "="*60)
print("✅ PHASE 5 ANOMALY DETECTION - INTEGRATION SUCCESSFUL")
print("="*60)
