#!/bin/bash

# Quick deployment script for Voice Agent
# This script helps you prepare and deploy your voice agent

echo "🚀 Voice Agent Deployment Helper"
echo "================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "Creating .env from template..."
    cp env.template .env
    echo "✅ .env file created. Please add your API keys!"
    echo ""
    echo "Edit .env and add:"
    echo "  - ASSEMBLY_API_KEY"
    echo "  - OPENAI_API_KEY"
    echo ""
    read -p "Press Enter after you've added your API keys..."
fi

# Check if API keys are set
source .env 2>/dev/null || true

if [ -z "$ASSEMBLY_API_KEY" ] || [ "$ASSEMBLY_API_KEY" == "your_assemblyai_api_key_here" ]; then
    echo "❌ ASSEMBLY_API_KEY not set in .env"
    exit 1
fi

if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" == "your_openai_api_key_here" ]; then
    echo "❌ OPENAI_API_KEY not set in .env"
    exit 1
fi

echo "✅ API keys found"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit: Voice Agent"
    echo "✅ Git repository initialized"
    echo ""
    echo "⚠️  Don't forget to:"
    echo "  1. Create a repository on GitHub"
    echo "  2. Run: git remote add origin https://github.com/yourusername/voice-agent.git"
    echo "  3. Run: git push -u origin main"
    echo ""
fi

echo "🎉 You're ready to deploy!"
echo ""
echo "Choose a deployment option:"
echo "1. Render (Recommended) - Follow DEPLOYMENT.md"
echo "2. Railway - Follow DEPLOYMENT.md"
echo "3. Heroku - Follow DEPLOYMENT.md"
echo "4. Docker - Build with: docker build -t voice-agent ."
echo ""
echo "See DEPLOYMENT.md for detailed instructions!"

