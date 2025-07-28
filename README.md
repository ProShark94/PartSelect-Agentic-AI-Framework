PartSelect AI Assistant
======================

A smart chat system that helps customers find appliance parts and get repair help. Uses AI to answer questions about refrigerators, dishwashers, and other appliances.

## What It Does

- **Smart Answers**: Uses your custom training data to give expert repair advice
- **Part Search**: Finds the right parts for your appliance model
- **Installation Help**: Step-by-step repair instructions
- **Always Works**: Has backup responses when AI services are down

## Key Features

**Custom Training System**:
- 16 pre-built appliance troubleshooting examples
- Learns from your expertise to give better answers
- Easy to add new repair scenarios

**AI Integration**:
- Uses multiple AI services (OpenAI, Deepseek, HuggingFace)
- Falls back to your training data when needed
- Always gives helpful responses

**Professional Interface**:
- Clean chat interface built with React
- User accounts and secure login
- Works on desktop and mobile

## Quick Start

### 1. Setup Backend
```bash
cd "Agentic AI framework"
python -m venv venv
source venv/bin/activate
cd backend
pip install flask flask-cors transformers torch
python app.py
```

### 2. Setup Frontend
```bash
cd frontend
npm install
npm run dev
```

### 3. Open in Browser
Go to `http://localhost:5174` and start chatting!

## Test These Questions

Try these to see the training system work:
- "My refrigerator isn't cooling properly"
- "My dishwasher is not cleaning dishes properly"
- "Water is leaking from my refrigerator"
- "How often should I replace my water filter?"

## Add Your Own Training Data

1. Edit `backend/data/training_conversations.json`
2. Add your question and expert answer
3. Restart the backend
4. Test your new question

Example:
```json
{
  "input": "My dryer won't start",
  "output": "Check the lint filter, door latch, and power connection. The thermal fuse may also need replacement."
}
```

## How It Works

1. **You ask a question** → System checks your training data first
2. **Training match found** → Returns your expert answer
3. **No match** → Uses AI or gives professional fallback response
4. **Always helpful** → Never gives "I don't know" responses

## Files You Care About

- `backend/data/training_conversations.json` - Your training data
- `backend/app.py` - Main server
- `frontend/src/` - Chat interface
- `TRAINING_GUIDE.md` - How to add more training data

## API

**Chat Endpoint**: `POST /chat`
```json
{
  "message": "My fridge is warm",
  "session_id": "optional"
}
```

**Response**:
```json
{
  "response": "Check the condenser coils and temperature settings...",
  "agent": "smart_fallback"
}
```

That's it! Simple, smart, and always helpful.
