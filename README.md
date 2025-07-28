PartSelect AI Assistant
======================

Smart AI-powered chat system for appliance troubleshooting and parts support. Uses custom training data to provide expert repair advice.

## Features

- **Expert Responses**: Uses your training data for accurate appliance troubleshooting
- **Multi-Agent AI**: OpenAI, Deepseek, and HuggingFace integration with smart fallbacks
- **Professional UI**: React frontend with authentication and responsive design
- **Always Available**: Works even when external AI services are down

## Quick Start

1. **Setup Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
   ```

2. **Setup Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Open**: http://localhost:5174

## Training Data

The system includes 16 expert appliance troubleshooting examples. Add your own training data to improve responses.

## Documentation

See `GUIDE.md` for complete setup instructions and training data management.

## Architecture

- **Backend**: Flask API with multiple AI agents
- **Frontend**: React with Vite and professional chat interface  
- **Training**: Smart similarity matching with fallback responses
- **Authentication**: JWT-based user management

## Test These Questions

Try these to see the training system work:
- "My refrigerator isn't cooling properly"
- "My dishwasher is not cleaning dishes properly"

