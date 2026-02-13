#!/usr/bin/env python3
"""
Academic Paper Summarizer - Startup Script
Handles environment setup and starts the FastAPI server
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def create_virtual_env():
    """Create virtual environment if it doesn't exist."""
    venv_path = Path("venv")
    if not venv_path.exists():
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✓ Virtual environment created")
    else:
        print("✓ Virtual environment already exists")

def activate_virtual_env():
    """Activate virtual environment."""
    if platform.system() == "Windows":
        activate_script = Path("venv/Scripts/activate.bat")
        if activate_script.exists():
            os.system(str(activate_script))
    else:
        activate_script = Path("venv/bin/activate")
        if activate_script.exists():
            os.system(f"source {activate_script}")

def install_dependencies():
    """Install required dependencies."""
    print("Checking dependencies...")
    try:
        import fastapi
        print("✓ Dependencies already installed")
    except ImportError:
        print("Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✓ Dependencies installed")

def check_env_file():
    """Check if .env file exists."""
    env_path = Path(".env")
    if not env_path.exists():
        print("\n⚠️  WARNING: .env file not found!")
        print("Please create a .env file with your ANTHROPIC_API_KEY")
        print("You can copy from .env.example and add your API key\n")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)

def start_server():
    """Start the FastAPI server."""
    print("\n" + "="*50)
    print("Starting Academic Paper Summarizer")
    print("="*50)
    print("\n✓ FastAPI server will be available at http://localhost:8000")
    print("✓ Frontend available at http://localhost:8001")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        sys.exit(0)

def main():
    """Main startup function."""
    print("\n" + "="*50)
    print("Academic Paper Summarizer - Setup")
    print("="*50 + "\n")
    
    create_virtual_env()
    install_dependencies()
    check_env_file()
    start_server()

if __name__ == "__main__":
    main()
