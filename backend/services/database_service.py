"""
Database Service Module

Handles persistent storage of validation results using SQLite.

This module provides database operations for:
- Creating and managing database schema
- Storing validation results with data quality metrics
- Querying historical validation data
- Generating audit trails

Database Options:
- SQLite (default): Built-in, no external setup required
- MySQL: Uncomment and configure for production
- PostgreSQL: Uncomment and configure for cloud deployment
"""

import sqlite3
import json
from datetime import datetime
import os

# ==================== DATABASE CONFIGURATION ====================

# Default SQLite database
DB_FILE = 'validation_results.db'

# For production, you can switch to MySQL or PostgreSQL
# DB_TYPE = os.getenv('DB_TYPE', 'sqlite')  # sqlite, mysql, postgresql


# ==================== DATABASE INITIALIZATION ====================

def get_db_connection():
    """
    Get SQLite database connection.
    
    Returns:
        sqlite3.Connection: Database connection with row factory
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """
    Initialize database schema.
    
    Creates validation_results table if it doesn't exist.
    This table stores all validation results with data quality metrics.
    
    Schema:
    - id: Auto-incrementing primary key
    - timestamp: When validation was performed
    - domain: Banking, Healthcare, or E-commerce
    - filename: Original uploaded file name
    - total_records: Total records processed
    - valid_records: Records that passed validation
    - invalid_records: Records that failed validation
    - completeness_score: Data completeness percentage (0-100)
    - validity_score: Data validity percentage (0-100)
    - consistency_score: Data consistency percentage (0-100)
    - final_score: Weighted final score (0-100)
    - errors: JSON array of validation error messages
    - anomaly_count: Number of records with anomalies (PHASE 5)
    - anomaly_score: Percentage of records with anomalies (PHASE 5)
    - anomalies: JSON array of detected anomalies (PHASE 5)
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Drop existing table for development (remove in production)
    # cursor.execute('DROP TABLE IF EXISTS validation_results')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS validation_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            domain TEXT NOT NULL,
            filename TEXT NOT NULL,
            total_records INTEGER NOT NULL,
            valid_records INTEGER NOT NULL,
            invalid_records INTEGER NOT NULL,
            completeness_score REAL NOT NULL,
            validity_score REAL NOT NULL,
            consistency_score REAL NOT NULL,
            final_score REAL NOT NULL,
            errors TEXT NOT NULL,
            anomaly_count INTEGER DEFAULT 0,
            anomaly_score REAL DEFAULT 0.0,
            anomalies TEXT DEFAULT '[]',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()


# ==================== DATA STORAGE OPERATIONS ====================

def store_validation_result(validation_result, domain, filename):
    """
    Store validation result in database.
    
    Persists the validation result with all data quality metrics to the database
    for future analysis and audit trails.
    
    Args:
        validation_result (ValidationResult): Result object containing:
            - total_records, valid_records, invalid_records
            - completeness_score, validity_score, consistency_score
            - final_score, errors
        domain (str): Validation domain (banking, healthcare, ecommerce)
        filename (str): Original filename that was validated
        
    Returns:
        int: Database record ID if successful, None if failed
        
    Example:
        >>> result = validate_data('file.csv', 'banking')
        >>> record_id = store_validation_result(result, 'banking', 'file.csv')
        >>> print(f"Stored as record {record_id}")
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        errors_json = json.dumps(validation_result.errors)
        anomalies_json = json.dumps(validation_result.anomalies)  # PHASE 5
        
        cursor.execute('''
            INSERT INTO validation_results (
                timestamp,
                domain,
                filename,
                total_records,
                valid_records,
                invalid_records,
                completeness_score,
                validity_score,
                consistency_score,
                final_score,
                errors,
                anomaly_count,
                anomaly_score,
                anomalies
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            timestamp,
            domain,
            filename,
            validation_result.total_records,
            validation_result.valid_records,
            validation_result.invalid_records,
            validation_result.completeness_score,
            validation_result.validity_score,
            validation_result.consistency_score,
            validation_result.final_score,
            errors_json,
            validation_result.anomaly_count,  # PHASE 5
            validation_result.anomaly_score,  # PHASE 5
            anomalies_json  # PHASE 5
        ))
        
        conn.commit()
        record_id = cursor.lastrowid
        conn.close()
        
        return record_id
    
    except Exception as e:
        print(f"Error storing validation result: {str(e)}")
        return None


# ==================== DATA RETRIEVAL OPERATIONS ====================

def get_validation_result(record_id):
    """
    Retrieve a specific validation result from database.
    
    Args:
        record_id (int): ID of the validation result record
        
    Returns:
        dict: Validation result record, or None if not found
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM validation_results WHERE id = ?
        ''', (record_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    except Exception as e:
        print(f"Error retrieving validation result: {str(e)}")
        return None


def get_domain_statistics(domain):
    """
    Get aggregated statistics for a specific domain.
    
    Useful for understanding overall data quality trends for a domain.
    
    Args:
        domain (str): Domain name (banking, healthcare, ecommerce)
        
    Returns:
        dict: Statistics including average scores, total validations, etc.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total_validations,
                ROUND(AVG(final_score), 2) as avg_final_score,
                ROUND(AVG(completeness_score), 2) as avg_completeness,
                ROUND(AVG(validity_score), 2) as avg_validity,
                ROUND(AVG(consistency_score), 2) as avg_consistency,
                MAX(final_score) as best_score,
                MIN(final_score) as worst_score
            FROM validation_results
            WHERE domain = ?
        ''', (domain.lower(),))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    except Exception as e:
        print(f"Error retrieving domain statistics: {str(e)}")
        return None


def get_recent_validations(limit=10):
    """
    Retrieve most recent validation results.
    
    Args:
        limit (int): Maximum number of records to return (default: 10)
        
    Returns:
        list: List of recent validation results
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, timestamp, domain, filename, final_score, 
                   total_records, valid_records
            FROM validation_results
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    except Exception as e:
        print(f"Error retrieving recent validations: {str(e)}")
        return []


def export_validation_data(domain=None, format='json'):
    """
    Export validation data for reporting or analysis.
    
    Args:
        domain (str): Optional domain filter
        format (str): Output format ('json' or 'csv')
        
    Returns:
        str: Exported data in specified format
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if domain:
            cursor.execute('''
                SELECT * FROM validation_results WHERE domain = ?
                ORDER BY timestamp DESC
            ''', (domain.lower(),))
        else:
            cursor.execute('''
                SELECT * FROM validation_results ORDER BY timestamp DESC
            ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        if format == 'json':
            data = [dict(row) for row in rows]
            return json.dumps(data, indent=2, default=str)
        
        elif format == 'csv':
            import csv
            from io import StringIO
            
            if not rows:
                return ''
            
            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=dict(rows[0]).keys())
            writer.writeheader()
            for row in rows:
                writer.writerow(dict(row))
            return output.getvalue()
        
        return json.dumps([dict(row) for row in rows], default=str)
    
    except Exception as e:
        print(f"Error exporting validation data: {str(e)}")
        return json.dumps([])


# ==================== DATABASE MAINTENANCE ====================

def clear_old_results(days=30):
    """
    Remove validation results older than specified days.
    
    Useful for database cleanup and maintenance.
    
    Args:
        days (int): Number of days to retain (default: 30)
        
    Returns:
        int: Number of records deleted
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cutoff_date = datetime.now().isoformat()
        
        cursor.execute('''
            DELETE FROM validation_results 
            WHERE datetime(created_at) < datetime('now', '-' || ? || ' days')
        ''', (days,))
        
        conn.commit()
        deleted_count = cursor.rowcount
        conn.close()
        
        return deleted_count
    
    except Exception as e:
        print(f"Error clearing old results: {str(e)}")
        return 0


def get_database_stats():
    """
    Get overall database statistics.
    
    Returns:
        dict: Database statistics
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as total_records FROM validation_results')
        total = cursor.fetchone()['total_records']
        
        cursor.execute('''
            SELECT domain, COUNT(*) as count 
            FROM validation_results 
            GROUP BY domain
        ''')
        by_domain = {row['domain']: row['count'] for row in cursor.fetchall()}
        
        cursor.execute('SELECT AVG(final_score) as avg_score FROM validation_results')
        avg_score = cursor.fetchone()['avg_score']
        
        conn.close()
        
        return {
            'total_records': total,
            'by_domain': by_domain,
            'average_final_score': round(avg_score, 2) if avg_score else 0,
            'database_file': DB_FILE
        }
    
    except Exception as e:
        print(f"Error getting database stats: {str(e)}")
        return {}


# Initialize database on module import
if not os.path.exists(DB_FILE):
    init_database()
