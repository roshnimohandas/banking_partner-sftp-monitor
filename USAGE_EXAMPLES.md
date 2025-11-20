# 📖 Usage Examples

Complete examples for using the SFTP monitoring system.

## 🚀 Quick Start

### Test SFTP Connection

```bash
# Test connection to your server
python test_real_sftp.py
```

**Output:**
```
======================================================================
🔍 SFTP CONNECTION TEST
======================================================================

📡 Connection Details:
   Host: 103.183.96.21
   Port: 2022
   Username: srv.42cssmtp
   Password: ****************

🔌 Attempting to connect...
✅ Connected successfully!

📂 Listing root directory (/)...
   Found 5 items
```

---

## 📊 Monitor Files with Email Alerts

### Basic Usage (Uses .env file)

```bash
python send_sftp_alert.py
```

This will:
- Connect to SFTP server from `.env` credentials
- Monitor root directory (`/`)
- Validate files as `PARTNER_A`
- Send email alerts for invalid files

### Specify Directory

```bash
# Monitor specific directory
python send_sftp_alert.py --path /incoming

# Monitor partner_a directory
python send_sftp_alert.py --path /partner_a

# Monitor with different partner validation
python send_sftp_alert.py --path /partner_b --partner PARTNER_B
```

### Specify Partner Type

```bash
# Validate as PARTNER_A (default)
python send_sftp_alert.py --partner PARTNER_A

# Validate as PARTNER_B
python send_sftp_alert.py --partner PARTNER_B

# Generic validation
python send_sftp_alert.py --partner GENERIC
```

### Override SFTP Credentials

```bash
# Use different credentials (not from .env)
python send_sftp_alert.py \
  --host 103.183.96.21 \
  --port 2022 \
  --username srv.42cssmtp \
  --password 'D]kjPL8Ccy6uGx3R' \
  --path /incoming \
  --partner PARTNER_A
```

### Full Example

```bash
# Monitor /data/partner_a directory
# Validate as PARTNER_A
# Using credentials from .env
python send_sftp_alert.py --path /data/partner_a --partner PARTNER_A
```

**Output:**
```
======================================================================
🔍 SFTP FILE MONITOR with EMAIL ALERTS
======================================================================

📋 Configuration:
   SFTP: srv.42cssmtp@103.183.96.21:2022
   Path: /data/partner_a
   Partner: PARTNER_A

📡 Connecting to SFTP server...
✅ Connected successfully!

📂 Scanning directory: /data/partner_a
   Found 8 file(s)

🔍 Validating files...
  ✅ PARTNER_A_20241120_140000_TRANSACTION.csv
  ✅ PARTNER_A_20241120_180000_SETTLEMENT.csv
  ❌ invalid_file.csv
     → Filename does not match PARTNER_A pattern...

======================================================================
📧 Sending email alert...
✅ Email sent successfully!
📬 Check inbox: roshni.mohandas@gmail.com
======================================================================

📊 Summary:
   Total: 8 files
   Valid: 7 ✅
   Invalid: 1 ❌
======================================================================
```

---

## 📧 Email Alert Examples

### Test Email System

```bash
# Simple email connection test
python quick_email_test.py
```

### Send Test Email

```bash
# Send sample HTML email
python test_email_alert.py
```

---

## 🔧 Advanced Usage

### Python Script

```python
from src.validators.sftp_client import SFTPClient
from src.validators.file_validator import FileValidator

# Connect to SFTP
client = SFTPClient(
    host="103.183.96.21",
    port=2022,
    username="srv.42cssmtp",
    password="D]kjPL8Ccy6uGx3R"
)

if client.connect():
    # List files in directory
    files = client.list_files("/incoming")

    # Validate each file
    validator = FileValidator(partner="PARTNER_A")

    for file in files:
        if not file['is_dir']:
            result = validator.validate_all(
                filename=file['filename'],
                file_size=file['size'],
                file_mtime=file['mtime']
            )

            if result['valid']:
                print(f"✅ {file['filename']}")
            else:
                print(f"❌ {file['filename']}")
                print(f"   Errors: {result['errors']}")

    client.disconnect()
```

### Interactive Python Session

```bash
python
```

```python
>>> from src.validators.sftp_client import SFTPClient
>>>
>>> # Connect
>>> client = SFTPClient("103.183.96.21", 2022, "srv.42cssmtp", "D]kjPL8Ccy6uGx3R")
>>> client.connect()
True
>>>
>>> # Explore directories
>>> files = client.list_files("/")
>>> for f in files:
...     print(f"{f['filename']} ({'DIR' if f['is_dir'] else f['size']})")
...
partner_a DIR
partner_b DIR
incoming DIR
archive DIR
>>>
>>> # Check specific directory
>>> files = client.list_files("/incoming")
>>> for f in files:
...     if not f['is_dir']:
...         print(f"{f['filename']} - {f['size']} bytes - {f['modified_date']}")
...
PARTNER_A_20241120_140000_TRANSACTION.csv - 2048576 bytes - 2024-11-20T14:00:00
>>>
>>> # Validate a file
>>> from src.validators.file_validator import validate_file
>>> result = validate_file("PARTNER_A_20241120_140000_TRANSACTION.csv", 2048576, "PARTNER_A")
>>> print(result)
{'filename': 'PARTNER_A_20241120_140000_TRANSACTION.csv', 'partner': 'PARTNER_A', 'valid': True, 'errors': [], 'warnings': []}
>>>
>>> client.disconnect()
```

---

## ⏰ Automated Monitoring

### Cron Job (Linux/Mac)

```bash
# Edit crontab
crontab -e
```

Add one of these:

```bash
# Check every 15 minutes
*/15 * * * * cd /path/to/banking_partner-sftp-monitor && /usr/bin/python3 send_sftp_alert.py --path /incoming >> logs/monitor.log 2>&1

# Check every hour
0 * * * * cd /path/to/banking_partner-sftp-monitor && /usr/bin/python3 send_sftp_alert.py --path /partner_a --partner PARTNER_A >> logs/partner_a.log 2>&1

# Check at specific times (9 AM and 3 PM)
0 9,15 * * * cd /path/to/banking_partner-sftp-monitor && /usr/bin/python3 send_sftp_alert.py --path /incoming >> logs/monitor.log 2>&1

# Monitor both partners
*/15 * * * * cd /path/to/banking_partner-sftp-monitor && /usr/bin/python3 send_sftp_alert.py --path /partner_a --partner PARTNER_A >> logs/partner_a.log 2>&1
*/15 * * * * cd /path/to/banking_partner-sftp-monitor && /usr/bin/python3 send_sftp_alert.py --path /partner_b --partner PARTNER_B >> logs/partner_b.log 2>&1
```

### Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Name: "SFTP Monitor"
4. Trigger: Daily at 9:00 AM, repeat every 15 minutes
5. Action: Start a program
6. Program: `C:\Python39\python.exe`
7. Arguments: `send_sftp_alert.py --path /incoming`
8. Start in: `C:\path\to\banking_partner-sftp-monitor`

### Using Python Script

```python
# monitor_scheduler.py
import schedule
import time
from send_sftp_alert import monitor_sftp
import os
from dotenv import load_dotenv

load_dotenv()

def job():
    host = os.getenv('SFTP_HOST')
    port = int(os.getenv('SFTP_PORT', 22))
    username = os.getenv('SFTP_USERNAME')
    password = os.getenv('SFTP_PASSWORD')

    # Monitor partner A
    monitor_sftp(host, port, username, password, '/partner_a', 'PARTNER_A')

    # Monitor partner B
    monitor_sftp(host, port, username, password, '/partner_b', 'PARTNER_B')

# Run every 15 minutes
schedule.every(15).minutes.do(job)

print("📅 Scheduler started. Monitoring every 15 minutes...")
while True:
    schedule.run_pending()
    time.sleep(60)
```

Run it:
```bash
python monitor_scheduler.py
```

---

## 🎯 Common Use Cases

### 1. Daily Morning Check

```bash
# Check all partners every morning at 9 AM
# Add to crontab:
0 9 * * * cd /path/to/project && python send_sftp_alert.py --path / >> logs/daily.log 2>&1
```

### 2. Real-time Monitoring

```bash
# Check every 5 minutes during business hours (9 AM - 6 PM)
*/5 9-18 * * 1-5 cd /path/to/project && python send_sftp_alert.py --path /incoming >> logs/realtime.log 2>&1
```

### 3. End-of-Day Report

```bash
# Generate report at 6 PM every weekday
0 18 * * 1-5 cd /path/to/project && python send_sftp_alert.py --path / --partner GENERIC >> logs/eod.log 2>&1
```

### 4. Weekend Check

```bash
# Check once on weekends at 10 AM
0 10 * * 0,6 cd /path/to/project && python send_sftp_alert.py --path / >> logs/weekend.log 2>&1
```

---

## 📋 Command Line Options

```bash
python send_sftp_alert.py --help
```

**Options:**
- `--path, -p` : Remote path to monitor (default: /)
- `--partner` : Partner code (PARTNER_A, PARTNER_B, GENERIC)
- `--host` : SFTP host (overrides .env)
- `--port` : SFTP port (overrides .env)
- `--username` : SFTP username (overrides .env)
- `--password` : SFTP password (overrides .env)

---

## 🔍 Troubleshooting Commands

### Test Connection

```bash
# Simple connection test
python test_real_sftp.py
```

### Test Email

```bash
# Test email configuration
python quick_email_test.py

# Send test email
python test_email_alert.py
```

### Debug Mode

```python
# Run with verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)

from src.validators.sftp_client import SFTPClient
client = SFTPClient("103.183.96.21", 2022, "srv.42cssmtp", "password")
client.connect()
```

### Check Specific File

```bash
python -c "
from src.validators.file_validator import validate_file
result = validate_file('PARTNER_A_20241120_140000_TRANSACTION.csv', 1024, 'PARTNER_A')
print(result)
"
```

---

## 📊 Expected Email Format

After running monitoring, you'll receive:

```
Subject: 🚨 SFTP Alert: X Invalid File(s) Detected

┌────────────────────────────────────────┐
│  🚨 SFTP File Monitor Alert            │
│  Invalid Files Detected                │
└────────────────────────────────────────┘

📊 Monitoring Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Files Scanned:     10
Valid Files:             8 ✅
Invalid Files:           2 ❌
Success Rate:            80.0%

❌ Invalid Files
┌──────────────────┬──────┬──────────────┐
│ Filename         │ Size │ Errors       │
└──────────────────┴──────┴──────────────┘

✅ Valid Files
[List of valid files...]
```

---

## 💡 Tips

1. **Start with root directory** (`/`) to explore structure
2. **Use interactive Python** to find correct paths
3. **Test manually first** before automating
4. **Check logs regularly** when using cron jobs
5. **Keep .env file secure** - never commit to Git

---

## 📞 Need Help?

- **Test connection**: `python test_real_sftp.py`
- **Test email**: `python test_email_alert.py`
- **View help**: `python send_sftp_alert.py --help`
- **Contact**: roshni.mohandas@gmail.com
