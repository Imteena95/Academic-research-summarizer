# Academic Paper Summarizer

A full-stack application that allows users to upload academic papers in PDF format and receive AI-powered summaries using Claude API.

## Features

- 📄 **PDF Upload**: Drag-and-drop or click to upload PDF files
- 🤖 **AI Summarization**: Uses Claude 3.5 Sonnet for intelligent summarization
- 📊 **Flexible Summary Lengths**: Choose between short, medium, or long summaries
- 🎨 **Modern UI**: Beautiful, responsive web interface
- ⚡ **Fast Processing**: Efficient text extraction and API integration
- 📋 **Copy to Clipboard**: Easily copy summaries for use elsewhere

## Project Structure

```
Academic-research-summarizer/
├── main.py                 # FastAPI backend application
├── index.html             # Frontend HTML/CSS/JavaScript
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Anthropic API key (get it from https://console.anthropic.com)

## Installation

### 1. Clone or navigate to the project directory

```bash
cd Academic-research-summarizer
```

### 2. Create a virtual environment (recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=your_actual_api_key_here
```

## Running the Application

### 1. Start the FastAPI backend

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### 2. Open the frontend

Open `index.html` in your web browser or serve it with a local server:

```bash
# Using Python 3
python -m http.server 8001

# Then visit http://localhost:8001
```

Or simply double-click `index.html` to open it directly in your browser.

## Usage

1. **Upload a PDF**: Click the upload area or drag and drop a PDF file
2. **Select Summary Length**: Choose between Short, Medium, or Long
3. **Click Summarize**: The backend will process the PDF and generate a summary
4. **Copy Summary**: Use the copy button to copy the summary to your clipboard

## API Endpoints

### POST `/upload-and-summarize`

Upload a PDF and get a summary.

**Parameters:**
- `file` (FormData): PDF file to upload
- `summary_length` (query): "short", "medium", or "long" (default: "medium")

**Response:**
```json
{
  "status": "success",
  "filename": "paper.pdf",
  "text_length": 5000,
  "summary": "The paper discusses..."
}
```

### GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## How It Works

1. **PDF Upload**: User uploads a PDF file through the web interface
2. **Text Extraction**: PyPDF2 extracts all text from the PDF
3. **Summarization**: Claude API processes the extracted text and generates a summary
4. **Display**: Summary is displayed in the web interface
5. **Cleanup**: Temporary files are automatically deleted

## Dependencies

- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI
- **PyPDF2**: PDF text extraction
- **Anthropic**: Claude API client
- **python-dotenv**: Environment variable management
- **python-multipart**: File upload handling

## Error Handling

The application includes comprehensive error handling for:
- Invalid file types (non-PDF files)
- Empty PDFs or PDFs with no extractable text
- API errors
- File system errors

## Limitations

- Maximum file size depends on your system's available memory
- Very large PDFs may take longer to process
- API rate limits apply based on your Anthropic account

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
- Ensure you've created a `.env` file with your API key
- Verify the key is correct and has proper permissions

### "Only PDF files are allowed"
- Make sure you're uploading a valid PDF file
- Check that the file extension is `.pdf`

### "Could not extract text from PDF"
- The PDF may be image-based (scanned document)
- Try a different PDF with selectable text

### CORS errors
- The backend is configured to accept requests from any origin
- If issues persist, check that the backend is running on `http://localhost:8000`

## Future Enhancements

- Support for multiple file formats (DOCX, TXT, etc.)
- Batch processing for multiple PDFs
- Summary export to PDF or Word
- Custom summarization prompts
- User authentication and history
- Database integration for storing summaries

## License

This project is open source and available for educational and commercial use.

## Support

For issues or questions, please check the error messages in the browser console and terminal output for debugging information.
