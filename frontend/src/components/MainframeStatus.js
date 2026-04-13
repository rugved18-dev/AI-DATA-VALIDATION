import React from 'react';

function MainframeStatus({ mainframeProcessing }) {
  if (!mainframeProcessing) {
    return null;
  }

  const { attempted, result, error } = mainframeProcessing;

  if (!attempted) {
    return (
      <div className="mainframe-section">
        <h2>⚙️ Mainframe Integration Status</h2>
        <div className="mainframe-card mainframe-disabled">
          <div className="mainframe-icon">⊘</div>
          <div className="mainframe-status-badge disabled">DISABLED</div>
          <div className="mainframe-message">Mainframe processing is disabled</div>
        </div>
      </div>
    );
  }

  if (error && !result) {
    return (
      <div className="mainframe-section">
        <h2>⚙️ Mainframe Integration Status</h2>
        <div className="mainframe-card mainframe-error">
          <div className="mainframe-icon">❌</div>
          <div className="mainframe-status-badge error">ERROR</div>
          <div className="mainframe-message">{error}</div>
          <div className="mainframe-note">
            The mainframe validation encountered an error, but Python validation results are available above.
          </div>
        </div>
      </div>
    );
  }

  if (result) {
    const { status, message, processed_records, valid_records, invalid_records, job_id, execution_time_ms, mainframe_status } = result;

    // Determine visual indicators based on status
    const getStatusColor = () => {
      switch (status) {
        case 'success':
          return 'success';
        case 'partial':
          return 'warning';
        case 'failed':
          return 'error';
        default:
          return 'info';
      }
    };

    const getStatusIcon = () => {
      switch (status) {
        case 'success':
          return '✅';
        case 'partial':
          return '⚠️';
        case 'failed':
          return '❌';
        default:
          return 'ℹ️';
      }
    };

    const statusColor = getStatusColor();
    const statusIcon = getStatusIcon();

    return (
      <div className="mainframe-section">
        <h2>⚙️ Mainframe Integration Status</h2>
        <div className={`mainframe-card mainframe-${statusColor}`}>
          {/* Header */}
          <div className="mainframe-header">
            <div className="mainframe-icon">{statusIcon}</div>
            <div className="mainframe-header-content">
              <div className={`mainframe-status-badge ${statusColor}`}>
                {status.toUpperCase()}
              </div>
              <div className="mainframe-message">{message}</div>
            </div>
          </div>

          {/* Main Metrics */}
          <div className="mainframe-metrics">
            <div className="mainframe-metric">
              <span className="metric-label">Processed Records:</span>
              <span className="metric-value">{processed_records}</span>
            </div>
            <div className="mainframe-metric">
              <span className="metric-label">Valid:</span>
              <span className="metric-value valid">{valid_records}</span>
            </div>
            <div className="mainframe-metric">
              <span className="metric-label">Invalid:</span>
              <span className="metric-value invalid">{invalid_records}</span>
            </div>
            <div className="mainframe-metric">
              <span className="metric-label">Execution Time:</span>
              <span className="metric-value">{execution_time_ms}ms</span>
            </div>
          </div>

          {/* Details Grid */}
          <div className="mainframe-details">
            <div className="detail-item">
              <span className="detail-label">Job ID</span>
              <code className="detail-value">{job_id}</code>
            </div>
            <div className="detail-item">
              <span className="detail-label">Status</span>
              <span className="detail-value">{mainframe_status}</span>
            </div>
          </div>

          {/* Progress Bar */}
          <div className="mainframe-progress">
            <div className="progress-label">Record Validity Distribution</div>
            <div className="progress-bar-container">
              <div
                className="progress-bar-valid"
                style={{
                  width: processed_records > 0 ? `${(valid_records / processed_records) * 100}%` : '0%'
                }}
              >
                {processed_records > 0 && `${((valid_records / processed_records) * 100).toFixed(1)}%`}
              </div>
            </div>
            <div className="progress-legend">
              <span className="legend-item valid-item">Valid Records</span>
              <span className="legend-item invalid-item">Invalid Records</span>
            </div>
          </div>

          {/* Error List (if any) */}
          {result.errors && result.errors.length > 0 && (
            <div className="mainframe-errors">
              <div className="errors-title">Mainframe Errors:</div>
              <ul className="errors-list">
                {result.errors.map((err, idx) => (
                  <li key={idx} className="error-item">
                    {err}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    );
  }

  return null;
}

export default MainframeStatus;
