import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import ChatPage from './pages/ChatPage';
import DocumentUploadPage from './pages/DocumentUploadPage';
import { useAuth } from './hooks/useAuth';
import './App.css';

const NavBar: React.FC = () => {
  const { isAuthenticated, logout } = useAuth();
  const location = useLocation();
  if (!isAuthenticated) return null;
  return (
    <nav className="navbar">
      <Link to="/chat" className={location.pathname === '/chat' ? 'active' : ''}>Chat</Link>
      <Link to="/upload" className={location.pathname === '/upload' ? 'active' : ''}>Upload</Link>
      <button onClick={logout} className="logout-btn">Logout</button>
    </nav>
  );
};

const App: React.FC = () => {
  const { isAuthenticated } = useAuth();

  return (
    <Router>
      <NavBar />
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route
          path="/chat"
          element={isAuthenticated ? <ChatPage /> : <LoginPage />}
        />
        <Route
          path="/upload"
          element={isAuthenticated ? <DocumentUploadPage /> : <LoginPage />}
        />
      </Routes>
    </Router>
  );
};

export default App;