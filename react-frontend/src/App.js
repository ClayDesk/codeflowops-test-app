import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';

function Home() {
  return (
    <div className="page">
      <h1>🚀 CodeFlowOps Test App</h1>
      <p>This is a test React application for CodeFlowOps deployment testing.</p>
      <div className="features">
        <h2>✨ Features Being Tested:</h2>
        <ul>
          <li>React 18 with modern hooks</li>
          <li>React Router for navigation</li>
          <li>API integration with Axios</li>
          <li>Environment variable usage</li>
          <li>Production build optimization</li>
        </ul>
      </div>
    </div>
  );
}

function About() {
  const [apiStatus, setApiStatus] = React.useState('Checking...');

  React.useEffect(() => {
    // Test API connection
    const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
    fetch(`${apiUrl}/health`)
      .then(response => response.json())
      .then(data => setApiStatus('✅ Connected'))
      .catch(error => setApiStatus('❌ Disconnected'));
  }, []);

  return (
    <div className="page">
      <h1>📊 About This Test</h1>
      <div className="status">
        <h2>System Status:</h2>
        <p><strong>API Connection:</strong> {apiStatus}</p>
        <p><strong>Environment:</strong> {process.env.NODE_ENV}</p>
        <p><strong>Build Time:</strong> {new Date().toISOString()}</p>
      </div>
      <div className="tech-stack">
        <h2>🛠️ Tech Stack:</h2>
        <ul>
          <li>React 18.2.0</li>
          <li>React Router 6.8.0</li>
          <li>Axios for API calls</li>
          <li>CSS3 for styling</li>
        </ul>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar">
          <div className="nav-brand">
            <Link to="/">CodeFlowOps Test</Link>
          </div>
          <div className="nav-links">
            <Link to="/">Home</Link>
            <Link to="/about">About</Link>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </main>

        <footer className="footer">
          <p>© 2025 CodeFlowOps Test Application - Deployed with ❤️</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
