from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import requests
import os
import time
from dotenv import load_dotenv
import io
from requests_toolbelt.multipart.encoder import MultipartEncoder

load_dotenv()

app = FastAPI(title="Voice-to-Voice AI Agent")

# Get frontend URL from environment or allow all for development
FRONTEND_URL = os.getenv("FRONTEND_URL", "*")
allowed_origins = [FRONTEND_URL] if FRONTEND_URL != "*" else ["*"]

# CORS middleware to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ASSEMBLY_API_KEY = os.getenv("ASSEMBLY_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not ASSEMBLY_API_KEY:
    raise ValueError("ASSEMBLY_API_KEY not found in environment variables")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Store conversation history (in production, use a database)
conversation_history = []


# Serve frontend static files
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")

@app.get("/api")
async def api_info():
    return {"message": "Voice-to-Voice AI Agent API", "status": "running"}

@app.get("/")
async def root():
    # Serve index.html from frontend directory
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Voice-to-Voice AI Agent API", "status": "running"}

# Mount static files after root route (serves CSS, JS, etc. if needed)
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")


@app.post("/talk")
async def talk(file: UploadFile = File(...)):
    """
    Main endpoint: Receives audio, transcribes it, gets GPT response, converts to speech
    """
    try:
        # 1. Upload audio to AssemblyAI
        audio_data = await file.read()
        
        # Validate audio data
        if not audio_data or len(audio_data) == 0:
            raise HTTPException(status_code=400, detail="Empty audio file received")
        
        upload_url = "https://api.assemblyai.com/v2/upload"
        headers = {"authorization": ASSEMBLY_API_KEY}
        
        # Use MultipartEncoder to ensure proper content-type is set
        # This explicitly sets the MIME type for the file part
        multipart_data = MultipartEncoder(
            fields={
                'file': ('recording.webm', audio_data, 'audio/webm')
            }
        )
        
        headers['Content-Type'] = multipart_data.content_type
        
        # Upload with properly formatted multipart data
        upload_resp = requests.post(
            upload_url,
            headers=headers,
            data=multipart_data,
            timeout=30
        )
        
        if upload_resp.status_code != 200:
            raise HTTPException(
                status_code=upload_resp.status_code,
                detail=f"AssemblyAI upload failed: {upload_resp.text}"
            )
        
        audio_url = upload_resp.json()['upload_url']
        
        # 2. Transcribe audio
        transcribe_url = "https://api.assemblyai.com/v2/transcript"
        transcribe_resp = requests.post(
            transcribe_url,
            json={"audio_url": audio_url},
            headers=headers
        )
        
        if transcribe_resp.status_code != 200:
            raise HTTPException(
                status_code=transcribe_resp.status_code,
                detail=f"AssemblyAI transcription failed: {transcribe_resp.text}"
            )
        
        transcript_id = transcribe_resp.json()['id']
        
        # Poll until transcription is complete
        max_attempts = 30
        attempt = 0
        while attempt < max_attempts:
            status_resp = requests.get(
                f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
                headers=headers
            )
            
            if status_resp.status_code != 200:
                raise HTTPException(
                    status_code=status_resp.status_code,
                    detail=f"Failed to get transcription status: {status_resp.text}"
                )
            
            status_data = status_resp.json()
            status = status_data.get('status')
            
            if status == 'completed':
                text = status_data.get('text', '')
                break
            elif status == 'error':
                raise HTTPException(
                    status_code=500,
                    detail=f"Transcription error: {status_data.get('error', 'Unknown error')}"
                )
            
            time.sleep(1)  # Wait 1 second before polling again
            attempt += 1
        else:
            raise HTTPException(
                status_code=408,
                detail="Transcription timeout - took too long to complete"
            )
        
        if not text:
            raise HTTPException(status_code=500, detail="Transcription returned empty text")
        
        # 3. Get response from GPT with conversation history
        messages = [
            {
                "role": "system",
                "content": "You are a friendly and helpful AI assistant. Keep your responses concise and conversational, suitable for voice interaction."
            }
        ]
        
        # Add conversation history
        messages.extend(conversation_history[-10:])  # Keep last 10 exchanges
        
        # Add current user message
        messages.append({"role": "user", "content": text})
        
        gpt_resp = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 300  # Keep responses concise for voice
            }
        )
        
        if gpt_resp.status_code != 200:
            raise HTTPException(
                status_code=gpt_resp.status_code,
                detail=f"OpenAI API error: {gpt_resp.text}"
            )
        
        gpt_data = gpt_resp.json()
        reply = gpt_data["choices"][0]["message"]["content"]
        
        # Update conversation history
        conversation_history.append({"role": "user", "content": text})
        conversation_history.append({"role": "assistant", "content": reply})
        
        # 4. Convert reply to speech using OpenAI TTS
        tts_resp = requests.post(
            "https://api.openai.com/v1/audio/speech",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "tts-1",
                "voice": "alloy",
                "input": reply
            }
        )
        
        if tts_resp.status_code != 200:
            raise HTTPException(
                status_code=tts_resp.status_code,
                detail=f"OpenAI TTS error: {tts_resp.text}"
            )
        
        # Return both text and audio
        audio_bytes = tts_resp.content
        
        return StreamingResponse(
            io.BytesIO(audio_bytes),
            media_type="audio/mpeg",
            headers={
                "X-Reply-Text": reply,
                "X-User-Text": text
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/reset")
async def reset_conversation():
    """Reset conversation history"""
    global conversation_history
    conversation_history = []
    return {"message": "Conversation history reset"}


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "assemblyai_configured": bool(ASSEMBLY_API_KEY),
        "openai_configured": bool(OPENAI_API_KEY)
    }

