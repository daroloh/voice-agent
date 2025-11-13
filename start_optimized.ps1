# Memory-Optimized Ollama Voice Agent Startup Script

Write-Host "Starting Memory-Optimized Voice Agent" -ForegroundColor Green

# Set memory optimization environment variables
$env:OLLAMA_NUM_PARALLEL = "1"
$env:OLLAMA_MAX_LOADED_MODELS = "1" 
$env:OLLAMA_KEEP_ALIVE = "0"

Write-Host "Memory optimization settings applied" -ForegroundColor Green
Write-Host "OLLAMA_NUM_PARALLEL = 1" -ForegroundColor Yellow
Write-Host "OLLAMA_MAX_LOADED_MODELS = 1" -ForegroundColor Yellow
Write-Host "OLLAMA_KEEP_ALIVE = 0 (unload after use)" -ForegroundColor Yellow

# Start the voice agent
Write-Host "Starting Voice Agent Server..." -ForegroundColor Green
python -m uvicorn server:app --reload --port 8000