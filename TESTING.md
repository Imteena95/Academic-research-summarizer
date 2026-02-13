# Testing Guide

## Setup Verification

### 1. Run Setup Verification Script
```bash
python verify_setup.py
```

This checks:
- Python version (3.8+)
- All dependencies installed
- Environment configuration
- Project files present

Expected output:
```
==================================================
Academic Paper Summarizer - Setup Verification
==================================================

Checking Python version...
✓ Python 3.11.0 - OK

Checking dependencies...
✓ FastAPI - OK
✓ Uvicorn - OK
✓ PyPDF2 - OK
✓ Anthropic - OK
✓ python-dotenv - OK

Checking environment configuration...
✓ .env file - OK

Checking project files...
✓ main.py - OK
✓ config.py - OK
✓ index.html - OK
✓ requirements.txt - OK
✓ README.md - OK

==================================================
Summary
==================================================
Python Version: ✓ PASS
Dependencies: ✓ PASS
Environment File: ✓ PASS
Project Files: ✓ PASS
==================================================

✓ All checks passed! You're ready to run the application.
```

---

## API Testing

### 1. Health Check Endpoint

**Test:** Verify API is running

```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{"status": "healthy"}
```

### 2. Root Endpoint

**Test:** Get API information

```bash
curl http://localhost:8000/
```

**Expected Response:**
```json
{"message": "Academic Paper Summarizer API"}
```

### 3. Upload and Summarize - Valid PDF

**Test:** Upload a valid PDF and get summary

```bash
curl -X POST http://localhost:8000/upload-and-summarize \
  -F "file=@sample.pdf" \
  -F "summary_length=short"
```

**Expected Response:**
```json
{
  "status": "success",
  "filename": "sample.pdf",
  "text_length": 5000,
  "summary": "The paper discusses..."
}
```

### 4. Upload and Summarize - Invalid File Type

**Test:** Upload non-PDF file

```bash
curl -X POST http://localhost:8000/upload-and-summarize \
  -F "file=@document.txt"
```

**Expected Response (400):**
```json
{"detail": "Only PDF files are allowed"}
```

### 5. Upload and Summarize - Empty PDF

**Test:** Upload PDF with no extractable text

```bash
curl -X POST http://localhost:8000/upload-and-summarize \
  -F "file=@empty.pdf"
```

**Expected Response (400):**
```json
{"detail": "Could not extract text from PDF"}
```

---

## Frontend Testing

### 1. Page Load Test

**Steps:**
1. Open `index.html` in browser
2. Verify page loads without errors
3. Check browser console for errors

**Expected:**
- Page displays correctly
- No console errors
- All UI elements visible

### 2. File Upload Test

**Steps:**
1. Click upload area
2. Select a PDF file
3. Verify filename appears

**Expected:**
- File selector opens
- Selected filename displays
- Summarize button becomes enabled

### 3. Drag and Drop Test

**Steps:**
1. Drag PDF file to upload area
2. Drop file
3. Verify filename appears

**Expected:**
- Upload area highlights on drag
- File is selected on drop
- Filename displays

### 4. Summary Length Selection

**Steps:**
1. Select "Short" option
2. Select "Medium" option
3. Select "Long" option

**Expected:**
- Radio buttons work correctly
- Selection persists

### 5. Summarization Test

**Steps:**
1. Upload valid PDF
2. Select summary length
3. Click "Summarize Paper"
4. Wait for processing

**Expected:**
- Loading spinner appears
- Summary displays after processing
- No errors in console

### 6. Copy to Clipboard Test

**Steps:**
1. Generate a summary
2. Click "Copy Summary" button
3. Paste in text editor

**Expected:**
- "Copied to clipboard!" message appears
- Summary text is copied correctly

### 7. Clear Button Test

**Steps:**
1. Upload file and generate summary
2. Click "Clear" button
3. Verify form resets

**Expected:**
- File selection cleared
- Summary hidden
- Form ready for new upload

### 8. Error Handling Test

**Steps:**
1. Try uploading non-PDF file
2. Try uploading empty PDF
3. Check error messages

**Expected:**
- Clear error messages displayed
- User can retry

---

## Performance Testing

### 1. Small PDF (< 5 pages)

**Test:** Upload small PDF

**Expected:**
- Processing time: 10-15 seconds
- Summary quality: Good
- No errors

### 2. Medium PDF (5-20 pages)

**Test:** Upload medium PDF

**Expected:**
- Processing time: 15-30 seconds
- Summary quality: Comprehensive
- No errors

### 3. Large PDF (> 20 pages)

**Test:** Upload large PDF

**Expected:**
- Processing time: 30-60 seconds
- Summary quality: Detailed
- No timeout errors

### 4. Concurrent Requests

**Test:** Send multiple requests simultaneously

```bash
for i in {1..5}; do
  curl -X POST http://localhost:8000/upload-and-summarize \
    -F "file=@sample.pdf" &
done
wait
```

**Expected:**
- All requests processed
- No server crashes
- Responses are correct

---

## Browser Compatibility Testing

### Desktop Browsers
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

### Mobile Browsers
- [ ] Chrome Mobile
- [ ] Safari iOS
- [ ] Firefox Mobile

### Expected Results
- Page loads correctly
- File upload works
- Responsive design adapts
- No console errors

---

## Security Testing

### 1. API Key Security

**Test:** Verify API key is not exposed

```bash
# Check if API key appears in responses
curl http://localhost:8000/health | grep -i "api"
```

**Expected:**
- No API key in response
- No sensitive data exposed

### 2. File Upload Security

**Test:** Try uploading malicious files

```bash
# Try uploading executable
curl -X POST http://localhost:8000/upload-and-summarize \
  -F "file=@malware.exe"
```

**Expected:**
- File rejected
- Error message displayed
- No file executed

### 3. CORS Testing

**Test:** Verify CORS headers

```bash
curl -i http://localhost:8000/health
```

**Expected:**
- CORS headers present
- Correct origin allowed

---

## Docker Testing

### 1. Build Docker Image

```bash
docker build -t academic-summarizer .
```

**Expected:**
- Build succeeds
- No errors

### 2. Run Docker Container

```bash
docker run -p 8000:8000 \
  -e ANTHROPIC_API_KEY=your_key \
  academic-summarizer
```

**Expected:**
- Container starts
- API accessible at localhost:8000

### 3. Docker Compose

```bash
docker-compose up -d
```

**Expected:**
- Service starts
- Health check passes
- API accessible

---

## Stress Testing

### 1. Large File Upload

**Test:** Upload 50MB PDF

**Expected:**
- File uploads successfully
- Processing completes
- No memory errors

### 2. Rapid Requests

**Test:** Send 10 requests in quick succession

**Expected:**
- All requests processed
- No dropped requests
- Server remains stable

### 3. Long Running Request

**Test:** Upload very large PDF (100+ pages)

**Expected:**
- Request doesn't timeout
- Summary generated correctly
- No memory leaks

---

## Regression Testing Checklist

After making changes, verify:

- [ ] Setup verification passes
- [ ] Health check works
- [ ] File upload works
- [ ] PDF text extraction works
- [ ] Summarization works
- [ ] All summary lengths work
- [ ] Error handling works
- [ ] Frontend loads correctly
- [ ] Copy to clipboard works
- [ ] Clear button works
- [ ] No console errors
- [ ] No API errors
- [ ] Docker builds successfully
- [ ] Docker runs successfully

---

## Test Data

### Sample PDFs for Testing

1. **Small PDF** - 2-3 pages
   - Use for quick testing
   - Fast processing

2. **Medium PDF** - 10-15 pages
   - Use for standard testing
   - Realistic use case

3. **Large PDF** - 50+ pages
   - Use for stress testing
   - Performance testing

4. **Image-based PDF** - Scanned document
   - Use for error handling
   - Should fail gracefully

5. **Empty PDF** - No text content
   - Use for error handling
   - Should fail gracefully

---

## Debugging Tips

### 1. Check Browser Console
```javascript
// Open DevTools (F12)
// Check Console tab for errors
```

### 2. Check Server Logs
```bash
# Terminal where server is running
# Look for error messages
```

### 3. Check Network Requests
```javascript
// Open DevTools (F12)
// Go to Network tab
// Check request/response details
```

### 4. Enable Debug Mode
Edit `main.py`:
```python
app = FastAPI(title="Academic Paper Summarizer", debug=True)
```

### 5. Test API Directly
```bash
# Use curl or Postman
# Test each endpoint individually
```

---

## Automated Testing

### Create Test Script

```python
import requests
import json

def test_health():
    response = requests.get('http://localhost:8000/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'healthy'
    print("✓ Health check passed")

def test_root():
    response = requests.get('http://localhost:8000/')
    assert response.status_code == 200
    assert 'message' in response.json()
    print("✓ Root endpoint passed")

def test_invalid_file():
    with open('test.txt', 'rb') as f:
        files = {'file': f}
        response = requests.post(
            'http://localhost:8000/upload-and-summarize',
            files=files
        )
    assert response.status_code == 400
    print("✓ Invalid file test passed")

if __name__ == '__main__':
    test_health()
    test_root()
    test_invalid_file()
    print("\n✓ All tests passed!")
```

Run tests:
```bash
python test_api.py
```

---

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - run: pip install -r requirements.txt
      - run: python verify_setup.py
      - run: python test_api.py
```

---

## Test Report Template

```
Test Date: YYYY-MM-DD
Tester: Name
Environment: Windows/Mac/Linux

Setup Verification: PASS/FAIL
API Health Check: PASS/FAIL
File Upload: PASS/FAIL
Summarization: PASS/FAIL
Error Handling: PASS/FAIL
Frontend: PASS/FAIL
Performance: PASS/FAIL
Security: PASS/FAIL

Issues Found:
- Issue 1
- Issue 2

Notes:
- Note 1
- Note 2

Overall Result: PASS/FAIL
```

---

## Support

For testing issues:
1. Check this guide
2. Review error messages
3. Check logs
4. Run verify_setup.py
5. Check API_DOCUMENTATION.md
