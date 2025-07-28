/**
 * Chat Window Component
 * 
 * Renders the main chat interface displaying message history and loading states.
 * Manages automatic scrolling and visual feedback for user interactions.
 */

import React from 'react';
import Message from './Message.jsx';
import './ChatWindow.css';

function ChatWindow({ messages, loading, bottomRef }) {
  return (
    <div className="chat-window">
      {messages.map((msg, idx) => (
        <Message key={idx} role={msg.role} content={msg.content} />
      ))}
      {loading && (
        <div className="message assistant loading">
          <span className="loader"></span>
          <span className="loading-text">Thinking...</span>
        </div>
      )}
      <div ref={bottomRef} />
    </div>
  );
}

export default ChatWindow;