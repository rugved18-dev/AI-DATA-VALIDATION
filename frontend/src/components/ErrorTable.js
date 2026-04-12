import React, { useState } from 'react';

function ErrorTable({ errors }) {
  const [expandedIndex, setExpandedIndex] = useState(null);

  // Parse errors to extract row number and message
  const parsedErrors = errors.map((error, index) => {
    const match = error.match(/Row (\d+): (.*)/);
    if (match) {
      return {
        id: index,
        row: match[1],
        message: match[2],
        severity: determineSeverity(match[2])
      };
    }
    return {
      id: index,
      row: 'N/A',
      message: error,
      severity: 'warning'
    };
  });

  function determineSeverity(message) {
    if (message.toLowerCase().includes('invalid')) return 'error';
    if (message.toLowerCase().includes('missing')) return 'warning';
    return 'info';
  }

  const getSeverityIcon = (severity) => {
    switch(severity) {
      case 'error': return '❌';
      case 'warning': return '⚠️';
      default: return 'ℹ️';
    }
  };

  return (
    <div className="error-table-section">
      <h2>📋 Validation Errors ({errors.length})</h2>
      
      <div className="error-table-wrapper">
        <table className="error-table">
          <thead>
            <tr>
              <th>Row</th>
              <th>Severity</th>
              <th>Error Message</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {parsedErrors.map((error, index) => (
              <tr
                key={error.id}
                className={`error-row ${error.severity}`}
                onClick={() => setExpandedIndex(expandedIndex === index ? null : index)}
              >
                <td className="row-number">{error.row}</td>
                <td className="severity">
                  <span className="severity-badge">{getSeverityIcon(error.severity)}</span>
                </td>
                <td className="message">{error.message}</td>
                <td className="action">
                  <button className="expand-btn">
                    {expandedIndex === index ? '−' : '+'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="error-summary">
        <p>📌 Tip: Review errors above to improve data quality and increase validation scores.</p>
      </div>
    </div>
  );
}

export default ErrorTable;
