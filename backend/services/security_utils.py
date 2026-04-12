"""
Security Utilities Module - PHASE 7

Input validation, sanitization, and security helpers for preventing
injection attacks, malformed data, and harmful content.
"""

import re
import logging
from typing import List, Any, Optional
import mimetypes

logger = logging.getLogger(__name__)


# ==================== CSV VALIDATION ====================

class CSVSecurityValidator:
    """Validate and sanitize CSV uploads."""
    
    # Maximum file size: 100MB
    MAX_FILE_SIZE = 100 * 1024 * 1024
    
    # Maximum rows per file
    MAX_ROWS = 100000
    
    # Maximum columns per row
    MAX_COLUMNS = 500
    
    # Allowed MIME types for CSV
    ALLOWED_MIMETYPES = ['text/csv', 'text/plain', 'application/csv']
    
    # Dangerous patterns that might indicate injection attacks
    DANGEROUS_PATTERNS = [
        r'^=',  # Formula injection
        r'^@',  # Command injection
        r'^[+\-]',  # Hidden formula
        r'^\\',  # LDAP injection
        r'javascript:',  # JavaScript injection
        r'<script',  # Script tags
        r'<!--',  # HTML comments with potential exploits
    ]
    
    @staticmethod
    def validate_filename(filename: str) -> bool:
        """
        Validate filename safety.
        
        Args:
            filename (str): File name to validate
            
        Returns:
            bool: True if safe, False otherwise
        """
        # Check for path traversal
        if '..' in filename or '/' in filename or '\\' in filename:
            logger.warning(f"Path traversal detected in filename: {filename}")
            return False
        
        # Check for null bytes
        if '\x00' in filename:
            logger.warning("Null byte detected in filename")
            return False
        
        # Allow alphanumeric, underscore, hyphen, and dot
        if not re.match(r'^[\w\-\.]+$', filename):
            logger.warning(f"Invalid characters in filename: {filename}")
            return False
        
        # Check file extension
        if not filename.lower().endswith(('.csv', '.txt')):
            logger.warning(f"Invalid file extension: {filename}")
            return False
        
        return True
    
    @staticmethod
    def validate_file_size(file_size: int) -> bool:
        """
        Validate file size.
        
        Args:
            file_size (int): File size in bytes
            
        Returns:
            bool: True if within limits
        """
        if file_size > CSVSecurityValidator.MAX_FILE_SIZE:
            logger.warning(f"File size {file_size} exceeds maximum {CSVSecurityValidator.MAX_FILE_SIZE}")
            return False
        
        if file_size == 0:
            logger.warning("Empty file submitted")
            return False
        
        return True
    
    @staticmethod
    def validate_file_type(filename: str, file_content: bytes) -> bool:
        """
        Validate file type by extension and content inspection.
        
        Args:
            filename (str): File name
            file_content (bytes): File content
            
        Returns:
            bool: True if valid CSV
        """
        # Check MIME type
        mime_type, _ = mimetypes.guess_type(filename)
        if mime_type and mime_type not in CSVSecurityValidator.ALLOWED_MIMETYPES:
            logger.warning(f"Invalid MIME type: {mime_type}")
            return False
        
        # Check file signature (magic bytes) - CSV should start with printable ASCII
        try:
            # Try to decode as UTF-8
            file_content.decode('utf-8')
        except UnicodeDecodeError:
            logger.warning("File is not valid UTF-8 text")
            return False
        
        return True
    
    @staticmethod
    def sanitize_cell_value(value: str) -> str:
        """
        Sanitize individual cell values to prevent injection attacks.
        
        Args:
            value (str): Cell value
            
        Returns:
            str: Sanitized value
        """
        if not isinstance(value, str):
            return str(value)
        
        # Strip leading/trailing whitespace
        value = value.strip()
        
        # Check for dangerous patterns
        for pattern in CSVSecurityValidator.DANGEROUS_PATTERNS:
            if re.match(pattern, value, re.IGNORECASE):
                logger.warning(f"Dangerous pattern detected: {pattern} in value: {value[:50]}")
                # Remove the dangerous prefix
                value = re.sub(f'^{pattern}', '', value, flags=re.IGNORECASE)
        
        # Remove null bytes
        value = value.replace('\x00', '')
        
        # Limit value length to prevent buffer overflow
        max_length = 10000
        if len(value) > max_length:
            logger.warning(f"Cell value exceeds max length {max_length}")
            value = value[:max_length]
        
        return value
    
    @staticmethod
    def validate_row_structure(row: List[Any], expected_columns: int) -> bool:
        """
        Validate row structure and column count.
        
        Args:
            row (List): Row data
            expected_columns (int): Expected number of columns
            
        Returns:
            bool: True if valid
        """
        if not isinstance(row, (list, tuple)):
            logger.warning("Row is not a list or tuple")
            return False
        
        if len(row) > CSVSecurityValidator.MAX_COLUMNS:
            logger.warning(f"Row has {len(row)} columns, max is {CSVSecurityValidator.MAX_COLUMNS}")
            return False
        
        # Allow some flexibility in column count (±1 for trailing/leading)
        if expected_columns > 0 and len(row) not in [expected_columns - 1, expected_columns, expected_columns + 1]:
            logger.warning(f"Column count mismatch: expected ~{expected_columns}, got {len(row)}")
            return False
        
        return True
    
    @staticmethod
    def sanitize_csv_data(file_content: str, max_rows: Optional[int] = None) -> tuple:
        """
        Sanitize complete CSV content.
        
        Args:
            file_content (str): Raw CSV content
            max_rows (int): Maximum rows to process
            
        Returns:
            tuple: (sanitized_lines, error_list)
        """
        if max_rows is None:
            max_rows = CSVSecurityValidator.MAX_ROWS
        
        lines = file_content.split('\n')
        sanitized_lines = []
        errors = []
        
        for idx, line in enumerate(lines):
            if idx >= max_rows:
                errors.append(f"File exceeds maximum {max_rows} rows. Truncated.")
                break
            
            if not line.strip():
                continue
            
            try:
                # Sanitize each value in the row
                values = line.split(',')
                sanitized_values = []
                
                for val in values:
                    sanitized_val = CSVSecurityValidator.sanitize_cell_value(val)
                    sanitized_values.append(sanitized_val)
                
                sanitized_line = ','.join(sanitized_values)
                sanitized_lines.append(sanitized_line)
                
            except Exception as e:
                errors.append(f"Row {idx + 1}: Error sanitizing - {str(e)}")
                continue
        
        return sanitized_lines, errors


# ==================== INPUT VALIDATION ====================

class InputValidator:
    """General input validation utilities."""
    
    @staticmethod
    def validate_domain(domain: str) -> bool:
        """
        Validate domain parameter.
        
        Args:
            domain (str): Domain name
            
        Returns:
            bool: True if valid
        """
        valid_domains = ['banking', 'healthcare', 'ecommerce']
        
        if not isinstance(domain, str):
            logger.warning(f"Domain is not a string: {type(domain)}")
            return False
        
        if domain.lower() not in valid_domains:
            logger.warning(f"Invalid domain: {domain}. Must be one of {valid_domains}")
            return False
        
        return True
    
    @staticmethod
    def validate_json_input(data: dict, required_fields: List[str]) -> tuple:
        """
        Validate JSON input structure.
        
        Args:
            data (dict): Input data
            required_fields (List[str]): Required field names
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not isinstance(data, dict):
            return False, "Input must be a JSON object"
        
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
        
        return True, ""
    
    @staticmethod
    def sanitize_string(value: str, max_length: int = 1000) -> str:
        """
        Sanitize string input.
        
        Args:
            value (str): String to sanitize
            max_length (int): Maximum length
            
        Returns:
            str: Sanitized string
        """
        if not isinstance(value, str):
            value = str(value)
        
        # Remove null bytes
        value = value.replace('\x00', '')
        
        # Remove control characters (except newline, tab)
        value = ''.join(char for char in value if ord(char) >= 32 or char in '\n\t')
        
        # Limit length
        if len(value) > max_length:
            value = value[:max_length]
        
        return value


# ==================== SQL INJECTION PREVENTION ====================

class SQLInjectionPrevention:
    """Prevent SQL injection attacks."""
    
    # Dangerous SQL keywords
    DANGEROUS_KEYWORDS = [
        'DROP', 'DELETE', 'INSERT', 'UPDATE', 'ALTER', 'EXEC',
        'EXECUTE', 'UNION', 'SELECT', 'TRUNCATE', 'REPLACE'
    ]
    
    @staticmethod
    def has_sql_patterns(value: str) -> bool:
        """
        Check if value contains SQL injection patterns.
        
        Args:
            value (str): Value to check
            
        Returns:
            bool: True if dangerous patterns detected
        """
        if not isinstance(value, str):
            return False
        
        # Check for dangerous keywords
        upper_value = value.upper()
        for keyword in SQLInjectionPrevention.DANGEROUS_KEYWORDS:
            if keyword in upper_value:
                return True
        
        # Check for SQL comment patterns
        if '--' in value or '/*' in value or '*/' in value:
            return True
        
        # Check for quote-based injection patterns
        if "'; DROP" in value or '"; DROP' in value:
            return True
        
        return False
    
    @staticmethod
    def sanitize_for_database(value: str) -> str:
        """
        Sanitize value before database insertion.
        
        Args:
            value (str): Value to sanitize
            
        Returns:
            str: Sanitized value
        """
        if SQLInjectionPrevention.has_sql_patterns(value):
            logger.warning(f"SQL injection pattern detected, value truncated")
            return value[:10]  # Return only first 10 chars
        
        # Double single quotes for SQL escaping
        value = value.replace("'", "''")
        
        return value


# ==================== LOGGING ====================

class SecurityLogger:
    """Enhanced logging for security events."""
    
    @staticmethod
    def log_validation_attempt(filename: str, domain: str, status: str, reason: str = ""):
        """
        Log validation attempt.
        
        Args:
            filename (str): File name
            domain (str): Domain
            status (str): Status (success, blocked, etc)
            reason (str): Reason for status
        """
        log_msg = f"Validation attempt - File: {filename}, Domain: {domain}, Status: {status}"
        if reason:
            log_msg += f", Reason: {reason}"
        
        if status == 'blocked':
            logger.warning(log_msg)
        elif status == 'error':
            logger.error(log_msg)
        else:
            logger.info(log_msg)
    
    @staticmethod
    def log_security_event(event_type: str, details: str, severity: str = "INFO"):
        """
        Log security event.
        
        Args:
            event_type (str): Type of event
            details (str): Event details
            severity (str): Severity level (INFO, WARNING, CRITICAL)
        """
        log_msg = f"SECURITY EVENT - Type: {event_type}, Details: {details}"
        
        if severity == "CRITICAL":
            logger.critical(log_msg)
        elif severity == "WARNING":
            logger.warning(log_msg)
        else:
            logger.info(log_msg)


if __name__ == '__main__':
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    # Test filename validation
    print("=" * 50)
    print("FILENAME VALIDATION TESTS")
    print("=" * 50)
    
    test_filenames = [
        'sample_data.csv',
        '../../../etc/passwd',
        'data\x00.csv',
        'valid_file.txt',
        'invalid.exe'
    ]
    
    for fname in test_filenames:
        valid = CSVSecurityValidator.validate_filename(fname)
        print(f"{fname}: {'✓ VALID' if valid else '✗ INVALID'}")
    
    # Test cell sanitization
    print("\n" + "=" * 50)
    print("CELL VALUE SANITIZATION TESTS")
    print("=" * 50)
    
    test_values = [
        '=1+1',
        '@SUM(A:A)',
        '+2*5',
        'normal_value',
        '<script>alert("xss")</script>'
    ]
    
    for val in test_values:
        sanitized = CSVSecurityValidator.sanitize_cell_value(val)
        print(f"Original: {val}")
        print(f"Sanitized: {sanitized}\n")
