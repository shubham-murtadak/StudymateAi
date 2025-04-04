import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import UploadPDFPage from './pages/UploadPDFPage';
import ChatbotPage from './pages/ChatbotPage';
import MCQPage from './pages/MCQPage';

const App = () => (
  <Router>
    <Routes>
      <Route path="/" element={<UploadPDFPage />} />
      <Route path="/chatbot" element={<ChatbotPage />} />
      <Route path="/mcq" element={<MCQPage />} />
    </Routes>
  </Router>
);

export default App;
