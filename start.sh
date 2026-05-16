#!/bin/bash

echo "🌀 Starting Vortex Programming Language Web IDE..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not installed. Please install pip."
    exit 1
fi

echo "✓ pip found"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed"

# Check if Vortex parser exists
if [ ! -d "../Vortex-Programming-Language/python_parser" ]; then
    echo ""
    echo "⚠️  Warning: Vortex parser not found in expected location"
    echo "   Expected: ../Vortex-Programming-Language/python_parser"
    echo "   Please ensure the Vortex-Programming-Language directory is in the parent folder"
    echo ""
fi

# Start the server
echo ""
echo "🚀 Starting Flask server..."
echo "📍 Server will be available at: http://localhost:5000"
echo "🌐 Network access: http://$(hostname -I | awk '{print $1}'):5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
