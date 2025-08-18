import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import ChatPage from './pages/ChatPage';
import DocumentUploadPage from './pages/DocumentUploadPage';
import { useAuth, AuthProvider } from './contexts/AuthContext';
import './App.css';

const NavBar: React.FC = () => {
  const { isAuthenticated, logout } = useAuth();
  const location = useLocation();
  if (!isAuthenticated) return null;
  return (
    <nav className="navbar">
      <div className="navbar-links">
        <Link to="/chat" className={location.pathname === '/chat' ? 'active' : ''}>Chat</Link>
        <Link to="/upload" className={location.pathname === '/upload' ? 'active' : ''}>Upload</Link>
      </div>
      <button onClick={logout} className="logout-btn">Logout</button>
    </nav>
  );
};

const AppRoutes: React.FC = () => {
  const { isAuthenticated } = useAuth();

  return (
    <>
      <NavBar />
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/chat" element={isAuthenticated ? <ChatPage /> : <LoginPage />} />
        <Route path="/upload" element={isAuthenticated ? <DocumentUploadPage /> : <LoginPage />} />
      </Routes>
    </>
  );
};

const App: React.FC = () => {
  return (
    <AuthProvider>
      <Router>
        <AppRoutes />
      </Router>
    </AuthProvider>
  );
};

export default App;