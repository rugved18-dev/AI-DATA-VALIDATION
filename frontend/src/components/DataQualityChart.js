import React from 'react';
import {
  BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell
} from 'recharts';

function DataQualityChart({ result }) {
  // Data for quality dimensions chart
  const qualityData = [
    { name: 'Completeness', value: result.completeness_score },
    { name: 'Validity', value: result.validity_score },
    { name: 'Consistency', value: result.consistency_score }
  ];

  // Data for records distribution pie chart
  const recordsData = [
    { name: 'Valid', value: result.valid_records },
    { name: 'Invalid', value: result.invalid_records }
  ];

  const COLORS = ['#10B981', '#EF4444'];

  return (
    <div className="charts-section">
      <h2>📊 Data Quality Visualization</h2>
      
      <div className="charts-grid">
        {/* Quality Dimensions Bar Chart */}
        <div className="chart-container">
          <h3>Quality Dimensions</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={qualityData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis domain={[0, 100]} />
              <Tooltip formatter={(value) => `${value.toFixed(1)}%`} />
              <Bar dataKey="value" fill="#3B82F6" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Records Distribution Pie Chart */}
        <div className="chart-container">
          <h3>Records Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={recordsData}
                cx="50%"
                cy="50%"
                labelLine={true}
                label={({ name, value }) => `${name}: ${value}`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {recordsData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Score Gauge */}
      <div className="score-gauge">
        <h3>Final Quality Score</h3>
        <div className="gauge-container">
          <div className="gauge-value">{result.final_score}%</div>
          <div className="gauge-label">{result.quality_rating}</div>
          <div className="gauge-bar">
            <div
              className={`gauge-fill ${result.quality_rating.toLowerCase()}`}
              style={{ width: `${result.final_score}%` }}
            ></div>
          </div>
          <div className="gauge-range">
            <span>0%</span>
            <span>50%</span>
            <span>100%</span>
          </div>
        </div>
      </div>

      {/* Anomaly Score Stats */}
      <div className="anomaly-stats">
        <h3>Anomaly Detection</h3>
        <div className="stats-row">
          <div className="stat-item">
            <span className="stat-label">Anomalies Detected:</span>
            <span className="stat-value">{result.anomaly_count}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Anomaly Score:</span>
            <span className="stat-value">{result.anomaly_score}%</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Clean Records:</span>
            <span className="stat-value">{result.total_records - result.anomaly_count}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DataQualityChart;
