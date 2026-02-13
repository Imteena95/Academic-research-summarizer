@echo off
REM Academic Paper Summarizer - Startup Script for Windows

echo.
echo ========================================
echo Academic Paper Summarizer
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo Dependencies installed.
) else (
    echo Dependencies already installed.
)

REM Check for .env file
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Please create a .env file with your ANTHROPIC_API_KEY
    echo You can copy from .env.example and add your API key
    echo.
    pause
)

REM Start the FastAPI server
echo.
echo Starting FastAPI server...
echo Server will be available at http://localhost:8000
echo Frontend will be available at http://localhost:8001
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py
