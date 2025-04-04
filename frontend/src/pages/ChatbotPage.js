import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

const ChatbotPage = () => {
  const [userInput, setUserInput] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const location = useLocation();
  const { filename } = location.state || {};

  const handleSend = async () => {
    if (userInput.trim() === '') return;

    const newChatHistory = [...chatHistory, { sender: 'user', message: userInput }];
    setChatHistory(newChatHistory);
    setUserInput('');

    try {
      const response = await axios.post('http://localhost:8001/chat', {
        filename: filename,
        message: userInput,
      });

      setChatHistory([...newChatHistory, { sender: 'ai', message: response.data.response }]);
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-100 to-gray-200 p-6 flex flex-col items-center">
      <h1 className="text-4xl font-bold text-gray-800 mb-6">💬 Chat with Your Notes</h1>

      <div className="w-full max-w-3xl bg-white rounded-2xl shadow-lg p-6 flex flex-col">
        <div className="h-[500px] overflow-y-auto border border-gray-300 rounded-lg p-4 bg-gray-50 mb-4">
          {chatHistory.map((chat, index) => (
            <div
              key={index}
              className={`mb-3 max-w-[75%] px-4 py-2 rounded-xl text-sm leading-relaxed whitespace-pre-wrap ${
                chat.sender === 'user'
                  ? 'bg-blue-100 ml-auto text-right shadow border border-blue-200'
                  : 'bg-gray-200 mr-auto text-left shadow border border-gray-300'
              }`}
            >
              {chat.sender === 'ai' ? (
                <ReactMarkdown>{chat.message}</ReactMarkdown>
              ) : (
                chat.message
              )}
            </div>
          ))}
        </div>

        <div className="flex items-center">
          <input
            type="text"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Type your question here..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-l-xl focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <button
            onClick={handleSend}
            className="px-6 py-2 bg-blue-500 text-white font-medium rounded-r-xl hover:bg-blue-600 transition"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatbotPage;
