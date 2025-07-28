// API integration for the PartSelect chat agent
export const getAIMessage = async (userQuery) => {
  try {
    // Get auth token from localStorage
    const token = localStorage.getItem('authToken');
    if (!token) {
      return {
        role: "assistant",
        content: "Please log in to continue using the chat."
      };
    }

    const response = await fetch('http://localhost:5001/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        message: userQuery
      })
    });

    if (!response.ok) {
      if (response.status === 401) {
        // Token expired or invalid
        localStorage.removeItem('authToken');
        return {
          role: "assistant",
          content: "Your session has expired. Please refresh the page and log in again."
        };
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    
    return {
      role: "assistant",
      content: data.response || "I'm sorry, I couldn't process your request at the moment."
    };
  } catch (error) {
    console.error('Error calling API:', error);
    return {
      role: "assistant",
      content: "I'm sorry, there was an error processing your request. Please try again."
    };
  }
};
