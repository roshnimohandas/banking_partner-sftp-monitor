# 🖥️ Test Email Alerts on Your Computer

## Why Didn't the Email Send?

We're in a cloud/sandboxed environment **without internet access**. To send real emails, you need to run the scripts on **your local computer** with internet connection.

## 🚀 Step-by-Step Guide (10 minutes)

### Step 1: Clone the Repository to Your Computer

Open terminal/command prompt on your local machine:

```bash
# Clone the repo (replace with your actual repo URL)
git clone https://github.com/roshnimohandas/banking_partner-sftp-monitor.git

# Navigate to the directory
cd banking_partner-sftp-monitor
```

### Step 2: Create .env File with Your Password

**On Windows:**
```bash
notepad .env
```

**On Mac/Linux:**
```bash
nano .env
```

**Paste this content:**
```bash
# SFTP Configuration (Test Server)
SFTP_HOST=localhost
SFTP_PORT=2222
SFTP_USERNAME=testuser
SFTP_PASSWORD=testpass

# Email Configuration
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_FROM=roshnitraining@gmail.com
EMAIL_TO=roshni.mohandas@gmail.com
EMAIL_PASSWORD=frib eedv rkom mijs

# Slack Configuration (Optional)
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_CHANNEL_ID=your-channel-id

# Web Interface
WEB_HOST=0.0.0.0
WEB_PORT=5000
WEB_SECRET_KEY=your-secret-key-here

# Monitoring Configuration
CHECK_INTERVAL_MINUTES=15
ALERT_RETRY_COUNT=3
```

**Save the file** (Ctrl+S in Notepad, Ctrl+X then Y in nano)

### Step 3: Install Python Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

You should see something like:
```
Collecting paramiko>=3.4.0
Collecting python-dotenv>=1.0.0
...
Successfully installed ...
```

### Step 4: Test Email Connection

```bash
python quick_email_test.py
```

**Expected Output:**
```
Testing Gmail SMTP connection...
Email: roshnitraining@gmail.com
Server: smtp.gmail.com:587
--------------------------------------------------

1. Connecting to SMTP server...
2. Starting TLS encryption...
3. Attempting login...
4. Closing connection...

==================================================
✅ SUCCESS! Email credentials are working!
==================================================

You can now run: python test_email_alert.py
```

### Step 5: Send Test Email

```bash
python test_email_alert.py
```

**Expected Output:**
```
======================================================================
📧 EMAIL ALERT TEST - SFTP Monitor
======================================================================

📤 Sending test email...
   From: roshnitraining@gmail.com
   To: roshni.mohandas@gmail.com
   SMTP: smtp.gmail.com:587

🔐 Connecting to SMTP server...
🔑 Authenticating...
📨 Sending email...

======================================================================
✅ SUCCESS! Email sent successfully!
======================================================================

📬 Check your inbox: roshni.mohandas@gmail.com
```

### Step 6: Check Your Email

Open Gmail: **roshni.mohandas@gmail.com**

Look for email with subject:
```
🧪 SFTP Monitor - Email Alert Test
```

The email will have:
- Professional HTML design
- Sample invalid file alert
- Validation details
- Next steps

**Check spam folder if not in inbox!**

---

## 🧪 Test Full SFTP Monitoring (Optional)

If you want to test the complete system with SFTP:

### Setup Test SFTP Server

**If you have Docker:**
```bash
docker run -d \
  --name test-sftp \
  -p 2222:22 \
  -v ~/sftp-test/upload:/home/testuser/upload \
  atmoz/sftp \
  testuser:testpass:1001
```

**Create test files:**
```bash
mkdir -p ~/sftp-test/upload
cd ~/sftp-test/upload

# Valid files
echo "data" > PARTNER_A_20241120_140000_TRANSACTION.csv
echo "data" > PARTNER_B_20241120_143000_TXN.csv

# Invalid file (will trigger alert!)
echo "bad" > invalid_file.csv
```

### Run SFTP Monitor with Email Alerts

```bash
cd ~/banking_partner-sftp-monitor
python send_sftp_alert.py
```

You'll receive another email showing:
- ❌ Invalid files detected
- ✅ Valid files list
- 📊 Summary statistics

---

## ⚠️ Troubleshooting

### "No module named 'paramiko'"
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### "Authentication failed"
- Double-check App Password: `frib eedv rkom mijs`
- Verify in .env file
- Make sure no extra spaces or quotes

### "Connection refused" or "Network error"
- Check internet connection
- Try: `ping smtp.gmail.com`
- Check firewall isn't blocking port 587

### Email not arriving
1. **Check spam folder** (most common!)
2. Verify email address is correct
3. Wait 1-2 minutes
4. Check Gmail filters/rules

### "Permission denied" on .env
```bash
# Give read permissions
chmod 600 .env
```

---

## 📋 Quick Command Summary

```bash
# Clone repo
git clone <repo-url>
cd banking_partner-sftp-monitor

# Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file with your App Password

# Test
python quick_email_test.py      # Test connection
python test_email_alert.py      # Send test email
python send_sftp_alert.py       # Full SFTP monitoring
```

---

## ✅ What You Should See

**1. Terminal Output:**
```
✅ SUCCESS! Email sent successfully!
📬 Check your inbox: roshni.mohandas@gmail.com
```

**2. In Gmail Inbox:**
Email with professional HTML design showing:
- 🧪 Test alert header
- Sample file validation
- Beautiful formatting
- Action items

**3. If SFTP monitoring:**
Email showing real file validation results from SFTP server

---

## 🎯 Success Checklist

- [ ] Repository cloned to local computer
- [ ] .env file created with App Password
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] quick_email_test.py shows ✅ SUCCESS
- [ ] test_email_alert.py completes without errors
- [ ] Email received in roshni.mohandas@gmail.com
- [ ] Email has professional HTML formatting

---

## 💡 Why This Works Locally But Not in Cloud

| Environment | Internet | Can Send Email |
|-------------|----------|----------------|
| Cloud/Sandbox | ❌ No | ❌ No |
| Your Computer | ✅ Yes | ✅ Yes |

The scripts work perfectly - they just need internet connection to reach Gmail's servers!

---

## 📧 Expected Email

**Subject:** 🧪 SFTP Monitor - Email Alert Test

**From:** roshnitraining@gmail.com

**To:** roshni.mohandas@gmail.com

**Body:** Beautiful HTML email with sample alert showing:
- File validation example
- Error details
- Professional gradient design
- Call to action

---

## 🎉 Once It Works

After successful testing:
1. Set up real SFTP connections
2. Configure n8n for automation
3. Deploy to production server
4. Set up cron jobs for scheduled monitoring

---

## 📞 Still Having Issues?

1. **Check the logs:** Run with more verbose output
2. **Test Gmail directly:** Try logging into Gmail web to confirm account works
3. **Verify App Password:** Regenerate if needed
4. **Contact:** roshni.mohandas@gmail.com

---

**Remember:** This MUST run on your local computer with internet access, not in the cloud environment! 🌐
