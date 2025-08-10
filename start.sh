#!/bin/bash

echo "🚀 Starting Trustpilot Email Scraper..."
echo "📦 Installing dependencies..."

# Install Python dependencies
pip install -r requirements.txt

echo "✅ Dependencies installed!"
echo "🌐 Starting web application..."
echo "📱 Open your browser and go to: http://localhost:5000"
echo "⏹️  Press Ctrl+C to stop the application"

# Start the Flask application
python app.py
