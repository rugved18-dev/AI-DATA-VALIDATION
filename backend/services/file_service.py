"""
File Service Module

Handles file upload validation and file operations.
"""

ALLOWED_EXTENSIONS = {'csv', 'txt'}


def allowed_file(filename):
    """
    Check if file has allowed extension.
    
    Validates that the uploaded file has one of the supported extensions
    (CSV or TXT).
    
    Args:
        filename (str): Name of the file to validate
        
    Returns:
        bool: True if file extension is allowed, False otherwise
        
    Example:
        >>> allowed_file('data.csv')
        True
        >>> allowed_file('data.pdf')
        False
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_allowed_extensions():
    """
    Get the set of allowed file extensions.
    
    Returns:
        set: Set of allowed extensions
    """
    return ALLOWED_EXTENSIONS
