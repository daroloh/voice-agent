from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import requests
import os
import time
from dotenv import load_dotenv
import io

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
        
        # Determine content type from uploaded file
        content_type = file.content_type or "audio/webm"
        
        # Normalize content type - remove codec info if present
        if ';' in content_type:
            content_type = content_type.split(';')[0]
        
        # Ensure we use a supported type - default to webm
        if content_type not in ['audio/webm', 'audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/mp4']:
            content_type = "audio/webm"
        
        # Try uploading as raw binary with explicit Content-Type header
        # This is AssemblyAI's preferred method for direct file uploads
        headers = {
            "authorization": ASSEMBLY_API_KEY,
            "content-type": content_type
        }
        
        print(f"Uploading to AssemblyAI: {len(audio_data)} bytes, content-type: {content_type}")
        
        # Upload as raw binary data (not multipart)
        upload_resp = requests.post(
            upload_url,
            headers=headers,
            data=audio_data,
            timeout=30
        )
        
        if upload_resp.status_code != 200:
            error_detail = upload_resp.text
            print(f"AssemblyAI upload failed: Status {upload_resp.status_code}, Response: {error_detail}")
            raise HTTPException(
                status_code=upload_resp.status_code,
                detail=f"AssemblyAI upload failed: {error_detail}"
            )
        
        # Parse response JSON
        try:
            upload_response_json = upload_resp.json()
            audio_url = upload_response_json.get('upload_url')
            if not audio_url:
                raise HTTPException(
                    status_code=500,
                    detail=f"AssemblyAI upload succeeded but no upload_url in response: {upload_response_json}"
                )
        except ValueError as e:
            print(f"Failed to parse AssemblyAI upload response: {upload_resp.text}")
            raise HTTPException(
                status_code=500,
                detail=f"Invalid response from AssemblyAI: {upload_resp.text[:200]}"
            )
        
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
                error_msg = status_data.get('error', 'Unknown error')
                print(f"AssemblyAI transcription error: {error_msg}")
                print(f"Full status data: {status_data}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Transcription error: {error_msg}"
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
        import traceback
        error_trace = traceback.format_exc()
        print(f"Unhandled exception in /talk endpoint: {str(e)}")
        print(f"Traceback: {error_trace}")
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)}"
        )


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

