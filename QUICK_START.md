# ⚡ Quick Start Guide (5 Minutes)

**New to programming?** This guide will get you running in 5 minutes!

## 📋 Before You Start
1. Install Python: Go to [python.org](https://python.org) → Download → Install
2. Install Node.js: Go to [nodejs.org](https://nodejs.org) → Download → Install
3. Download this project (ask someone to help you get it on your computer)

## 🚀 3 Simple Steps

### Step 1: Start the Backend (The Brain) 🧠
```bash
# Go to the backend folder
cd backend

# Install Python tools
pip install -r requirements.txt

# Start the server
python app.py
```

**Keep this window open!** You should see: `Running on http://127.0.0.1:10000`

### Step 2: Start the Frontend (The Website) 🌐
Open a **NEW** terminal window:
```bash
# Go to the frontend folder
cd frontend

# Install website tools
npm install

# Start the website
npm run dev
```

**Keep this window open too!** You should see: `Local: http://localhost:3000`

### Step 3: Try It Out! 🎯
1. Open your web browser
2. Go to: `http://localhost:3000`
3. Click "Sign Up" and create an account
4. Upload one of these test files:
   - `data/example1_normal.log` (normal traffic)
   - `data/example2_suspicious.log` (hacker attack)
   - `data/example3_mixed.log` (mixed activity)
5. See the AI detect anomalies! 🔍

## 🎉 That's It!

You now have an AI-powered security tool running on your computer!

**Next Steps:**
- Read the full `README.md` to understand how it works
- Try uploading your own log files
- Experiment with the code

**Need Help?** 
- Make sure both terminal windows stay open
- Check the troubleshooting section in `README.md`
- The backend runs on port 10000, frontend on port 3000 