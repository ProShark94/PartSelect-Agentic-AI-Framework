import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { API_BASE_URL } from './config.js';
import './styles.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId] = useState('sess-' + Math.random().toString(36).substring(2, 10));
  const bottomRef = useRef(null);

  // Authentication state
  const [token, setToken] = useState(() => localStorage.getItem('authToken') || '');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [mode, setMode] = useState('login');

  // Attach token to axios default headers when it changes
  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }
  }, [token]);

  // Scroll to bottom when messages update
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed || !token) return;
    
    setMessages((msgs) => [...msgs, { role: 'user', content: trimmed }]);
    setLoading(true);
    setInput('');
    
    try {
      const response = await axios.post(`${API_BASE_URL}/chat`, {
        message: trimmed,
        session_id: sessionId,
      });
      const { response: answer } = response.data;
      setMessages((msgs) => [...msgs, { role: 'assistant', content: answer }]);
    } catch (err) {
      console.error('Chat error:', err);
      setMessages((msgs) => [
        ...msgs,
        { role: 'assistant', content: 'Sorry, an error occurred while processing your request.' },
      ]);
    } finally {
      setLoading(false);
    }
  };

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
      alert('Authentication failed: ' + (err.response?.data?.error || err.message));
    }
  };

  const handleLogout = () => {
    setToken('');
    localStorage.removeItem('authToken');
    setMessages([]);
    setUsername('');
    setPassword('');
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
        <button onClick={handleLogout} style={{ float: 'right', fontSize: '14px', padding: '5px 10px' }}>
          Logout
        </button>
      </header>
      <main className="chat-main">
        <div className="chat-window">
          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role}`}>
              <div className="message-content">
                {typeof msg.content === 'string' ? msg.content : JSON.stringify(msg.content)}
              </div>
            </div>
          ))}
          {loading && (
            <div className="message assistant loading">
              <span className="loader"></span>
              <span className="loading-text">Thinking...</span>
            </div>
          )}
          <div ref={bottomRef} />
        </div>
        <form className="chat-input-form" onSubmit={handleSubmit}>
          <input
            type="text"
            className="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about parts, compatibility, installation or orders..."
            aria-label="Chat input"
          />
          <button type="submit" className="chat-send-button" disabled={loading || !input.trim()}>
            Send
          </button>
        </form>
      </main>
    </div>
  );
}

export default App;
