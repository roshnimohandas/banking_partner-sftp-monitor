# 🏦 42Cards Banking Partner SFTP Monitor

Automated SFTP file monitoring system for banking partner file validation and alerting.

## 📋 Overview

This project provides a comprehensive solution for monitoring SFTP folders where banking partner files (PARTNER_A, PARTNER_B, etc.) are placed. It validates files against regulatory patterns, checks file metadata, and sends alerts when issues are detected.

## ✨ Features

- **Automated SFTP Monitoring**: Scheduled monitoring of SFTP directories
- **File Validation**:
  - Naming convention validation (regulatory patterns)
  - File size and format checks
  - File age verification
  - Presence verification
- **MCP Server**: Custom Model Context Protocol server with tools for:
  - SFTP connection management
  - File existence checks
  - Metadata validation
  - Alert dispatching
- **Web Dashboard**: Real-time monitoring interface
- **Multi-channel Alerts**: Slack, Email, and Webhook notifications
- **n8n Workflow**: Pre-configured automation workflow
- **Multi-partner Support**: Configurable for multiple banking partners

## 🏗️ Architecture

```
┌─────────────────┐
│  n8n Workflow   │  ← Scheduled monitoring
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  SFTP Client    │  ← Connect & list files
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  File Validator │  ← Validate files
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Alert System   │  ← Send notifications
└─────────────────┘
         │
    ┌────┴────┬────────┐
    ▼         ▼        ▼
  Slack    Email   Webhook
```

## 📁 Project Structure

```
banking_partner-sftp-monitor/
├── src/
│   ├── validators/           # File validation logic
│   │   ├── file_validator.py # Validation rules
│   │   └── sftp_client.py    # SFTP operations
│   ├── mcp_server/           # MCP server implementation
│   │   └── server.py         # MCP tools
│   └── web/                  # Web interface
│       ├── app.py            # Flask application
│       ├── templates/        # HTML templates
│       └── static/           # CSS/JS assets
├── config/                   # Configuration files
│   ├── partners.json         # Partner configurations
│   ├── mcp_config.json       # MCP server config
│   └── n8n_env.example       # n8n environment vars
├── n8n_workflows/            # n8n workflow definitions
│   └── sftp_monitor_workflow.json
├── tests/                    # Test files
├── docs/                     # Documentation
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
└── README.md                # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- n8n (optional, for workflow automation)
- SFTP server access
- Slack workspace (optional, for alerts)
- SMTP server (optional, for email alerts)

### Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd banking_partner-sftp-monitor
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

```bash
cp .env.example .env
# Edit .env with your credentials
```

5. **Update partner configurations**

Edit `config/partners.json` with your banking partner details:

```json
{
  "partners": [
    {
      "id": "PARTNER_A",
      "name": "Banking Partner A",
      "sftp": {
        "host": "your-sftp-host.com",
        "username": "your-username"
      }
    }
  ]
}
```

## 💻 Usage

### 1. Web Interface (Recommended for Trial)

Start the web dashboard:

```bash
python src/web/app.py
```

Access the dashboard at `http://localhost:5000`

**Features:**
- Connect to SFTP servers
- Monitor directories in real-time
- View validation results
- See alerts and notifications

### 2. MCP Server

Run the MCP server:

```bash
python -m src.mcp_server.server
```

**Available MCP Tools:**

- `connect_sftp`: Connect to SFTP server
- `list_files`: List files in directory
- `check_file_exists`: Check if file exists
- `validate_file`: Validate file metadata
- `send_slack_alert`: Send Slack notification
- `monitor_files`: Monitor and validate multiple files

### 3. n8n Workflow (For Production)

**Setup n8n:**

```bash
# Using Docker (recommended)
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

**Import Workflow:**

1. Access n8n at `http://localhost:5678`
2. Go to Workflows → Import from File
3. Select `n8n_workflows/sftp_monitor_workflow.json`
4. Configure credentials:
   - SFTP credentials for each partner
   - Slack API credentials
   - Email SMTP credentials
5. Activate the workflow

**Workflow Features:**
- Runs every 15 minutes (configurable)
- Lists files from SFTP server
- Validates each file
- Sends alerts for invalid files
- Generates monitoring summary

### 4. Direct Python Usage

```python
from src.validators.sftp_client import SFTPClient
from src.validators.file_validator import FileValidator

# Connect to SFTP
with SFTPClient(
    host="sftp.example.com",
    username="user",
    password="pass"
) as client:
    # List files
    files = client.list_files("/incoming")

    # Validate files
    validator = FileValidator(partner="PARTNER_A")
    for file in files:
        result = validator.validate_all(
            filename=file['filename'],
            file_size=file['size'],
            file_mtime=file['mtime']
        )
        print(result)
```

## 🔧 Configuration

### Banking Partner Configuration

Edit `config/partners.json`:

```json
{
  "id": "YOUR_BANK",
  "name": "Your Bank Name",
  "validation": {
    "regex": "^BANK_\\d{8}_\\d{6}_TYPE\\.csv$",
    "min_size_bytes": 100,
    "max_size_bytes": 104857600,
    "max_age_hours": 24
  },
  "schedule": {
    "check_interval_minutes": 15,
    "expected_files": [
      {
        "name": "TRANSACTION",
        "frequency": "daily",
        "expected_time": "09:00"
      }
    ]
  },
  "alerts": {
    "slack_channel": "#alerts",
    "email_recipients": ["admin@company.com"]
  }
}
```

### Environment Variables

Key variables in `.env`:

```bash
# SFTP Configuration
SFTP_HOST=your-sftp-host.com
SFTP_USERNAME=your-username
SFTP_PASSWORD=your-password

# Slack Alerts
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_CHANNEL_ID=your-channel

# Email Alerts
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_FROM=alerts@company.com
EMAIL_TO=admin@company.com

# Web Interface
WEB_PORT=5000
```

## 📊 Validation Rules

### File Naming Conventions

**PARTNER_A (Banking Partner A):**
- Pattern: `CUB_YYYYMMDD_HHMMSS_TYPE.csv`
- Example: `CUB_20231120_143000_TRANSACTION.csv`
- Types: TRANSACTION, SETTLEMENT, REPORT

**PARTNER_B (Banking Partner B):**
- Pattern: `SSFB_YYYYMMDD_HHMMSS_TYPE.csv`
- Example: `SSFB_20231120_143000_TXN.csv`
- Types: TXN, SETTLE, RPT

**Generic:**
- Pattern: `PARTNER_YYYYMMDD_HHMMSS_TYPE.ext`
- Extensions: .csv, .txt, .xlsx

### File Size Limits

- **Minimum**: 100 bytes (prevents empty files)
- **Maximum**: 100 MB (configurable per partner)

### File Age Validation

- **Default**: Files older than 24 hours trigger warnings
- Configurable per partner

## 🔔 Alert System

### Slack Alerts

1. Create a Slack App
2. Add Bot Token Scopes: `chat:write`, `channels:read`
3. Install app to workspace
4. Copy Bot User OAuth Token to `SLACK_BOT_TOKEN`
5. Invite bot to your channel

### Email Alerts

1. Configure SMTP settings in `.env`
2. For Gmail, use App Passwords
3. Set recipients in partner config

### Webhook Alerts

- Send JSON payload to custom endpoint
- Useful for integration with other systems

## 🧪 Testing

Run tests:

```bash
pytest tests/
```

Run with coverage:

```bash
pytest --cov=src tests/
```

## 📈 Monitoring Dashboard

The web dashboard provides:

- **Real-time Status**: Connection status and last check time
- **File Statistics**: Total, valid, and invalid file counts
- **File List**: Detailed view of all monitored files
- **Alert History**: Recent alerts and errors
- **WebSocket Updates**: Live notifications for new alerts

## 🔒 Security Best Practices

1. **Credentials**: Never commit `.env` file
2. **SSH Keys**: Prefer key-based authentication over passwords
3. **Network**: Use VPN or secure network for SFTP connections
4. **Secrets**: Use environment variables for all sensitive data
5. **Access Control**: Limit SFTP user permissions to read-only if possible

## 🐛 Troubleshooting

### Common Issues

**1. SFTP Connection Failed**
```bash
# Check connectivity
telnet sftp-host.com 22

# Verify credentials
# Test with FileZilla or similar SFTP client
```

**2. Slack Alerts Not Working**
```bash
# Verify token
# Check bot permissions
# Ensure bot is in the channel
```

**3. Files Not Validating**
```bash
# Check filename pattern matches
# Verify file size is within limits
# Check file timestamps
```

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🎯 Roadmap

- [ ] Add support for more banking partners
- [ ] Implement file content validation
- [ ] Add database storage for historical data
- [ ] Create detailed analytics dashboard
- [ ] Add API endpoints for external integrations
- [ ] Implement retry logic for failed transfers
- [ ] Add support for multiple SFTP servers per partner

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Email: support@company.com

## 🙏 Acknowledgments

- Built with Python, Flask, n8n, and MCP
- Uses paramiko for SFTP operations
- Designed for 42Cards banking operations

---

**Note**: This is a trial version using free/open-source tools. Production deployment may require commercial licenses for some components.
