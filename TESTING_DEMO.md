# 🧪 Testing & Demo Guide

Complete guide to set up and demo the SFTP monitoring system with a test SFTP server.

## Quick Demo Setup (15 minutes)

This guide will help you:
1. Set up a local SFTP server
2. Upload test files
3. Run the monitoring system
4. Trigger email/Slack alerts
5. See the system in action

## Option 1: Docker SFTP Server (Recommended - Easiest)

### Step 1: Create Test SFTP Server

```bash
# Create directory for SFTP data
mkdir -p ~/sftp-test/upload

# Run SFTP server with Docker
docker run -d \
  --name test-sftp \
  -p 2222:22 \
  -v ~/sftp-test/upload:/home/testuser/upload \
  atmoz/sftp \
  testuser:testpass:1001
```

Your SFTP server is now running on `localhost:2222`!

- **Host**: `localhost`
- **Port**: `2222`
- **Username**: `testuser`
- **Password**: `testpass`
- **Upload path**: `/upload`

### Step 2: Verify SFTP Connection

Test the connection:

```bash
# Using sftp command
sftp -P 2222 testuser@localhost
# Password: testpass
# Once connected, type: ls
# You should see the /upload directory
# Type: quit
```

Or use FileZilla/WinSCP:
- Host: `sftp://localhost`
- Port: `2222`
- Username: `testuser`
- Password: `testpass`

### Step 3: Create Test Files

Create sample banking files that match our validation patterns:

```bash
# Navigate to test directory
cd ~/sftp-test/upload

# Create PARTNER_A test files
echo "partner_a,transaction,test,data" > PARTNER_A_20241120_140000_TRANSACTION.csv
echo "partner_a,settlement,test,data" > PARTNER_A_20241120_180000_SETTLEMENT.csv
echo "partner_a,report,test,data" > PARTNER_A_20241120_100000_REPORT.csv

# Create PARTNER_B test files
echo "partner_b,txn,test,data" > PARTNER_B_20241120_143000_TXN.csv
echo "partner_b,settle,test,data" > PARTNER_B_20241120_173000_SETTLE.csv

# Create an INVALID file (wrong naming)
echo "invalid" > invalid_file.csv

# Verify files are created
ls -lh
```

**Expected output:**
```
-rw-r--r-- 1 user user   30 Nov 20 14:00 PARTNER_A_20241120_140000_TRANSACTION.csv
-rw-r--r-- 1 user user   30 Nov 20 18:00 PARTNER_A_20241120_180000_SETTLEMENT.csv
-rw-r--r-- 1 user user   25 Nov 20 10:00 PARTNER_A_20241120_100000_REPORT.csv
-rw-r--r-- 1 user user   25 Nov 20 14:30 PARTNER_B_20241120_143000_TXN.csv
-rw-r--r-- 1 user user   30 Nov 20 17:30 PARTNER_B_20241120_173000_SETTLE.csv
-rw-r--r-- 1 user user    8 Nov 20 14:35 invalid_file.csv
```

### Step 4: Configure Your Application

Update `.env` file in your project:

```bash
cd /path/to/banking_partner-sftp-monitor
nano .env
```

Add/Update these settings:

```bash
# SFTP Configuration (Test Server)
SFTP_HOST=localhost
SFTP_PORT=2222
SFTP_USERNAME=testuser
SFTP_PASSWORD=testpass

# Email Configuration (Gmail example)
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_FROM=your-email@gmail.com
EMAIL_TO=roshni.mohandas@gmail.com
EMAIL_PASSWORD=your-app-password

# Slack Configuration (Optional)
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_CHANNEL_ID=your-channel-id

# Web Interface
WEB_HOST=0.0.0.0
WEB_PORT=5000
```

**Important**: For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833):
1. Go to Google Account Settings
2. Security → 2-Step Verification → App Passwords
3. Generate a new app password for "Mail"
4. Use this password in `EMAIL_PASSWORD`

### Step 5: Test Python Validator

```bash
# Activate virtual environment
source venv/bin/activate

# Test the SFTP connection and validator
python << 'EOF'
from src.validators.sftp_client import SFTPClient
from src.validators.file_validator import FileValidator

# Connect to test SFTP
print("🔌 Connecting to SFTP server...")
with SFTPClient(
    host="localhost",
    port=2222,
    username="testuser",
    password="testpass"
) as client:
    print("✅ Connected successfully!")

    # List files
    print("\n📂 Listing files in /upload...")
    files = client.list_files("/upload")

    for file in files:
        print(f"\n📄 File: {file['filename']}")
        print(f"   Size: {file['size']} bytes")
        print(f"   Modified: {file['modified_date']}")

        # Validate each file
        validator_a = FileValidator(partner="PARTNER_A")
        validator_b = FileValidator(partner="PARTNER_B")

        # Try PARTNER_A validation
        result_a = validator_a.validate_all(
            filename=file['filename'],
            file_size=file['size'],
            file_mtime=file['mtime']
        )

        # Try PARTNER_B validation
        result_b = validator_b.validate_all(
            filename=file['filename'],
            file_size=file['size'],
            file_mtime=file['mtime']
        )

        # Determine which partner this file belongs to
        if result_a['valid']:
            print(f"   ✅ Valid PARTNER_A file")
        elif result_b['valid']:
            print(f"   ✅ Valid PARTNER_B file")
        else:
            print(f"   ❌ Invalid file")
            print(f"   Errors: {result_a['errors']}")

print("\n✅ Test completed!")
EOF
```

**Expected output:**
```
🔌 Connecting to SFTP server...
✅ Connected successfully!

📂 Listing files in /upload...

📄 File: PARTNER_A_20241120_140000_TRANSACTION.csv
   Size: 30 bytes
   Modified: 2024-11-20T14:00:00
   ✅ Valid PARTNER_A file

📄 File: PARTNER_B_20241120_143000_TXN.csv
   Size: 25 bytes
   Modified: 2024-11-20T14:30:00
   ✅ Valid PARTNER_B file

📄 File: invalid_file.csv
   Size: 8 bytes
   Modified: 2024-11-20T14:35:00
   ❌ Invalid file
   Errors: ['Filename does not match PARTNER_A pattern...']

✅ Test completed!
```

### Step 6: Test Email Alert

```bash
# Test sending email alert
python << 'EOF'
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

# Email configuration
smtp_host = os.getenv('EMAIL_SMTP_HOST')
smtp_port = int(os.getenv('EMAIL_SMTP_PORT'))
from_email = os.getenv('EMAIL_FROM')
to_email = os.getenv('EMAIL_TO')
password = os.getenv('EMAIL_PASSWORD')

# Create test alert email
message = MIMEMultipart('alternative')
message['Subject'] = '🧪 SFTP Monitor - Test Alert'
message['From'] = from_email
message['To'] = to_email

html = """
<html>
  <body>
    <h2>🧪 Test Alert - File Detected</h2>
    <p><strong>File:</strong> PARTNER_A_20241120_140000_TRANSACTION.csv</p>
    <p><strong>Partner:</strong> PARTNER_A</p>
    <p><strong>Status:</strong> ✅ Valid</p>
    <p><strong>Size:</strong> 30 bytes</p>
    <p><strong>Time:</strong> 14:00</p>
    <hr>
    <p>This is a test alert from your SFTP monitoring system.</p>
    <p><em>If you received this email, your alert system is working correctly!</em></p>
  </body>
</html>
"""

message.attach(MIMEText(html, 'html'))

try:
    print("📧 Sending test email...")
    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(from_email, password)
    server.sendmail(from_email, to_email, message.as_string())
    server.quit()
    print(f"✅ Test email sent successfully to {to_email}!")
except Exception as e:
    print(f"❌ Failed to send email: {str(e)}")
    print("Please check your email configuration in .env file")
EOF
```

### Step 7: Start the Web Dashboard

```bash
# Start Flask backend
python src/web/app.py &

# Wait for server to start
sleep 3

# Open browser
echo "🌐 Dashboard running at http://localhost:5000"
```

**Access the dashboard:**
1. Open browser: http://localhost:5000
2. Click "Connect" to SFTP
3. Enter connection details:
   - Connection Name: `test-server`
   - Host: `localhost`
   - Port: `2222`
   - Username: `testuser`
   - Password: `testpass`
4. Click "Start Monitoring"
5. Select Remote Path: `/upload`
6. Select Partner: `PARTNER_A` or `PARTNER_B`

You should see:
- ✅ Valid files in green
- ❌ Invalid files in red
- File details (size, modified time)

### Step 8: Simulate Real-Time File Arrival

Open a new terminal and add files while monitoring:

```bash
# Simulate file arrival every 10 seconds
cd ~/sftp-test/upload

# Valid file
echo "new,data,here" > PARTNER_A_$(date +%Y%m%d_%H%M%S)_TRANSACTION.csv
echo "✅ Added valid PARTNER_A file"

sleep 10

# Another valid file
echo "partner,b,data" > PARTNER_B_$(date +%Y%m%d_%H%M%S)_TXN.csv
echo "✅ Added valid PARTNER_B file"

sleep 10

# Invalid file (should trigger alert)
echo "bad" > invalid_$(date +%Y%m%d_%H%M%S).csv
echo "❌ Added invalid file - should trigger alert!"
```

Watch the dashboard update in real-time!

### Step 9: Test Complete Workflow

Test the complete monitoring and alerting workflow:

```bash
python << 'EOF'
from src.validators.sftp_client import SFTPClient
from src.validators.file_validator import FileValidator
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to SFTP
print("🔌 Connecting to SFTP...")
with SFTPClient(
    host="localhost",
    port=2222,
    username="testuser",
    password="testpass"
) as client:

    # Monitor /upload directory
    print("📂 Monitoring /upload directory...")
    files = client.list_files("/upload")

    validator_a = FileValidator(partner="PARTNER_A")
    invalid_files = []
    valid_files = []

    # Validate all files
    for file in files:
        if file['is_dir']:
            continue

        result = validator_a.validate_all(
            filename=file['filename'],
            file_size=file['size'],
            file_mtime=file['mtime']
        )

        if result['valid']:
            valid_files.append(file['filename'])
            print(f"✅ {file['filename']} - Valid")
        else:
            invalid_files.append({
                'filename': file['filename'],
                'errors': result['errors']
            })
            print(f"❌ {file['filename']} - Invalid: {result['errors']}")

    # Send summary email
    if invalid_files:
        print(f"\n📧 Sending alert email for {len(invalid_files)} invalid files...")

        # Email configuration
        smtp_host = os.getenv('EMAIL_SMTP_HOST')
        smtp_port = int(os.getenv('EMAIL_SMTP_PORT'))
        from_email = os.getenv('EMAIL_FROM')
        to_email = os.getenv('EMAIL_TO')
        password = os.getenv('EMAIL_PASSWORD')

        message = MIMEMultipart('alternative')
        message['Subject'] = f'🚨 SFTP Alert: {len(invalid_files)} Invalid Files Detected'
        message['From'] = from_email
        message['To'] = to_email

        error_list = '\n'.join([
            f"<li><strong>{f['filename']}</strong>: {', '.join(f['errors'])}</li>"
            for f in invalid_files
        ])

        html = f"""
        <html>
          <body>
            <h2>🚨 Invalid Files Detected</h2>
            <p>Found {len(invalid_files)} invalid file(s) on SFTP server:</p>
            <ul>{error_list}</ul>
            <hr>
            <h3>Summary:</h3>
            <p>✅ Valid files: {len(valid_files)}</p>
            <p>❌ Invalid files: {len(invalid_files)}</p>
            <p><em>Timestamp: {os.popen('date').read().strip()}</em></p>
          </body>
        </html>
        """

        message.attach(MIMEText(html, 'html'))

        try:
            server = smtplib.SMTP(smtp_host, smtp_port)
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, message.as_string())
            server.quit()
            print(f"✅ Alert email sent to {to_email}!")
        except Exception as e:
            print(f"❌ Failed to send email: {str(e)}")
    else:
        print("\n✅ All files are valid - No alerts needed")

print("\n🎉 Demo completed successfully!")
EOF
```

## Option 2: OpenSSH SFTP Server (Linux/Mac)

If you don't want to use Docker:

```bash
# On Linux
sudo apt-get install openssh-server
sudo systemctl start ssh

# On Mac
sudo systemsetup -setremotelogin on

# Create test user
sudo useradd -m -s /bin/bash testuser
echo "testuser:testpass" | sudo chpasswd

# Create upload directory
sudo mkdir -p /home/testuser/upload
sudo chown testuser:testuser /home/testuser/upload
```

Connect on port 22 instead of 2222.

## Cleanup

When done testing:

```bash
# Stop Docker SFTP server
docker stop test-sftp
docker rm test-sftp

# Remove test files
rm -rf ~/sftp-test

# Stop Flask server
pkill -f "python src/web/app.py"
```

## Demo Checklist

- [ ] SFTP server running
- [ ] Test files created with correct naming
- [ ] Test files created with incorrect naming
- [ ] Python validator connects successfully
- [ ] Files are validated correctly (valid ✅ / invalid ❌)
- [ ] Email sent successfully on test
- [ ] Web dashboard shows files
- [ ] Invalid files trigger alerts
- [ ] Real-time file monitoring works

## Troubleshooting

**SFTP connection refused:**
```bash
# Check if Docker container is running
docker ps | grep test-sftp

# Check port is not in use
lsof -i :2222

# Restart container
docker restart test-sftp
```

**Email not sending:**
- Verify Gmail App Password is correct
- Check 2-factor authentication is enabled
- Test SMTP connection: `telnet smtp.gmail.com 587`

**Files not appearing:**
- Verify files are in correct directory: `docker exec test-sftp ls -la /home/testuser/upload`
- Check file permissions
- Ensure filenames match the pattern exactly

## Next Steps

After successful demo:
1. Set up n8n for automated workflows (see `docs/DEPLOYMENT.md`)
2. Configure Google Sheets logging
3. Deploy React dashboard to GitHub Pages
4. Set up production SFTP credentials

---

**Questions?** Email: roshni.mohandas@gmail.com
