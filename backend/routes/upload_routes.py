"""
Upload Routes Module - PHASE 7 ENHANCED

Handles all HTTP endpoints for file upload, validation, and result storage with
security enhancements including rate limiting, input sanitization, and logging.

PHASE 7 ENHANCEMENTS:
- Rate limiting on upload endpoint
- CSV input sanitization
- Domain validation
- Security logging
- COBOL mainframe integration ready
"""

import os
import logging
from datetime import datetime
from flask import request, jsonify
from werkzeug.utils import secure_filename
from services.validation_service import validate_data
from services.file_service import allowed_file, get_allowed_extensions
from services.database_service import store_validation_result
from services.security_utils import CSVSecurityValidator, InputValidator, SecurityLogger

logger = logging.getLogger(__name__)


def register_routes(app):
    """
    Register all routes with the Flask application.
    
    Args:
        app: Flask application instance
    """
    
    @app.route('/', methods=['GET'])
    def home():
        """
        Health check endpoint.
        
        Returns a simple status message to verify backend is running.
        Used for:
        - Deployment verification
        - Health monitoring
        - Load balancer checks
        
        Route: GET /
        
        Returns:
            tuple: JSON response and HTTP 200 status
            
        Example:
            GET http://localhost:5000/
            Response: {"message": "Backend Running"}
        """
        return jsonify({'message': 'Backend Running'}), 200
    
    
    @app.route('/upload', methods=['POST'])
    def upload_file():
        """
        Main file upload, validation, and storage endpoint (PHASE 7 SECURED).
        
        PHASE 7 SECURITY FEATURES:
        - Rate limiting: 10 uploads per hour per IP
        - CSV input sanitization: Prevents injection attacks
        - Domain validation
        - Security logging and audit trail
        - File type/size validation
        - COBOL mainframe integration ready
        
        Accepts a CSV file and domain parameter, validates the data according to
        domain-specific rules, calculates data quality dimensions, stores results
        in the database, and returns comprehensive quality metrics.
        
        Route: POST /upload
        
        Request Format:
        {
            'file': <CSV or TXT file>,
            'domain': 'banking' | 'healthcare' | 'ecommerce'
        }
        
        Response Format (with Data Quality Dimensions & Anomalies):
        {
            'record_id': int (database record ID),
            'total_records': int,
            'valid_records': int,
            'invalid_records': int,
            'score_percentage': float (legacy, for backward compatibility),
            
            # Data Quality Dimensions
            'completeness_score': float (0-100),
            'validity_score': float (0-100),
            'consistency_score': float (0-100),
            'final_score': float (0-100, weighted),
            'quality_rating': str (Excellent/Good/Acceptable/Poor),
            
            # Anomaly Detection (Phase 5)
            'anomaly_count': int,
            'anomaly_score': float,
            'anomalies': [list of detected anomalies],
            
            # Storage Info
            'stored': bool (successfully stored in database),
            'timestamp': ISO datetime string,
            
            'errors': [list of error strings with row numbers]
        }
        
        Returns:
            tuple: JSON response and HTTP status code
                - 200: Validation completed successfully (stored in database)
                - 400: Missing or invalid input, file validation failed
                - 413: File too large
                - 429: Rate limit exceeded
                - 500: Server error
        """
        try:
            # ===== PHASE 7: RATE LIMITING CHECK =====
            from app import rate_limit_store
            
            client_ip = request.remote_addr or 'unknown'
            if rate_limit_store.is_rate_limited(client_ip, max_requests=10, time_window=3600):
                logger.warning(f"Rate limit exceeded for IP: {client_ip}")
                SecurityLogger.log_security_event(
                    'RATE_LIMIT_EXCEEDED',
                    f'IP: {client_ip}, Endpoint: /upload',
                    'WARNING'
                )
                
                return jsonify({
                    'error': 'Rate limit exceeded. Maximum 10 uploads per hour.',
                    'retry_after': 3600
                }), 429
            
            # ===== VALIDATION: Request Parameters =====
            
            # Check file is provided
            if 'file' not in request.files:
                SecurityLogger.log_validation_attempt(
                    'unknown', 'unknown', 'blocked',
                    'No file provided'
                )
                return jsonify({'error': 'No file provided'}), 400
            
            # Check domain is provided
            if 'domain' not in request.form:
                SecurityLogger.log_validation_attempt(
                    'unknown', 'unknown', 'blocked',
                    'No domain specified'
                )
                return jsonify({'error': 'No domain specified'}), 400
            
            file = request.files['file']
            domain = request.form.get('domain')
            
            # ===== PHASE 7: DOMAIN VALIDATION =====
            
            if not InputValidator.validate_domain(domain):
                SecurityLogger.log_validation_attempt(
                    file.filename, domain, 'blocked',
                    f'Invalid domain: {domain}'
                )
                return jsonify({
                    'error': 'Invalid domain. Must be: banking, healthcare, or ecommerce'
                }), 400
            
            # ===== PHASE 7: FILENAME VALIDATION =====
            
            if not CSVSecurityValidator.validate_filename(file.filename):
                SecurityLogger.log_validation_attempt(
                    file.filename, domain, 'blocked',
                    'Invalid filename format'
                )
                return jsonify({
                    'error': 'Invalid filename. Only alphanumeric, dash, and underscore allowed.'
                }), 400
            
            # ===== VALIDATION: File =====
            
            # Check file is selected (not empty filename)
            if file.filename == '':
                SecurityLogger.log_validation_attempt(
                    file.filename, domain, 'blocked',
                    'No file selected'
                )
                return jsonify({'error': 'No file selected'}), 400
            
            # ===== PHASE 7: FILE SIZE VALIDATION =====
            
            file_size = len(file.read())
            file.seek(0)  # Reset file pointer
            
            if not CSVSecurityValidator.validate_file_size(file_size):
                SecurityLogger.log_validation_attempt(
                    file.filename, domain, 'blocked',
                    f'File too large: {file_size} bytes'
                )
                return jsonify({
                    'error': f'File too large. Maximum size is {CSVSecurityValidator.MAX_FILE_SIZE} bytes.'
                }), 413
            
            # ===== PHASE 7: FILE TYPE VALIDATION =====
            
            if not CSVSecurityValidator.validate_file_type(file.filename, file.read()):
                file.seek(0)
                SecurityLogger.log_validation_attempt(
                    file.filename, domain, 'blocked',
                    'Invalid file type or encoding'
                )
                return jsonify({
                    'error': 'Invalid file type. Must be UTF-8 encoded CSV or text file.'
                }), 400
            
            file.seek(0)  # Reset file pointer again
            
            # Check file extension is allowed
            if not allowed_file(file.filename):
                allowed_exts = ', '.join(get_allowed_extensions())
                SecurityLogger.log_validation_attempt(
                    file.filename, domain, 'blocked',
                    f'Invalid extension. Allowed: {allowed_exts}'
                )
                return jsonify({
                    'error': f'File type not allowed. Allowed types: {allowed_exts}'
                }), 400
            
            # ===== FILE HANDLING: Save Uploaded File =====
            
            # Generate secure filename with timestamp to avoid collisions
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            
            upload_folder = 'uploads'
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            
            logger.info(f"File saved: {file_path} for domain: {domain}")
            
            # ===== PHASE 7: READ AND SANITIZE FILE CONTENT =====
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                
                # Sanitize CSV data
                sanitized_lines, errors = CSVSecurityValidator.sanitize_csv_data(file_content)
                
                if errors:
                    logger.warning(f"Sanitization errors: {errors}")
                    SecurityLogger.log_security_event(
                        'CSV_SANITIZATION_WARNINGS',
                        f'File: {filename}, Errors: {len(errors)}',
                        'WARNING'
                    )
                
                # Write sanitized data back
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(sanitized_lines))
                
            except Exception as e:
                logger.error(f"Error during file sanitization: {str(e)}")
                SecurityLogger.log_security_event(
                    'FILE_SANITIZATION_ERROR',
                    f'File: {filename}, Error: {str(e)}',
                    'CRITICAL'
                )
                return jsonify({
                    'error': 'Error processing file content'
                }), 400
            
            # ===== VALIDATION: Perform Data Validation With Quality Metrics =====
            
            result = validate_data(file_path, domain)
            
            # ===== PHASE 7: COBOL MAINFRAME INTEGRATION READY =====
            # Uncomment to enable mainframe processing (requires RabbitMQ setup)
            # from services.mainframe_service import process_with_mainframe
            # result = process_with_mainframe(result.to_dict(), domain)
            
            # ===== STORAGE: Save Results to Database (PHASE 3) =====
            
            # Store validation result with all data quality metrics
            record_id = store_validation_result(result, domain, file.filename)
            stored = record_id is not None
            
            # ===== PHASE 7: SECURITY LOGGING =====
            
            SecurityLogger.log_validation_attempt(
                file.filename,
                domain,
                'success',
                f'Record ID: {record_id}, Score: {result.final_score:.1f}%'
            )
            
            # ===== RESPONSE: Return Enhanced Validation Results =====
            
            response_data = result.to_dict()
            response_data['record_id'] = record_id
            response_data['stored'] = stored
            response_data['timestamp'] = datetime.now().isoformat()
            
            logger.info(f"Validation complete. Final score: {result.final_score:.1f}%")
            
            return jsonify(response_data), 200
        
        except Exception as e:
            logger.error(f"Unexpected error in upload: {str(e)}")
            SecurityLogger.log_security_event(
                'UPLOAD_ERROR',
                f'Error: {str(e)}',
                'CRITICAL'
            )
            return jsonify({'error': f'Server error: {str(e)}'}), 500

    
    
    @app.route('/results/<int:record_id>', methods=['GET'])
    def get_result(record_id):
        """
        Retrieve a previously stored validation result (PHASE 3).
        
        Route: GET /results/<record_id>
        
        Args:
            record_id (int): Database record ID from previous validation
            
        Returns:
            tuple: JSON response with validation result and HTTP status
            
        Example:
            GET /results/42
            Response: {...full validation result...}
        """
        from services.database_service import get_validation_result
        
        result = get_validation_result(record_id)
        if result:
            return jsonify(result), 200
        else:
            return jsonify({'error': 'Record not found'}), 404
    
    
    @app.route('/stats/<domain>', methods=['GET'])
    def get_domain_stats(domain):
        """
        Get aggregated statistics for a domain (PHASE 3).
        
        Route: GET /stats/<domain>
        
        Returns aggregated quality metrics for all validations in a domain.
        Useful for trend analysis and quality monitoring.
        
        Args:
            domain (str): Domain name (banking, healthcare, ecommerce)
            
        Returns:
            tuple: JSON response with domain statistics and HTTP status
            
        Example:
            GET /stats/banking
            Response: {
                "total_validations": 25,
                "avg_final_score": 92.5,
                "avg_completeness": 98.0,
                "avg_validity": 92.0,
                "avg_consistency": 90.0,
                "best_score": 99.5,
                "worst_score": 78.3
            }
        """
        from services.database_service import get_domain_statistics
        
        stats = get_domain_statistics(domain)
        if stats:
            return jsonify(stats), 200
        else:
            return jsonify({'error': 'No statistics available for this domain'}), 404
    
    
    @app.route('/history', methods=['GET'])
    def get_history():
        """
        Get recent validation history (PHASE 3).
        
        Route: GET /history?limit=10
        
        Returns most recent validation records from database.
        
        Query Parameters:
            limit (int): Maximum records to return (default: 10, max: 100)
            
        Returns:
            tuple: JSON response with recent validations and HTTP status
        """
        from services.database_service import get_recent_validations
        
        limit = request.args.get('limit', 10, type=int)
        limit = min(limit, 100)  # Cap at 100
        
        validations = get_recent_validations(limit)
        return jsonify({'total': len(validations), 'validations': validations}), 200
    
    
    @app.route('/export', methods=['GET'])
    def export_data():
        """
        Export validation data for analysis (PHASE 3).
        
        Route: GET /export?domain=banking&format=json
        
        Query Parameters:
            domain (str): Optional - filter by domain
            format (str): json or csv (default: json)
            
        Returns:
            tuple: Data in specified format and HTTP status
        """
        from services.database_service import export_validation_data
        
        domain = request.args.get('domain', None)
        format_type = request.args.get('format', 'json')
        
        if format_type not in ['json', 'csv']:
            return jsonify({'error': 'Format must be json or csv'}), 400
        
        data = export_validation_data(domain, format_type)
        
        if format_type == 'csv':
            return data, 200, {'Content-Type': 'text/csv'}
        else:
            return data, 200, {'Content-Type': 'application/json'}
    
    
    @app.route('/db-stats', methods=['GET'])
    def database_stats():
        """
        Get overall database statistics (PHASE 3).
        
        Route: GET /db-stats
        
        Returns database health and usage statistics.
        
        Returns:
            tuple: JSON response with database stats and HTTP status
        """
        from services.database_service import get_database_stats
        
        stats = get_database_stats()
        return jsonify(stats), 200
    
    
    # ==================== ERROR HANDLERS ====================
    
    @app.errorhandler(413)
    def request_entity_too_large(error):
        """
        Handle file size exceeded error.
        
        Returns:
            tuple: JSON error message and HTTP 413 status
            
        Note: Configure max file size in app.config['MAX_CONTENT_LENGTH']
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
                allowed_exts = ', '.join(get_allowed_extensions())
                return jsonify({
                    'error': f'File type not allowed. Allowed types: {allowed_exts}'
                }), 400
            
            # ===== FILE HANDLING: Save Uploaded File =====
            
            # Generate secure filename with timestamp to avoid collisions
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            
            upload_folder = 'uploads'
            file_path = os.path.join(upload_folder, filename)
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
            
        Note: Configure max file size in app.config['MAX_CONTENT_LENGTH']
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
