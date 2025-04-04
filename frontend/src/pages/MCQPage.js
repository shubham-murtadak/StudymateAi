import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';

const MCQPage = () => {
  const [mcqs, setMcqs] = useState([]);
  const [selectedOptions, setSelectedOptions] = useState({});
  const [score, setScore] = useState(null);
  const location = useLocation();
  const { filename } = location.state || {};

  useEffect(() => {
    if (filename) {
      axios
        .post('http://localhost:8001/mcq', { collection_name: filename })
        .then(response => {
          if (Array.isArray(response.data.mcqs.mcqs)) {
            setMcqs(response.data.mcqs.mcqs);
          } else {
            console.error('Invalid MCQ data format:', response.data);
            setMcqs([]);
          }
        })
        .catch(error => {
          console.error('Error fetching MCQs:', error);
          setMcqs([]);
        });
    } else {
      console.error('Filename is missing in navigation state');
    }
  }, [filename]);

  const handleOptionChange = (questionIndex, option) => {
    setSelectedOptions(prev => ({
      ...prev,
      [questionIndex]: option,
    }));
  };

  const handleSubmit = () => {
    let newScore = 0;
    mcqs.forEach((mcq, index) => {
      if (selectedOptions[index] === mcq.correct_option) {
        newScore += 1;
      }
    });
    setScore(newScore);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-yellow-100 to-purple-200 p-6 flex flex-col items-center">
      <div className="bg-white shadow-2xl rounded-2xl p-8 max-w-3xl w-full">
        <h1 className="text-3xl font-extrabold text-center text-gray-800 mb-8">
          Multiple Choice Questions
        </h1>

        {mcqs.length === 0 ? (
          <p className="text-center text-gray-500">No MCQs available.</p>
        ) : (
          mcqs.map((mcq, index) => (
            <div key={index} className="mb-6 p-5 border rounded-xl shadow-md bg-gray-50">
              <p className="text-lg font-semibold text-gray-700 mb-3">{index + 1}. {mcq.question}</p>
              <div className="space-y-2">
                {mcq.options.map((option, optionIndex) => {
                  const isSelected = selectedOptions[index] === option;
                  const isCorrect = option === mcq.correct_option;
                  let optionClass =
                    'block p-3 rounded-md border transition-all duration-200 cursor-pointer';

                  if (score !== null) {
                    if (isCorrect) {
                      optionClass += ' bg-green-100 border-green-500 text-green-800 font-semibold';
                    } else if (isSelected && !isCorrect) {
                      optionClass += ' bg-red-100 border-red-500 text-red-800';
                    } else {
                      optionClass += ' bg-gray-100';
                    }
                  } else {
                    optionClass += ' hover:bg-blue-100 border-gray-300';
                  }

                  return (
                    <label key={optionIndex} className={optionClass}>
                      <input
                        type="radio"
                        name={`question-${index}`}
                        value={option}
                        checked={isSelected}
                        onChange={() => handleOptionChange(index, option)}
                        disabled={score !== null}
                        className="mr-2"
                      />
                      {option}
                    </label>
                  );
                })}
              </div>
            </div>
          ))
        )}

        {mcqs.length > 0 && (
          <button
            onClick={handleSubmit}
            disabled={Object.keys(selectedOptions).length !== mcqs.length}
            className={`w-full py-3 mt-6 text-white text-lg font-medium rounded-lg transition ${
              Object.keys(selectedOptions).length !== mcqs.length
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700'
            }`}
          >
            Submit
          </button>
        )}

        {score !== null && (
          <div className="mt-6 p-4 bg-green-100 border border-green-400 rounded-lg text-center">
            <p className="text-lg font-semibold text-green-800">
              Your Score: {score} / {mcqs.length}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default MCQPage;
