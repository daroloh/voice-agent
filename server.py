from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import requests
import os
import time
from dotenv import load_dotenv
import io
import asyncio
import edge_tts

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
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

if not ASSEMBLY_API_KEY:
    raise ValueError("ASSEMBLY_API_KEY not found in environment variables")

# Store conversation history (in production, use a database)
conversation_history = []


def generate_fallback_response(user_input):
    """Generate simple rule-based responses when Ollama is unavailable"""
    user_lower = user_input.lower()
    
    if "hello" in user_lower or "hi" in user_lower:
        return "Hello! Nice to meet you. I'm currently running in fallback mode, but I can still chat with you!"
    elif "how are you" in user_lower:
        return "I'm doing well, thank you for asking! How are you doing today?"
    elif "weather" in user_lower:
        return "I don't have access to current weather data, but I hope it's nice where you are!"
    elif "name" in user_lower:
        return "I'm your voice AI assistant, currently running in simple mode while we work on the main AI model."
    elif "time" in user_lower or "date" in user_lower:
        import datetime
        now = datetime.datetime.now()
        return f"It's currently {now.strftime('%I:%M %p')} on {now.strftime('%B %d, %Y')}."
    elif "thank" in user_lower:
        return "You're very welcome! I'm happy to help."
    elif "bye" in user_lower or "goodbye" in user_lower:
        return "Goodbye! It was great talking with you. Have a wonderful day!"
    else:
        return f"I heard you say: '{user_input}'. I'm currently in simple response mode, but your voice recognition is working perfectly! The AI model will be available once we resolve the memory issue."


def generate_smart_response(user_input, conversation_history):
    """Generate intelligent responses using pattern matching and context"""
    user_lower = user_input.lower()
    
    # Greetings
    if any(word in user_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]):
        return "Hello there! It's great to hear from you. What would you like to talk about today?"
    
    # How are you / feelings
    elif any(phrase in user_lower for phrase in ["how are you", "how's it going", "how do you feel"]):
        return "I'm doing wonderfully, thank you for asking! I'm excited to chat with you. How has your day been going?"
    
    # Questions about the assistant
    elif any(word in user_lower for word in ["who are you", "what are you", "your name"]):
        return "I'm your AI voice assistant! I can chat with you, answer questions, and help with various topics. What would you like to know?"
    
    # Time and date
    elif any(word in user_lower for word in ["time", "date", "day", "clock"]):
        import datetime
        now = datetime.datetime.now()
        day_part = "morning" if now.hour < 12 else "afternoon" if now.hour < 18 else "evening"
        return f"It's {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d, %Y')}. Good {day_part}!"
    
    # Weather
    elif "weather" in user_lower:
        return "I don't have access to live weather data right now, but I'd love to chat about other topics! Is there anything else I can help you with?"
    
    # Thanks
    elif any(word in user_lower for word in ["thank", "thanks", "appreciate"]):
        return "You're absolutely welcome! I'm here to help and I'm glad I could assist you. Is there anything else you'd like to talk about?"
    
    # Goodbye
    elif any(word in user_lower for word in ["bye", "goodbye", "see you", "farewell"]):
        return "It's been wonderful talking with you! Take care and have a fantastic rest of your day. See you next time!"
    
    # Help or questions
    elif any(word in user_lower for word in ["help", "what can you do", "assist"]):
        return "I can chat with you about various topics, answer questions, help with planning, or just have a friendly conversation. What would you like to explore together?"
    
    # Personal questions
    elif any(phrase in user_lower for phrase in ["tell me about", "what do you think", "your opinion"]):
        return "That's an interesting topic! I'd love to discuss it with you. Could you tell me more about what specifically interests you about this?"
    
    # Compliments
    elif any(word in user_lower for word in ["great", "awesome", "amazing", "wonderful", "fantastic"]):
        return "Thank you so much! That's very kind of you to say. I'm really enjoying our conversation too!"
    
    # Questions (who, what, where, when, why, how)
    elif any(user_lower.startswith(word) for word in ["who", "what", "where", "when", "why", "how"]):
        return f"That's a great question about '{user_input}'. While I don't have access to live data right now, I'd be happy to discuss this topic with you. What's your take on it?"
    
    # Default intelligent response
    else:
        # Try to be contextual based on conversation history
        if len(conversation_history) > 0:
            return f"Interesting point about '{user_input}'. I can see we're having a nice conversation! What else would you like to explore together?"
        else:
            return f"Thank you for sharing that with me. '{user_input}' sounds like an interesting topic. I'm currently running in smart fallback mode - while I can't access external AI models right now, I'm here to chat and help however I can!"


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
        
        # 3. Get response from Ollama with conversation history
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
        
        # Try Ollama first with optimized settings, fallback if it fails
        try:
            ollama_resp = requests.post(
                f"{OLLAMA_BASE_URL}/api/chat",
                headers={
                    "Content-Type": "application/json"
                },
                json={
                    "model": OLLAMA_MODEL,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 150,  # Shorter responses for voice
                        "num_ctx": 1024,     # Smaller context window
                    },
                    "keep_alive": "0"  # Unload model after use to save memory
                },
                timeout=15
            )
            
            if ollama_resp.status_code == 200:
                ollama_data = ollama_resp.json()
                reply = ollama_data["message"]["content"]
                print(f"✅ Ollama response: {reply[:50]}...")
            else:
                print(f"Ollama error: {ollama_resp.text}")
                reply = generate_smart_response(text, conversation_history)
                
        except Exception as e:
            print(f"Ollama connection failed: {e}")
            reply = generate_smart_response(text, conversation_history)
        
        # Update conversation history
        conversation_history.append({"role": "user", "content": text})
        conversation_history.append({"role": "assistant", "content": reply})
        
        # 4. For now, return text-only response due to TTS issues
        # TODO: Fix Edge TTS permission issue
        try:
            # Try Edge TTS but fallback gracefully
            communicate = edge_tts.Communicate(reply, "en-US-AriaNeural")
            audio_data = b""
            
            # Get audio data with timeout
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            
            if audio_data and len(audio_data) > 1024:
                # Return audio response
                return StreamingResponse(
                    io.BytesIO(audio_data),
                    media_type="audio/mpeg",
                    headers={
                        "X-Reply-Text": reply,
                        "X-User-Text": text
                    }
                )
        except Exception as tts_error:
            print(f"TTS Error: {tts_error}")
        
        # Fallback: Return a minimal audio response with text in headers
        # Create a tiny silent audio file (1 second of silence)
        import struct
        sample_rate = 16000
        duration = 0.1  # 0.1 seconds
        samples = int(sample_rate * duration)
        silence = struct.pack('<' + ('h' * samples), *([0] * samples))
        
        return StreamingResponse(
            io.BytesIO(silence),
            media_type="audio/wav",
            headers={
                "X-Reply-Text": reply,
                "X-User-Text": text,
                "X-TTS-Status": "fallback-silent-audio"
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
    # Check if Ollama is available
    ollama_available = False
    try:
        ollama_resp = requests.get(f"{OLLAMA_BASE_URL}/api/version", timeout=5)
        ollama_available = ollama_resp.status_code == 200
    except:
        pass
    
    return {
        "status": "healthy",
        "assemblyai_configured": bool(ASSEMBLY_API_KEY),
        "ollama_configured": ollama_available,
        "ollama_base_url": OLLAMA_BASE_URL,
        "ollama_model": OLLAMA_MODEL
    }

