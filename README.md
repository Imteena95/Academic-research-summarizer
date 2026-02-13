

---

# Academic Paper Summarizer

A full-stack application that allows users to upload academic papers in PDF format and receive AI-powered summaries using **Ollama (orca-mini model)** for local, privacy-friendly summarization.

## Features

- 📄 **PDF Upload**: Drag-and-drop or click to upload PDF files
- 🤖 **Local AI Summarization**: Uses Ollama with orca-mini model (no API keys needed, runs completely offline)
- 📊 **Multi-Level Summaries**: Choose between ELI5, Technical, or Expert level summaries
- 📑 **Section-Aware Parsing**: Automatically detects and summarizes paper sections (abstract, introduction, methodology, results, conclusion)
- 🔍 **arXiv Integration**: Fetch papers directly using arXiv IDs
- 🔗 **Related Work Suggestions**: Finds related papers based on keywords
- 🎨 **Modern UI**: Beautiful, responsive web interface with tabbed navigation
- ⚡ **Fast Processing**: Efficient text extraction and local AI processing

## Project Structure

```
Academic-research-summarizer/
├── main_advanced.py         # FastAPI backend with Ollama integration
├── index.html               # Frontend HTML/CSS/JavaScript
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
└── README.md                # This file
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- **Ollama** (local AI server) - Download from [https://ollama.ai](https://ollama.ai)

## Installation

### 1. Clone or navigate to the project directory
```bash
cd Academic-research-summarizer
```

### 2. Create a virtual environment (recommended)
```bash
# On Windows
python -m venv venv311
venv311\Scripts\activate

# On macOS/Linux
python3 -m venv venv311
source venv311/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install and set up Ollama
```bash
# Download Ollama from https://ollama.ai
# Then pull the orca-mini model
ollama pull orca-mini
```

### 5. Environment variables (optional)
Create a `.env` file if you need to customize settings:
```bash
cp .env.example .env
```

## Running the Application

### 1. Start Ollama (in a separate terminal)
```bash
ollama serve
```
Or ensure Ollama is running in the background.

### 2. Start the FastAPI backend
```bash
python main_advanced.py
```
The API will be available at `http://localhost:8001`

### 3. Open the frontend
Simply double-click `index.html` in your file explorer, or serve it with:
```bash
# Using Python
python -m http.server 8000
# Then visit http://localhost:8000
```

## Usage

1. **Upload a Paper**: Click the upload area or drag and drop a PDF file
2. **Or Fetch from arXiv**: Enter an arXiv ID (e.g., 2301.12345)
3. **Select Summary Level**: Choose between ELI5, Technical, or Expert
4. **Customize Options**: Toggle figures/tables and methodology recreation
5. **Click Summarize**: The backend processes the PDF and generates a section-aware summary
6. **Find Related Work**: Click "Find Related Papers" to discover similar research

## API Endpoints

### `POST /upload-paper`
Upload a PDF file for processing.

**Response:**
```json
{
  "status": "success",
  "paper_id": "filename",
  "title": "Paper Title",
  "authors": ["Author 1", "Author 2"],
  "sections": ["abstract", "introduction", "methodology"],
  "page_count": 10
}
```

### `POST /arxiv-paper?arxiv_id=2301.12345`
Fetch and process a paper from arXiv.

### `POST /summarize`
Generate a multi-level summary.

**Request Body:**
```json
{
  "paper_id": "filename",
  "summary_level": "technical",
  "include_figures": true,
  "include_methodology": true
}
```

### `GET /related-work/{paper_id}`
Find related papers based on keywords.

### `GET /health`
Health check endpoint.

## How It Works

1. **PDF Upload/arXiv Fetch**: User provides a PDF or arXiv ID
2. **Text Extraction**: PyPDF2 extracts all text from the PDF
3. **Section Parsing**: Regex patterns detect paper sections (abstract, introduction, methodology, etc.)
4. **Local AI Summarization**: Ollama (orca-mini) generates summaries at different complexity levels
5. **Display Results**: Summaries are shown in organized boxes by section
6. **Related Work**: Keyword extraction and arXiv search for similar papers

## Dependencies

- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI
- **PyPDF2**: PDF text extraction
- **arxiv**: arXiv API client for fetching papers
- **Requests**: HTTP requests for Ollama API
- **python-multipart**: File upload handling
- **python-dotenv**: Environment variable management

## Why Ollama?

This project uses **Ollama** instead of cloud-based APIs like Claude because:
- 🔒 **Privacy**: All processing happens locally - your papers never leave your computer
- 💰 **Free**: No API costs or usage limits
- 🚀 **Offline**: Works without internet connection
- 📚 **Academic Focus**: orca-mini model performs well on research content

## Troubleshooting

### "Ollama not found"
- Ensure Ollama is installed from [https://ollama.ai](https://ollama.ai)
- Run `ollama serve` to start the service
- Pull the model: `ollama pull orca-mini`

### "Port 8001 already in use"
- Change the port in `main_advanced.py` (last line)
- Or kill the existing process using the port

### "Only PDF files are allowed"
- Make sure you're uploading a valid PDF file

### "Could not extract text from PDF"
- The PDF may be image-based (scanned document)
- Try a different PDF with selectable text

### Module not found errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

## Future Enhancements

- [ ] Support for more AI models (Llama 2, Mistral)
- [ ] Batch processing multiple PDFs
- [ ] Summary export to PDF/Word
- [ ] Citation extraction and formatting
- [ ] User accounts and history
- [ ] Full-text search across papers
- [ ] Integration with more academic sources (IEEE, ACM)

## License

This project is open source and available for educational and research use.

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Local AI powered by [Ollama](https://ollama.ai/) and [orca-mini](https://ollama.ai/library/orca-mini)
- arXiv integration via [arxiv.py](https://github.com/lukasschwab/arxiv.py)

---
