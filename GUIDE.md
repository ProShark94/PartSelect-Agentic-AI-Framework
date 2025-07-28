Complete Guide 
==============

## Core Idea

A smart AI assistant that helps customers with appliance parts and repairs. Uses your expertise to give better answers than generic AI.

## Quick Setup

### 1. Backend Setup
```bash
cd "Agentic AI framework"
python -m venv venv
source venv/bin/activate
cd backend
pip install -r requirements.txt
python app.py
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 3. Open Browser
Go to `http://localhost:5174` and start chatting!

## Training Data

Training data teaches your AI assistant how to answer questions. Instead of generic responses, it gives expert advice based on your knowledge.

## Current Training Data

Your system has 16 pre-built examples for:
- Refrigerator problems (cooling, leaking, lights)
- Dishwasher issues (cleaning, drainage)
- Water filter replacement
- General appliance troubleshooting

## Test Current Training

Try these questions to see it work:
- "My refrigerator isn't cooling properly"
- "My dishwasher is not cleaning dishes properly" 
- "Water is leaking from my refrigerator"
- "How often should I replace my water filter?"

You should get specific, expert answers instead of generic responses.

## Add New Training Data

### Step 1: Find the File
Open `backend/data/training_conversations.json`

### Step 2: Add Your Example
```json
{
  "input": "My washing machine is noisy",
  "output": "Check if the load is balanced. If noise continues, the drum bearings may be worn and need replacement. Also inspect the drive belt for wear."
}
```

### Step 3: Restart Backend
Stop the backend (Ctrl+C) and run `python app.py` again.

### Step 4: Test
Ask your new question and verify you get the expert response.

## Writing Good Training Data

**Good Input Examples:**
- "My dryer takes too long"
- "Dishwasher won't drain"
- "Refrigerator making noise"

**Good Output Examples:**
- Specific troubleshooting steps
- Multiple possible causes
- Part names when relevant
- Professional but simple language

**Bad Examples:**
- Vague inputs: "help me"
- Generic outputs: "contact support"
- Too technical: complex part numbers only

## How Matching Works

The system finds the best training example by:
1. Comparing your question to training examples
2. Looking for common words (especially appliance terms)
3. Giving extra weight to: refrigerator, dishwasher, cooling, leaking, etc.
4. Using the best match if similarity is above 20%

## Troubleshooting

**Problem**: Training data not loading
**Solution**: Check JSON syntax - missing commas or quotes

**Problem**: No training matches found
**Solution**: Add more variations of the same question

**Problem**: Wrong response returned
**Solution**: Make your input more specific with appliance names

## JSON Format

Your training file should look like this:
```json
[
  {
    "input": "First question",
    "output": "First expert answer"
  },
  {
    "input": "Second question", 
    "output": "Second expert answer"
  }
]
```

## Tips

1. **Start Simple**: Add 5-10 common questions first
2. **Test Everything**: Always test new training data
3. **Be Specific**: Include appliance names in questions
4. **Update Regularly**: Add new scenarios as you encounter them

