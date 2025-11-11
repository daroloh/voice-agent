# ✅ Deployment Checklist

Use this checklist to ensure your voice agent is ready for deployment.

## Pre-Deployment

- [ ] **API Keys Obtained**
  - [ ] AssemblyAI API key from https://www.assemblyai.com/app/account
  - [ ] OpenAI API key from https://platform.openai.com/api-keys
  - [ ] Keys tested locally and working

- [ ] **Code Review**
  - [ ] All files committed to Git
  - [ ] `.env` file is in `.gitignore` (never commit API keys!)
  - [ ] Code works locally
  - [ ] No hardcoded API keys in code

- [ ] **Environment Variables**
  - [ ] `ASSEMBLY_API_KEY` ready
  - [ ] `OPENAI_API_KEY` ready
  - [ ] `FRONTEND_URL` set (or use `*` for same-domain deployment)

## GitHub Setup

- [ ] **Repository Created**
  - [ ] Repository created on GitHub
  - [ ] Code pushed to GitHub
  - [ ] Repository is public or you have access for deployment platform

## Deployment Platform Setup

### Render
- [ ] Account created at render.com
- [ ] GitHub repository connected
- [ ] Web service created
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `uvicorn server:app --host 0.0.0.0 --port $PORT`
- [ ] Environment variables added:
  - [ ] `ASSEMBLY_API_KEY`
  - [ ] `OPENAI_API_KEY`
  - [ ] `FRONTEND_URL` (optional)
- [ ] Service deployed successfully
- [ ] Service is accessible via URL

### Railway
- [ ] Account created at railway.app
- [ ] GitHub repository connected
- [ ] Project created
- [ ] Environment variables added:
  - [ ] `ASSEMBLY_API_KEY`
  - [ ] `OPENAI_API_KEY`
  - [ ] `FRONTEND_URL` (optional)
- [ ] Service deployed successfully
- [ ] Service is accessible via URL

### Heroku
- [ ] Account created at heroku.com
- [ ] Heroku CLI installed
- [ ] Logged in via CLI
- [ ] App created
- [ ] Environment variables set:
  - [ ] `ASSEMBLY_API_KEY`
  - [ ] `OPENAI_API_KEY`
  - [ ] `FRONTEND_URL` (optional)
- [ ] Code deployed
- [ ] Service is accessible via URL

## Testing

- [ ] **Basic Functionality**
  - [ ] Frontend loads correctly
  - [ ] UI displays properly
  - [ ] No console errors in browser

- [ ] **Microphone Access**
  - [ ] Browser requests microphone permission
  - [ ] Microphone permission granted
  - [ ] Recording starts when button clicked
  - [ ] Recording stops when button clicked again

- [ ] **Voice Processing**
  - [ ] Audio is sent to backend
  - [ ] Transcription works (speech-to-text)
  - [ ] GPT generates response
  - [ ] Text-to-speech works
  - [ ] Audio playback works

- [ ] **Conversation**
  - [ ] Multiple exchanges work
  - [ ] Conversation history maintained
  - [ ] Reset button works
  - [ ] Messages display correctly

- [ ] **Error Handling**
  - [ ] Error messages display correctly
  - [ ] Invalid API keys show error
  - [ ] Network errors handled gracefully
  - [ ] Empty transcriptions handled

## Post-Deployment

- [ ] **Monitoring**
  - [ ] Check deployment logs for errors
  - [ ] Monitor API usage
  - [ ] Check response times
  - [ ] Verify HTTPS is enabled

- [ ] **Security**
  - [ ] HTTPS enabled (required for microphone)
  - [ ] API keys not exposed in frontend
  - [ ] CORS configured correctly
  - [ ] Environment variables secure

- [ ] **Documentation**
  - [ ] Update README with deployment URL
  - [ ] Document any custom configurations
  - [ ] Note any platform-specific settings

## Optional Enhancements

- [ ] **Custom Domain**
  - [ ] Domain purchased/configured
  - [ ] DNS configured
  - [ ] SSL certificate configured
  - [ ] Custom domain working

- [ ] **Analytics**
  - [ ] Analytics tracking added (optional)
  - [ ] Error tracking configured (optional)
  - [ ] Usage monitoring set up (optional)

- [ ] **Performance**
  - [ ] Response times acceptable
  - [ ] Audio quality good
  - [ ] No memory leaks
  - [ ] Optimized for production

## Troubleshooting

If something doesn't work:

1. **Check Logs**
   - View deployment logs
   - Check browser console
   - Review server logs

2. **Verify Environment Variables**
   - Ensure all variables are set
   - Check for typos
   - Verify API keys are valid

3. **Test Locally**
   - Test with same environment variables
   - Verify code works locally
   - Check for local vs production differences

4. **Common Issues**
   - Microphone not working → Check HTTPS
   - CORS errors → Verify FRONTEND_URL
   - API errors → Check API keys and quotas
   - Slow responses → Check API limits and cold starts

## Success Criteria

Your deployment is successful when:

✅ Frontend loads without errors
✅ Microphone access works
✅ Voice recording works
✅ Transcription works
✅ GPT responses work
✅ Text-to-speech works
✅ Audio playback works
✅ Conversation flows naturally
✅ Error handling works
✅ HTTPS is enabled
✅ Service is accessible 24/7

## Next Steps

After successful deployment:

1. Share your app URL with others
2. Monitor usage and costs
3. Gather user feedback
4. Plan enhancements (streaming, persistence, etc.)
5. Scale if needed

---

**Need Help?** Check [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions or open an issue on GitHub.

