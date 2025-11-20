# Deployment Guide

Complete deployment guide for the 42Cards SFTP Monitoring System.

## Deployment Options

### Option 1: GitHub Pages (Free - Recommended for Trial)

Best for: Static React dashboard with data from Google Sheets or static JSON

**Pros:**
- Completely free
- Easy to set up
- SSL included
- Fast CDN delivery

**Cons:**
- Static hosting only (no backend)
- Must use external data source

#### Steps:

1. **Build the React Dashboard**

```bash
cd dashboard
npm install
npm run build
```

2. **Deploy to GitHub Pages**

```bash
# Install gh-pages
npm install --save-dev gh-pages

# Add to package.json scripts:
"deploy": "npm run build && gh-pages -d dist"

# Deploy
npm run deploy
```

3. **Configure GitHub Repository**

- Go to repository Settings → Pages
- Select `gh-pages` branch
- Your dashboard will be at: `https://username.github.io/repo-name/`

4. **Update Data Source**

Edit `dashboard/src/utils/api.js` to use Google Sheets published URL or static JSON.

---

### Option 2: Internal 42Cards Server

Best for: Full-stack deployment with Flask backend

**Requirements:**
- Linux server (Ubuntu 20.04+)
- Python 3.9+
- Node.js 18+
- nginx
- PM2 or systemd

#### Steps:

1. **Server Setup**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip python3-venv nginx nodejs npm

# Install PM2
sudo npm install -g pm2
```

2. **Clone Repository**

```bash
cd /opt
sudo git clone https://github.com/your-org/banking_partner-sftp-monitor.git
cd banking_partner-sftp-monitor
sudo chown -R $USER:$USER .
```

3. **Setup Python Backend**

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Edit with your credentials
```

4. **Setup React Dashboard**

```bash
cd dashboard
npm install
npm run build
```

5. **Configure nginx**

```bash
sudo nano /etc/nginx/sites-available/sftp-monitor
```

```nginx
server {
    listen 80;
    server_name sftp-monitor.42cards.com;

    # React Dashboard
    location / {
        root /opt/banking_partner-sftp-monitor/dashboard/dist;
        try_files $uri $uri/ /index.html;
    }

    # Flask API
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/sftp-monitor /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

6. **Setup Flask with PM2**

```bash
# Create PM2 config
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: 'sftp-monitor-api',
    script: 'venv/bin/python',
    args: 'src/web/app.py',
    cwd: '/opt/banking_partner-sftp-monitor',
    env: {
      WEB_HOST: '0.0.0.0',
      WEB_PORT: 5000
    }
  }]
}
EOF

# Start with PM2
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

7. **Setup SSL with Let's Encrypt**

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d sftp-monitor.42cards.com
```

---

### Option 3: Docker Deployment

Best for: Containerized deployment with easy scaling

#### Create Docker Files

**Dockerfile (Backend)**

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "src/web/app.py"]
```

**Dockerfile (Dashboard)**

```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY dashboard/package*.json ./
RUN npm install

COPY dashboard/ .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
```

**docker-compose.yml**

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    env_file:
      - .env
    volumes:
      - ./config:/app/config
    restart: unless-stopped

  dashboard:
    build:
      context: .
      dockerfile: Dockerfile.dashboard
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    env_file:
      - config/n8n_env.example
    volumes:
      - n8n_data:/home/node/.n8n
    restart: unless-stopped

volumes:
  n8n_data:
```

#### Deploy with Docker

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## n8n Deployment

### Option 1: Docker (Recommended)

```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=admin \
  -e N8N_BASIC_AUTH_PASSWORD=your-password \
  n8nio/n8n
```

### Option 2: npm

```bash
npm install -g n8n
n8n
```

### Import Workflows

1. Access n8n at `http://your-server:5678`
2. Login with credentials
3. Go to Workflows → Import from File
4. Import each workflow from `n8n_workflows/` directory
5. Configure credentials for each service

---

## Environment Variables

Create production `.env` file:

```bash
# SFTP - PARTNER_A
SFTP_CUB_HOST=prod-sftp.cub.com
SFTP_CUB_PORT=22
SFTP_CUB_USERNAME=company_prod
SFTP_CUB_PASSWORD=secure_password

# SFTP - PARTNER_B
SFTP_SSFB_HOST=prod-sftp.ssfb.com
SFTP_SSFB_PORT=22
SFTP_SSFB_USERNAME=company_prod
SFTP_SSFB_PASSWORD=secure_password

# Slack
SLACK_BOT_TOKEN=xoxb-production-token
SLACK_CHANNEL_ID=C01234567

# Email
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_FROM=alerts@company.com
EMAIL_TO=admin@company.com,finance@company.com
EMAIL_PASSWORD=app_password

# Google Sheets
GOOGLE_SHEET_ID=your-production-sheet-id

# Web
WEB_HOST=0.0.0.0
WEB_PORT=5000
WEB_SECRET_KEY=generate-secure-random-key

# n8n
N8N_HOST=0.0.0.0
N8N_PORT=5678
N8N_PROTOCOL=https
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=secure-password
WEBHOOK_URL=https://n8n.42cards.com/webhook
```

---

## Security Checklist

- [ ] Change all default passwords
- [ ] Use environment variables for all secrets
- [ ] Enable SSL/TLS for all services
- [ ] Configure firewall (ufw or iptables)
- [ ] Set up SSH key authentication
- [ ] Disable root SSH login
- [ ] Regular security updates
- [ ] Configure fail2ban
- [ ] Use strong passwords (16+ characters)
- [ ] Implement IP whitelisting for SFTP

---

## Monitoring & Maintenance

### 1. Setup Monitoring

```bash
# Install monitoring tools
sudo apt install htop iotop nethogs

# Check service status
pm2 status
docker-compose ps
systemctl status nginx
```

### 2. Log Management

```bash
# View logs
pm2 logs sftp-monitor-api
docker-compose logs -f
tail -f /var/log/nginx/access.log

# Rotate logs
sudo nano /etc/logrotate.d/sftp-monitor
```

```
/opt/banking_partner-sftp-monitor/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
}
```

### 3. Backup Strategy

```bash
# Backup script
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d)
BACKUP_DIR=/backup/sftp-monitor

# Backup configs
tar -czf $BACKUP_DIR/config-$DATE.tar.gz config/

# Backup Google Sheets (export)
# Add Google Sheets backup logic

# Backup n8n workflows
docker exec n8n n8n export:workflow --all --output=/data/workflows-$DATE.json

# Keep last 30 days
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
EOF

chmod +x backup.sh

# Schedule daily backup
crontab -e
# Add: 0 2 * * * /opt/banking_partner-sftp-monitor/backup.sh
```

---

## Scaling Considerations

### For High Volume

1. **Database**: Move from SQLite to PostgreSQL
2. **Caching**: Implement Redis for API caching
3. **Load Balancer**: Add nginx load balancer for multiple Flask instances
4. **Queue**: Use Celery for background tasks
5. **CDN**: Use Cloudflare for dashboard

### Cost Estimate (Production)

**Free Tier Option:**
- GitHub Pages: Free
- Google Sheets: Free (with limits)
- Slack: Free tier
- n8n: Self-hosted (server cost only)

**Paid Option (Small Scale):**
- VPS (2 CPU, 4GB RAM): $10-20/month
- Domain: $12/year
- Email (SendGrid): Free tier or $15/month
- Total: ~$25-35/month

---

## Troubleshooting

### Common Issues

**1. Dashboard not loading**
```bash
# Check nginx
sudo nginx -t
sudo systemctl status nginx

# Check permissions
ls -la /opt/banking_partner-sftp-monitor/dashboard/dist
```

**2. API not responding**
```bash
# Check Flask
pm2 logs sftp-monitor-api
curl http://localhost:5000/api/status
```

**3. n8n workflows failing**
```bash
# Check n8n logs
docker logs n8n
# Verify credentials in n8n UI
```

**4. SFTP connection timeout**
```bash
# Test connectivity
telnet sftp-host.com 22
# Check firewall
sudo ufw status
```

---

## Rollback Procedure

```bash
# Stop services
pm2 stop all
docker-compose down

# Restore from backup
tar -xzf /backup/sftp-monitor/config-YYYYMMDD.tar.gz

# Restart services
pm2 restart all
docker-compose up -d
```

---

## Support & Updates

### Update Procedure

```bash
cd /opt/banking_partner-sftp-monitor
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
cd dashboard && npm install && npm run build
pm2 restart all
```

### Getting Help

- **Documentation**: Check `/docs` folder
- **Logs**: Review application logs
- **Issues**: Create GitHub issue
- **Email**: support@company.com
