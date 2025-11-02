# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Configure API Key

Create `backend/.env`:
```
OPENAI_API_KEY=your_api_key_here
```

### Step 3: Start Backend

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

✅ Backend running at `http://localhost:8000`

### Step 4: Frontend Setup (New Terminal)

```bash
cd system-design-web
npm install
npm run dev
```

✅ Frontend running at `http://localhost:3000`

### Step 5: Use the App!

1. Open `http://localhost:3000` in your browser
2. Enter a system design requirement
3. Click "Generate System Design"
4. View the beautiful markdown document!

## 🐛 Troubleshooting

**Backend errors:**
- Make sure you have Python 3.10+
- Verify `.env` file exists with `OPENAI_API_KEY`
- Check that port 8000 is not in use

**Frontend errors:**
- Run `npm install` to install dependencies
- Make sure port 3000 is not in use
- Check that backend is running on port 8000

**API connection errors:**
- Verify backend is running: `http://localhost:8000/health`
- Check CORS settings in `backend/main.py`

