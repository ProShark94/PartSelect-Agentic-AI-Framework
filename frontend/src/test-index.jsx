import React from 'react';
import ReactDOM from 'react-dom/client';

// Minimal test component
function TestComponent() {
  return (
    <div style={{ padding: '20px', fontFamily: 'Arial', background: '#f0f0f0', minHeight: '100vh' }}>
      <h1 style={{ color: '#003366' }}>🎉 React is Working!</h1>
      <p>If you can see this message, React is successfully loading.</p>
      <div style={{ background: 'white', padding: '15px', borderRadius: '8px', marginTop: '20px' }}>
        <h3>Debug Info:</h3>
        <p>✅ React: Loaded</p>
        <p>✅ JavaScript: Working</p>
        <p>✅ Vite: Running</p>
        <p>🔄 Next: Load the full chat app</p>
      </div>
    </div>
  );
}

try {
  const root = ReactDOM.createRoot(document.getElementById('root'));
  root.render(<TestComponent />);
  console.log('✅ React app mounted successfully');
} catch (error) {
  console.error('❌ Error mounting React app:', error);
  // Fallback to plain HTML if React fails
  document.getElementById('root').innerHTML = `
    <div style="padding: 20px; font-family: Arial;">
      <h1 style="color: red;">React Loading Failed</h1>
      <p>Error: ${error.message}</p>
      <p>Check the browser console for more details.</p>
    </div>
  `;
}
