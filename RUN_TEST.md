# 🚀 Run Email Alert Test - Quick Guide

## Before You Start

### 1. Get Gmail App Password

**IMPORTANT**: You MUST use a Gmail App Password, not your regular password!

1. **Enable 2-Factor Authentication**:
   - Go to: https://myaccount.google.com/security
   - Click "2-Step Verification"
   - Follow the setup process

2. **Generate App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select app: **Mail**
   - Select device: **Other (Custom name)** → Type "SFTP Monitor"
   - Click **Generate**
   - Copy the 16-character code (e.g., `abcd efgh ijkl mnop`)

### 2. Update .env File

Edit the `.env` file in the project root:

```bash
cd banking_partner-sftp-monitor
nano .env
```

Update this line with your App Password:

```bash
EMAIL_PASSWORD=abcd-efgh-ijkl-mnop
```

Replace `abcd-efgh-ijkl-mnop` with your actual 16-character App Password.

## 🧪 Test 1: Simple Email Test (30 seconds)

```bash
# Make sure you're in the project directory
cd banking_partner-sftp-monitor

# Activate virtual environment
source venv/bin/activate

# Run test
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

**Check Your Email:**
- Open Gmail: roshni.mohandas@gmail.com
- Look for email: "🧪 SFTP Monitor - Email Alert Test"
- Beautiful HTML email with sample alert

## 🔍 Test 2: Full SFTP Monitoring (5 minutes)

### Setup Test SFTP Server

```bash
# Run test SFTP server
docker run -d \
  --name test-sftp \
  -p 2222:22 \
  -v ~/sftp-test/upload:/home/testuser/upload \
  atmoz/sftp \
  testuser:testpass:1001

# Create test directory
mkdir -p ~/sftp-test/upload
cd ~/sftp-test/upload
```

### Create Test Files

```bash
# Valid files (will show as ✅)
echo "partner_a,transaction,data" > PARTNER_A_20241120_140000_TRANSACTION.csv
echo "partner_a,settlement,data" > PARTNER_A_20241120_180000_SETTLEMENT.csv
echo "partner_b,txn,data" > PARTNER_B_20241120_143000_TXN.csv

# Invalid file (will trigger ❌ alert!)
echo "invalid" > invalid_file.csv
echo "bad_name" > wrong_format.txt

# Check files created
ls -lh
```

### Run Monitoring with Email Alerts

```bash
cd ~/banking_partner-sftp-monitor

# Run the monitor
python send_sftp_alert.py
```

**You'll See:**
```
======================================================================
🔍 SFTP FILE MONITOR with EMAIL ALERTS
======================================================================

📡 Connecting to SFTP server...
   Host: localhost:2222
   Path: /upload
   Partner: PARTNER_A

✅ Connected successfully!

📂 Scanning directory: /upload
   Found 5 file(s)

🔍 Validating files...
  ✅ PARTNER_A_20241120_140000_TRANSACTION.csv
  ✅ PARTNER_A_20241120_180000_SETTLEMENT.csv
  ✅ PARTNER_B_20241120_143000_TXN.csv
  ❌ invalid_file.csv
     → Filename does not match PARTNER_A pattern...
  ❌ wrong_format.txt
     → Invalid file extension...

======================================================================
📧 Sending email alert...
✅ Email sent successfully!
📬 Check inbox: roshni.mohandas@gmail.com
======================================================================

📊 Summary:
   Total: 5 files
   Valid: 3 ✅
   Invalid: 2 ❌
======================================================================
```

**Check Your Email Again:**
You'll receive a detailed HTML email showing:
- ❌ Invalid files table with errors
- ✅ Valid files list
- 📊 Summary statistics
- ⚠️ Action required section

## 🎯 What the Email Looks Like

```
Subject: 🚨 SFTP Alert: 2 Invalid File(s) Detected

┌─────────────────────────────────────────┐
│  🚨 SFTP File Monitor Alert             │
│  Invalid Files Detected                 │
└─────────────────────────────────────────┘

📊 Monitoring Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Files Scanned:     5
Valid Files:             3 ✅
Invalid Files:           2 ❌
Success Rate:            60.0%

❌ Invalid Files
┌──────────────────┬──────┬──────────────┐
│ Filename         │ Size │ Errors       │
├──────────────────┼──────┼──────────────┤
│ invalid_file.csv │ 8 B  │ Invalid      │
│                  │      │ filename...  │
├──────────────────┼──────┼──────────────┤
│ wrong_format.txt │ 10 B │ Invalid ext  │
└──────────────────┴──────┴──────────────┘

✅ Valid Files
• PARTNER_A_20241120_140000_TRANSACTION.csv - 28 B
• PARTNER_A_20241120_180000_SETTLEMENT.csv - 28 B
• PARTNER_B_20241120_143000_TXN.csv - 23 B
```

## ⚠️ Troubleshooting

### "Authentication Failed"
- You're using regular password instead of App Password
- Follow steps above to generate App Password
- Update `.env` file with the 16-character code

### "Connection Refused" (SFTP)
- Docker not running: `docker ps`
- Wrong port: Should be 2222
- Restart: `docker restart test-sftp`

### "Module not found"
- Virtual environment not activated
- Run: `source venv/bin/activate`
- Install deps: `pip install -r requirements.txt`

### Email Not Arriving
- Check spam folder
- Verify EMAIL_TO address in .env
- Test with: `python quick_email_test.py`

## 🧹 Cleanup

When done testing:

```bash
# Stop SFTP server
docker stop test-sftp
docker rm test-sftp

# Remove test files
rm -rf ~/sftp-test

# Deactivate virtual environment
deactivate
```

## 📧 Email Addresses

- **Sender**: roshnitraining@gmail.com (needs App Password)
- **Recipient**: roshni.mohandas@gmail.com (gets the alerts)

## ✅ Success Criteria

You'll know it's working when:
1. Test email arrives in roshni.mohandas@gmail.com inbox
2. Email has professional HTML formatting
3. Shows sample invalid file alert
4. SFTP monitor runs without errors
5. Detailed alert email shows real file validation results

## 🎉 Next Steps

Once emails are working:
1. Connect to real SFTP server (update .env)
2. Set up n8n workflows for automation
3. Configure Google Sheets logging
4. Deploy to production

---

**Need Help?** Email: roshni.mohandas@gmail.com
