# 🎤 Voice-to-Voice AI Agent (Ollama Edition)

A full-stack conversational AI agent that enables natural voice-to-voice interactions using **Ollama** for free, local AI processing. Users speak into their microphone, the audio is transcribed, processed by a local Ollama model, and a voice response is generated and played back.

## 🏗️ Architecture

```
User speaks → AssemblyAI (STT) → Ollama (Local LLM) → Edge TTS → User hears reply
```

### Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML + JavaScript (vanilla)
- **Speech-to-Text**: AssemblyAI
- **Conversation Logic**: Ollama (Local LLM - llama3.2, mistral, etc.)
- **Text-to-Speech**: Microsoft Edge TTS (free)

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed
- API Key:
  - [AssemblyAI API Key](https://www.assemblyai.com/app/account) (for speech-to-text)

### Installation

#### Option 1: Automated Setup (Windows)

1. **Clone or navigate to the project directory**

2. **Run the setup script**
   ```powershell
   .\setup_ollama.ps1
   ```
   This script will:
   - Check if Ollama is installed
   - Download the llama3.2 model if needed
   - Install Python dependencies
   - Create .env file from template

3. **Edit .env file**
   Add your AssemblyAI API key:
   ```
   ASSEMBLY_API_KEY=your_assemblyai_key_here
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama3.2
   ```

4. **Start Ollama service** (if not auto-started)
   ```bash
   ollama serve
   ```

5. **Start the voice agent**
   ```bash
   uvicorn server:app --reload
   ```

#### Option 2: Manual Setup

1. **Install Ollama**
   - Download from: https://ollama.ai/
   - Install and restart your terminal

2. **Download a model**
   ```bash
   ollama pull llama3.2
   # or try: ollama pull mistral, ollama pull codellama
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.template .env
   ```
   Edit `.env` and configure:
   ```
   ASSEMBLY_API_KEY=your_assemblyai_key_here
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama3.2
   FRONTEND_URL=*
   ```

5. **Start Ollama service**
   ```bash
   ollama serve
   ```

6. **Start the backend server**
   ```bash
   uvicorn server:app --reload
   ```
   The API will be available at `http://localhost:8000`

7. **Open the frontend**
   Navigate to `http://localhost:8000` in your browser

8. **Test it out!**
   - Click "Start Recording"
   - Speak into your microphone
   - Click "Stop Recording"
   - Wait for the AI response

## 📁 Project Structure

```
VoiceAgent/
├── server.py              # FastAPI backend (Ollama integration)
├── requirements.txt       # Python dependencies (includes edge-tts)
├── setup_ollama.ps1      # Automated setup script (Windows)
├── env.template          # Environment variables template
├── .env                  # Your actual configuration (not in git)
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

**Response**: Audio stream (MPEG) or JSON fallback
- Audio Headers:
  - `X-Reply-Text`: The text response from Ollama
  - `X-User-Text`: The transcribed user input
- JSON fallback (if TTS fails):
  ```json
  {
    "user_text": "What you said",
    "reply_text": "AI response",
    "message": "Status message"
  }
  ```

### `GET /health`
Health check endpoint.

**Response**: JSON
```json
{
  "status": "healthy",
  "assemblyai_configured": true,
  "ollama_configured": true,
  "ollama_base_url": "http://localhost:11434",
  "ollama_model": "llama3.2"
}
```

### `POST /reset`
Reset conversation history.

**Response**: JSON
```json
{"message": "Conversation history reset"}
```

## 🎯 How It Works

### 1. Speech-to-Text (AssemblyAI)
- User records audio via browser microphone
- Audio is sent to backend as a blob
- Backend uploads audio to AssemblyAI
- AssemblyAI transcribes the audio to text

### 2. Conversation Logic (Ollama)
- Transcribed text is sent to local Ollama instance
- Ollama processes the request using your chosen model (llama3.2, mistral, etc.)
- Response is generated locally on your machine
- Conversation history is maintained for context

### 3. Text-to-Speech (Microsoft Edge TTS)
- Ollama response is converted to speech using Edge TTS (free)
- Audio is streamed back to frontend
- Frontend plays the audio response

## 🤖 Available Models

Popular Ollama models you can use:

- **llama3.2** (default) - Good balance of quality and speed
- **llama3.1** - Larger, more capable model
- **mistral** - Fast and efficient
- **codellama** - Specialized for coding tasks
- **phi** - Microsoft's small but capable model

To switch models:
1. Download the model: `ollama pull model_name`
2. Update your `.env` file: `OLLAMA_MODEL=model_name`
3. Restart the server

## 💰 Cost Comparison

### This Ollama Setup
- **Ollama**: FREE (runs locally)
- **AssemblyAI**: ~$0.37/hour of audio
- **Edge TTS**: FREE
- **Total**: ~$0.37/hour

### Original OpenAI Setup
- **OpenAI GPT-4o-mini**: ~$0.15 per 1M tokens
- **OpenAI TTS**: ~$15 per 1M characters
- **AssemblyAI**: ~$0.37/hour of audio
- **Total**: Varies, but TTS can be expensive

## 🚢 Deployment

**Note**: Deploying Ollama requires more resources than typical cloud free tiers.

### Local Development (Recommended)
- Perfect for development, testing, and personal use
- No API costs for LLM (only AssemblyAI for STT)
- Full privacy - everything runs locally

### Cloud Deployment Options
1. **VPS with Ollama** - DigitalOcean, Linode, AWS EC2
2. **GPU Instances** - For faster model inference
3. **Hybrid** - Backend on cloud, Ollama locally (modify OLLAMA_BASE_URL)

## 🎨 Features

- ✅ Real-time voice recording
- ✅ Speech-to-text transcription (AssemblyAI)
- ✅ **Local LLM processing (Ollama)**
- ✅ **Free text-to-speech (Edge TTS)**
- ✅ Context-aware AI responses
- ✅ Conversation history
- ✅ Modern, responsive UI
- ✅ Error handling and fallbacks
- ✅ **Privacy-focused (LLM runs locally)**
- ✅ **Cost-effective (minimal API usage)**

## 🔮 Future Enhancements

- [ ] Model switching UI
- [ ] Streaming responses from Ollama
- [ ] Custom model fine-tuning
- [ ] Voice activity detection
- [ ] Multiple TTS voice options
- [ ] Conversation export/import
- [ ] Multi-language support
- [ ] Docker containerization

## 🐛 Troubleshooting

### Ollama Issues
- **Ollama not responding**: Check if `ollama serve` is running
- **Model not found**: Run `ollama pull llama3.2` to download
- **Port conflicts**: Change OLLAMA_BASE_URL in .env if using different port

### Performance Issues
- **Slow responses**: Try smaller models like `phi` or `mistral`
- **Memory issues**: Monitor RAM usage, consider smaller models
- **CPU usage**: Ollama uses CPU by default, consider GPU setup for faster inference

### General Issues
- **Microphone not working**: Check browser permissions
- **TTS not working**: Check if edge-tts is installed: `pip install edge-tts`
- **API errors**: Verify AssemblyAI key is correct

## 🔒 Privacy & Security

- **LLM Processing**: 100% local, nothing sent to external services
- **Speech-to-Text**: Uses AssemblyAI (audio sent to their servers)
- **Text-to-Speech**: Uses Microsoft Edge TTS (text sent to Microsoft)
- **Conversation History**: Stored locally in memory (resets on restart)

## 📝 License

MIT License - feel free to use this project for your portfolio or learning!

## 🙏 Credits

- [Ollama](https://ollama.ai/) for local LLM hosting
- [AssemblyAI](https://www.assemblyai.com/) for speech-to-text
- [Microsoft Edge TTS](https://github.com/rany2/edge-tts) for text-to-speech
- Built with [FastAPI](https://fastapi.tiangolo.com/)