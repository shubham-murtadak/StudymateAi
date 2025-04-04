import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const UploadPDFPage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isUploaded, setIsUploaded] = useState(false);
  const navigate = useNavigate();

  const sanitizeFilename = (filename) => {
    return filename.replace(/[^\w\s]/gi, '').replace(/\s+/g, '');
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    setIsUploaded(false);
  };

  const handleUpload = () => {
    if (!selectedFile) {
      alert('Please select a PDF file first.');
      return;
    }

    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);

    axios.post('http://localhost:8001/upload/', formData)
      .then((response) => {
        console.log('File uploaded successfully:', response.data);
        setIsUploading(false);
        setIsUploaded(true);
      })
      .catch((error) => {
        console.error('Error uploading file:', error);
        setIsUploading(false);
        setIsUploaded(false);
      });
  };

  const handleNavigateToChatbot = () => {
    if (!isUploaded) {
      alert('Please upload a PDF file first.');
      return;
    }
    const sanitizedFilename = sanitizeFilename(selectedFile.name);
    navigate('/chatbot', { state: { filename: sanitizedFilename } });
  };

  const handleGenerateMCQ = () => {
    if (!isUploaded) {
      alert('Please upload a PDF file first.');
      return;
    }
    const sanitizedFilename = sanitizeFilename(selectedFile.name);
    navigate('/mcq', { state: { filename: sanitizedFilename } });
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-100 to-purple-200">
      {/* Navbar */}
      <nav className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-blue-600">📘 StudyMate AI</h1>
          <span className="text-sm text-gray-500">Your smart study buddy</span>
        </div>
      </nav>

      {/* Main Content */}
      <div className="flex-grow flex flex-col items-center justify-center p-6">
        <div className="bg-white shadow-xl rounded-2xl p-8 max-w-lg w-full">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-6">
            Upload Your Notes
          </h2>

          {/* Upload Box */}
          <div className="flex flex-col items-center p-6 border-2 border-dashed border-gray-400 rounded-lg w-full mb-6 bg-gray-50">
            <input
              type="file"
              accept="application/pdf"
              onChange={handleFileChange}
              className="hidden"
              id="fileInput"
            />
            <label htmlFor="fileInput" className="cursor-pointer flex flex-col items-center">
              <svg
                className="w-12 h-12 text-gray-400 mb-3"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 48 48"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M14 22v-6a8 8 0 0116 0v6m-4 0v-6a4 4 0 00-8 0v6m-4 0h16a4 4 0 014 4v8a4 4 0 01-4 4H14a4 4 0 01-4-4v-8a4-4 0 014-4z"
                />
              </svg>
              <span className="text-gray-600">
                Drag & Drop or <span className="text-blue-500 underline">browse</span>
              </span>
            </label>
            {selectedFile && (
              <span className="text-green-600 mt-2 text-sm font-medium">
                Selected: {selectedFile.name}
              </span>
            )}
          </div>

          {/* Uploading Spinner */}
          {isUploading && (
            <div className="flex justify-center mb-4">
              <div className="loader border-4 border-blue-300 border-t-blue-600 rounded-full w-8 h-8 animate-spin"></div>
            </div>
          )}

          {/* Upload Button */}
          <button
            onClick={handleUpload}
            className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition mb-4"
            disabled={isUploading}
          >
            {isUploading ? 'Uploading...' : 'Upload PDF'}
          </button>

          {/* Action Buttons */}
          <div className="flex justify-between space-x-4">
            <button
              onClick={handleGenerateMCQ}
              className="flex-1 py-3 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 transition"
              disabled={!isUploaded || isUploading}
            >
              Generate MCQ
            </button>
            <button
              onClick={handleNavigateToChatbot}
              className="flex-1 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition"
              disabled={!isUploaded || isUploading}
            >
              Ask a Question
            </button>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-white shadow-inner">
        <div className="max-w-7xl mx-auto px-4 py-4 text-center text-gray-600 text-sm">
          © {new Date().getFullYear()} StudyMate AI — Upload, Chat, and Learn Smarter ✨
        </div>
      </footer>
    </div>
  );
};

export default UploadPDFPage;
