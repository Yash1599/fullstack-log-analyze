# 🔍 Fullstack Log Analyzer

## What is this project?

This is a **smart web application** that can look at computer log files and automatically find suspicious or unusual activities. Think of it as a detective for your website logs!

### What are logs?
Logs are like a diary for your website. Every time someone visits your website, downloads a file, or tries to access something, it gets written down in a log file. For example:
```
192.168.1.100 - - [10/Jan/2024:14:30:15 +0000] "GET /index.html HTTP/1.1" 200
```
This means: Someone from IP address 192.168.1.100 visited the homepage at 2:30 PM and it worked fine (status 200).

### What does this app do?
Our app reads these log files and uses **artificial intelligence** to spot problems like:
- 🚨 Hackers trying to break into admin pages
- 🚨 Someone making too many requests (like a robot attack)
- 🚨 Errors and failed attempts to access files
- 🚨 Unusual behavior that doesn't look normal

---

## 🎯 How the AI Works (Simple Explanation)

Our app uses **two different methods** to catch bad guys:

### Method 1: Rule-Based Detection (Like a Security Guard)
Just like a security guard follows rules, our app has 3 simple rules:

1. **Too Many Requests Rule**: If the same person (IP address) makes more than 3 requests, flag it as suspicious
   - **Confidence**: 80% sure this is bad
   - **Why**: Real people don't usually click that fast

2. **Suspicious Pages Rule**: If someone tries to access admin pages or login pages
   - **Examples**: `/admin`, `/wp-login.php`
   - **Confidence**: 90% sure this is bad
   - **Why**: Hackers often try these common admin URLs

3. **Error Codes Rule**: If the website returns error codes (400, 404, 500, etc.)
   - **Confidence**: 70% sure this is bad
   - **Why**: Too many errors might mean someone is trying things they shouldn't

### Method 2: AI-Based Detection (Like a Smart Detective)
This is the really cool part! Our app uses machine learning:

1. **Training**: We first show the AI examples of "normal" log entries
2. **Learning**: The AI learns what normal behavior looks like
3. **Detection**: When it sees new logs, it can spot things that don't look normal

**Technical Details** (for curious minds):
- Uses `SentenceTransformer` to convert log text into numbers (vectors)
- Uses `IsolationForest` algorithm to find outliers
- Assumes 15% of logs might be anomalies

---

## 🛠️ What You Need Before Starting

### For Your Computer:
- **Python 3.8 or newer** - The backend programming language
- **Node.js 16 or newer** - For the frontend website
- **Git** - To download the code
- **A web browser** - To see the results

### For beginners:
- **Python**: Go to [python.org](https://python.org) and download Python
- **Node.js**: Go to [nodejs.org](https://nodejs.org) and download Node.js
- **Git**: Go to [git-scm.com](https://git-scm.com) and download Git

---

## 📥 Step 1: Get the Code

First, download the project to your computer:

```bash
# Download the project
git clone <your-repository-url>

# Go into the project folder
cd fullstack-log-analyzer
```

---

## 🏗️ Step 2: Set Up the Backend (The Brain)

The backend is like the brain of our app - it does all the smart analysis.

### 2.1: Go to the backend folder
```bash
cd backend
```

### 2.2: Create a safe space for Python packages
```bash
# Create a virtual environment (like a separate room for this project)
python -m venv venv

# Activate it (enter the room)
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 2.3: Install the required tools
```bash
# Install all the Python packages our app needs
pip install -r requirements.txt
```

**What this installs:**
- `Flask` - Creates the web server
- `sentence-transformers` - The AI for understanding text
- `scikit-learn` - Machine learning tools
- `pymongo` - For storing data
- `flask-cors` - Lets the frontend talk to backend

### 2.4: Start the backend server
```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:10000
```

**Keep this terminal window open!** The backend is now running and waiting for requests.

---

## 🎨 Step 3: Set Up the Frontend (The Face)

The frontend is the pretty website that users see and interact with.

### 3.1: Open a NEW terminal window
(Keep the backend running in the first terminal)

### 3.2: Go to the frontend folder
```bash
cd frontend
```

### 3.3: Install the website tools
```bash
# Install all the website packages
npm install
```

**What this installs:**
- `Next.js` - The website framework
- `React` - For interactive user interfaces
- `Bootstrap` - For pretty styling
- `Chart.js` - For showing graphs
- `Axios` - For talking to the backend

### 3.4: Start the frontend server
```bash
npm run dev
```

You should see:
```
 ▲ Next.js 15.3.3
 - Local:        http://localhost:3000
```

---

## 🚀 Step 4: Use the Application

### 4.1: Open your web browser
Go to: `http://localhost:3000`

### 4.2: Create an account
1. Click "Sign Up"
2. Enter a username and password
3. Click "Create Account"

### 4.3: Log in
1. Enter your username and password
2. Click "Login"

### 4.4: Upload a log file
1. Click "Choose File"
2. Select one of the example log files (see below)
3. Click "Upload and Analyze"
4. Wait for the AI to analyze it
5. See the results with charts and detailed analysis!

---

## 📊 Example Log Files for Testing

We've included 4 example log files in **two convenient locations**:

### 📁 File Locations:
- **`data/`** folder (root of project) - For general testing
- **`backend/sample_logs/`** folder - For easy backend testing and development

### 🎯 Available Files:

### 1. `example1_normal.log` - Clean Traffic
**What's in it**: Normal website visitors doing normal things
- People viewing homepage, about page, contact page
- All requests successful (status code 200)
- Different IP addresses (real users)

**Expected Result**: Very few or no anomalies detected

### 2. `example2_suspicious.log` - Hacker Attack
**What's in it**: Someone trying to hack the website
- One IP address making many requests (rule violation)
- Trying to access `/admin` and `/wp-login.php` (suspicious pages)
- Getting error codes like 401, 403, 404, 500

**Expected Result**: Many anomalies detected with high confidence

### 3. `example3_mixed.log` - Real World Scenario
**What's in it**: Mix of normal users and suspicious activity
- Most traffic is normal
- Some failed attempts to access admin pages
- One IP making too many requests
- Some 404 errors (page not found)

**Expected Result**: Some anomalies detected, showing the AI can distinguish good from bad

### 4. `example4_realworld.log` - Advanced Attack Patterns
**What's in it**: Realistic web attack scenarios you might see in production
- **Normal users**: Regular visitors browsing legitimate pages
- **WordPress attacks**: Attempts to find `/wp-admin`, `/wp-login.php`
- **Database hunting**: Looking for `/phpmyadmin`, `/mysql`, `/.env`
- **API attacks**: Unauthorized attempts to access `/api/` endpoints
- **Config file searches**: Trying to find sensitive files like `config.php`, `backup.sql`

**Expected Result**: Multiple attack patterns detected with varying confidence levels

### 🔧 How to Access Sample Files:

#### From Web Interface:
1. Navigate to either `data/` or `backend/sample_logs/` folder
2. Select any of the example files when uploading
3. Click "Upload and Analyze"

#### From Python Code (Backend Development):
```python
from anomaly import parse_log_file

# Use files from backend/sample_logs/ for easy testing
results = parse_log_file('sample_logs/example1_normal.log')
print(f"Found {len([r for r in results if r['anomaly']])} anomalies")
```

---

## 🔧 Understanding the Results

When you upload a log file, you'll see:

### Summary Cards
- **Total Logs**: How many log entries were analyzed
- **Anomalies Found**: How many suspicious entries were detected
- **Clean Logs**: How many normal entries were found
- **Average Confidence**: How sure the AI is about its detections

### Charts
- **Pie Chart**: Shows the proportion of normal vs. suspicious logs
- **Bar Chart**: Shows different types of anomalies found

### Detailed Table
For each suspicious log entry, you'll see:
- **IP Address**: Where the request came from
- **Request**: What they were trying to access
- **Status Code**: Whether it worked or failed
- **Reason**: Why our AI thinks it's suspicious
- **Confidence**: How sure the AI is (0% to 100%)

---

## 🎛️ Environment Setup (Optional)

For advanced users who want to customize:

### Backend Environment Variables
Create a file called `.env` in the `backend/` folder:
```env
# Database connection
MONGO_URI=mongodb://localhost:27017/loganalyzer

# JWT secret for user authentication
JWT_SECRET=your-secret-key-here

# Flask settings
FLASK_ENV=development
FLASK_DEBUG=True
```

### Frontend Environment Variables
Create a file called `.env.local` in the `frontend/` folder:
```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:10000
```

---

## 🐛 Troubleshooting Common Problems

### Problem: "Command not found: python"
**Solution**: Python isn't installed. Go to [python.org](https://python.org) and install Python.

### Problem: "Command not found: npm"
**Solution**: Node.js isn't installed. Go to [nodejs.org](https://nodejs.org) and install Node.js.

### Problem: Backend won't start
**Solution**: 
1. Make sure you're in the `backend/` folder
2. Make sure your virtual environment is activated
3. Run `pip install -r requirements.txt` again

### Problem: Frontend shows "Cannot connect to backend"
**Solution**:
1. Make sure the backend is running on port 10000
2. Check that both servers are running
3. Try refreshing the page

### Problem: "Port already in use"
**Solution**: 
- For backend: Change port in `app.py` (look for `port=10000`)
- For frontend: Use `npm run dev -- -p 3001` to use a different port

### Problem: Uploads fail
**Solution**:
1. Make sure your log file is in the correct format
2. Check that the `uploads/` folder exists in the backend
3. Make sure the file isn't too large (>10MB)

---

## 📁 Project Structure

```
fullstack-log-analyzer/
├── frontend/                 # Website (React + Next.js)
│   ├── app/                 # Website pages
│   ├── context/             # User authentication
│   ├── package.json         # Frontend dependencies
│   └── README.md            # Frontend documentation
├── backend/                 # Server (Python + Flask)
│   ├── app.py              # Main server file
│   ├── anomaly.py          # AI detection logic
│   ├── auth.py             # User login/signup
│   ├── requirements.txt    # Python dependencies
│   ├── uploads/            # Where uploaded files go
│   └── sample_logs/        # Example log files for testing
│       ├── README.md       # Sample files documentation
│       ├── example1_normal.log
│       ├── example2_suspicious.log
│       ├── example3_mixed.log
│       └── example4_realworld.log
├── data/                   # Example log files for testing (duplicate location)
│   ├── example1_normal.log
│   ├── example2_suspicious.log
│   ├── example3_mixed.log
│   └── example4_realworld.log
└── README.md               # This file!
```