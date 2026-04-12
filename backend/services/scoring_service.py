"""
Scoring Service Module

Handles calculation of validation scores and data quality metrics.

Implements industry-standard data quality framework with three dimensions:
- Completeness: % of records with all required fields
- Validity: % of records matching validation rules
- Consistency: % of records following data patterns
"""


def calculate_score_percentage(valid_records, total_records):
    """
    Calculate the basic validation success percentage (LEGACY).
    
    Computes the percentage of valid records out of total records processed.
    Use calculate_weighted_score for comprehensive data quality assessment.
    
    Args:
        valid_records (int): Number of valid records
        total_records (int): Total number of records processed
        
    Returns:
        float: Percentage of valid records (0-100), rounded to 2 decimal places
        
    Example:
        >>> calculate_score_percentage(95, 100)
        95.0
    """
    if total_records == 0:
        return 0
    
    percentage = (valid_records / total_records * 100)
    return round(percentage, 2)


# ==================== DATA QUALITY DIMENSIONS ====================

def calculate_completeness_score(complete_records, total_records):
    """
    Calculate data completeness score.
    
    Measures percentage of records with all required fields populated.
    A complete record has no missing or null values in required fields.
    
    Use Case:
    - If CSV has 3 columns (age, income, credit_score) and a record missing
      income value, it's incomplete
    
    Args:
        complete_records (int): Records with all required fields present
        total_records (int): Total records processed
        
    Returns:
        float: Completeness score (0-100), rounded to 2 decimal places
        
    Example:
        >>> calculate_completeness_score(98, 100)
        98.0
    """
    if total_records == 0:
        return 0.0
    return round((complete_records / total_records) * 100, 2)


def calculate_validity_score(valid_records, total_records):
    """
    Calculate data validity score.
    
    Measures percentage of records that pass all domain-specific validation rules.
    A valid record has correct data types and values within acceptable ranges.
    
    Use Case:
    - Banking: age between 18-80, income > 0, credit_score 300-850
    - Healthcare: age between 0-120, blood_group is valid (A+, B-, etc.)
    - E-commerce: price > 0, stock >= 0
    
    Args:
        valid_records (int): Records passing domain validation rules
        total_records (int): Total records processed
        
    Returns:
        float: Validity score (0-100), rounded to 2 decimal places
        
    Example:
        >>> calculate_validity_score(95, 100)
        95.0
    """
    if total_records == 0:
        return 0.0
    return round((valid_records / total_records) * 100, 2)


def calculate_consistency_score(consistent_records, total_records):
    """
    Calculate data consistency score.
    
    Measures percentage of records that follow established data patterns
    and maintain logical relationships between fields.
    
    Examples of consistency checks:
    - If product price changes, verify consistency with historical patterns
    - If income value is unusually high/low compared to peers
    - If age values follow expected distribution patterns
    
    Args:
        consistent_records (int): Records following established patterns
        total_records (int): Total records processed
        
    Returns:
        float: Consistency score (0-100), rounded to 2 decimal places
        
    Example:
        >>> calculate_consistency_score(92, 100)
        92.0
    """
    if total_records == 0:
        return 0.0
    return round((consistent_records / total_records) * 100, 2)


# ==================== WEIGHTED DATA QUALITY SCORE ====================

def calculate_weighted_score(completeness, validity, consistency):
    """
    Calculate final weighted data quality score.
    
    Industry-Standard Formula:
        final_score = (
            0.4 * completeness +    # 40% - Data Presence
            0.4 * validity +        # 40% - Data Correctness
            0.2 * consistency       # 20% - Data Uniformity
        )
    
    Weight Justification:
    - Completeness (40%): Most critical - missing data is unusable
    - Validity (40%): Critical - incorrect data causes wrong decisions
    - Consistency (20%): Important - anomalies indicate problems but less critical
    
    Quality Ratings:
    - Score >= 95%: EXCELLENT - Production ready
    - Score >= 85%: GOOD - Minor issues only
    - Score >= 75%: ACCEPTABLE - Needs review before use
    - Score < 75%: POOR - Significant remediation required
    
    Args:
        completeness (float): Completeness score (0-100)
        validity (float): Validity score (0-100)
        consistency (float): Consistency score (0-100)
        
    Returns:
        float: Final weighted score (0-100), rounded to 2 decimal places
        
    Example:
        >>> calculate_weighted_score(98.5, 95.0, 92.0)
        95.8
        >>> score = calculate_weighted_score(completeness=100, validity=90, consistency=80)
        >>> print(f"Final Score: {score}%")
    """
    if completeness < 0 or validity < 0 or consistency < 0:
        return 0.0
    
    weighted_score = (
        0.4 * completeness +
        0.4 * validity +
        0.2 * consistency
    )
    
    # Cap at 100%
    return round(min(weighted_score, 100.0), 2)


def get_quality_rating(score):
    """
    Get human-readable quality rating from numerical score.
    
    Args:
        score (float): Final data quality score (0-100)
        
    Returns:
        dict: Contains rating and description
        
    Example:
        >>> rating = get_quality_rating(92.5)
        >>> print(rating['rating'])
        'Good'
        >>> print(rating['description'])
        'Minor issues detected. Suitable for use with caution.'
    """
    if score >= 95:
        return {
            'rating': 'Excellent',
            'description': 'Highest quality data. Production ready.',
            'action': 'Approve for use'
        }
    elif score >= 85:
        return {
            'rating': 'Good',
            'description': 'Minor issues detected. Suitable for use with caution.',
            'action': 'Review and approve with notes'
        }
    elif score >= 75:
        return {
            'rating': 'Acceptable',
            'description': 'Moderate issues found. Needs review before use.',
            'action': 'Remediate before use'
        }
    else:
        return {
            'rating': 'Poor',
            'description': 'Significant data quality issues. Not recommended for use.',
            'action': 'Major remediation required'
        }


# ==================== SCORE BREAKDOWN ====================

def get_score_breakdown(completeness, validity, consistency, final_score):
    """
    Generate detailed score breakdown for reporting and analysis.
    
    Useful for:
    - Data quality dashboards
    - Executive reporting
    - Identifying specific improvement areas
    - Tracking quality trends over time
    
    Args:
        completeness (float): Completeness score
        validity (float): Validity score
        consistency (float): Consistency score
        final_score (float): Final weighted score
        
    Returns:
        dict: Detailed breakdown with weights and contributions
    """
    return {
        'dimensions': {
            'completeness': {
                'score': completeness,
                'weight': 0.4,
                'contribution': round(completeness * 0.4, 2)
            },
            'validity': {
                'score': validity,
                'weight': 0.4,
                'contribution': round(validity * 0.4, 2)
            },
            'consistency': {
                'score': consistency,
                'weight': 0.2,
                'contribution': round(consistency * 0.2, 2)
            }
        },
        'final_score': final_score,
        'quality_rating': get_quality_rating(final_score)
    }
