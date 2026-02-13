"""
Configuration settings for Academic Paper Summarizer (Free Version)
Uses Ollama - completely free, runs locally
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Server Configuration
HOST = "0.0.0.0"
PORT = 8000
DEBUG = False

# File Upload Configuration
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {".pdf"}

# Summarization Configuration
SUMMARY_LENGTHS = {
    "short": "Provide a concise summary in 2-3 paragraphs.",
    "medium": "Provide a comprehensive summary in 4-6 paragraphs.",
    "long": "Provide a detailed summary in 8-10 paragraphs with key findings and conclusions."
}

DEFAULT_SUMMARY_LENGTH = "medium"

# CORS Configuration
CORS_ORIGINS = ["*"]
CORS_CREDENTIALS = True
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]

# Note: This version uses Ollama which is completely free and runs locally
# No API key needed!
