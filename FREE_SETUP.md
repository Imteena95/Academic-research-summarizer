# FREE Setup - No API Key Needed!

## This version uses Ollama (completely free, runs locally)

### Step 1: Install Ollama

1. Go to: https://ollama.ai
2. Click **Download**
3. Choose your OS (Windows, Mac, or Linux)
4. Install it like any other program
5. Run Ollama

### Step 2: Download a Model

Open Command Prompt and type:
```bash
ollama pull mistral
```

This downloads the Mistral model (free, ~4GB). Wait for it to finish.

### Step 3: Start Ollama

Ollama should be running in the background. You can see it in your system tray.

### Step 4: Install Dependencies

In your project terminal, type:
```bash
pip install -r requirements.txt
```

### Step 5: Start the Server

Type:
```bash
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 6: Open the Interface

Open a new terminal and type:
```bash
start index.html
```

Or manually open `index.html` in your browser.

### Step 7: Upload and Summarize

1. Upload a PDF
2. Click "Summarize Paper"
3. Wait for the summary (first time takes longer)

---

## Cost: $0 (Completely Free!)

- Ollama: Free
- Mistral Model: Free
- This app: Free

---

## Troubleshooting

### "Ollama is not running"
- Make sure Ollama is installed and running
- Check system tray for Ollama icon
- Restart Ollama if needed

### "Connection refused"
- Ollama might not be running
- Start Ollama application
- Wait a few seconds
- Try again

### Slow summarization
- First run is slower (model loading)
- Subsequent runs are faster
- Depends on your computer specs

### Out of memory
- Close other applications
- Use shorter PDFs
- Restart Ollama

---

## Alternative Models (Also Free)

You can use other models instead of Mistral:

```bash
ollama pull llama2
ollama pull neural-chat
ollama pull orca-mini
```

Then edit `main.py` line 28 and change:
```python
"model": "mistral",
```
to:
```python
"model": "llama2",  # or any other model
```

---

## System Requirements

- **RAM:** 8GB minimum (16GB recommended)
- **Disk Space:** 5-10GB for models
- **Internet:** Only needed for downloading models

---

**Completely Free - No Payments Ever!**
