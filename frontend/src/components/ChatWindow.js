import React, { useState, useEffect, useRef } from "react";
import "./ChatWindow.css";
import { getAIMessage } from "../api/api";
import { marked } from "marked";

function ChatWindow() {
  const defaultMessage = [{
    role: "assistant",
    content: "Hi! I'm here to help you find appliance parts. What can I help you with today?"
  }];

  const [messages, setMessages] = useState(defaultMessage);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (input.trim() !== "" && !isLoading) {
      const userMessage = input.trim();
      
      // Set user message
      setMessages(prevMessages => [...prevMessages, { role: "user", content: userMessage }]);
      setInput("");
      setIsLoading(true);

      try {
        // Call API & set assistant message
        const newMessage = await getAIMessage(userMessage);
        setMessages(prevMessages => [...prevMessages, newMessage]);
      } catch (error) {
        console.error('Error getting AI response:', error);
        setMessages(prevMessages => [...prevMessages, {
          role: "assistant",
          content: "I'm sorry, there was an error processing your request. Please try again."
        }]);
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="messages-container">
      {messages.map((message, index) => (
        <div key={index} className={`${message.role}-message-container`}>
          {message.content && (
            <div className={`message ${message.role}-message`}>
              <div 
                dangerouslySetInnerHTML={{
                  __html: marked(message.content).replace(/<p>|<\/p>/g, "")
                }}
              />
            </div>
          )}
        </div>
      ))}
      {isLoading && (
        <div className="assistant-message-container">
          <div className="message assistant-message loading">
            Thinking...
          </div>
        </div>
      )}
      <div ref={messagesEndRef} />
      <div className="input-area">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about appliance parts..."
          onKeyPress={handleKeyPress}
          disabled={isLoading}
        />
        <button 
          className="send-button" 
          onClick={handleSend}
          disabled={isLoading || input.trim() === ""}
        >
          {isLoading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default ChatWindow;
