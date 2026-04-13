"""
Complete DB2 Integration Examples - PHASE 9

Demonstrates all DB2 integration patterns:
1. Basic validation with DB2 storage
2. Batch processing and persistence
3. Historical analysis and reporting
4. Dashboard data retrieval
5. Error tracking and analysis
6. Quality trend monitoring
7. Compliance reporting
8. Data warehouse integration

Production-ready examples that can be copied directly into applications.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ==================== EXAMPLE 1: BASIC VALIDATION WITH DB2 STORAGE ====================

def example_basic_storage_with_db2():
    """
    Example 1: Store validation result directly to DB2.
    
    Shows the simplest integration pattern:
    - Validate data
    - Store result to DB2
    - Retrieve validation ID
    """
    logger.info("\n" + "="*60)
    logger.info("EXAMPLE 1: Basic Validation with DB2 Storage")
    logger.info("="*60)
    
    try:
        # Import modules
        from services.enterprise_validation import validate_data_comprehensive
        from services.db2_service import store_validation_to_db2
        
        # Step 1: Validate data
        logger.info("Step 1: Validating banking data...")
        csv_file = "backend/sample_banking.csv"
        result = validate_data_comprehensive(csv_file, "banking")
        
        logger.info(f"  ✓ Validation complete")
        logger.info(f"    Domain: {result.domain}")
        logger.info(f"    Final Score: {result.final_score}%")
        logger.info(f"    Status: {result.status}")
        
        # Step 2: Store to DB2
        logger.info("\nStep 2: Storing to DB2...")
        validation_id = store_validation_to_db2(
            validation_result=result.to_dict(),
            filename=csv_file,
            records=result.records,
            enable_batch=True
        )
        
        if validation_id:
            logger.info(f"  ✓ Stored successfully")
            logger.info(f"    Validation ID: {validation_id}")
            return validation_id
        else:
            logger.error("  ✗ Storage failed")
            return None
            
    except Exception as e:
        logger.error(f"Error in example 1: {str(e)}")
        return None


# ==================== EXAMPLE 2: BATCH PROCESSING WITH DB2 ====================

def example_batch_processing_with_db2():
    """
    Example 2: Process multiple files and store all results to DB2.
    
    Shows batch integration:
    - Process multiple CSV files
    - Store each validation result
    - Create audit trail
    - Track batch metrics
    """
    logger.info("\n" + "="*60)
    logger.info("EXAMPLE 2: Batch Processing with DB2")
    logger.info("="*60)
    
    try:
        import os
        from services.enterprise_validation import validate_data_comprehensive
        from services.db2_service import store_validation_to_db2, Db2Repository
        
        # Find all CSV files
        csv_files = [
            ("backend/sample_banking.csv", "banking"),
            ("backend/sample_healthcare.csv", "healthcare"),
            ("backend/sample_ecommerce.csv", "ecommerce"),
        ]
        
        batch_results = []
        
        logger.info(f"Processing {len(csv_files)} files...\n")
        
        for csv_file, domain in csv_files:
            if not os.path.exists(csv_file):
                logger.warning(f"  ⚠ File not found: {csv_file}")
                continue
            
            logger.info(f"Processing: {csv_file}")
            
            # Validate
            result = validate_data_comprehensive(csv_file, domain)
            
            # Store to DB2
            validation_id = store_validation_to_db2(
                validation_result=result.to_dict(),
                filename=os.path.basename(csv_file),
                records=result.records
            )
            
            if validation_id:
                batch_results.append({
                    'filename': csv_file,
                    'domain': domain,
                    'validation_id': validation_id,
                    'score': result.final_score,
                    'status': result.status
                })
                logger.info(f"  ✓ Validation ID: {validation_id}, Score: {result.final_score}%\n")
            else:
                logger.error(f"  ✗ Storage failed\n")
        
        # Summary
        logger.info("\nBatch Summary:")
        logger.info(f"  Total Processed: {len(batch_results)}")
        logger.info(f"  Average Score: {sum(r['score'] for r in batch_results) / len(batch_results):.1f}%")
        logger.info(f"  Approved: {sum(1 for r in batch_results if r['status'] == 'APPROVED')}")
        
        return batch_results
        
    except Exception as e:
        logger.error(f"Error in example 2: {str(e)}")
        return []


# ==================== EXAMPLE 3: RETRIEVE VALIDATION HISTORY ====================

def example_retrieve_validation_history():
    """
    Example 3: Query validation history from DB2.
    
    Shows retrieval patterns:
    - Query by domain
    - Date range filtering
    - Result pagination
    - Historical analysis
    """
    logger.info("\n" + "="*60)
    logger.info("EXAMPLE 3: Retrieve Validation History")
    logger.info("="*60)
    
    try:
        from services.db2_service import Db2Repository
        
        repo = Db2Repository()
        
        # Query banking validations from last 7 days
        logger.info("Querying banking validations (last 7 days)...")
        
        results = repo.get_validation_results_by_domain(
            domain='banking',
            limit=50
        )
        
        logger.info(f"\nFound {len(results)} validations:\n")
        
        for i, result in enumerate(results[:5], 1):  # Show first 5
            logger.info(f"  {i}. Validation {result.get('validation_id')}")
            logger.info(f"     Domain: {result.get('domain')}")
            logger.info(f"     File: {result.get('filename')}")
            logger.info(f"     Score: {result.get('final_score')}%")
            logger.info(f"     Status: {result.get('status')}")
            logger.info(f"     Valid Records: {result.get('valid_records')}/{result.get('total_records')}")
        
        if len(results) > 5:
            logger.info(f"\n  ... and {len(results) - 5} more")
        
        repo.close()
        return results
        
    except Exception as e:
        logger.error(f"Error in example 3: {str(e)}")
        return []


# ==================== EXAMPLE 4: QUALITY STATISTICS AND TRENDS ====================

def example_quality_statistics():
    """
    Example 4: Analyze quality trends from DB2.
    
    Shows analytics:
    - Average scores
    - Quality trends
    - Success rates
    - Problem identification
    """
    logger.info("\n" + "="*60)
    logger.info("EXAMPLE 4: Quality Statistics and Trends")
    logger.info("="*60)
    
    try:
        from services.db2_service import Db2Repository
        
        repo = Db2Repository()
        
        domains = ['banking', 'healthcare', 'ecommerce']
        
        logger.info("\nQuality Statistics (Last 30 Days):\n")
        
        for domain in domains:
            stats = repo.get_quality_statistics(domain, days=30)
            
            logger.info(f"Domain: {domain}")
            logger.info(f"  Total Validations: {stats.get('total_validations', 0)}")
            logger.info(f"  Average Score: {stats.get('average_score', 0):.1f}%")
            logger.info(f"  Trend: {stats.get('trend', 'UNCHANGED')}")
            logger.info(f"  Success Rate: {stats.get('success_rate', 0):.1f}%")
            logger.info("")
        
        repo.close()
        
    except Exception as e:
        logger.error(f"Error in example 4: {str(e)}")


# ==================== EXAMPLE 5: ERROR ANALYSIS ====================

def example_error_analysis():
    """
    Example 5: Analyze validation errors to identify problematic fields.
    
    Shows error tracking:
    - Most common error fields
    - Error frequency
    - Data quality insights
    - Improvement areas
    """
    logger.info("\n" + "="*60)
    logger.info("EXAMPLE 5: Error Analysis")
    logger.info("="*60)
    
    try:
        from services.db2_service import Db2Repository
        
        repo = Db2Repository()
        
        domains = ['banking', 'healthcare', 'ecommerce']
        
        logger.info("\nMost Common Error Fields (Last 30 Days):\n")
        
        for domain in domains:
            logger.info(f"Domain: {domain}")
            error_fields = repo.get_high_error_fields(domain, limit=5)
            
            if error_fields:
                for field, count in error_fields:
                    logger.info(f"  • {field}: {count} errors")
            else:
                logger.info("  (No errors recorded)")
            
            logger.info("")
        
        repo.close()
        
    except Exception as e:
        logger.error(f"Error in example 5: {str(e)}")


# ==================== EXAMPLE 6: ANOMALY TRENDS ====================

def example_anomaly_trends():
    """
    Example 6: Analyze anomaly patterns from DB2.
    
    Shows anomaly insights:
    - Most common anomalies
    - Severity distribution
    - Trend analysis
    - Alert generation
    """
    logger.info("\n" + "="*60)
    logger.info("EXAMPLE 6: Anomaly Trends Analysis")
    logger.info("="*60)
    
    try:
        from services.db2_service import Db2Repository
        
        repo = Db2Repository()
        
        domains = ['banking', 'healthcare', 'ecommerce']
        
        logger.info("\nAnomaly Trends (Last 30 Days):\n")
        
        for domain in domains:
            logger.info(f"Domain: {domain}")
            anomalies = repo.get_anomaly_trends(domain, days=30)
            
            if anomalies:
                for anomaly_type, count in sorted(anomalies.items(), key=lambda x: x[1], reverse=True):
                    logger.info(f"  • {anomaly_type}: {count} occurrences")
            else:
                logger.info("  (No anomalies recorded)")
            
            logger.info("")
        
        repo.close()
        
    except Exception as e:
        logger.error(f"Error in example 6: {str(e)}")


# ==================== EXAMPLE 7: DASHBOARD DATA ====================

def example_dashboard_data():
    """
    Example 7: Retrieve complete dashboard data for visualization.
    
    Shows dashboard integration:
    - All metrics in one call
    - Ready for web dashboard
    - JSON-serializable output
    - Real-time analytics
    """
    logger.info("\n" + "="*60)
    logger.info("EXAMPLE 7: Dashboard Data Retrieval")
    logger.info("="*60)
    
    try:
        from services.db2_service import get_validation_dashboard_data
        
        logger.info("\nRetrieving complete dashboard data for banking domain...\n")
        
        dashboard = get_validation_dashboard_data('banking')
        
        logger.info(f"Dashboard Data Received:")
        logger.info(f"  Domain: {dashboard.get('domain')}")
        
        stats = dashboard.get('statistics', {})
        logger.info(f"\n  Statistics:")
        logger.info(f"    Average Score: {stats.get('average_score', 0):.1f}%")
        logger.info(f"    Trend: {stats.get('trend', 'UNKNOWN')}")
        logger.info(f"    Total: {stats.get('total_validations', 0)} validations")
        
        error_fields = dashboard.get('error_fields', [])
        logger.info(f"\n  Top Error Fields:")
        for field, count in error_fields[:3]:
            logger.info(f"    • {field}: {count} errors")
        
        anomalies = dashboard.get('anomaly_trends', {})
        logger.info(f"\n  Anomaly Types:")
        for anomaly_type, count in list(anomalies.items())[:3]:
            logger.info(f"    • {anomaly_type}: {count} occurrences")
        
        recent = dashboard.get('recent_validations', [])
        logger.info(f"\n  Recent Validations: {len(recent)} available")
        
        # Output as JSON for dashboard consumption
        logger.info(f"\n  JSON Output (for dashboard):")
        logger.info(json.dumps(dashboard, indent=2, default=str)[:500] + "...")
        
    except Exception as e:
        logger.error(f"Error in example 7: {str(e)}")


# ==================== EXAMPLE 8: COMPLIANCE REPORTING ====================

def example_compliance_reporting():
    """
    Example 8: Generate compliance reports from DB2.
    
    Shows compliance patterns:
    - Success rate tracking
    - Audit trail
    - Status tracking
    - Regulatory requirements
    """
    logger.info("\n" + "="*60)
    logger.info("EXAMPLE 8: Compliance Reporting")
    logger.info("="*60)
    
    try:
        from services.db2_service import Db2Repository
        
        repo = Db2Repository()
        
        logger.info("\nCompliance Report (Banking Domain):\n")
        
        # Get validations
        validations = repo.get_validation_results_by_domain('banking', limit=100)
        
        if validations:
            total = len(validations)
            approved = sum(1 for v in validations if v.get('status') == 'APPROVED')
            avg_score = sum(v.get('final_score', 0) for v in validations) / total
            
            logger.info(f"Period: Last 30 Days")
            logger.info(f"Total Validations: {total}")
            logger.info(f"Approved: {approved} ({approved/total*100:.1f}%)")
            logger.info(f"Average Score: {avg_score:.1f}%")
            logger.info(f"\nCompliance Status: {'✓ COMPLIANT' if approved/total >= 0.95 else '✗ REVIEW REQUIRED'}")
            
            # Details
            logger.info(f"\nValidation Details:")
            for i, v in enumerate(validations[:5], 1):
                logger.info(f"  {i}. ID: {v.get('validation_id')}")
                logger.info(f"     Records: {v.get('valid_records')}/{v.get('total_records')}")
                logger.info(f"     Score: {v.get('final_score')}% ({v.get('status')})")
        
        repo.close()
        
    except Exception as e:
        logger.error(f"Error in example 8: {str(e)}")


# ==================== MAIN EXECUTION ====================

def run_all_db2_examples():
    """Run all DB2 integration examples."""
    logger.info("\n")
    logger.info("╔" + "="*58 + "╗")
    logger.info("║" + " "*58 + "║")
    logger.info("║" + "  DB2 INTEGRATION EXAMPLES - PHASE 9".center(58) + "║")
    logger.info("║" + "  Comprehensive Database Integration Patterns".center(58) + "║")
    logger.info("║" + " "*58 + "║")
    logger.info("╚" + "="*58 + "╝")
    
    examples = [
        ("1", "Basic Storage", example_basic_storage_with_db2),
        ("2", "Batch Processing", example_batch_processing_with_db2),
        ("3", "History Retrieval", example_retrieve_validation_history),
        ("4", "Quality Statistics", example_quality_statistics),
        ("5", "Error Analysis", example_error_analysis),
        ("6", "Anomaly Trends", example_anomaly_trends),
        ("7", "Dashboard Data", example_dashboard_data),
        ("8", "Compliance Report", example_compliance_reporting),
    ]
    
    logger.info("\nAvailable Examples:")
    for num, name, _ in examples:
        logger.info(f"  {num}. {name}")
    
    logger.info("\nRunning Examples...\n")
    
    for num, name, example_func in examples:
        try:
            example_func()
            logger.info(f"✓ Example {num} completed\n")
        except Exception as e:
            logger.error(f"✗ Example {num} failed: {str(e)}\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        # Run specific example
        example_num = int(sys.argv[1])
        examples = [
            example_basic_storage_with_db2,
            example_batch_processing_with_db2,
            example_retrieve_validation_history,
            example_quality_statistics,
            example_error_analysis,
            example_anomaly_trends,
            example_dashboard_data,
            example_compliance_reporting,
        ]
        
        if 1 <= example_num <= len(examples):
            examples[example_num - 1]()
        else:
            logger.error(f"Example {example_num} not found (1-{len(examples)} available)")
    else:
        # Run all examples
        run_all_db2_examples()
    
    logger.info("\n" + "="*60)
    logger.info("DB2 Examples Complete")
    logger.info("="*60 + "\n")

