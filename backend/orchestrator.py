"""
Orchestrator for Complete Validation Workflow - WITH DB2 INTEGRATION (Phase 9)

Coordinates all validation phases:
1. Input validation and parsing
2. Domain-specific validation
3. Quality score calculation
4. Anomaly detection
5. COBOL batch processing
6. Mainframe integration
7. Message queue formation
8. DB2 persistence (Phase 9) ← NEW
9. Report generation
10. Result aggregation

This module ties together all validation services into a seamless workflow.
"""

import json
import os
import sys
import logging
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import csv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import validation services
try:
    from services.enterprise_validation import (
        validate_data_comprehensive,
        RecordValidation,
        ValidationResult
    )
    ENTERPRISE_VALIDATION_AVAILABLE = True
except ImportError:
    ENTERPRISE_VALIDATION_AVAILABLE = False
    logger.warning("Enterprise validation service not available")

# Import DB2 service (Phase 9)
try:
    from services.db2_service import (
        store_validation_to_db2,
        Db2Repository,
        get_validation_dashboard_data,
        retrieve_validation_history
    )
    DB2_AVAILABLE = True
except ImportError:
    DB2_AVAILABLE = False
    logger.warning("DB2 service not available (Phase 9)")

# Import mainframe service
try:
    from services.mainframe_service import (
        MainframeConfig,
        process_validation_with_mainframe
    )
    MAINFRAME_AVAILABLE = True
except ImportError:
    MAINFRAME_AVAILABLE = False
    logger.warning("Mainframe service not available")


# ==================== PHASE 9: DB2 INTEGRATION ====================

class Db2OrchestrationMixin:
    """
    Mixin for adding DB2 persistence to validation workflow.
    
    Handles storage of validation results, records, anomalies, and errors
    to IBM DB2 database for historical tracking and analytics.
    """
    
    @staticmethod
    def _store_to_db2(validation_result: ValidationResult,
                     csv_file: str,
                     enable_batch: bool = True) -> Optional[int]:
        """
        Store validation result to DB2.
        
        Args:
            validation_result: Validation result object
            csv_file: Source CSV file path
            enable_batch: Use batch insert for records
            
        Returns:
            Validation ID if successful, None otherwise
        """
        if not DB2_AVAILABLE:
            logger.warning("DB2 service not available - skipping persistence")
            return None
        
        try:
            logger.info("Storing validation result to DB2...")
            
            validation_id = store_validation_to_db2(
                validation_result=validation_result.to_dict(),
                filename=os.path.basename(csv_file),
                records=validation_result.records,
                enable_batch=enable_batch
            )
            
            if validation_id:
                logger.info(f"✓ Stored to DB2 (Validation ID: {validation_id})")
                return validation_id
            else:
                logger.error("✗ DB2 storage failed")
                return None
                
        except Exception as e:
            logger.error(f"Error storing to DB2: {str(e)}")
            return None


# ==================== MAIN ORCHESTRATION ====================

class ComprehensiveValidator(Db2OrchestrationMixin):
    """
    Complete validation orchestrator with all phases.
    
    Implements 10-phase workflow:
    1. Input validation
    2. CSV parsing
    3. Domain validation
    4. Quality scoring
    5. Anomaly detection
    6. COBOL conversion
    7. COBOL execution
    8. Message queueing
    9. Mainframe integration
    10. DB2 persistence (Phase 9)
    """
    
    def __init__(self, enable_db2: bool = True, enable_mainframe: bool = True):
        """Initialize validator with feature flags."""
        self.enable_db2 = enable_db2 and DB2_AVAILABLE
        self.enable_mainframe = enable_mainframe and MAINFRAME_AVAILABLE
        logger.info(f"Validator initialized (DB2: {self.enable_db2}, Mainframe: {self.enable_mainframe})")
    
    def validate_with_complete_workflow(self, csv_file: str, domain: str) -> Optional[Dict]:
        """
        Execute complete validation workflow with DB2 integration.
        
        10-Step Process:
        1. Input validation
        2. CSV parsing  
        3. Domain validation
        4. Quality scoring
        5. Anomaly detection
        6. COBOL conversion
        7. COBOL execution
        8. Message queueing
        9. Mainframe integration
        10. DB2 persistence & Result aggregation
        
        Args:
            csv_file: Path to CSV file
            domain: Validation domain (banking, healthcare, ecommerce)
            
        Returns:
            Complete validation result dictionary
        """
        
        start_time = time.time()
        
        logger.info("\n" + "="*70)
        logger.info("STARTING COMPLETE VALIDATION WORKFLOW WITH DB2 INTEGRATION")
        logger.info("="*70)
        
        try:
            # ===== PHASE 1: INPUT VALIDATION =====
            logger.info("\n[Step 1/10] Input Validation...")
            
            if not os.path.exists(csv_file):
                raise FileNotFoundError(f"CSV file not found: {csv_file}")
            
            if domain.lower() not in ['banking', 'healthcare', 'ecommerce']:
                raise ValueError(f"Invalid domain: {domain}")
            
            logger.info(f"✓ Input valid: {csv_file} ({domain})")
            
            # ===== PHASES 2-5: VALIDATION EXECUTION =====
            logger.info("\n[Step 2-5/10] Running validation phases...")
            
            if not ENTERPRISE_VALIDATION_AVAILABLE:
                raise ImportError("Validation service not available")
            
            result = validate_data_comprehensive(csv_file, domain)
            
            logger.info(f"✓ Validation complete:")
            logger.info(f"  - Records: {result.total_records}")
            logger.info(f"  - Valid: {result.valid_records}")
            logger.info(f"  - Score: {result.final_score}%")
            logger.info(f"  - Status: {result.status}")
            
            # ===== PHASE 6-8: COBOL & MESSAGE HANDLING =====
            logger.info("\n[Step 6-8/10] COBOL processing & message queue...")
            
            if self.enable_mainframe:
                logger.info("Mainframe integration enabled")
                # In real deployment, COBOL processing would happen here
                logger.info("⚠ COBOL processing: Simulation mode (no COBOL executable)")
            else:
                logger.info("Mainframe integration disabled")
            
            logger.info("✓ Message queue ready")
            
            # ===== PHASE 9: DB2 PERSISTENCE (NEW) =====
            logger.info("\n[Step 9/10] DB2 Persistence (Phase 9)...")
            
            validation_id = None
            if self.enable_db2:
                validation_id = self._store_to_db2(result, csv_file, enable_batch=True)
            else:
                logger.info("DB2 persistence disabled")
            
            # ===== PHASE 10: RESULT AGGREGATION =====
            logger.info("\n[Step 10/10] Result aggregation...")
            
            elapsed = time.time() - start_time
            
            final_result = {
                'validation_id': validation_id,
                'timestamp': datetime.now().isoformat(),
                'csv_file': csv_file,
                'domain': result.domain,
                'total_records': result.total_records,
                'valid_records': result.valid_records,
                'invalid_records': result.invalid_records,
                'anomaly_count': result.anomaly_count,
                'scores': {
                    'completeness': result.completeness_score,
                    'validity': result.validity_score,
                    'consistency': result.consistency_score,
                    'final': result.final_score
                },
                'status': result.status,
                'quality_rating': result.quality_rating,
                'processing_time_ms': int(elapsed * 1000),
                'db2_stored': validation_id is not None,
                'mainframe_enabled': self.enable_mainframe
            }
            
            logger.info(f"✓ Aggregation complete")
            
            # ===== SUMMARY =====
            logger.info("\n" + "="*70)
            logger.info("VALIDATION WORKFLOW COMPLETE")
            logger.info("="*70)
            logger.info(f"Final Score: {final_result['scores']['final']}%")
            logger.info(f"Status: {final_result['status']}")
            logger.info(f"Processing Time: {final_result['processing_time_ms']}ms")
            if validation_id:
                logger.info(f"DB2 Validation ID: {validation_id}")
            logger.info("="*70 + "\n")
            
            return final_result
            
        except Exception as e:
            logger.error(f"\n✗ Workflow failed: {str(e)}")
            logger.error(f"Processing time: {(time.time() - start_time):.2f}s")
            return None
    
    def process_batch_validation(self, csv_files: List[Tuple[str, str]]) -> Dict[str, Any]:
        """
        Process multiple files with batch statistics.
        
        Args:
            csv_files: List of (csv_file, domain) tuples
            
        Returns:
            Batch results with statistics
        """
        
        logger.info("\n" + "="*70)
        logger.info("STARTING BATCH VALIDATION")
        logger.info("="*70)
        
        batch_results = []
        start_time = time.time()
        
        for i, (csv_file, domain) in enumerate(csv_files, 1):
            logger.info(f"\n[{i}/{len(csv_files)}] {os.path.basename(csv_file)}")
            
            result = self.validate_with_complete_workflow(csv_file, domain)
            
            if result:
                batch_results.append(result)
        
        elapsed = time.time() - start_time
        
        # Calculate batch statistics
        if batch_results:
            avg_score = sum(r['scores']['final'] for r in batch_results) / len(batch_results)
            approved = sum(1 for r in batch_results if r['status'] == 'APPROVED')
        else:
            avg_score = 0
            approved = 0
        
        batch_summary = {
            'total_files': len(csv_files),
            'processed': len(batch_results),
            'avg_score': avg_score,
            'approved': approved,
            'approval_rate': approved / len(batch_results) * 100 if batch_results else 0,
            'total_time_ms': int(elapsed * 1000),
            'results': batch_results
        }
        
        logger.info("\n" + "="*70)
        logger.info("BATCH SUMMARY")
        logger.info("="*70)
        logger.info(f"Total Files: {batch_summary['total_files']}")
        logger.info(f"Processed: {batch_summary['processed']}")
        logger.info(f"Average Score: {batch_summary['avg_score']:.1f}%")
        logger.info(f"Approved: {batch_summary['approved']}")
        logger.info(f"Approval Rate: {batch_summary['approval_rate']:.1f}%")
        logger.info(f"Total Time: {batch_summary['total_time_ms']}ms")
        logger.info("="*70 + "\n")
        
        return batch_summary


# ==================== COMMAND-LINE INTERFACE ====================

def main():
    """Main entry point with CLI support."""
    
    validator = ComprehensiveValidator(enable_db2=True, enable_mainframe=True)
    
    if len(sys.argv) < 2:
        print("Usage: python orchestrator.py <csv_file> <domain>")
        print("       python orchestrator.py batch <csv_file1> <domain1> [<csv_file2> <domain2> ...]")
        print("       python orchestrator.py demo")
        print("\nDomains: banking, healthcare, ecommerce")
        return
    
    mode = sys.argv[1]
    
    if mode == "demo":
        run_demo(validator)
    
    elif mode == "batch":
        # Batch mode: orchestrator.py batch file1.csv domain1 file2.csv domain2
        if len(sys.argv) < 4 or (len(sys.argv) - 2) % 2 != 0:
            print("Error: Batch mode requires pairs of (file, domain)")
            return
        
        csv_files = []
        for i in range(2, len(sys.argv), 2):
            csv_file = sys.argv[i]
            domain = sys.argv[i + 1]
            csv_files.append((csv_file, domain))
        
        batch_result = validator.process_batch_validation(csv_files)
        print("\nBatch processing complete!")
    
    else:
        # Single file mode
        csv_file = mode
        domain = sys.argv[2] if len(sys.argv) > 2 else None
        
        if not domain:
            print("Error: Domain required")
            print("Usage: python orchestrator.py <csv_file> <domain>")
            return
        
        result = validator.validate_with_complete_workflow(csv_file, domain)
        
        if result:
            print("\n" + json.dumps(result, indent=2))


def run_demo(validator: ComprehensiveValidator):
    """Run interactive demo."""
    
    print("\n" + "="*70)
    print("INTERACTIVE DEMO - Validation Orchestrator with DB2 Integration")
    print("="*70 + "\n")
    
    demo_files = [
        ("backend/sample_banking.csv", "banking"),
        ("backend/sample_healthcare.csv", "healthcare"),
        ("backend/sample_ecommerce.csv", "ecommerce"),
    ]
    
    print("Available demo datasets:")
    for i, (file, domain) in enumerate(demo_files, 1):
        exists = "✓" if os.path.exists(file) else "✗"
        print(f"  {i}. {exists} {file} ({domain})")
    
    print("\n0. Run all datasets")
    print("q. Quit")
    
    choice = input("\nSelect option: ").strip()
    
    if choice == "q":
        return
    
    elif choice == "0":
        # Run all
        results = validator.process_batch_validation(demo_files)
        
        print("\n" + "="*70)
        print("Demo Summary")
        print("="*70)
        print(f"Files Processed: {results['processed']}/{results['total_files']}")
        print(f"Average Score: {results['avg_score']:.1f}%")
        print(f"Approval Rate: {results['approval_rate']:.1f}%")
        
        # Show DB2 info
        if DB2_AVAILABLE:
            print("\nDB2 Integration:")
            for r in results.get('results', []):
                if r.get('db2_stored'):
                    print(f"  • {r['domain']}: Validation ID {r['validation_id']}")
    
    elif choice.isdigit() and 1 <= int(choice) <= len(demo_files):
        # Run specific
        idx = int(choice) - 1
        csv_file, domain = demo_files[idx]
        validator.validate_with_complete_workflow(csv_file, domain)
    
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()

