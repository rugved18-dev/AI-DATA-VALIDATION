"""
PHASE 5: Anomaly Detection Service

Detects statistical outliers and unusual patterns in data.
Identifies records that deviate significantly from expected ranges.
"""

def detect_anomalies_banking(record, statistics=None):
    """
    Detect anomalies in banking records.
    
    Identifies unusual patterns like:
    - Extremely high/low income
    - Unusual credit score patterns
    - Age outliers
    
    Args:
        record (dict): Banking record with age, income, credit_score
        statistics (dict): Optional statistical baseline
        
    Returns:
        list: List of anomaly messages
    """
    anomalies = []
    
    try:
        income = float(record.get('income', 0))
        age = int(record.get('age', 0))
        credit_score = int(record.get('credit_score', 0))
        
        # ===== INCOME ANOMALIES =====
        # Flag unusually high income
        if income > 10000000:
            anomalies.append(f"⚠️ ANOMALY: Unusually high income (${income:,.0f})")
        elif income > 1000000:
            anomalies.append(f"🔔 ALERT: Very high income (${income:,.0f})")
        
        # Flag unusually low income
        elif income < 20000:
            anomalies.append(f"🔔 ALERT: Very low income (${income:,.0f})")
        
        # ===== AGE ANOMALIES =====
        if age > 75:
            anomalies.append(f"🔔 ALERT: Senior age ({age} years)")
        elif age < 25:
            anomalies.append(f"🔔 ALERT: Young customer ({age} years)")
        
        # ===== CREDIT SCORE ANOMALIES =====
        if credit_score > 800:
            anomalies.append(f"✨ EXCELLENT: Outstanding credit ({credit_score})")
        elif credit_score < 350:
            anomalies.append(f"⚠️ ANOMALY: Poor credit score ({credit_score})")
        
        # ===== INCOME-CREDIT CORRELATION =====
        # Unusual pattern: Very high income but low credit score
        if income > 500000 and credit_score < 600:
            anomalies.append("⚠️ ANOMALY: High income but low credit (mismatch)")
        
        # Very low income but excellent credit score
        elif income < 50000 and credit_score > 750:
            anomalies.append("⚠️ ANOMALY: Low income but excellent credit (unusual)")
        
    except (ValueError, TypeError):
        pass
    
    return anomalies


def detect_anomalies_healthcare(record, statistics=None):
    """
    Detect anomalies in healthcare records.
    
    Args:
        record (dict): Healthcare record with age, blood_group
        statistics (dict): Optional statistical baseline
        
    Returns:
        list: List of anomaly messages
    """
    anomalies = []
    
    try:
        age = int(record.get('age', 0))
        blood_group = str(record.get('blood_group', '')).upper().strip()
        
        # ===== AGE ANOMALIES =====
        if age > 110:
            anomalies.append(f"⚠️ ANOMALY: Extremely old age ({age} years)")
        elif age > 100:
            anomalies.append(f"✨ NOTABLE: Centenarian patient ({age} years)")
        
        if age < 1:
            anomalies.append(f"🔔 ALERT: Infant patient (age: {age})")
        
        # ===== BLOOD GROUP PATTERNS =====
        # Note: Blood group distributions vary by population
        rare_groups = ['AB-', 'AB+']
        if blood_group in rare_groups:
            anomalies.append(f"🔔 NOTE: Rare blood group ({blood_group})")
        
    except (ValueError, TypeError):
        pass
    
    return anomalies


def detect_anomalies_ecommerce(record, statistics=None):
    """
    Detect anomalies in e-commerce records.
    
    Args:
        record (dict): E-commerce record with price, stock
        statistics (dict): Optional statistical baseline
        
    Returns:
        list: List of anomaly messages
    """
    anomalies = []
    
    try:
        price = float(record.get('price', 0))
        stock = int(record.get('stock', 0))
        
        # ===== PRICE ANOMALIES =====
        if price > 100000:
            anomalies.append(f"⚠️ ANOMALY: Extremely high price (${price:,.2f})")
        elif price > 10000:
            anomalies.append(f"🔔 ALERT: High-value item (${price:,.2f})")
        
        if price < 0.01:
            anomalies.append(f"⚠️ ANOMALY: Suspiciously low price (${price:.4f})")
        elif price < 1:
            anomalies.append(f"🔔 ALERT: Very low-priced item (${price:.2f})")
        
        # ===== STOCK ANOMALIES =====
        if stock > 1000000:
            anomalies.append(f"⚠️ ANOMALY: Excessive stock ({stock:,} units)")
        elif stock > 100000:
            anomalies.append(f"🔔 ALERT: Very high stock ({stock:,} units)")
        
        if stock == 0:
            anomalies.append("🔔 NOTE: Out of stock")
        
        # ===== PRICE-STOCK CORRELATION =====
        # Unusual: Premium product with massive stock
        if price > 5000 and stock > 50000:
            anomalies.append("⚠️ ANOMALY: Premium item with excessive stock")
        
        # Budget item with very low stock
        if price < 10 and stock < 5:
            anomalies.append("⚠️ ANOMALY: Budget item with critical low stock")
        
    except (ValueError, TypeError):
        pass
    
    return anomalies


def calculate_anomaly_score(anomalies_count, total_records):
    """
    Calculate percentage of records with anomalies.
    
    Args:
        anomalies_count (int): Number of records with anomalies
        total_records (int): Total records processed
        
    Returns:
        float: Percentage of anomalous records (0-100)
    """
    if total_records == 0:
        return 0.0
    return round((anomalies_count / total_records) * 100, 2)


def get_anomaly_severity(anomaly_text):
    """
    Classify anomaly severity based on text.
    
    Args:
        anomaly_text (str): Anomaly message
        
    Returns:
        str: One of: 'HIGH', 'MEDIUM', 'LOW', 'INFO'
    """
    if '⚠️ ANOMALY' in anomaly_text or 'UNUSUALLY' in anomaly_text.upper():
        return 'HIGH'
    elif '🔔 ALERT' in anomaly_text:
        return 'MEDIUM'
    elif '✨' in anomaly_text:
        return 'INFO'
    else:
        return 'LOW'
