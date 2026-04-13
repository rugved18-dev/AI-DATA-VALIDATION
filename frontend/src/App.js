import React, { useState } from 'react';
import './App.css';
import DomainSelector from './components/DomainSelector';
import FileUpload from './components/FileUpload';
import DashboardCards from './components/DashboardCards';
import DataQualityChart from './components/DataQualityChart';
import ErrorTable from './components/ErrorTable';
import AnomalyList from './components/AnomalyList';
import MainframeStatus from './components/MainframeStatus';

function App() {
  const [selectedDomain, setSelectedDomain] = useState('banking');
  const [validationResult, setValidationResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileUpload = async (file) => {
    setLoading(true);
    setError(null);
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('domain', selectedDomain);

    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      const data = await response.json();
      setValidationResult(data);
    } catch (err) {
      setError(err.message || 'Error uploading file');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🏢 Enterprise Data Quality Assessment System</h1>
        <p>Multi-Domain Validation with Anomaly Detection</p>
      </header>

      <div className="App-container">
        {/* Domain Selector */}
        <DomainSelector selectedDomain={selectedDomain} onSelectDomain={setSelectedDomain} />

        {/* File Upload */}
        <FileUpload onUpload={handleFileUpload} loading={loading} domain={selectedDomain} />

        {/* Error Messages */}
        {error && <div className="error-message">❌ {error}</div>}

        {/* Results Section */}
        {validationResult && (
          <div className="results-section">
            {/* Dashboard Cards */}
            <DashboardCards result={validationResult} />

            {/* Mainframe Integration Status */}
            <MainframeStatus mainframeProcessing={validationResult.mainframe_processing} />

            {/* Data Quality Charts */}
            <DataQualityChart result={validationResult} />

            {/* Error Table */}
            {validationResult.errors && validationResult.errors.length > 0 && (
              <ErrorTable errors={validationResult.errors} />
            )}

            {/* Anomalies List */}
            {validationResult.anomalies && validationResult.anomalies.length > 0 && (
              <AnomalyList anomalies={validationResult.anomalies} />
            )}
          </div>
        )}

        {/* Info Message */}
        {!validationResult && (
          <div className="info-message">
            📊 Select a domain, upload a CSV file, and analyze your data quality
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
