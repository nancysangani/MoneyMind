#!/bin/bash

echo "🚀 MoneyMind CLI - Quick Start"
echo "================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

echo "✅ Python 3 found"

# Check Ollama
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama not found. Installing..."
    echo ""
    echo "Visit: https://ollama.com"
    echo "Or run: brew install ollama (Mac)"
    echo ""
    read -p "Press Enter after installing Ollama..."
fi

echo "✅ Ollama found"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install ollama --break-system-packages --quiet

# Pull model
echo ""
echo "📥 Downloading AI model (Llama 3.2)..."
echo "This may take a few minutes..."
ollama pull llama3.2

# Check if Ollama is running
if ! curl -s http://localhost:11434 > /dev/null; then
    echo ""
    echo "⚠️  Ollama server not running. Starting..."
    echo "Opening new terminal for Ollama server..."
    
    # Start Ollama in background (platform specific)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        osascript -e 'tell app "Terminal" to do script "ollama serve"'
    else
        # Linux
        ollama serve &
    fi
    
    echo "Waiting for server to start..."
    sleep 3
fi

echo "✅ Ollama server running"

# Setup MoneyMind
echo ""
echo "⚙️  Setting up MoneyMind directories..."
python3 moneymind.py setup

# Create demo data
echo ""
read -p "Create demo data in Downloads? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 demo_data_generator.py
    echo "✅ Demo data created"
fi

echo ""
echo "🎉 Setup Complete!"
echo ""
echo "Try these commands:"
echo "  python3 moneymind.py organize    # Organize financial documents"
echo "  python3 moneymind.py audit       # Audit subscriptions"
echo "  python3 moneymind.py dashboard   # Generate dashboard"
echo ""
echo "💎 MoneyMind - Your AI Financial Analyst"