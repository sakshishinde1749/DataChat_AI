import React, { useState } from 'react';

function UploadPrompt({ onFileSelect, error: parentError }) {
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState(null);

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
    
    const file = e.dataTransfer.files[0];
    handleFile(file);
  };

  const handleFile = (file) => {
    setError(null);
    
    if (!file) return;

    const fileType = file.name.split('.').pop().toLowerCase();
    
    if (fileType === 'csv') {
      onFileSelect(file, 'csv');
    } else if (fileType === 'pdf') {
      onFileSelect(file, 'pdf');
    } else {
      setError('Please upload a CSV or PDF file');
    }
  };

  return (
    <div className="upload-prompt">
      <div className="upload-content">
        <h2>Welcome to DataChat AI</h2>
        <p>Upload your data file to start the analysis</p>
        
        <div className="upload-options">
          <div className="upload-option">
            <div className="option-icon">
              <svg viewBox="0 0 24 24" width="32" height="32">
                <path fill="currentColor" d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20M10,19L12,15H9V11H15V15L13,19H10Z" />
              </svg>
            </div>
            <h3>CSV File</h3>
            <p>Upload structured data in CSV format for detailed analysis</p>
            <div 
              className={`file-drop-zone ${dragActive ? 'active' : ''}`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <input
                type="file"
                accept=".csv"
                onChange={(e) => handleFile(e.target.files[0])}
                className="file-input"
              />
              <span>Drop your CSV file here or click to browse</span>
            </div>
          </div>
          
          <div className="upload-option">
            <div className="option-icon">
              <svg viewBox="0 0 24 24" width="32" height="32">
                <path fill="currentColor" d="M12,10.5H13V13.5H12V10.5M7,11.5H8V12.5H7V11.5M20,6V18A2,2 0 0,1 18,20H6A2,2 0 0,1 4,18V6A2,2 0 0,1 6,4H18A2,2 0 0,1 20,6M9.5,10.5A0.5,0.5 0 0,0 9,10H7A0.5,0.5 0 0,0 6.5,10.5V13.5A0.5,0.5 0 0,0 7,14H9A0.5,0.5 0 0,0 9.5,13.5V10.5M14.5,10.5A0.5,0.5 0 0,0 14,10H12A0.5,0.5 0 0,0 11.5,10.5V13.5A0.5,0.5 0 0,0 12,14H14A0.5,0.5 0 0,0 14.5,13.5V10.5M17.5,9H16V14H17.5V9Z" />
              </svg>
            </div>
            <h3>PDF File</h3>
            <p>Extract and analyze data from PDF documents</p>
            <div 
              className={`file-drop-zone ${dragActive ? 'active' : ''}`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <input
                type="file"
                accept=".pdf"
                onChange={(e) => handleFile(e.target.files[0])}
                className="file-input"
              />
              <span>Drop your PDF file here or click to browse</span>
            </div>
          </div>
        </div>

        {(error || parentError) && (
          <div className="upload-error">
            {error || parentError}
          </div>
        )}

        <div className="upload-info">
          <h4>Features</h4>
          <ul>
            <li>CSV Data Analysis</li>
            <li>PDF Text Extraction</li>
            <li>Natural Language Queries</li>
            <li>Smart Data Insights</li>
            <li>Interactive Visualizations</li>
            <li>Context-Aware Responses</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default UploadPrompt; 