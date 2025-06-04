# 🚀 Deployment Environment Variable Fix

## ❌ The Problem
Getting error: `Environment Variable "NEXT_PUBLIC_API_URL" references Secret "api-url", which does not exist.`

## ✅ The Solution

### Step 1: Vercel Dashboard Setup

1. **Go to your Vercel project dashboard**
   - Visit [vercel.com](https://vercel.com)
   - Click on your project

2. **Navigate to Settings**
   - Click "Settings" tab
   - Click "Environment Variables" in the sidebar

3. **Add the Environment Variable**
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: Your backend URL (see options below)
   - **Environments**: Select "Production", "Preview", and "Development"

### Step 2: Choose Your Backend URL

#### Option A: Deploy Backend to Render (Recommended)
```
NEXT_PUBLIC_API_URL = https://your-backend-app.onrender.com
```

#### Option B: Use Local Development
```
NEXT_PUBLIC_API_URL = http://localhost:10000
```

#### Option C: Deploy Backend to Railway/Heroku
```
NEXT_PUBLIC_API_URL = https://your-app.railway.app
NEXT_PUBLIC_API_URL = https://your-app.herokuapp.com
```

### Step 3: Backend Deployment (If Using Render)

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Connect your GitHub account

2. **Deploy Backend**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Environment**: Python 3

3. **Add Backend Environment Variables on Render**
   ```
   PORT = 10000
   MONGO_URI = your-mongodb-connection-string
   JWT_SECRET = your-secret-key
   FLASK_ENV = production
   ```

4. **Get Your Backend URL**
   - After deployment, copy the URL (e.g., `https://your-app.onrender.com`)
   - Use this URL in Vercel environment variables

### Step 4: Redeploy Frontend

1. **Trigger Redeploy**
   - In Vercel dashboard, go to "Deployments"
   - Click "Redeploy" on the latest deployment
   - OR push a new commit to trigger automatic deployment

2. **Verify Environment Variable**
   - Check that `NEXT_PUBLIC_API_URL` is set correctly
   - Test the frontend → backend connection

## 🔧 Alternative: Using .env.local (Development)

For local development, create `frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:10000
```

## 🧪 Testing the Fix

1. **Check Environment Variable**
   ```bash
   # In your frontend, add this to a page to test:
   console.log('API URL:', process.env.NEXT_PUBLIC_API_URL)
   ```

2. **Test API Connection**
   - Try to sign up/login
   - Upload a log file
   - Check browser console for errors

## 📝 Common Deployment URLs

### Frontend (Vercel)
```
https://your-project.vercel.app
```

### Backend Options
```
Render:   https://your-backend.onrender.com
Railway:  https://your-backend.railway.app
Heroku:   https://your-backend.herokuapp.com
```

## 🔍 Troubleshooting

### Issue: CORS Errors
**Solution**: Update backend CORS settings
```python
# In backend/app.py
CORS(app, origins=["https://your-frontend.vercel.app"])
```

### Issue: Environment Variable Not Working
**Solution**: 
1. Check spelling: `NEXT_PUBLIC_API_URL` (case sensitive)
2. Redeploy after adding environment variables
3. Make sure it starts with `NEXT_PUBLIC_` for client-side access

### Issue: Backend Not Accessible
**Solution**:
1. Make sure backend is deployed and running
2. Check backend logs for errors
3. Verify the URL is correct and accessible

## ✅ Success Checklist

- [ ] Removed `@api-url` reference from vercel.json
- [ ] Added `NEXT_PUBLIC_API_URL` in Vercel environment variables
- [ ] Backend is deployed and accessible
- [ ] Frontend can connect to backend
- [ ] Login/signup works
- [ ] File upload works 