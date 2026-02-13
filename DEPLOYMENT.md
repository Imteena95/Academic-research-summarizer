# Deployment Guide

## Local Development

### Prerequisites
- Python 3.8+
- pip
- Anthropic API key

### Setup
1. Create `.env` file with your API key
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python main.py`
4. Open `index.html` in browser

## Docker Deployment

### Prerequisites
- Docker
- Docker Compose (optional)

### Using Docker Compose (Recommended)

1. Create `.env` file with your API key:
```
ANTHROPIC_API_KEY=your_key_here
```

2. Run:
```bash
docker-compose up -d
```

3. Access at `http://localhost:8000`

### Using Docker Directly

1. Build the image:
```bash
docker build -t academic-summarizer .
```

2. Run the container:
```bash
docker run -p 8000:8000 \
  -e ANTHROPIC_API_KEY=your_key_here \
  -v $(pwd)/uploads:/app/uploads \
  academic-summarizer
```

## Cloud Deployment

### Heroku

1. Install Heroku CLI
2. Create `Procfile`:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

3. Deploy:
```bash
heroku create your-app-name
heroku config:set ANTHROPIC_API_KEY=your_key_here
git push heroku main
```

### AWS (EC2)

1. Launch EC2 instance (Ubuntu 22.04)
2. SSH into instance
3. Install Python and dependencies:
```bash
sudo apt update
sudo apt install python3-pip python3-venv
```

4. Clone repository and setup:
```bash
git clone your-repo
cd Academic-research-summarizer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. Create `.env` with API key
6. Run with systemd or supervisor

### Google Cloud Run

1. Create `requirements.txt` (already done)
2. Deploy:
```bash
gcloud run deploy academic-summarizer \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars ANTHROPIC_API_KEY=your_key_here
```

### Railway

1. Connect GitHub repository
2. Add environment variable: `ANTHROPIC_API_KEY`
3. Set start command: `python main.py`
4. Deploy

## Production Considerations

### Security
- Use environment variables for API keys (never commit them)
- Enable HTTPS/SSL
- Implement rate limiting
- Add authentication if needed
- Validate file uploads

### Performance
- Use a production ASGI server (Gunicorn + Uvicorn)
- Add caching for frequently summarized papers
- Implement request queuing for high load
- Use CDN for static files

### Monitoring
- Set up logging
- Monitor API usage
- Track error rates
- Monitor response times

### Scaling
- Use load balancer
- Horizontal scaling with multiple instances
- Database for storing summaries
- Message queue for async processing

## Production ASGI Server Setup

### Using Gunicorn + Uvicorn

1. Install:
```bash
pip install gunicorn
```

2. Run:
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

3. Or use systemd service file:
```ini
[Unit]
Description=Academic Paper Summarizer
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/path/to/app
Environment="PATH=/path/to/app/venv/bin"
ExecStart=/path/to/app/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

## Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Increase timeout for large files
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

## SSL/TLS with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d your-domain.com
```

Then update Nginx config to use SSL certificates.

## Monitoring with PM2

1. Install PM2:
```bash
npm install -g pm2
```

2. Create `ecosystem.config.js`:
```javascript
module.exports = {
  apps: [{
    name: 'academic-summarizer',
    script: './main.py',
    interpreter: 'python',
    instances: 1,
    exec_mode: 'cluster',
    env: {
      ANTHROPIC_API_KEY: 'your_key_here'
    }
  }]
};
```

3. Start:
```bash
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

## Troubleshooting Deployment

### Port already in use
```bash
lsof -i :8000
kill -9 <PID>
```

### Permission denied
```bash
chmod +x main.py
```

### Module not found
```bash
pip install -r requirements.txt
```

### API key not working
- Verify key is correct
- Check environment variable is set
- Restart application after setting env var

## Backup and Recovery

- Regularly backup uploaded files
- Store API keys securely (use secrets manager)
- Keep application logs
- Version control your code
