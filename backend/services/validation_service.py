"""
Validation Service Module

Handles domain-specific validation logic and data quality dimension calculation.

Supports validation for multiple domains:
- Banking: Financial profiles validation
- Healthcare: Patient health records validation
- E-commerce: Product inventory validation

Calculates three data quality dimensions:
- Completeness: % of records with all required fields
- Validity: % of records passing domain rules
- Consistency: % of records following patterns

PHASE 5: Anomaly Detection - Identifies statistical outliers
"""

import csv
from models.validation_result import ValidationResult
from services.scoring_service import (
    calculate_completeness_score,
    calculate_validity_score,
    calculate_consistency_score,
    calculate_weighted_score
)
from services.anomaly_detection import (
    detect_anomalies_banking,
    detect_anomalies_healthcare,
    detect_anomalies_ecommerce,
    calculate_anomaly_score
)


# ==================== DOMAIN FIELD DEFINITIONS ====================

DOMAIN_FIELDS = {
    'banking': ['age', 'income', 'credit_score'],
    'healthcare': ['age', 'blood_group'],
    'ecommerce': ['price', 'stock']
}


def is_record_complete(record, domain):
    """
    Check if record has all required fields (Completeness Dimension).
    
    Args:
        record (dict): CSV record
        domain (str): Domain type
        
    Returns:
        bool: True if all required fields are present and non-empty
    """
    required_fields = DOMAIN_FIELDS.get(domain.lower(), [])
    for field in required_fields:
        value = record.get(field, '').strip()
        if not value:
            return False
    return True


def is_record_consistent(record, domain):
    """
    Check if record follows data patterns (Consistency Dimension).
    
    Consistency checks for:
    - Data type consistency
    - Reasonable ranges
    - Logical relationships between fields
    
    Args:
        record (dict): CSV record
        domain (str): Domain type
        
    Returns:
        bool: True if record follows established patterns
    """
    try:
        domain = domain.lower()
        
        if domain == 'banking':
            age = int(record.get('age', 0))
            income = float(record.get('income', 0))
            # Consistency: older age might have lower income volatility (example)
            # For now, check if types are convertible
            return True
        
        elif domain == 'healthcare':
            age = int(record.get('age', 0))
            # Consistency: age should be within realistic human range
            return 0 <= age <= 150  # Allows for data outliers but within realm
        
        elif domain == 'ecommerce':
            price = float(record.get('price', 0))
            stock = int(record.get('stock', 0))
            # Consistency: price and stock should be coherent
            # (avoid extreme outliers)
            return 0.01 <= price <= 1000000 and -1 <= stock <= 1000000
        
        return True
    
    except (ValueError, TypeError):
        return False


# ==================== BANKING DOMAIN VALIDATION ====================

def validate_banking_record(record):
    """
    Validate a single banking record.
    
    Expected fields:
    - age: Integer between 18 and 80
    - income: Float/Decimal greater than 0
    - credit_score: Integer between 300 and 850
    
    Future Integration:
    - Connect to DB2 to validate against regulatory compliance rules
    - Integrate with COBOL programs for legacy credit scoring algorithms
    - Call external services for fraud detection
    
    Args:
        record (dict): Dictionary containing banking data
        
    Returns:
        tuple: (is_valid: bool, errors: list of error messages)
        
    Example:
        >>> record = {'age': 25, 'income': 50000, 'credit_score': 750}
        >>> is_valid, errors = validate_banking_record(record)
        >>> is_valid
        True
    """
    try:
        age = int(record.get('age', 0))
        income = float(record.get('income', 0))
        credit_score = int(record.get('credit_score', 0))
        
        errors = []
        
        # Age validation: 18-80 years (legal working age)
        if age < 18 or age > 80:
            errors.append(f"Invalid age {age}: Must be between 18 and 80")
        
        # Income validation: Must be positive and reasonable
        if income <= 0:
            errors.append(f"Invalid income {income}: Must be greater than 0")
        
        # Credit score validation: Standard FICO range
        if credit_score < 300 or credit_score > 850:
            errors.append(f"Invalid credit score {credit_score}: Must be between 300 and 850")
        
        return len(errors) == 0, errors
    
    except (ValueError, TypeError) as e:
        return False, [f"Data type error in banking record: {str(e)}"]


# ==================== HEALTHCARE DOMAIN VALIDATION ====================

def validate_healthcare_record(record):
    """
    Validate a single healthcare record.
    
    Expected fields:
    - age: Integer between 0 and 120
    - blood_group: String from list [A+, A-, B+, B-, O+, O-, AB+, AB-]
    
    Future Integration:
    - Connect to COBOL patient management systems
    - Integrate with HL7/FHIR standards for medical records
    - Validate against hospital databases
    - Connect to pharmacy systems for drug interaction checks
    
    Args:
        record (dict): Dictionary containing healthcare data
        
    Returns:
        tuple: (is_valid: bool, errors: list of error messages)
        
    Example:
        >>> record = {'age': 30, 'blood_group': 'O+'}
        >>> is_valid, errors = validate_healthcare_record(record)
        >>> is_valid
        True
    """
    try:
        age = int(record.get('age', 0))
        blood_group = str(record.get('blood_group', '')).upper().strip()
        
        errors = []
        valid_blood_groups = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
        
        # Age validation: 0-120 years (realistic human age range)
        if age < 0 or age > 120:
            errors.append(f"Invalid age {age}: Must be between 0 and 120")
        
        # Blood group validation: Standard ABO-Rh system
        if blood_group not in valid_blood_groups:
            errors.append(
                f"Invalid blood group '{blood_group}': "
                f"Must be one of {valid_blood_groups}"
            )
        
        return len(errors) == 0, errors
    
    except (ValueError, TypeError) as e:
        return False, [f"Data type error in healthcare record: {str(e)}"]


# ==================== ECOMMERCE DOMAIN VALIDATION ====================

def validate_ecommerce_record(record):
    """
    Validate a single e-commerce product record.
    
    Expected fields:
    - price: Float/Decimal greater than 0
    - stock: Integer greater than or equal to 0
    
    Future Integration:
    - Connect to inventory management systems
    - Integrate with COBOL mainframe for purchase order processing
    - Validate against supplier databases
    - Update DB2 inventory tables in real-time
    - Price optimization engine integration
    
    Args:
        record (dict): Dictionary containing e-commerce product data
        
    Returns:
        tuple: (is_valid: bool, errors: list of error messages)
        
    Example:
        >>> record = {'price': 99.99, 'stock': 50}
        >>> is_valid, errors = validate_ecommerce_record(record)
        >>> is_valid
        True
    """
    try:
        price = float(record.get('price', 0))
        stock = int(record.get('stock', 0))
        
        errors = []
        
        # Price validation: Must be positive
        if price <= 0:
            errors.append(f"Invalid price {price}: Must be greater than 0")
        
        # Stock validation: Cannot be negative
        if stock < 0:
            errors.append(f"Invalid stock {stock}: Cannot be negative")
        
        # Price reasonability check: Prevent system errors from extreme values
        if price > 9999999:
            errors.append(f"Invalid price {price}: Exceeds maximum allowed price")
        
        return len(errors) == 0, errors
    
    except (ValueError, TypeError) as e:
        return False, [f"Data type error in e-commerce record: {str(e)}"]


# ==================== MAIN VALIDATION ORCHESTRATOR ====================

def validate_data(file_path, domain):
    """
    Main validation orchestrator with Data Quality Dimension calculation.
    
    Routes data validation requests to domain-specific validators and
    aggregates results with data quality metrics:
    - Completeness: % of records with all required fields
    - Validity: % of records passing validation rules
    - Consistency: % of records following established patterns
    - Final Score: Weighted combination (40% + 40% + 20%)
    
    This function is designed to be called from:
    - REST API endpoints
    - COBOL programs (via message queue - future)
    - Batch processing jobs
    - Third-party systems
    
    Args:
        file_path (str): Path to the CSV file to validate
        domain (str): Domain type ('banking', 'healthcare', or 'ecommerce')
        
    Returns:
        ValidationResult: Object containing:
            - Record counts
            - Data quality dimensions (completeness, validity, consistency)
            - Final weighted score
            - Error details
        
    Example:
        >>> result = validate_data('data.csv', 'banking')
        >>> print(f"Final Score: {result.final_score}%")
        >>> print(f"Quality: {result.to_dict()['quality_rating']}")
    """
    result = ValidationResult()
    domain = domain.lower()
    
    # Map domains to their respective validation functions
    validators = {
        'banking': validate_banking_record,
        'healthcare': validate_healthcare_record,
        'ecommerce': validate_ecommerce_record
    }
    
    # Validate domain parameter
    if domain not in validators:
        result.errors.append(
            f"Unknown domain '{domain}'. "
            f"Must be one of: {list(validators.keys())}"
        )
        return result
    
    validator = validators[domain]
    
    try:
        # Open and read CSV file
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # Validate CSV has headers
            if reader.fieldnames is None:
                result.errors.append("File is empty or invalid CSV format")
                return result
            
            # Process each row in the CSV
            for row_num, record in enumerate(reader, start=2):  # start=2: row 1 is header
                result.total_records += 1
                
                # ===== COMPLETENESS DIMENSION =====
                # Check if record has all required fields populated
                if is_record_complete(record, domain):
                    result.complete_records += 1
                
                # ===== VALIDITY DIMENSION =====
                # Check if record passes domain validation rules
                is_valid, record_errors = validator(record)
                if is_valid:
                    result.valid_records += 1
                else:
                    result.invalid_records += 1
                    for error in record_errors:
                        result.errors.append(f"Row {row_num}: {error}")
                
                # ===== CONSISTENCY DIMENSION =====
                # Check if record follows established patterns
                if is_record_consistent(record, domain):
                    result.consistent_records += 1
                
                # ===== PHASE 5: ANOMALY DETECTION =====
                # Detect statistical outliers and unusual patterns
                anomaly_detectors = {
                    'banking': detect_anomalies_banking,
                    'healthcare': detect_anomalies_healthcare,
                    'ecommerce': detect_anomalies_ecommerce
                }
                
                if domain in anomaly_detectors:
                    record_anomalies = anomaly_detectors[domain](record)
                    if record_anomalies:
                        result.anomaly_count += 1
                        for anomaly in record_anomalies:
                            result.anomalies.append(f"Row {row_num}: {anomaly}")
    
    except Exception as e:
        result.errors.append(f"File processing error: {str(e)}")
    
    # ===== CALCULATE DATA QUALITY SCORES =====
    result.completeness_score = calculate_completeness_score(
        result.complete_records, result.total_records
    )
    result.validity_score = calculate_validity_score(
        result.valid_records, result.total_records
    )
    result.consistency_score = calculate_consistency_score(
        result.consistent_records, result.total_records
    )
    result.final_score = calculate_weighted_score(
        result.completeness_score,
        result.validity_score,
        result.consistency_score
    )
    
    # ===== PHASE 5: Calculate Anomaly Score =====
    result.anomaly_score = calculate_anomaly_score(
        result.anomaly_count, result.total_records
    )
    
    return result


# ==================== DOMAIN-SPECIFIC VALIDATORS ====================

def validate_banking_record(record):
    """
    Validate a single banking record.
    
    Expected fields:
    - age: Integer between 18 and 80
    - income: Float/Decimal greater than 0
    - credit_score: Integer between 300 and 850
    
    Future Integration:
    - Connect to DB2 to validate against regulatory compliance rules
    - Integrate with COBOL programs for legacy credit scoring algorithms
    - Call external services for fraud detection
    
    Args:
        record (dict): Dictionary containing banking data
        
    Returns:
        tuple: (is_valid: bool, errors: list of error messages)
        
    Example:
        >>> record = {'age': 25, 'income': 50000, 'credit_score': 750}
        >>> is_valid, errors = validate_banking_record(record)
        >>> is_valid
        True
    """
    try:
        age = int(record.get('age', 0))
        income = float(record.get('income', 0))
        credit_score = int(record.get('credit_score', 0))
        
        errors = []
        
        # Age validation: 18-80 years (legal working age)
        if age < 18 or age > 80:
            errors.append(f"Invalid age {age}: Must be between 18 and 80")
        
        # Income validation: Must be positive and reasonable
        if income <= 0:
            errors.append(f"Invalid income {income}: Must be greater than 0")
        
        # Credit score validation: Standard FICO range
        if credit_score < 300 or credit_score > 850:
            errors.append(f"Invalid credit score {credit_score}: Must be between 300 and 850")
        
        return len(errors) == 0, errors
    
    except (ValueError, TypeError) as e:
        return False, [f"Data type error in banking record: {str(e)}"]


# ==================== HEALTHCARE DOMAIN VALIDATION ====================

def validate_healthcare_record(record):
    """
    Validate a single healthcare record.
    
    Expected fields:
    - age: Integer between 0 and 120
    - blood_group: String from list [A+, A-, B+, B-, O+, O-, AB+, AB-]
    
    Future Integration:
    - Connect to COBOL patient management systems
    - Integrate with HL7/FHIR standards for medical records
    - Validate against hospital databases
    - Connect to pharmacy systems for drug interaction checks
    
    Args:
        record (dict): Dictionary containing healthcare data
        
    Returns:
        tuple: (is_valid: bool, errors: list of error messages)
        
    Example:
        >>> record = {'age': 30, 'blood_group': 'O+'}
        >>> is_valid, errors = validate_healthcare_record(record)
        >>> is_valid
        True
    """
    try:
        age = int(record.get('age', 0))
        blood_group = str(record.get('blood_group', '')).upper().strip()
        
        errors = []
        valid_blood_groups = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
        
        # Age validation: 0-120 years (realistic human age range)
        if age < 0 or age > 120:
            errors.append(f"Invalid age {age}: Must be between 0 and 120")
        
        # Blood group validation: Standard ABO-Rh system
        if blood_group not in valid_blood_groups:
            errors.append(
                f"Invalid blood group '{blood_group}': "
                f"Must be one of {valid_blood_groups}"
            )
        
        return len(errors) == 0, errors
    
    except (ValueError, TypeError) as e:
        return False, [f"Data type error in healthcare record: {str(e)}"]


# ==================== ECOMMERCE DOMAIN VALIDATION ====================

def validate_ecommerce_record(record):
    """
    Validate a single e-commerce product record.
    
    Expected fields:
    - price: Float/Decimal greater than 0
    - stock: Integer greater than or equal to 0
    
    Future Integration:
    - Connect to inventory management systems
    - Integrate with COBOL mainframe for purchase order processing
    - Validate against supplier databases
    - Update DB2 inventory tables in real-time
    - Price optimization engine integration
    
    Args:
        record (dict): Dictionary containing e-commerce product data
        
    Returns:
        tuple: (is_valid: bool, errors: list of error messages)
        
    Example:
        >>> record = {'price': 99.99, 'stock': 50}
        >>> is_valid, errors = validate_ecommerce_record(record)
        >>> is_valid
        True
    """
    try:
        price = float(record.get('price', 0))
        stock = int(record.get('stock', 0))
        
        errors = []
        
        # Price validation: Must be positive
        if price <= 0:
            errors.append(f"Invalid price {price}: Must be greater than 0")
        
        # Stock validation: Cannot be negative
        if stock < 0:
            errors.append(f"Invalid stock {stock}: Cannot be negative")
        
        # Price reasonability check: Prevent system errors from extreme values
        if price > 9999999:
            errors.append(f"Invalid price {price}: Exceeds maximum allowed price")
        
        return len(errors) == 0, errors
    
    except (ValueError, TypeError) as e:
        return False, [f"Data type error in e-commerce record: {str(e)}"]


# ==================== MAIN VALIDATION ORCHESTRATOR ====================

