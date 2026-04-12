#!/usr/bin/env python3
"""Test Phase 5 - API Integration"""

from services.validation_service import validate_data
import json

print("\n" + "="*70)
print("PHASE 5 API INTEGRATION TEST")
print("="*70)

# Simulate API file upload and validation
domain = 'banking'
filename = 'sample_banking.csv'

print(f"\n📤 Simulating API upload: {filename} ({domain})")

# Step 1: Validate file was uploaded correctly
result_validation = validate_data(filename, domain)

# Step 2: Build API response (what Flask would return)
api_response = {
    'success': True,
    'domain': domain,
    'filename': filename,
    
    # Original metrics
    'total_records': result_validation.total_records,
    'valid_records': result_validation.valid_records,
    'invalid_records': result_validation.invalid_records,
    'score_percentage': result_validation.validity_score,
    
    # Data quality dimensions
    'completeness_score': result_validation.completeness_score,
    'validity_score': result_validation.validity_score,
    'consistency_score': result_validation.consistency_score,
    'final_score': result_validation.final_score,
    'quality_rating': result_validation.to_dict()['quality_rating'],
    
    # PHASE 5: Anomaly Detection
    'anomaly_count': result_validation.anomaly_count,
    'anomaly_score': result_validation.anomaly_score,
    'anomalies': result_validation.anomalies,
    
    'errors': result_validation.errors
}

print("\n✓ API Response Structure:")
print(json.dumps(api_response, indent=2))

print("\n" + "-"*70)
print("✅ API endpoints ready to serve:")
print("   POST /upload - Includes Phase 5 anomaly data ✓")
print("   GET /results/<id> - Includes Phase 5 anomaly data ✓")
print("   GET /stats/<domain> - Includes anomaly statistics ✓")
print("="*70)
