# Voice Agent Ollama Setup Script
# This script helps set up the voice agent to work with Ollama

Write-Host "Voice Agent Ollama Setup" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# Check if Ollama is installed
Write-Host "Checking if Ollama is installed..." -ForegroundColor Yellow
try {
    $ollamaVersion = ollama --version
    Write-Host "Ollama is installed: $ollamaVersion" -ForegroundColor Green
} catch {
    Write-Host "Ollama is not installed!" -ForegroundColor Red
    Write-Host "Please install Ollama from: https://ollama.ai/" -ForegroundColor Red
    Write-Host "After installation, restart your terminal and run this script again." -ForegroundColor Red
    exit 1
}

# Check if Ollama service is running
Write-Host "Checking if Ollama service is running..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:11434/api/version" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "Ollama service is running" -ForegroundColor Green
    }
} catch {
    Write-Host "Ollama service is not running!" -ForegroundColor Red
    Write-Host "Please start Ollama service by running: ollama serve" -ForegroundColor Yellow
    Write-Host "Or it might start automatically depending on your installation." -ForegroundColor Yellow
}

# Check if llama3.2 model is available
Write-Host "Checking for llama3.2 model..." -ForegroundColor Yellow
$models = ollama list
if ($models -match "llama3.2") {
    Write-Host "llama3.2 model is available" -ForegroundColor Green
} else {
    Write-Host "llama3.2 model not found. Downloading..." -ForegroundColor Yellow
    Write-Host "This may take a while depending on your internet connection..." -ForegroundColor Yellow
    ollama pull llama3.2
    if ($LASTEXITCODE -eq 0) {
        Write-Host "llama3.2 model downloaded successfully" -ForegroundColor Green
    } else {
        Write-Host "Failed to download llama3.2 model" -ForegroundColor Red
    }
}

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
try {
    pip install -r requirements.txt
    Write-Host "Python dependencies installed successfully" -ForegroundColor Green
} catch {
    Write-Host "Failed to install Python dependencies" -ForegroundColor Red
    Write-Host "Please make sure Python and pip are installed and in your PATH" -ForegroundColor Red
}

# Check if .env file exists
Write-Host "Checking environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host ".env file exists" -ForegroundColor Green
} else {
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item "env.template" ".env"
    Write-Host ".env file created from template" -ForegroundColor Green
    Write-Host "Please edit .env file and add your AssemblyAI API key" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Edit .env file and add your AssemblyAI API key" -ForegroundColor White
Write-Host "2. Make sure Ollama service is running (ollama serve)" -ForegroundColor White
Write-Host "3. Start the voice agent: python server.py" -ForegroundColor White
Write-Host ""
Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "- Language Model: Ollama (llama3.2)" -ForegroundColor White
Write-Host "- Speech-to-Text: AssemblyAI" -ForegroundColor White
Write-Host "- Text-to-Speech: Microsoft Edge TTS (free)" -ForegroundColor White
Write-Host ""
Write-Host "Test your setup by visiting: http://localhost:8000/health" -ForegroundColor White