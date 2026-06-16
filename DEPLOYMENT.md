# Student Finance Tracker - Deployment Guide

## Local Development Deployment

### Windows
```bash
# 1. Open PowerShell as Administrator
# 2. Navigate to project directory
cd C:\Users\Administrator\Downloads\project

# 3. Run setup script
.\setup.bat

# 4. Initialize database
python init_db.py

# 5. Start development server
python run.py
```

### macOS/Linux
```bash
cd /path/to/project

chmod +x setup.sh
./setup.sh

python init_db.py

python run.py
```

---

## Production Deployment (Linux/Ubuntu Server)

### Prerequisites
- Ubuntu 20.04 LTS or later
- Python 3.8+
- MySQL 5.7+
- Nginx
- Supervisor (optional, for process management)

### Step 1: Server Setup
```bash
sudo apt update
sudo apt upgrade -y

# Install Python and pip
sudo apt install python3-pip python3-venv -y

# Install MySQL
sudo apt install mysql-server -y
sudo mysql_secure_installation

# Install Nginx
sudo apt install nginx -y

# Install Supervisor (optional)
sudo apt install supervisor -y
```

### Step 2: Clone and Setup Project
```bash
# Create app directory
sudo mkdir -p /var/www/student-finance-tracker
cd /var/www/student-finance-tracker

# Clone or copy project files
git clone <repo> .
# OR copy files manually

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn
```

### Step 3: Configure Environment
```bash
# Copy and edit environment file
cp .env.example .env
sudo nano .env

# Add production values:
# - Strong SECRET_KEY
# - MySQL credentials
# - OpenAI API key
# - Email configuration
# - Set FLASK_ENV=production
```

### Step 4: Initialize Database
```bash
python init_db.py
```

### Step 5: Collect Static Files (optional)
```bash
# Ensure static files are accessible
chmod 755 app/static
```

### Step 6: Configure Gunicorn

Create `/var/www/student-finance-tracker/wsgi.py`:
```python
from run import app

if __name__ == "__main__":
    app.run()
```

Test Gunicorn:
```bash
gunicorn --workers 4 --bind 127.0.0.1:8000 wsgi:app
```

### Step 7: Configure Supervisor (Optional)

Create `/etc/supervisor/conf.d/student-finance.conf`:
```ini
[program:student-finance]
directory=/var/www/student-finance-tracker
command=/var/www/student-finance-tracker/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:8000 wsgi:app
autostart=true
autorestart=true
user=www-data
startsecs=10
stopwaitsecs=10
stdout_logfile=/var/log/student-finance/gunicorn.log
stderr_logfile=/var/log/student-finance/gunicorn.log
```

Then:
```bash
sudo mkdir -p /var/log/student-finance
sudo chown www-data:www-data /var/log/student-finance
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start student-finance
```

### Step 8: Configure Nginx

Create `/etc/nginx/sites-available/student-finance`:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Certificates (use Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    client_max_body_size 20M;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /var/www/student-finance-tracker/app/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/student-finance /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 9: Set Up SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y

sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

### Step 10: Set Permissions
```bash
sudo chown -R www-data:www-data /var/www/student-finance-tracker
sudo chmod -R 755 /var/www/student-finance-tracker
sudo chmod -R 775 /var/www/student-finance-tracker/app/static
```

---

## Docker Deployment

### Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "run:app"]
```

### Create docker-compose.yml
```yaml
version: '3.8'

services:
  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: student_finance_tracker
      MYSQL_USER: studentfinance
      MYSQL_PASSWORD: StudentFinance@123
    ports:
      - "3306:3306"
    volumes:
      - db_data:/var/lib/mysql

  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=mysql+pymysql://studentfinance:StudentFinance@123@db:3306/student_finance_tracker
      - FLASK_ENV=production
      - SECRET_KEY=your-secret-key
      - OPENAI_API_KEY=your-api-key
    depends_on:
      - db
    volumes:
      - .:/app

volumes:
  db_data:
```

Run with Docker:
```bash
docker-compose up -d
```

---

## Heroku Deployment

### Create Procfile
```
web: gunicorn --workers 4 run:app
release: python init_db.py
```

### Create runtime.txt
```
python-3.9.16
```

### Deploy
```bash
heroku create your-app-name
heroku addons:create cleardb:ignite
heroku config:set SECRET_KEY=your-secret-key
heroku config:set OPENAI_API_KEY=your-api-key
git push heroku main
```

---

## Performance Optimization

### Database Optimization
```sql
-- Add indexes for frequently queried fields
ALTER TABLE expenses ADD INDEX idx_user_date (user_id, expense_date);
ALTER TABLE income ADD INDEX idx_user_date (user_id, date);
ALTER TABLE ai_chat_history ADD INDEX idx_user_timestamp (user_id, timestamp);
```

### Caching
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/dashboard')
@cache.cached(timeout=300)
def dashboard():
    # Dashboard will be cached for 5 minutes
    pass
```

### Connection Pooling (Already Configured)
```python
# In config.py - already optimized
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,
    "pool_recycle": 280,
    "pool_size": 10,
    "max_overflow": 20,
}
```

---

## Monitoring & Logging

### Application Logging
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240000, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Application startup')
```

### Monitor with Uptime Robot
1. Visit https://uptimerobot.com
2. Add monitoring for your domain
3. Set alert email

### Monitor with New Relic
```bash
pip install newrelic
newrelic-admin run-program gunicorn wsgi:app
```

---

## Backup & Recovery

### Database Backup (Daily)
```bash
# Create backup script backup.sh
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/student-finance"
mkdir -p $BACKUP_DIR

mysqldump -u studentfinance -p[password] student_finance_tracker > \
  $BACKUP_DIR/backup_$DATE.sql

# Compress old backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -exec gzip {} \;

# Add to crontab
crontab -e
# 0 2 * * * /path/to/backup.sh  # Daily at 2 AM
```

### Restore from Backup
```bash
mysql -u studentfinance -p student_finance_tracker < backup.sql
```

---

## Security Hardening

### Update Dependencies Regularly
```bash
pip install --upgrade pip
pip list --outdated
pip install -U package_name
```

### Security Scanning
```bash
pip install safety
safety check
```

### Regular Updates
```bash
# Keep system updated
sudo apt update && sudo apt upgrade -y

# Keep SSL certificate updated
sudo certbot renew --dry-run
```

---

## Troubleshooting Deployment

### Problem: Gunicorn Can't Connect to MySQL
**Solution**: Ensure MySQL is running and credentials are correct
```bash
mysql -u studentfinance -p
# Test login
```

### Problem: Static Files Not Loading
**Solution**: Configure Nginx properly
```bash
sudo nginx -t  # Check syntax
sudo systemctl reload nginx
```

### Problem: 502 Bad Gateway
**Solution**: Check Gunicorn logs
```bash
sudo tail -f /var/log/supervisor/student-finance-stderr.log
```

### Problem: High Memory Usage
**Solution**: Reduce worker count and increase memory limit
```bash
gunicorn --workers 2 --worker-class sync wsgi:app
```

---

## Monitoring Commands

```bash
# Check Gunicorn status
ps aux | grep gunicorn

# Check Nginx status
sudo systemctl status nginx

# Check MySQL status
sudo systemctl status mysql

# Monitor logs
sudo tail -f /var/log/student-finance/gunicorn.log
sudo tail -f /var/log/nginx/error.log
```

---

**Document Version**: 1.0.0  
**Last Updated**: 2026-06-16
