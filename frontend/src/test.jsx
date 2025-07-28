import React from 'react';
import ReactDOM from 'react-dom/client';

// Simple test component
function TestApp() {
  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h1>Test React App</h1>
      <p>If you can see this, React is working!</p>
    </div>
  );
}

// Try to render the test component
try {
  const root = ReactDOM.createRoot(document.getElementById('root'));
  root.render(<TestApp />);
  console.log('React app mounted successfully');
} catch (error) {
  console.error('Error mounting React app:', error);
}
