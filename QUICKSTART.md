# Quick Start Guide

## 5-Minute Setup

### Step 1: Get Your API Key
1. Go to https://console.anthropic.com
2. Sign up or log in
3. Create an API key
4. Copy the key

### Step 2: Configure Environment
1. Open `.env.example` in a text editor
2. Copy its contents
3. Create a new file named `.env` in the project root
4. Paste the contents and replace `your_api_key_here` with your actual API key

Example `.env` file:
```
ANTHROPIC_API_KEY=sk-ant-v1-xxxxxxxxxxxxxxxxxxxxx
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Start the Server
```bash
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 5: Open the Frontend
Open `index.html` in your web browser

## Using the Application

1. **Upload PDF**: Click the upload area or drag a PDF file
2. **Choose Summary Length**: Select Short, Medium, or Long
3. **Click Summarize**: Wait for processing
4. **Copy Result**: Use the copy button to copy the summary

## Troubleshooting

### "ModuleNotFoundError: No module named 'fastapi'"
```bash
pip install -r requirements.txt
```

### "ANTHROPIC_API_KEY not found"
- Check that `.env` file exists in the project root
- Verify the API key is correct
- Restart the server after creating/updating `.env`

### "Only PDF files are allowed"
- Make sure you're uploading a `.pdf` file
- Check the file extension

### "Could not extract text from PDF"
- The PDF might be image-based (scanned)
- Try a different PDF with selectable text

## API Testing

Test the health endpoint:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy"}
```

## Next Steps

- Customize the summary prompt in `config.py`
- Modify the UI styling in `index.html`
- Add more API endpoints as needed
- Deploy to production (see README.md for details)
