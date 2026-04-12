import React from 'react';

function DashboardCards({ result }) {
  const cards = [
    {
      title: 'Total Records',
      value: result.total_records,
      icon: '📊',
      color: '#3B82F6'
    },
    {
      title: 'Valid Records',
      value: result.valid_records,
      percentage: ((result.valid_records / result.total_records) * 100).toFixed(1) + '%',
      icon: '✅',
      color: '#10B981'
    },
    {
      title: 'Invalid Records',
      value: result.invalid_records,
      percentage: ((result.invalid_records / result.total_records) * 100).toFixed(1) + '%',
      icon: '❌',
      color: '#EF4444'
    },
    {
      title: 'Quality Score',
      value: result.final_score + '%',
      rating: result.quality_rating,
      icon: '⭐',
      color: '#F59E0B'
    },
    {
      title: 'Anomalies',
      value: result.anomaly_count,
      percentage: result.anomaly_score + '%',
      icon: '🔔',
      color: '#8B5CF6'
    }
  ];

  return (
    <div className="dashboard-cards">
      <h2>📈 Data Quality Metrics</h2>
      <div className="cards-grid">
        {cards.map((card, index) => (
          <div key={index} className="card" style={{ borderTop: `4px solid ${card.color}` }}>
            <div className="card-icon">{card.icon}</div>
            <div className="card-title">{card.title}</div>
            <div className="card-value">{card.value}</div>
            {card.percentage && <div className="card-percentage">{card.percentage}</div>}
            {card.rating && <div className="card-rating">{card.rating}</div>}
          </div>
        ))}
      </div>
    </div>
  );
}

export default DashboardCards;
