"""
Flask Backend for Multi-Domain AI Data Validation System

This backend provides APIs for data validation across different domains:
- Banking: Validate customer financial profiles
- Healthcare: Validate patient health records
- E-commerce: Validate product inventory data

Future Integration Points:
- COBOL Mainframe Systems: Message queue integration for legacy system compatibility
- DB2 Database: Enhanced validation against regulatory rules and historical data
- Microservices: RESTful APIs for scalable validation

Author: AI Data Validation Team
Version: 1.0.0
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import csv
from datetime import datetime
from werkzeug.utils import secure_filename

# ==================== FLASK APP INITIALIZATION ====================

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for frontend communication

# ==================== CONFIGURATION ====================

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'txt'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB limit

# Create uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# ==================== UTILITY FUNCTIONS ====================

def allowed_file(filename):
    """
    Check if file has allowed extension.
    
    Args:
        filename (str): Name of the file to validate
        
    Returns:
        bool: True if file extension is allowed, False otherwise
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ==================== DATA STRUCTURES ====================

class ValidationResult:
    """
    Data structure to hold validation results across all domains.
    
    This class is designed to be modular and compatible with:
    - JSON serialization for API responses
    - COBOL record structures (future mainframe integration)
    - Database schemas (DB2 integration)
    
    Attributes:
        total_records (int): Total number of records processed
        valid_records (int): Number of valid records
        invalid_records (int): Number of invalid records
        errors (list): List of validation error messages
    """
    
    def __init__(self):
        self.total_records = 0
        self.valid_records = 0
        self.invalid_records = 0
        self.errors = []
    
    def to_dict(self):
        """
        Convert validation result to JSON-compatible dictionary.
        
        Returns:
            dict: Result dictionary with score percentage calculated
        """
        score_percentage = (
            (self.valid_records / self.total_records * 100) 
            if self.total_records > 0 
            else 0
        )
        
        return {
            'total_records': self.total_records,
            'valid_records': self.valid_records,
            'invalid_records': self.invalid_records,
            'score_percentage': round(score_percentage, 2),
            'errors': self.errors
        }


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
    Main validation orchestrator function.
    
    Routes data validation requests to domain-specific validators and
    aggregates the results. This function acts as the central validation engine
    and is designed to be called from:
    - REST API endpoints
    - COBOL programs (via message queue - future)
    - Batch processing jobs
    - Third-party systems
    
    Args:
        file_path (str): Path to the CSV file to validate
        domain (str): Domain type ('banking', 'healthcare', or 'ecommerce')
        
    Returns:
        ValidationResult: Object containing validation statistics and errors
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
                
                # Validate individual record
                is_valid, record_errors = validator(record)
                
                if is_valid:
                    result.valid_records += 1
                else:
                    result.invalid_records += 1
                    # Add row number to error messages for easy debugging
                    for error in record_errors:
                        result.errors.append(f"Row {row_num}: {error}")
    
    except Exception as e:
        result.errors.append(f"File processing error: {str(e)}")
    
    return result


# ==================== API ENDPOINTS ====================

@app.route('/', methods=['GET'])
def home():
    """
    Health check endpoint.
    
    Returns a simple status message to verify backend is running.
    Used for:
    - Deployment verification
    - Health monitoring
    - Load balancer checks
    
    Returns:
        tuple: JSON response and HTTP 200 status
    """
    return jsonify({'message': 'Backend Running'}), 200


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Main file upload and validation endpoint.
    
    Accepts a CSV file and domain parameter, validates the data according to
    domain-specific rules, and returns validation results.
    
    Request Format:
    {
        'file': <CSV or TXT file>,
        'domain': 'banking' | 'healthcare' | 'ecommerce'
    }
    
    Response Format:
    {
        'total_records': int,
        'valid_records': int,
        'invalid_records': int,
        'score_percentage': float (0-100),
        'errors': [list of error strings with row numbers]
    }
    
    Example Request:
    POST /upload
    Content-Type: multipart/form-data
    
    file: <CSV file>
    domain: banking
    
    Example Response:
    {
        "total_records": 100,
        "valid_records": 95,
        "invalid_records": 5,
        "score_percentage": 95.0,
        "errors": [
            "Row 12: Invalid age 15: Must be between 18 and 80",
            "Row 45: Invalid credit score 250: Must be between 300 and 850"
        ]
    }
    
    Returns:
        tuple: JSON response and HTTP status code
            - 200: Validation completed successfully
            - 400: Missing or invalid input
            - 413: File too large
            - 500: Server error
    """
    try:
        # ===== VALIDATION: Request Parameters =====
        
        # Check file is provided
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        # Check domain is provided
        if 'domain' not in request.form:
            return jsonify({'error': 'No domain specified'}), 400
        
        file = request.files['file']
        domain = request.form.get('domain')
        
        # ===== VALIDATION: File =====
        
        # Check file is selected (not empty filename)
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file extension is allowed
        if not allowed_file(file.filename):
            return jsonify({
                'error': f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # ===== FILE HANDLING: Save Uploaded File =====
        
        # Generate secure filename with timestamp to avoid collisions
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # ===== VALIDATION: Perform Data Validation =====
        
        result = validate_data(file_path, domain)
        
        # ===== RESPONSE: Return Validation Results =====
        
        return jsonify(result.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


# ==================== ERROR HANDLERS ====================

@app.errorhandler(413)
def request_entity_too_large(error):
    """
    Handle file size exceeded error.
    
    Returns:
        tuple: JSON error message and HTTP 413 status
    """
    return jsonify({
        'error': 'File too large. Maximum size is 16MB'
    }), 413


@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 Not Found error.
    
    Returns:
        tuple: JSON error message and HTTP 404 status
    """
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Handle 500 Internal Server Error.
    
    Returns:
        tuple: JSON error message and HTTP 500 status
    """
    return jsonify({'error': 'Internal server error'}), 500


# ==================== APPLICATION ENTRY POINT ====================

if __name__ == '__main__':
    """
    Main application entry point.
    
    Configuration:
    - debug=True: Enables auto-reload and detailed error messages
    - host='0.0.0.0': Accept connections from any IP
    - port=5000: Default Flask development port
    
    Production Deployment:
    - Use production WSGI server (Gunicorn, uWSGI)
    - Set debug=False
    - Use environment variables for sensitive config
    
    Future Enhancements:
    - Add logging and monitoring
    - Implement message queue for COBOL integration
    - Add database connection pools for DB2
    - Implement request tracing for debugging
    """
    app.run(debug=True, host='0.0.0.0', port=5000)