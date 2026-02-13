# API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
No authentication required. Secure your API key in the `.env` file.

---

## Endpoints

### 1. Health Check

**Endpoint:** `GET /health`

**Description:** Check if the API is running and healthy.

**Request:**
```bash
curl http://localhost:8000/health
```

**Response (200 OK):**
```json
{
  "status": "healthy"
}
```

---

### 2. Root Endpoint

**Endpoint:** `GET /`

**Description:** Get API information.

**Request:**
```bash
curl http://localhost:8000/
```

**Response (200 OK):**
```json
{
  "message": "Academic Paper Summarizer API"
}
```

---

### 3. Upload and Summarize

**Endpoint:** `POST /upload-and-summarize`

**Description:** Upload a PDF file and receive an AI-generated summary.

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | File | Yes | PDF file to upload |
| summary_length | String | No | Summary length: "short", "medium", or "long" (default: "medium") |

**Request Example (cURL):**
```bash
curl -X POST http://localhost:8000/upload-and-summarize \
  -F "file=@paper.pdf" \
  -F "summary_length=medium"
```

**Request Example (Python):**
```python
import requests

with open('paper.pdf', 'rb') as f:
    files = {'file': f}
    data = {'summary_length': 'medium'}
    response = requests.post(
        'http://localhost:8000/upload-and-summarize',
        files=files,
        data=data
    )
    print(response.json())
```

**Request Example (JavaScript):**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('summary_length', 'medium');

fetch('http://localhost:8000/upload-and-summarize', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

**Response (200 OK):**
```json
{
  "status": "success",
  "filename": "research_paper.pdf",
  "text_length": 15234,
  "summary": "This paper investigates the effects of machine learning on natural language processing. The authors propose a novel approach using transformer-based architectures... [full summary]"
}
```

**Response (400 Bad Request):**
```json
{
  "detail": "Only PDF files are allowed"
}
```

or

```json
{
  "detail": "Could not extract text from PDF"
}
```

**Response (500 Internal Server Error):**
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Summary Length Options

### Short
- **Length:** 2-3 paragraphs
- **Use Case:** Quick overview
- **Processing Time:** ~10-15 seconds

### Medium (Default)
- **Length:** 4-6 paragraphs
- **Use Case:** Comprehensive summary
- **Processing Time:** ~15-25 seconds

### Long
- **Length:** 8-10 paragraphs
- **Use Case:** Detailed analysis with findings
- **Processing Time:** ~25-40 seconds

---

## Error Codes

| Code | Error | Description |
|------|-------|-------------|
| 200 | Success | Request processed successfully |
| 400 | Bad Request | Invalid file type or empty PDF |
| 500 | Internal Server Error | Server error during processing |

---

## Rate Limiting

Currently no rate limiting is implemented. For production, consider adding:
- Per-IP rate limiting
- Per-API-key rate limiting
- Request queuing

---

## File Upload Specifications

**Supported Format:** PDF (.pdf)

**Maximum File Size:** 50 MB (configurable in `config.py`)

**Validation:**
- File extension must be `.pdf`
- File must contain extractable text
- Empty PDFs will be rejected

---

## Response Format

All responses are in JSON format with the following structure:

**Success Response:**
```json
{
  "status": "success",
  "filename": "string",
  "text_length": "integer",
  "summary": "string"
}
```

**Error Response:**
```json
{
  "detail": "string"
}
```

---

## CORS Headers

The API includes CORS headers for cross-origin requests:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: *
```

---

## Request/Response Examples

### Example 1: Successful Summary

**Request:**
```bash
curl -X POST http://localhost:8000/upload-and-summarize \
  -F "file=@machine_learning.pdf" \
  -F "summary_length=short"
```

**Response:**
```json
{
  "status": "success",
  "filename": "machine_learning.pdf",
  "text_length": 8542,
  "summary": "This paper presents a novel deep learning architecture for image classification. The authors introduce a new attention mechanism that improves accuracy by 15% compared to baseline models. The proposed method is evaluated on standard benchmarks and shows promising results."
}
```

### Example 2: Invalid File Type

**Request:**
```bash
curl -X POST http://localhost:8000/upload-and-summarize \
  -F "file=@document.txt"
```

**Response:**
```json
{
  "detail": "Only PDF files are allowed"
}
```

### Example 3: Empty PDF

**Request:**
```bash
curl -X POST http://localhost:8000/upload-and-summarize \
  -F "file=@empty.pdf"
```

**Response:**
```json
{
  "detail": "Could not extract text from PDF"
}
```

---

## Performance Metrics

### Average Response Times
- Small PDF (< 5 pages): 10-15 seconds
- Medium PDF (5-20 pages): 15-30 seconds
- Large PDF (> 20 pages): 30-60 seconds

### Factors Affecting Performance
- PDF file size
- Number of pages
- Text complexity
- API response time
- Network latency

---

## Best Practices

1. **Error Handling:** Always check the response status
2. **Timeouts:** Set appropriate request timeouts (60+ seconds)
3. **File Validation:** Validate files before uploading
4. **Retry Logic:** Implement retry logic for failed requests
5. **Logging:** Log all API interactions for debugging

---

## Troubleshooting

### "Only PDF files are allowed"
- Ensure file has `.pdf` extension
- Verify file is a valid PDF

### "Could not extract text from PDF"
- PDF might be image-based (scanned)
- Try a different PDF with selectable text

### Timeout Error
- PDF might be too large
- Network connection might be slow
- Increase timeout value

### API Key Error
- Verify `ANTHROPIC_API_KEY` is set in `.env`
- Check API key is valid
- Restart server after updating `.env`

---

## Integration Examples

### Python Integration
```python
import requests
import json

def summarize_paper(pdf_path, length='medium'):
    with open(pdf_path, 'rb') as f:
        files = {'file': f}
        data = {'summary_length': length}
        response = requests.post(
            'http://localhost:8000/upload-and-summarize',
            files=files,
            data=data,
            timeout=60
        )
    
    if response.status_code == 200:
        return response.json()['summary']
    else:
        raise Exception(response.json()['detail'])

# Usage
summary = summarize_paper('paper.pdf', 'medium')
print(summary)
```

### JavaScript Integration
```javascript
async function summarizePaper(file, length = 'medium') {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('summary_length', length);

  try {
    const response = await fetch(
      'http://localhost:8000/upload-and-summarize',
      {
        method: 'POST',
        body: formData,
        timeout: 60000
      }
    );

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail);
    }

    const data = await response.json();
    return data.summary;
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

// Usage
const fileInput = document.getElementById('fileInput');
summarizePaper(fileInput.files[0], 'medium')
  .then(summary => console.log(summary))
  .catch(error => console.error(error));
```

---

## API Versioning

Current Version: 1.0

Future versions may include:
- Batch processing
- Async processing with webhooks
- Custom summarization prompts
- Multiple language support

---

## Support

For API issues:
1. Check this documentation
2. Review error messages
3. Check browser console (frontend)
4. Check terminal output (backend)
5. Run `verify_setup.py` for diagnostics
