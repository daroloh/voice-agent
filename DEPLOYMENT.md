# Deployment Guide

This guide will walk you through deploying your Voice-to-Voice AI Agent to various hosting platforms.

## 📋 Prerequisites

- GitHub account (for version control and deployment)
- API keys:
  - [AssemblyAI API Key](https://www.assemblyai.com/app/account)
  - [OpenAI API Key](https://platform.openai.com/api-keys)

---

## Option 1: Render (Recommended for Beginners)

Render is user-friendly and offers a free tier perfect for this project.

### Step 1: Prepare Your Repository

1. **Initialize Git** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/yourusername/voice-agent.git
   git push -u origin main
   ```

### Step 2: Deploy on Render

1. **Sign up/Login** at [render.com](https://render.com)

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your `voice-agent` repository

3. **Configure Service**:
   - **Name**: `voice-agent` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free (or paid for better performance)

4. **Add Environment Variables**:
   - Click "Environment" tab
   - Add the following:
     ```
     ASSEMBLY_API_KEY=your_actual_key_here
     OPENAI_API_KEY=your_actual_key_here
     FRONTEND_URL=*  (or your frontend URL if deploying separately)
     ```

5. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Your app will be available at `https://your-app.onrender.com`

### Step 3: Access Your App

- Open `https://your-app.onrender.com` in your browser
- The frontend is served automatically from the backend
- Test the voice agent!

**Note**: Free tier on Render spins down after 15 minutes of inactivity. First request may take 30-60 seconds to wake up.

---

## Option 2: Railway 🚂

Railway is another excellent option with easy deployment.

### Step 1: Deploy on Railway

1. **Sign up** at [railway.app](https://railway.app)

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your repository

3. **Configure Environment Variables**:
   - Go to "Variables" tab
   - Add:
     ```
     ASSEMBLY_API_KEY=your_actual_key_here
     OPENAI_API_KEY=your_actual_key_here
     FRONTEND_URL=*
     ```

4. **Deploy**:
   - Railway auto-detects Python and FastAPI
   - Deployment starts automatically
   - Your app will be available at `https://your-app.up.railway.app`

### Step 2: Access Your App

- Open the provided Railway URL
- Test your voice agent!

---

## Option 3: Heroku 🟣

Heroku requires a credit card for verification but offers a free tier.

### Step 1: Install Heroku CLI

```bash
# Windows (using chocolatey)
choco install heroku-cli

# Or download from https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Deploy

1. **Login to Heroku**:
   ```bash
   heroku login
   ```

2. **Create Heroku App**:
   ```bash
   heroku create your-app-name
   ```

3. **Set Environment Variables**:
   ```bash
   heroku config:set ASSEMBLY_API_KEY=your_actual_key_here
   heroku config:set OPENAI_API_KEY=your_actual_key_here
   heroku config:set FRONTEND_URL=*
   ```

4. **Deploy**:
   ```bash
   git push heroku main
   ```

5. **Open Your App**:
   ```bash
   heroku open
   ```

---

## Option 4: Docker Deployment 🐳

Deploy using Docker to any platform that supports containers (AWS, Google Cloud, Azure, DigitalOcean, etc.).

### Step 1: Build Docker Image

```bash
docker build -t voice-agent .
```

### Step 2: Run Locally

```bash
docker run -p 8000:8000 \
  -e ASSEMBLY_API_KEY=your_key \
  -e OPENAI_API_KEY=your_key \
  -e FRONTEND_URL=* \
  voice-agent
```

### Step 3: Deploy to Cloud

- **AWS ECS/Fargate**: Upload to ECR, create ECS service
- **Google Cloud Run**: `gcloud run deploy --source .`
- **Azure Container Instances**: Use Azure CLI
- **DigitalOcean App Platform**: Connect GitHub, select Dockerfile

---

## Option 5: Separate Frontend + Backend (Advanced)

Deploy frontend and backend separately for better scalability.

### Backend Deployment

Follow any of the options above (Render, Railway, Heroku, etc.)

### Frontend Deployment

1. **Update API URL in Frontend**:
   Edit `frontend/index.html`:
   ```javascript
   const API_URL = 'https://your-backend-url.onrender.com';
   ```

2. **Deploy Frontend to Vercel**:
   ```bash
   npm i -g vercel
   cd frontend
   vercel
   ```

3. **Deploy Frontend to Netlify**:
   - Drag and drop `frontend/` folder to Netlify
   - Or use Netlify CLI: `netlify deploy --prod`

4. **Update Backend CORS**:
   Set `FRONTEND_URL` environment variable to your frontend URL:
   ```
   FRONTEND_URL=https://your-frontend.vercel.app
   ```

---

## Post-Deployment Configuration

### 1. Custom Domain (Optional)

- **Render**: Go to Settings → Custom Domain
- **Railway**: Go to Settings → Generate Domain
- **Heroku**: Use Heroku CLI: `heroku domains:add yourdomain.com`

### 2. Environment Variables

Make sure these are set in your hosting platform:
- `ASSEMBLY_API_KEY` (required)
- `OPENAI_API_KEY` (required)
- `FRONTEND_URL` (optional, defaults to `*`)

### 3. HTTPS

All platforms above provide HTTPS by default. Make sure your app uses HTTPS for microphone access (required by browsers).

---

## Troubleshooting

### Issue: Microphone not working

**Solution**: 
- Ensure you're using HTTPS (browsers require HTTPS for microphone access)
- Check browser permissions for microphone access
- Test in Chrome/Firefox (Safari may have issues)

### Issue: CORS errors

**Solution**:
- Set `FRONTEND_URL` environment variable to your frontend URL
- Or set it to `*` if frontend is served from same domain
- Restart your backend service

### Issue: API errors

**Solution**:
- Verify API keys are correct in environment variables
- Check API quotas/limits
- Review logs in your hosting platform

### Issue: Slow responses

**Solution**:
- Upgrade to paid tier (free tiers may have cold starts)
- Consider using streaming API (future enhancement)
- Optimize audio file size

### Issue: Deployment fails

**Solution**:
- Check build logs for errors
- Verify `requirements.txt` is correct
- Ensure Python version matches (3.11)
- Check that all files are committed to Git

---

## Monitoring & Logs

### Render
- Go to "Logs" tab in your service dashboard
- View real-time logs and errors

### Railway
- Click on your service → "Deployments" → View logs
- Use Railway CLI: `railway logs`

### Heroku
- View logs: `heroku logs --tail`
- Or use Heroku dashboard → "More" → "View logs"

---

## Next Steps

After deployment:

1. **Test thoroughly** with different audio inputs
2. **Monitor usage** and API costs
3. **Set up alerts** for errors (if platform supports)
4. **Optimize** based on usage patterns
5. **Add features**:
   - Streaming responses
   - Conversation persistence
   - Multiple languages
   - Custom AI personas

---

## Cost Estimates

### Free Tier Limits:

- **Render**: 750 hours/month free, then $7/month
- **Railway**: $5 free credit/month, then pay-as-you-go
- **Heroku**: Free tier deprecated, $7/month minimum
- **API Costs**: 
  - AssemblyAI: ~$0.00025 per minute of audio
  - OpenAI GPT-4o-mini: ~$0.15 per 1M tokens
  - OpenAI TTS: ~$15 per 1M characters

### Estimated Monthly Cost:
- **Light usage** (100 conversations/day): ~$5-10/month
- **Moderate usage** (500 conversations/day): ~$20-30/month
- **Heavy usage** (1000+ conversations/day): ~$50+/month

---

## Deployment Checklist

- [ ] API keys configured
- [ ] Environment variables set
- [ ] Code pushed to GitHub
- [ ] Backend deployed and accessible
- [ ] Frontend loads correctly
- [ ] Microphone permissions working
- [ ] Voice recording works
- [ ] Transcription works
- [ ] GPT responses work
- [ ] TTS playback works
- [ ] HTTPS enabled
- [ ] Custom domain configured (optional)
- [ ] Monitoring set up (optional)

---

## You're Done!

Your voice agent is now live on the web! Share the URL with others and start using it.

For questions or issues, check the main [README.md](README.md) or open an issue on GitHub.

