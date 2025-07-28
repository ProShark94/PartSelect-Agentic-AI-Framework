import React, { useState } from 'react';
import axios from 'axios';
import { API_BASE_URL } from './config.js';
import './styles.css';

function SimpleApp() {
  const [token, setToken] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [mode, setMode] = useState('login');

  const handleAuth = async (e) => {
    e.preventDefault();
    if (!username || !password) return;
    try {
      const endpoint = mode === 'login' ? '/auth/login' : '/auth/register';
      const resp = await axios.post(`${API_BASE_URL}${endpoint}`, { username, password });
      const { token: newToken } = resp.data;
      setToken(newToken);
      localStorage.setItem('authToken', newToken);
    } catch (err) {
      alert('Authentication failed: ' + err.message);
    }
  };

  // If not authenticated, show login/register form
  if (!token) {
    return (
      <div className="app-container">
        <header className="app-header">
          <h1>PartSelect Chat Assistant</h1>
        </header>
        <main className="chat-main" style={{ maxWidth: '400px' }}>
          <h2>{mode === 'login' ? 'Login' : 'Register'}</h2>
          <form onSubmit={handleAuth} className="auth-form">
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="chat-input"
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="chat-input"
              required
            />
            <button type="submit" className="chat-send-button">
              {mode === 'login' ? 'Login' : 'Register'}
            </button>
          </form>
          <p>
            {mode === 'login' ? 'Need an account?' : 'Already have an account?'}{' '}
            <button
              type="button"
              onClick={() => setMode(mode === 'login' ? 'register' : 'login')}
              className="link-button"
            >
              {mode === 'login' ? 'Register' : 'Login'}
            </button>
          </p>
        </main>
      </div>
    );
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>PartSelect Chat Assistant</h1>
        <p>Logged in successfully! (Full chat coming soon)</p>
      </header>
      <main className="chat-main">
        <p>Authentication successful! The chat interface would appear here.</p>
        <button onClick={() => {
          setToken('');
          localStorage.removeItem('authToken');
        }}>
          Logout
        </button>
      </main>
    </div>
  );
}

export default SimpleApp;
