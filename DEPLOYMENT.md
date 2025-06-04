# Deployment Guide

This guide covers deploying your Fullstack Log Analyzer to production using:
- **Vercel** for the Next.js frontend
- **Render** for the Flask backend

## 🚀 Backend Deployment (Render)

### 1. Prepare Your Repository

Make sure your code is pushed to a Git repository (GitHub, GitLab, or Bitbucket).

### 2. Deploy to Render

1. **Sign up** at [render.com](https://render.com)
2. **Connect your repository**
3. **Create a new Web Service**
   - **Repository**: Select your repo
   - **Branch**: `main` or `master`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`

### 3. Configure Environment Variables

In your Render dashboard, add these environment variables:

```
FLASK_ENV=production
SECRET_KEY=your-super-secret-key
PORT=10000
```

### 4. Note Your Backend URL

After deployment, Render will provide a URL like:
```
https://your-app-name.onrender.com
```

**Save this URL** - you'll need it for the frontend configuration.

## 🌐 Frontend Deployment (Vercel)

### 1. Install Vercel CLI (Optional)

```bash
npm i -g vercel
```

### 2. Deploy to Vercel

#### Option A: Using Vercel Dashboard

1. **Sign up** at [vercel.com](https://vercel.com)
2. **Import your repository**
3. **Configure the project**:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

#### Option B: Using Vercel CLI

```bash
cd frontend
vercel
```

Follow the prompts and select the frontend directory.

### 3. Configure Environment Variables

In your Vercel dashboard (NOT in vercel.json), add this environment variable:

**Important**: Do not add environment variables in `vercel.json`. Use the Vercel dashboard instead.

1. Go to your project in Vercel dashboard
2. Click "Settings" → "Environment Variables"
3. Add:
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://your-render-app-name.onrender.com`
   - **Environments**: Select "Production", "Preview", and "Development"

**Replace** `your-render-app-name` with your actual Render service name.

### 4. Redeploy

After adding environment variables, redeploy your Vercel app to apply the changes.

## 🔧 Configuration Files

### Backend Configuration (`backend/render.yaml`)

```yaml
services:
  - type: web
    name: log-analyzer-backend
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "python app.py"
    plan: free
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.16
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
    healthCheckPath: /
```

### Frontend Configuration (`frontend/vercel.json`)

```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/next"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/$1"
    }
  ]
}
```

## 🛠️ Local Development with Environment Variables

Create a `.env.local` file in the frontend directory:

```env
# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:10000
```

## 🔄 Deployment Workflow

### Initial Deployment

1. **Deploy Backend** (Render first)
2. **Get Backend URL** from Render dashboard
3. **Configure Frontend** with backend URL
4. **Deploy Frontend** (Vercel)

### Updates

1. **Push changes** to your repository
2. **Render** will auto-deploy backend changes
3. **Vercel** will auto-deploy frontend changes

## 🔒 Security Considerations

### Production Environment Variables

- **Never commit** `.env` files to version control
- **Use strong secrets** for JWT signing
- **Configure CORS** properly for your domain

### Backend Security

```python
# In production, update CORS origins in app.py
CORS(app, origins=["https://your-vercel-app.vercel.app"])
```

### Frontend Security

- All API calls use HTTPS in production
- JWT tokens are handled securely
- Environment variables are properly scoped

## 📊 Monitoring & Debugging

### Backend Logs (Render)
- View logs in Render dashboard
- Monitor API performance
- Check for errors and exceptions

### Frontend Logs (Vercel)
- View function logs in Vercel dashboard
- Monitor build and deployment status
- Check browser console for client errors

## 🚨 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Update `origins` in `app.py` with your Vercel URL
   - Ensure environment variables are set correctly

2. **API Connection Failed**
   - Verify `NEXT_PUBLIC_API_URL` in Vercel environment variables
   - Check that backend is running on Render

3. **Build Failures**
   - Check build logs in respective dashboards
   - Verify all dependencies are in requirements.txt/package.json

4. **File Upload Issues**
   - Render free tier has limited storage
   - Consider using cloud storage for larger files

### Environment Variable Template

```bash
# Backend (Render)
FLASK_ENV=production
SECRET_KEY=your-super-secret-key
PORT=10000

# Frontend (Vercel)
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
```

## 🎯 Production Checklist

- [ ] Backend deployed to Render
- [ ] Frontend deployed to Vercel
- [ ] Environment variables configured
- [ ] CORS settings updated
- [ ] SSL certificates active (automatic)
- [ ] API endpoints accessible
- [ ] Authentication working
- [ ] File uploads functional
- [ ] Error monitoring setup

## 🌟 Advanced Features

### Custom Domain Setup

1. **Vercel**: Add custom domain in dashboard
2. **Render**: Configure custom domain (paid plans)

### Database Integration

Consider adding PostgreSQL for persistent data:
- Render PostgreSQL add-on
- Update backend to use database instead of in-memory storage

### File Storage

For production file handling:
- AWS S3 integration
- Cloudinary for file management
- Render persistent disks (paid plans)

---

Your Fullstack Log Analyzer is now production-ready! 🚀 