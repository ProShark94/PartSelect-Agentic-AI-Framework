Setup Guide
===========

## What You're Building

A smart chat assistant that helps customers with appliance parts and repairs. It uses your expertise to give better answers than generic AI.

## Project Structure

```
Agentic AI framework/
├── backend/          # Server that handles chat requests
├── frontend/         # Web interface for users
├── venv/            # Python dependencies
└── data/            # Your training data
```

## Installation

### Requirements
- Python 3.12+
- Node.js 16+
- 2GB+ RAM

### Backend Setup
```bash
cd "Agentic AI framework"
python -m venv venv
source venv/bin/activate
cd backend
pip install flask flask-cors transformers torch scikit-learn PyJWT bcrypt
python app.py
```

Server runs at: `http://localhost:5001`

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Web interface at: `http://localhost:5174`

## How It Works

### 1. User Asks Question
Customer types: "My refrigerator isn't cooling"

### 2. System Finds Answer
- First checks your training data
- If match found, returns your expert answer
- Otherwise uses AI or professional fallback

### 3. Expert Response
Returns: "Check condenser coils, temperature settings, and door seals..."

## Key Components

### Training Data (`data/training_conversations.json`)
Your custom question-answer pairs that make the AI smarter.

### Smart Fallback (`agents/smart_fallback.py`)
Matches user questions to your training data using word similarity.

### Chat Interface (`frontend/src/`)
Clean React app where customers interact with the assistant.

### Main Server (`app.py`)
Handles web requests and coordinates everything.

## Features

**Always Helpful**: Never says "I don't know" - always provides useful guidance

**Custom Training**: Uses your 16 pre-built appliance examples + any you add

**Multiple AI Sources**: Falls back through OpenAI → Deepseek → HuggingFace → Your training data

**Professional Interface**: Clean chat with user accounts and message history

**Real-time**: Instant responses, auto-scrolling, loading indicators

## API Endpoints

### Chat
```
POST /chat
{
  "message": "My dishwasher won't start",
  "session_id": "optional"
}
```

### User Registration
```
POST /auth/register
{
  "username": "customer",
  "password": "password"
}
```

### Reset Chat
```
POST /reset
{
  "session_id": "abc123"
}
```

## Customization

### Add Training Data
1. Edit `backend/data/training_conversations.json`
2. Add your question and expert answer
3. Restart backend

### Modify Responses
- Edit `agents/smart_fallback.py` for fallback responses
- Modify similarity threshold for matching
- Add new appliance-specific terms

### UI Changes
- Edit React components in `frontend/src/components/`
- Modify styling and layout
- Add new features

## Environment Variables

Create `.env` file:
```
OPENAI_API_KEY=your_key_here
DEEPSEEK_API_KEY=your_key_here
JWT_SECRET_KEY=your_secret_here
```

## Troubleshooting

**Backend won't start**: Check Python version and dependencies
**Frontend won't load**: Run `npm install` and check Node.js version
**No training matches**: Check JSON syntax in training file
**API errors**: Verify environment variables

## Testing

Test these questions to verify training data works:
- "My refrigerator isn't cooling properly"
- "My dishwasher is not cleaning dishes properly"
- "Water is leaking from my refrigerator"

You should get specific, expert responses.

## Performance

- Response time: 0.1-2 seconds
- Memory usage: ~1GB
- Concurrent users: 10-50 (development mode)
- Training data: Instant loading

## Production Deployment

For production use:
1. Use gunicorn instead of Flask dev server
2. Add database for training data
3. Use Redis for session storage
4. Set up proper error logging
5. Use HTTPS and secure headers

Simple, effective, and ready to help your customers!
