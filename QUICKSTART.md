# 🚀 Quick Start Guide - 42Cards SFTP Monitor

Get started in 5 minutes with this trial setup!

## Prerequisites

- Python 3.9+
- Node.js 18+
- Git

## 1. Clone & Setup (2 minutes)

```bash
# Clone repository
git clone <repository-url>
cd banking_partner-sftp-monitor

# Setup Python environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

Edit `.env` with your SFTP credentials:

```bash
SFTP_HOST=your-sftp-host.com
SFTP_USERNAME=your-username
SFTP_PASSWORD=your-password
```

## 2. Start Flask Web Dashboard (1 minute)

```bash
python src/web/app.py
```

Open http://localhost:5000 in your browser

## 3. Start React Dashboard (2 minutes)

```bash
cd dashboard
npm install
npm run dev
```

Open http://localhost:3000 in your browser

## 4. Test SFTP Connection

```python
from src.validators.sftp_client import SFTPClient
from src.validators.file_validator import FileValidator

# Connect to SFTP
with SFTPClient(
    host="your-host.com",
    username="user",
    password="pass"
) as client:
    files = client.list_files("/path")
    print(f"Found {len(files)} files")

    # Validate files
    validator = FileValidator(partner="PARTNER_A")
    for file in files:
        result = validator.validate_all(
            filename=file['filename'],
            file_size=file['size']
        )
        print(f"{file['filename']}: {result['valid']}")
```

## 5. Run MCP Server (Optional)

```bash
python -m src.mcp_server.server
```

## Next Steps

### For Trial/Demo:
1. Use Flask dashboard at http://localhost:5000
2. Test with your SFTP server
3. View file validation results

### For Production:
1. Read [DEPLOYMENT.md](docs/DEPLOYMENT.md)
2. Set up n8n workflows (see n8n_workflows/)
3. Configure Google Sheets (see docs/GOOGLE_SHEETS_SETUP.md)
4. Deploy React dashboard to GitHub Pages

## Common Use Cases

### Check File Exists

```bash
curl -X POST http://localhost:5000/api/connect \
  -H "Content-Type: application/json" \
  -d '{
    "connection_name": "test",
    "host": "sftp.example.com",
    "username": "user",
    "password": "pass"
  }'

curl -X POST http://localhost:5000/api/monitor/test \
  -H "Content-Type: application/json" \
  -d '{
    "remote_path": "/incoming",
    "partner": "PARTNER_A"
  }'
```

### Validate Single File

```python
from src.validators.file_validator import validate_file

result = validate_file(
    filename="CUB_20241120_143000_TRANSACTION.csv",
    file_size=2048576,  # 2MB
    partner="PARTNER_A"
)

print(result)
# {
#   'filename': 'CUB_20241120_143000_TRANSACTION.csv',
#   'partner': 'PARTNER_A',
#   'valid': True,
#   'errors': [],
#   'warnings': []
# }
```

## Troubleshooting

**Can't connect to SFTP?**
- Check credentials in .env
- Test with FileZilla or similar client
- Verify network connectivity

**Dashboard not loading?**
- Check if Flask is running on port 5000
- Check browser console for errors
- Verify Python dependencies installed

**Files not validating?**
- Check file naming pattern in config/partners.json
- Review validation rules in src/validators/file_validator.py
- Check file size limits

## Architecture Overview

```
┌─────────────┐
│   n8n       │ ← Automation workflows (optional)
└──────┬──────┘
       │
┌──────▼──────┐
│ SFTP Server │ ← Banking partner files
└──────┬──────┘
       │
┌──────▼──────────┐
│ Python Validator│ ← File validation
└──────┬──────────┘
       │
┌──────▼──────────┐
│ Flask API       │ ← Backend API
└──────┬──────────┘
       │
┌──────▼──────────┐
│ React Dashboard │ ← Web UI
└─────────────────┘
       │
┌──────▼──────────┐
│ Google Sheets   │ ← Data logging (optional)
└─────────────────┘
```

## File Structure

```
banking_partner-sftp-monitor/
├── src/
│   ├── validators/       # Python validation logic
│   ├── mcp_server/       # MCP server
│   └── web/              # Flask web app
├── dashboard/            # React dashboard
├── n8n_workflows/        # n8n automation
├── config/               # Configuration files
└── docs/                 # Documentation
```

## Support

- 📖 Read full docs in [README.md](README.md)
- 🚀 Deployment guide: [DEPLOYMENT.md](docs/DEPLOYMENT.md)
- 📊 Google Sheets: [GOOGLE_SHEETS_SETUP.md](docs/GOOGLE_SHEETS_SETUP.md)
- 🐛 Issues: Create GitHub issue
- 📧 Email: support@company.com

## What's Included

✅ Python file validators
✅ SFTP client with retry logic
✅ Flask web dashboard
✅ React monitoring dashboard
✅ MCP server for automation
✅ n8n workflows (PARTNER_A Daily, PARTNER_B Weekly, Ad-hoc)
✅ Google Sheets integration
✅ Slack/Email alerts
✅ Multi-partner support (PARTNER_A, PARTNER_B)
✅ Deployment guides

## Trial Limitations

This is a trial version using free/open-source tools:

- Flask (development server, not production-ready)
- React (client-side only)
- n8n Community Edition
- Google Sheets (free tier limits)
- No database (uses in-memory storage)

For production deployment, see [DEPLOYMENT.md](docs/DEPLOYMENT.md).

---

**Ready to go live?** Follow the [Production Deployment Guide](docs/DEPLOYMENT.md)
