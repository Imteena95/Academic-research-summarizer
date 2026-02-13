"""
Test script to verify the Academic Paper Summarizer setup
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8 or higher."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor} - FAILED (requires 3.8+)")
        return False

def check_dependencies():
    """Check if all required dependencies are installed."""
    print("\nChecking dependencies...")
    dependencies = {
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'PyPDF2': 'PyPDF2',
        'anthropic': 'Anthropic',
        'dotenv': 'python-dotenv',
    }
    
    all_installed = True
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"✓ {name} - OK")
        except ImportError:
            print(f"✗ {name} - NOT INSTALLED")
            all_installed = False
    
    return all_installed

def check_env_file():
    """Check if .env file exists and has API key."""
    print("\nChecking environment configuration...")
    env_path = Path(".env")
    
    if not env_path.exists():
        print("✗ .env file - NOT FOUND")
        print("  Create .env file with: ANTHROPIC_API_KEY=your_key_here")
        return False
    
    with open(env_path, 'r') as f:
        content = f.read()
        if 'ANTHROPIC_API_KEY' in content and 'your_api_key_here' not in content:
            print("✓ .env file - OK")
            return True
        else:
            print("✗ .env file - ANTHROPIC_API_KEY not configured")
            return False

def check_files():
    """Check if all required files exist."""
    print("\nChecking project files...")
    required_files = [
        'main.py',
        'config.py',
        'index.html',
        'requirements.txt',
        'README.md',
    ]
    
    all_exist = True
    for file in required_files:
        if Path(file).exists():
            print(f"✓ {file} - OK")
        else:
            print(f"✗ {file} - NOT FOUND")
            all_exist = False
    
    return all_exist

def main():
    """Run all checks."""
    print("="*50)
    print("Academic Paper Summarizer - Setup Verification")
    print("="*50)
    
    checks = [
        ("Python Version", check_python_version()),
        ("Dependencies", check_dependencies()),
        ("Environment File", check_env_file()),
        ("Project Files", check_files()),
    ]
    
    print("\n" + "="*50)
    print("Summary")
    print("="*50)
    
    all_passed = True
    for check_name, result in checks:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{check_name}: {status}")
        if not result:
            all_passed = False
    
    print("="*50)
    
    if all_passed:
        print("\n✓ All checks passed! You're ready to run the application.")
        print("\nStart the server with:")
        print("  python main.py")
        print("\nThen open index.html in your browser.")
        return 0
    else:
        print("\n✗ Some checks failed. Please fix the issues above.")
        print("\nFor help, see QUICKSTART.md or README.md")
        return 1

if __name__ == "__main__":
    sys.exit(main())
