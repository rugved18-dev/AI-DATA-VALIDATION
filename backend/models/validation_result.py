"""
Validation Result Model

Data structure to hold validation results with Data Quality Dimensions.

This module contains the ValidationResult class with advanced data quality metrics:
- Completeness: % of records with all required fields populated
- Validity: % of records that meet domain validation rules
- Consistency: % of records that are consistent with data patterns

Compatible with:
- JSON serialization for API responses
- COBOL record structures (mainframe integration)
- Database storage for audit trails
- Data quality assessment systems
"""


class ValidationResult:
    """
    Data structure to hold validation results with Data Quality Dimensions.
    
    Implements industry-standard data quality framework with three dimensions:
    1. Completeness: Are all required fields present?
    2. Validity: Do values conform to business rules?
    3. Consistency: Are values consistent with patterns?
    
    Attributes:
        total_records (int): Total number of records processed
        valid_records (int): Number of records passing all validation
        invalid_records (int): Number of records failing validation
        errors (list): List of validation error messages
        completeness_score (float): % of records with complete data (0-100)
        validity_score (float): % of records with valid values (0-100)
        consistency_score (float): % of records with consistent data (0-100)
        final_score (float): Weighted final data quality score (0-100)
    
    Scoring Formula (Industry Standard):
        final_score = (
            0.4 * completeness_score +    # 40% weight: Data presence
            0.4 * validity_score +        # 40% weight: Data correctness
            0.2 * consistency_score       # 20% weight: Data uniformity
        )
    """
    
    def __init__(self):
        """Initialize validation result with default values."""
        self.total_records = 0
        self.valid_records = 0
        self.invalid_records = 0
        self.errors = []
        
        # Data Quality Dimensions
        self.completeness_score = 0.0  # % of complete records
        self.validity_score = 0.0      # % of valid records
        self.consistency_score = 0.0   # % of consistent records
        self.final_score = 0.0         # Weighted final score
        
        # Tracking for dimension calculations
        self.complete_records = 0      # Records with all fields present
        self.consistent_records = 0    # Records following patterns
        
        # PHASE 5: Anomaly Detection
        self.anomalies = []            # List of detected anomalies
        self.anomaly_count = 0         # Count of records with anomalies
        self.anomaly_score = 0.0       # % of records with anomalies
    
    def calculate_scores(self):
        """
        Calculate all data quality dimension scores.
        
        Called after validation is complete to compute:
        - Completeness: complete_records / total_records * 100
        - Validity: valid_records / total_records * 100
        - Consistency: consistent_records / total_records * 100
        - Final Score: Weighted combination of above
        
        Industry Best Practices:
        - Score >= 95%: Excellent data quality
        - Score >= 85%: Good data quality
        - Score >= 75%: Acceptable data quality
        - Score < 75%: Poor data quality (requires remediation)
        """
        if self.total_records == 0:
            self.completeness_score = 0.0
            self.validity_score = 0.0
            self.consistency_score = 0.0
            self.final_score = 0.0
            return
        
        # Calculate individual scores
        self.completeness_score = round(
            (self.complete_records / self.total_records * 100), 2
        )
        self.validity_score = round(
            (self.valid_records / self.total_records * 100), 2
        )
        self.consistency_score = round(
            (self.consistent_records / self.total_records * 100), 2
        )
        
        # Calculate weighted final score
        # Formula: 40% Completeness + 40% Validity + 20% Consistency
        self.final_score = round(
            (0.4 * self.completeness_score) +
            (0.4 * self.validity_score) +
            (0.2 * self.consistency_score),
            2
        )
    
    def to_dict(self):
        """
        Convert validation result to JSON-compatible dictionary.
        
        Includes all data quality dimensions and metrics for comprehensive
        analysis and storage.
        
        Returns:
            dict: Result dictionary with:
                - Record counts
                - Legacy score_percentage (for backward compatibility)
                - Data Quality Dimensions (completeness, validity, consistency)
                - Final weighted quality score
                - PHASE 5: Anomalies detected
                - Error details
        """
        return {
            'total_records': self.total_records,
            'valid_records': self.valid_records,
            'invalid_records': self.invalid_records,
            
            # Legacy score (backward compatibility)
            'score_percentage': self.validity_score,
            
            # Data Quality Dimensions (NEW)
            'completeness_score': self.completeness_score,
            'validity_score': self.validity_score,
            'consistency_score': self.consistency_score,
            'final_score': self.final_score,
            
            # Quality Assessment
            'quality_rating': self._get_quality_rating(),
            
            # PHASE 5: Anomaly Detection
            'anomaly_count': self.anomaly_count,
            'anomaly_score': self.anomaly_score,
            'anomalies': self.anomalies,
            
            # Error details
            'errors': self.errors
        }
    
    def _get_quality_rating(self):
        """
        Get human-readable quality rating based on final score.
        
        Returns:
            str: One of: Excellent, Good, Acceptable, Poor
        """
        if self.final_score >= 95:
            return 'Excellent'
        elif self.final_score >= 85:
            return 'Good'
        elif self.final_score >= 75:
            return 'Acceptable'
        else:
            return 'Poor'
