# 🎤 Voice-to-Voice AI Agent

A full-stack conversational AI agent that enables natural voice-to-voice interactions. Users speak into their microphone, the audio is transcribed, processed by GPT, and a voice response is generated and played back.

## 🏗️ Architecture

```
User speaks → AssemblyAI (STT) → OpenAI GPT → OpenAI TTS → User hears reply
```

### Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML + JavaScript (vanilla)
- **Speech-to-Text**: AssemblyAI
- **Conversation Logic**: OpenAI GPT-4o-mini
- **Text-to-Speech**: OpenAI TTS

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js (optional, for serving frontend)
- API Keys:
  - [AssemblyAI API Key](https://www.assemblyai.com/app/account)
  - [OpenAI API Key](https://platform.openai.com/api-keys)

### Installation

1. **Clone or navigate to the project directory**

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.template .env
   ```
   Then edit `.env` and add your API keys:
   ```
   ASSEMBLY_API_KEY=your_actual_key_here
   OPENAI_API_KEY=your_actual_key_here
   FRONTEND_URL=*  (optional, defaults to "*")
   ```

4. **Start the backend server**
   ```bash
   uvicorn server:app --reload
   ```
   The API will be available at `http://localhost:8000`

5. **Open the frontend**
   - Option 1: Open `frontend/index.html` directly in your browser
   - Option 2: Use a simple HTTP server:
     ```bash
     # Python
     cd frontend
     python -m http.server 8080
     
     # Or Node.js
     npx http-server frontend -p 8080
     ```
   - Then navigate to `http://localhost:8080`

6. **Test it out!**
   - Click "Start Recording"
   - Speak into your microphone
   - Click "Stop Recording"
   - Wait for the AI response

## 📁 Project Structure

```
VoiceAgent/
├── server.py              # FastAPI backend
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Your actual API keys (not in git)
├── README.md             # This file
├── .gitignore           # Git ignore rules
└── frontend/
    └── index.html       # Frontend UI
```

## 🔧 API Endpoints

### `POST /talk`
Main endpoint that processes audio input.

**Request**: Multipart form data with audio file
- `file`: Audio file (webm, mp3, wav, etc.)

**Response**: Audio stream (MPEG)
- Headers:
  - `X-Reply-Text`: The text response from GPT
  - `X-User-Text`: The transcribed user input

### `POST /reset`
Reset conversation history.

**Response**: JSON
```json
{"message": "Conversation history reset"}
```

### `GET /health`
Health check endpoint.

**Response**: JSON
```json
{
  "status": "healthy",
  "assemblyai_configured": true,
  "openai_configured": true
}
```

## 🎯 How It Works

### 1. Speech-to-Text (AssemblyAI)
- User records audio via browser microphone
- Audio is sent to backend as a blob
- Backend uploads audio to AssemblyAI
- AssemblyAI transcribes the audio to text

### 2. Conversation Logic (OpenAI GPT)
- Transcribed text is sent to OpenAI GPT-4o-mini
- GPT generates a contextual response
- Conversation history is maintained for context

### 3. Text-to-Speech (OpenAI TTS)
- GPT response is converted to speech using OpenAI TTS
- Audio is streamed back to frontend
- Frontend plays the audio response

## 🚢 Deployment

### Quick Start

**The easiest way to deploy is using Render (recommended for beginners):**

1. **Push your code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/voice-agent.git
   git push -u origin main
   ```

2. **Deploy on Render**:
   - Go to [render.com](https://render.com) and sign up
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Use these settings:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`
   - Add environment variables:
     - `ASSEMBLY_API_KEY=your_key`
     - `OPENAI_API_KEY=your_key`
     - `FRONTEND_URL=*`
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Your app will be live at `https://your-app.onrender.com`

**The frontend is automatically served from the backend**, so you don't need separate deployment!

### Detailed Deployment Guide

For detailed instructions on deploying to Render, Railway, Heroku, Docker, and more, see **[DEPLOYMENT.md](DEPLOYMENT.md)**.

### Deployment Options

- **Render** (Recommended) - Free tier, easy setup
- **Railway** - Simple deployment, pay-as-you-go
- **Heroku** - Classic platform, requires credit card
- **Docker** - Deploy anywhere (AWS, GCP, Azure, etc.)
- **Separate Frontend/Backend** - For advanced setups

## 🎨 Features

- ✅ Real-time voice recording
- ✅ Speech-to-text transcription
- ✅ Context-aware AI responses
- ✅ Text-to-speech playback
- ✅ Conversation history
- ✅ Modern, responsive UI
- ✅ Error handling

## 🔮 Future Enhancements

- [ ] Streaming responses (AssemblyAI Realtime API)
- [ ] Multi-language support
- [ ] Custom AI personas
- [ ] Metrics dashboard (latency, token usage)
- [ ] Chat history persistence
- [ ] Voice activity detection (auto-start/stop)
- [ ] Multiple TTS voice options

## 🐛 Troubleshooting

### Microphone not working
- Check browser permissions for microphone access
- Ensure you're using HTTPS (required for microphone in most browsers)

### CORS errors
- Update `allow_origins` in `server.py` to your frontend URL
- Or use `["*"]` for development only

### API errors
- Verify your API keys are correct in `.env`
- Check API quotas/limits
- Review error messages in browser console and terminal

### Audio playback issues
- Ensure browser supports the audio format
- Check browser console for errors

## 📝 License

MIT License - feel free to use this project for your portfolio or learning!

## 🙏 Credits

- [AssemblyAI](https://www.assemblyai.com/) for speech-to-text
- [OpenAI](https://openai.com/) for GPT and TTS
- Built with [FastAPI](https://fastapi.tiangolo.com/)

