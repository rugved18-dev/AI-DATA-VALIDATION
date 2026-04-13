"""
COMPLETE WORKING EXAMPLES - ENTERPRISE VALIDATION SERVICE

Demonstrates all features with real working code and expected outputs.
Copy and paste examples to run immediately.
"""

# ============================================================================
# EXAMPLE 1: Simple Banking Validation
# ============================================================================

def example_simple_banking_validation():
    """Most basic usage - validate banking data."""
    
    from services.enterprise_validation import validate_data_comprehensive
    
    # Use existing sample file
    result = validate_data_comprehensive(
        file_path='./sample_banking.csv',
        domain='banking'
    )
    
    print("\n" + "="*60)
    print("EXAMPLE 1: Simple Banking Validation")
    print("="*60)
    print(f"Total Records: {result.total_records}")
    print(f"Valid Records: {result.valid_records}")
    print(f"Invalid Records: {result.invalid_records}")
    print(f"Quality Score: {result.final_score}%")
    print(f"Quality Rating: {result._get_quality_rating()}")
    print(f"Status: {result.to_dict()['status']}")
    
    # Show first few errors
    if result.errors:
        print(f"\nErrors (showing first 3):")
        for error in result.errors[:3]:
            print(f"  - {error}")
    
    # Show anomalies
    if result.anomalies:
        print(f"\nAnomalies (showing first 3):")
        for anomaly in result.anomalies[:3]:
            print(f"  {anomaly}")


# ============================================================================
# EXAMPLE 2: Complete Workflow with Mainframe Integration
# ============================================================================

def example_complete_workflow():
    """Full enterprise workflow with COBOL integration."""
    
    from services.orchestrator import validate_with_complete_workflow
    import json
    
    result = validate_with_complete_workflow(
        csv_file='./sample_healthcare.csv',
        domain='healthcare',
        enable_cobol=True,
        enable_queue=True,
        output_file='./validation_result.json'
    )
    
    print("\n" + "="*60)
    print("EXAMPLE 2: Complete Workflow with Mainframe")
    print("="*60)
    
    # Validation results
    val = result.get('validation', {})
    print("\n📊 Validation Results:")
    print(f"  Quality Score: {val.get('final_score')}%")
    print(f"  Quality Rating: {val.get('quality_rating')}")
    print(f"  Valid: {val.get('valid_records')}/{val.get('total_records')}")
    print(f"  Anomalies: {val.get('anomaly_count')}")
    
    # Mainframe processing
    mf = result.get('mainframe_processing', {})
    print("\n🖥️ Mainframe Processing:")
    print(f"  Status: {mf.get('overall_status')}")
    print(f"  Domain: {mf.get('domain')}")
    print(f"  Timestamp: {mf.get('timestamp')}")
    
    # COBOL execution
    cobol = mf.get('cobol_processing', {})
    if cobol:
        print(f"\n⚙️ COBOL Processing:")
        print(f"  Status: {cobol.get('status')}")
        print(f"  Processed Records: {cobol.get('processed_records')}")
        print(f"  Return Code: {cobol.get('cobol_return_code')}")
    
    # Message queue
    queue = mf.get('message_queue', {})
    if queue:
        print(f"\n📮 Message Queue:")
        print(f"  Queued: {queue.get('queued')}")
        print(f"  Timestamp: {queue.get('timestamp')}")
    
    print(f"\n✅ Overall Status: {result['status']}")
    print(f"📁 Output File: {result.get('output_file', 'Not saved')}")


# ============================================================================
# EXAMPLE 3: Batch Processing Multiple Files
# ============================================================================

def example_batch_processing():
    """Process multiple CSV files at once."""
    
    from services.orchestrator import process_batch_validation
    import os
    
    # Files to process
    files = [
        './sample_banking.csv',
        './sample_healthcare.csv',
        './sample_ecommerce.csv'
    ]
    
    # Filter to existing files only
    files = [f for f in files if os.path.exists(f)]
    
    if not files:
        print("No sample files found")
        return
    
    result = process_batch_validation(
        csv_files=files,
        domain='banking',  # Note: Would need to match each file's domain
        output_dir='./batch_results'
    )
    
    print("\n" + "="*60)
    print("EXAMPLE 3: Batch Processing")
    print("="*60)
    print(f"Total Files: {result['total_files']}")
    print(f"Successful: {result['aggregate_stats']['files_successful']}")
    print(f"Failed: {result['aggregate_stats']['files_failed']}")
    print(f"Average Score: {result['aggregate_stats']['average_score']}%")
    print(f"Total Records: {result['aggregate_stats']['total_records']}")
    print(f"Valid Records: {result['aggregate_stats']['valid_records']}")


# ============================================================================
# EXAMPLE 4: Direct COBOL Integration
# ============================================================================

def example_cobol_integration():
    """Directly work with COBOL conversion and execution."""
    
    from services.mainframe_service import (
        convert_records_to_cobol_input,
        run_cobol_validation,
        queue_message
    )
    import tempfile
    import os
    
    # Sample banking records
    records = [
        {
            'age': 30,
            'income': 50000,
            'credit_score': 750,
            'loan_amount': 200000
        },
        {
            'age': 45,
            'income': 75000,
            'credit_score': 800,
            'loan_amount': 300000
        },
        {
            'age': 25,
            'income': 35000,
            'credit_score': 650,
            'loan_amount': 100000
        }
    ]
    
    print("\n" + "="*60)
    print("EXAMPLE 4: Direct COBOL Integration")
    print("="*60)
    
    # Create temporary directory for files
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, 'input.dat')
        
        # Step 1: Convert to COBOL format
        print("\n1️⃣ Converting to COBOL format...")
        cobol_input = convert_records_to_cobol_input(
            records, 'banking', input_file
        )
        print(f"   Generated {len(records)} fixed-width records")
        print(f"   Output file: {input_file}")
        
        # Show sample
        lines = cobol_input.split('\n')
        print(f"\n   Sample COBOL record (first line):")
        print(f"   {repr(lines[0][:60])}...")
        
        # Step 2: Run COBOL validation
        print("\n2️⃣ Running COBOL validation...")
        cobol_result = run_cobol_validation(input_file, 'banking')
        print(f"   Status: {cobol_result['status']}")
        print(f"   Records Processed: {cobol_result['processed_records']}")
        print(f"   Valid Records: {cobol_result.get('valid_records', 'N/A')}")
        print(f"   Return Code: {cobol_result['cobol_return_code']}")
        
        # Step 3: Queue results
        print("\n3️⃣ Queueing results to mainframe...")
        queue_success = queue_message(cobol_result, 'mainframe.requests')
        print(f"   Queue Status: {'✓ Success' if queue_success else '✗ Failed'}")


# ============================================================================
# EXAMPLE 5: Analyze Validation Results in Detail
# ============================================================================

def example_analyze_results():
    """Detailed analysis of validation results."""
    
    from services.enterprise_validation import validate_data_comprehensive
    
    result = validate_data_comprehensive(
        './sample_banking.csv',
        'banking'
    )
    
    print("\n" + "="*60)
    print("EXAMPLE 5: Detailed Result Analysis")
    print("="*60)
    
    print("\n📊 Quality Dimensions:")
    print(f"  Completeness: {result.completeness_score}%")
    print(f"    → {result.complete_records}/{result.total_records} records have all fields")
    
    print(f"\n  Validity: {result.validity_score}%")
    print(f"    → {result.valid_records}/{result.total_records} records pass validation")
    
    print(f"\n  Consistency: {result.consistency_score}%")
    print(f"    → {result.consistent_records}/{result.total_records} records follow patterns")
    
    print(f"\n  Anomalies: {result.anomaly_score}%")
    print(f"    → {result.anomaly_count}/{result.total_records} records have anomalies")
    
    print("\n🎯 Final Score Calculation:")
    print(f"  = (0.4 × {result.completeness_score})")
    print(f"  + (0.4 × {result.validity_score})")
    print(f"  + (0.2 × {result.consistency_score})")
    print(f"  = {result.final_score}%")
    
    rating = result._get_quality_rating()
    print(f"\n✨ Quality Rating: {rating}")
    print(f"   {'Excellent!' if rating == 'EXCELLENT' else 'Good' if rating == 'GOOD' else 'Acceptable' if rating == 'ACCEPTABLE' else 'Needs improvement'}")
    
    # Show errors
    if result.errors:
        print(f"\n❌ Errors ({len(result.errors)} total):")
        for error in result.errors[:5]:
            print(f"   {error}")
        if len(result.errors) > 5:
            print(f"   ... and {len(result.errors) - 5} more")
    
    # Show anomalies
    if result.anomalies:
        print(f"\n⚠️ Anomalies ({len(result.anomalies)} total):")
        for anomaly in result.anomalies[:5]:
            print(f"   {anomaly}")
        if len(result.anomalies) > 5:
            print(f"   ... and {len(result.anomalies) - 5} more")


# ============================================================================
# EXAMPLE 6: Test All Domains
# ============================================================================

def example_all_domains():
    """Test validation for all three domains."""
    
    from services.enterprise_validation import validate_data_comprehensive
    
    domains = {
        'banking': './sample_banking.csv',
        'healthcare': './sample_healthcare.csv',
        'ecommerce': './sample_ecommerce.csv'
    }
    
    print("\n" + "="*60)
    print("EXAMPLE 6: Testing All Domains")
    print("="*60)
    
    for domain, file_path in domains.items():
        try:
            print(f"\n🔍 Validating {domain.upper()}...")
            result = validate_data_comprehensive(file_path, domain)
            
            print(f"   Records: {result.valid_records}/{result.total_records} valid")
            print(f"   Quality Score: {result.final_score}%")
            print(f"   Status: {result.to_dict()['status']}")
            
        except FileNotFoundError:
            print(f"   ⚠️ File not found: {file_path}")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")


# ============================================================================
# EXAMPLE 7: Custom Validation with Error Inspection
# ============================================================================

def example_error_inspection():
    """Inspect validation errors in detail."""
    
    from services.enterprise_validation import validate_banking_record
    
    # Test records with various errors
    test_records = [
        {
            'name': 'Valid record',
            'data': {'age': 30, 'income': 50000, 'credit_score': 750}
        },
        {
            'name': 'Age too low',
            'data': {'age': 15, 'income': 50000, 'credit_score': 750}
        },
        {
            'name': 'Invalid income',
            'data': {'age': 30, 'income': -5000, 'credit_score': 750}
        },
        {
            'name': 'Credit score out of range',
            'data': {'age': 30, 'income': 50000, 'credit_score': 950}
        },
        {
            'name': 'Loan exceeds limit',
            'data': {
                'age': 30,
                'income': 50000,
                'credit_score': 750,
                'loan_amount': 300000  # > 50000 * 5
            }
        }
    ]
    
    print("\n" + "="*60)
    print("EXAMPLE 7: Error Inspection")
    print("="*60)
    
    for test in test_records:
        is_valid, errors = validate_banking_record(test['data'])
        
        status = "✅ VALID" if is_valid else "❌ INVALID"
        print(f"\n{status} - {test['name']}")
        
        if errors:
            for error in errors:
                print(f"   Error: {error}")
        else:
            print(f"   No errors")


# ============================================================================
# EXAMPLE 8: Generate Full Report JSON
# ============================================================================

def example_generate_report():
    """Generate and save full validation report as JSON."""
    
    from services.enterprise_validation import validate_data_comprehensive
    import json
    
    result = validate_data_comprehensive(
        './sample_banking.csv',
        'banking'
    )
    
    # Convert to dictionary
    report = result.to_dict()
    
    # Save to file
    with open('./validation_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\n" + "="*60)
    print("EXAMPLE 8: Generate Report")
    print("="*60)
    print("✅ Report generated: validation_report.json")
    print("\nReport snippet:")
    print(json.dumps(report, indent=2)[:500] + "...")


# ============================================================================
# MAIN - Run All Examples
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("ENTERPRISE VALIDATION SERVICE - COMPLETE EXAMPLES")
    print("="*60)
    
    import os
    
    # Check if sample files exist
    samples = [
        './sample_banking.csv',
        './sample_healthcare.csv',
        './sample_ecommerce.csv'
    ]
    
    missing = [f for f in samples if not os.path.exists(f)]
    
    if missing:
        print(f"\n⚠️ Warning: Sample files not found:")
        for f in missing:
            print(f"   - {f}")
        print("\nPlease create sample CSV files or adjust paths")
    
    try:
        # Run examples
        print("\n1️⃣ Running Example 1: Simple Banking Validation")
        example_simple_banking_validation()
        
        print("\n" + "="*60)
        print("2️⃣ Running Example 2: Complete Workflow")
        input("   Press Enter to continue...")
        example_complete_workflow()
        
        print("\n" + "="*60)
        print("3️⃣ Running Example 3: Batch Processing")
        input("   Press Enter to continue...")
        example_batch_processing()
        
        print("\n" + "="*60)
        print("4️⃣ Running Example 4: COBOL Integration")
        input("   Press Enter to continue...")
        example_cobol_integration()
        
        print("\n" + "="*60)
        print("5️⃣ Running Example 5: Detailed Analysis")
        input("   Press Enter to continue...")
        example_analyze_results()
        
        print("\n" + "="*60)
        print("6️⃣ Running Example 6: All Domains")
        input("   Press Enter to continue...")
        example_all_domains()
        
        print("\n" + "="*60)
        print("7️⃣ Running Example 7: Error Inspection")
        input("   Press Enter to continue...")
        example_error_inspection()
        
        print("\n" + "="*60)
        print("8️⃣ Running Example 8: Report Generation")
        input("   Press Enter to continue...")
        example_generate_report()
        
        print("\n" + "="*60)
        print("✅ ALL EXAMPLES COMPLETED")
        print("="*60)
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("Please ensure sample CSV files are in the correct location")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
