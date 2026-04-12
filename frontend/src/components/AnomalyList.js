import React from 'react';

function AnomalyList({ anomalies }) {
  const getAnomalySeverity = (anomaly) => {
    if (anomaly.includes('ALERT:') || anomaly.includes('🔴')) return 'high';
    if (anomaly.includes('ANOMALY:') || anomaly.includes('⚠️')) return 'medium';
    if (anomaly.includes('EXCELLENT') || anomaly.includes('✨')) return 'info';
    return 'low';
  };

  const getSeverityColor = (severity) => {
    switch(severity) {
      case 'high': return '#DC2626';
      case 'medium': return '#F59E0B';
      case 'info': return '#3B82F6';
      default: return '#6B7280';
    }
  };

  const getSeverityLabel = (severity) => {
    switch(severity) {
      case 'high': return 'HIGH';
      case 'medium': return 'MEDIUM';
      case 'info': return 'INFO';
      default: return 'LOW';
    }
  };

  return (
    <div className="anomaly-section">
      <h2>🔔 Detected Anomalies ({anomalies.length})</h2>
      
      <div className="anomaly-list">
        {anomalies.map((anomaly, index) => {
          const severity = getAnomalySeverity(anomaly);
          const color = getSeverityColor(severity);
          const label = getSeverityLabel(severity);

          return (
            <div
              key={index}
              className={`anomaly-item ${severity}`}
              style={{ borderLeft: `4px solid ${color}` }}
            >
              <div className="anomaly-header">
                <span className="anomaly-severity" style={{ backgroundColor: color }}>
                  {label}
                </span>
                <span className="anomaly-index">#{index + 1}</span>
              </div>
              <div className="anomaly-content">
                <p className="anomaly-text">{anomaly}</p>
              </div>
            </div>
          );
        })}
      </div>

      <div className="anomaly-summary">
        <div className="summary-stat">
          <span className="label">HIGH Severity:</span>
          <span className="value">{anomalies.filter(a => getAnomalySeverity(a) === 'high').length}</span>
        </div>
        <div className="summary-stat">
          <span className="label">MEDIUM Severity:</span>
          <span className="value">{anomalies.filter(a => getAnomalySeverity(a) === 'medium').length}</span>
        </div>
        <div className="summary-stat">
          <span className="label">INFO:</span>
          <span className="value">{anomalies.filter(a => getAnomalySeverity(a) === 'info').length}</span>
        </div>
      </div>

      <div className="anomaly-tip">
        <p>💡 Anomalies are statistical outliers. They don't cause validation to fail but indicate unusual patterns worth investigating.</p>
      </div>
    </div>
  );
}

export default AnomalyList;
