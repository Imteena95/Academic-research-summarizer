from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import PyPDF2
import requests
from config import (
    UPLOAD_DIR,
    SUMMARY_LENGTHS,
    DEFAULT_SUMMARY_LENGTH,
    CORS_ORIGINS,
    CORS_CREDENTIALS,
    CORS_METHODS,
    CORS_HEADERS,
)

app = FastAPI(title="Academic Paper Summarizer")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_CREDENTIALS,
    allow_methods=CORS_METHODS,
    allow_headers=CORS_HEADERS,
)

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Ollama API endpoint (runs locally, completely free)
OLLAMA_API_URL = "http://localhost:11434/api/generate"


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file."""
    try:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            
            # Extract text from all pages
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")


def summarize_text(text: str, summary_length: str = DEFAULT_SUMMARY_LENGTH) -> str:
    """Summarize text using Ollama (free, local)."""
    try:
        length_prompt = SUMMARY_LENGTHS.get(summary_length, SUMMARY_LENGTHS[DEFAULT_SUMMARY_LENGTH])
        
        # Check if Ollama is running
        try:
            response = requests.post(
                OLLAMA_API_URL,
                json={
                    "model": "orca-mini",
                    "prompt": f"""Please summarize the following academic paper. {length_prompt}
                    
Focus on:
- Main research question/objective
- Methodology
- Key findings
- Conclusions and implications

Paper content:
{text[:3000]}""",  # Limit text to avoid timeout
                    "stream": False,
                    "temperature": 0.7,
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "Could not generate summary")
            else:
                raise Exception(f"Ollama API error: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            raise Exception(
                "Ollama is not running. Please install and start Ollama:\n"
                "1. Download from https://ollama.ai\n"
                "2. Install and run Ollama\n"
                "3. Run: ollama pull orca-mini\n"
                "4. Ollama will run on http://localhost:11434"
            )
            
    except Exception as e:
        raise Exception(f"Error summarizing text: {str(e)}")


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Academic Paper Summarizer API (Free - Using Ollama)"}


@app.post("/upload-and-summarize")
async def upload_and_summarize(file: UploadFile = File(...), summary_length: str = "medium"):
    """Upload PDF and get summary."""
    file_path = None
    try:
        # Validate file type
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Save uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, 'wb') as f:
            content = await file.read()
            f.write(content)
        
        # Extract text from PDF
        extracted_text = extract_text_from_pdf(file_path)
        
        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        # Summarize text
        summary = summarize_text(extracted_text, summary_length)
        
        # Clean up uploaded file
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        
        return JSONResponse({
            "status": "success",
            "filename": file.filename,
            "text_length": len(extracted_text),
            "summary": summary
        })
    
    except HTTPException:
        raise
    except Exception as e:
        # Clean up file if it exists
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
