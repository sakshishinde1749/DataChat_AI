import React, { useState } from 'react';
import ChatInterface from './components/ChatInterface';
import UploadPrompt from './components/UploadPrompt';
import './App.css';
import axios from 'axios';

function App() {
  const [data, setData] = useState(null);
  const [fileType, setFileType] = useState(null);
  const [error, setError] = useState(null);

  const handleFileSelect = async (file, type) => {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const response = await axios.post(`http://127.0.0.1:5000/upload/${type}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        }
      });
      
      if (response.data.error) {
        throw new Error(response.data.error);
      }
      
      setData(response.data);
      setFileType(type);
      setError(null);
    } catch (error) {
      console.error('Error uploading file:', error);
      setError(error.response?.data?.error || error.message || 'Error uploading file');
      setData(null);
      setFileType(null);
    }
  };

  return (
    <div className="App">
      {!data ? (
        <UploadPrompt onFileSelect={handleFileSelect} error={error} />
      ) : (
        <ChatInterface data={data} fileType={fileType} />
      )}
    </div>
  );
}

export default App; 