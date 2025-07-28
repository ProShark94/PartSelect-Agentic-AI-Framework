import React, { useState, useEffect } from "react";
import "./App.css";
import ChatWindow from "./components/ChatWindow";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({ username: '', password: '' });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    // Check if user is already authenticated
    const token = localStorage.getItem('authToken');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setError(''); // Clear error when user types
  };

  const handleAuth = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const endpoint = isLogin ? '/auth/login' : '/auth/register';
      const response = await fetch(`http://localhost:5001${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem('authToken', data.token);
        setIsAuthenticated(true);
        setFormData({ username: '', password: '' });
      } else {
        setError(data.error || 'Authentication failed');
      }
    } catch (error) {
      console.error('Auth error:', error);
      setError('Network error. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    setIsAuthenticated(false);
    setFormData({ username: '', password: '' });
  };

  if (!isAuthenticated) {
    return (
      <div className="App">
        <div className="heading">
          PartSelect Appliance Parts Assistant
        </div>
        <div className="auth-container">
          <form className="auth-form" onSubmit={handleAuth}>
            <h2>{isLogin ? 'Sign In' : 'Create Account'}</h2>
            
            {error && <div className="error-message">{error}</div>}
            
            <input
              type="text"
              name="username"
              placeholder="Username"
              value={formData.username}
              onChange={handleInputChange}
              required
              disabled={isLoading}
            />
            
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleInputChange}
              required
              disabled={isLoading}
            />
            
            <button type="submit" disabled={isLoading}>
              {isLoading ? '...' : (isLogin ? 'Sign In' : 'Create Account')}
            </button>
            
            <div className="auth-toggle">
              {isLogin ? "Don't have an account?" : "Already have an account?"}{' '}
              <button
                type="button"
                onClick={() => {
                  setIsLogin(!isLogin);
                  setError('');
                  setFormData({ username: '', password: '' });
                }}
                disabled={isLoading}
              >
                {isLogin ? 'Create Account' : 'Sign In'}
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <div className="heading">
        PartSelect Appliance Parts Assistant
        <button 
          onClick={handleLogout}
          style={{
            position: 'absolute',
            right: '20px',
            background: 'none',
            border: '1px solid #ddd',
            padding: '5px 10px',
            borderRadius: '5px',
            cursor: 'pointer',
            fontSize: '12px'
          }}
        >
          Logout
        </button>
      </div>
      <ChatWindow />
    </div>
  );
}

export default App;
