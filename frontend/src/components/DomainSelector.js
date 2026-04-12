import React from 'react';

function DomainSelector({ selectedDomain, onSelectDomain }) {
  const domains = [
    { value: 'banking', label: '🏦 Banking', color: '#1E3A8A' },
    { value: 'healthcare', label: '🏥 Healthcare', color: '#DC2626' },
    { value: 'ecommerce', label: '🛒 E-commerce', color: '#059669' }
  ];

  return (
    <div className="domain-selector">
      <h2>Select Domain</h2>
      <div className="domain-buttons">
        {domains.map(domain => (
          <button
            key={domain.value}
            className={`domain-btn ${selectedDomain === domain.value ? 'active' : ''}`}
            onClick={() => onSelectDomain(domain.value)}
            style={{ borderColor: domain.color }}
          >
            {domain.label}
          </button>
        ))}
      </div>
    </div>
  );
}

export default DomainSelector;
