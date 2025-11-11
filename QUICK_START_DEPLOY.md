# ⚡ Quick Start: Deploy Your Voice Agent in 5 Minutes

This is the fastest way to get your voice agent online!

## Step 1: Get API Keys (2 minutes)

1. **AssemblyAI**: https://www.assemblyai.com/app/account
   - Sign up (free tier available)
   - Copy your API key

2. **OpenAI**: https://platform.openai.com/api-keys
   - Sign up (requires payment method)
   - Create an API key
   - Copy your API key

## Step 2: Push to GitHub (1 minute)

```bash
# Initialize Git (if not already done)
git init
git add .
git commit -m "Voice Agent - Ready to deploy"

# Create repository on GitHub, then:
git remote add origin https://github.com/yourusername/voice-agent.git
git push -u origin main
```

## Step 3: Deploy on Render (2 minutes)

1. **Go to**: https://render.com
2. **Sign up** with GitHub (one-click)
3. **Click**: "New +" → "Web Service"
4. **Connect** your GitHub repository
5. **Configure**:
   - **Name**: `voice-agent` (or any name)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`
6. **Add Environment Variables**:
   - Click "Environment" tab
   - Add:
     - Key: `ASSEMBLY_API_KEY`, Value: `your_assemblyai_key`
     - Key: `OPENAI_API_KEY`, Value: `your_openai_key`
     - Key: `FRONTEND_URL`, Value: `*`
7. **Click**: "Create Web Service"
8. **Wait**: 5-10 minutes for deployment

## Step 4: Test (30 seconds)

1. **Open** your app URL (e.g., `https://your-app.onrender.com`)
2. **Click** "Start Recording"
3. **Speak** into your microphone
4. **Click** "Stop Recording"
5. **Listen** to the AI response!

## 🎉 Done!

Your voice agent is now live on the web!

### What's Next?

- Share your app URL with friends
- Customize the AI persona (edit system prompt in `server.py`)
- Add features (see `DEPLOYMENT.md` for ideas)
- Monitor usage and costs

### Troubleshooting

**Microphone not working?**
- Make sure you're using HTTPS (Render provides this automatically)
- Grant microphone permissions in your browser
- Try Chrome or Firefox

**API errors?**
- Check your API keys are correct
- Verify you have credits/quota
- Check the logs in Render dashboard

**Need help?**
- See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guide
- See [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) for checklist
- Check Render logs for errors

---

**That's it!** You now have a working voice agent on the web. 🚀

