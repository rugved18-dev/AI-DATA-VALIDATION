import React, { useState } from 'react';

function FileUpload({ onUpload, loading, domain }) {
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onUpload(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      onUpload(e.target.files[0]);
    }
  };

  return (
    <div className="file-upload-container">
      <div
        className={`file-upload-area ${dragActive ? 'active' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <h2>📁 Upload CSV File</h2>
        <p>Drag and drop your CSV file here or click to select</p>
        
        <input
          type="file"
          id="file-input"
          accept=".csv,.txt"
          onChange={handleChange}
          disabled={loading}
          className="file-input"
        />
        
        <label htmlFor="file-input" className={`file-label ${loading ? 'loading' : ''}`}>
          {loading ? '⏳ Uploading...' : '📤 Choose File'}
        </label>
        
        <p className="file-info">Domain: <strong>{domain.charAt(0).toUpperCase() + domain.slice(1)}</strong></p>
      </div>
    </div>
  );
}

export default FileUpload;
