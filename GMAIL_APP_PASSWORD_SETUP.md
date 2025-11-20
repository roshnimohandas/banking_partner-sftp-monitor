# 📧 Gmail App Password Setup Guide

Complete guide to enable programmatic access for email alerts.

## Why You Need This

Gmail **blocks** regular passwords when used by applications/scripts for security reasons. You must use an **App Password** - a 16-character code specifically for apps.

## 🔐 Step-by-Step Setup (5 minutes)

### Step 1: Enable 2-Factor Authentication (2FA)

**IMPORTANT**: You MUST enable 2FA first, or App Passwords won't be available.

1. **Go to Google Account Security**:
   - Open: https://myaccount.google.com/security
   - Or: Google Account → Security

2. **Find "2-Step Verification"**:
   - Look for "Signing in to Google" section
   - Click on "2-Step Verification"

3. **Enable 2FA**:
   - Click "Get Started"
   - Enter your password
   - Enter your phone number
   - Choose verification method:
     - **Text message (SMS)** - Recommended for beginners
     - **Phone call**
     - **Google Authenticator app**
   - Enter the verification code sent to your phone
   - Click "Turn On"

4. **Confirm it's enabled**:
   - You should see "2-Step Verification is ON"
   - Keep this tab open for next step

### Step 2: Generate App Password

1. **Go to App Passwords**:
   - Direct link: https://myaccount.google.com/apppasswords
   - Or: Google Account → Security → 2-Step Verification → App passwords (at the bottom)

2. **Sign in if prompted**:
   - Enter your Gmail password (regular password)
   - Complete 2FA verification

3. **Create New App Password**:

   **Option A: Using Dropdown (Old Interface)**
   - Click "Select app" dropdown → Choose **"Mail"**
   - Click "Select device" dropdown → Choose **"Other (Custom name)"**
   - Type: **"SFTP Monitor"** or **"Python Script"**
   - Click **"Generate"**

   **Option B: Direct Input (New Interface)**
   - You might see a text box directly
   - Type: **"SFTP Monitor"**
   - Click **"Create"**

4. **Copy the Password**:
   - You'll see a 16-character password in a yellow box
   - Example: `abcd efgh ijkl mnop`
   - **IMPORTANT**: Copy this NOW - you can't see it again!
   - Click "Done" when copied

### Step 3: Update Your .env File

1. **Open terminal/command prompt**:

```bash
cd banking_partner-sftp-monitor
nano .env
```

Or use any text editor (VS Code, Notepad++, etc.)

2. **Update the EMAIL_PASSWORD line**:

**Before:**
```bash
EMAIL_PASSWORD=YOUR-16-CHAR-APP-PASSWORD-HERE
```

**After (example):**
```bash
EMAIL_PASSWORD=abcd efgh ijkl mnop
```

**Note**: You can keep the spaces or remove them - both work:
```bash
EMAIL_PASSWORD=abcdefghijklmnop
# OR
EMAIL_PASSWORD=abcd efgh ijkl mnop
```

3. **Save the file**:
   - In nano: Press `Ctrl+X`, then `Y`, then `Enter`
   - In other editors: File → Save

### Step 4: Test the Connection

```bash
cd banking_partner-sftp-monitor

# Activate virtual environment
source venv/bin/activate

# Quick test
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

Check your inbox at **roshni.mohandas@gmail.com** - you should receive a beautiful test email!

---

## 📱 Alternative: Using Gmail Authenticator App

If you prefer Google Authenticator instead of SMS:

1. **Download Google Authenticator**:
   - iOS: App Store
   - Android: Google Play Store

2. **Setup in Security Settings**:
   - Go to: https://myaccount.google.com/security
   - Click "2-Step Verification"
   - Scroll to "Authenticator app"
   - Click "Set up"
   - Scan QR code with Authenticator app
   - Enter 6-digit code from app

3. **Then follow App Password steps above**

---

## 🔍 Troubleshooting

### Issue 1: "App passwords" option not showing

**Cause**: 2-Factor Authentication not enabled

**Fix**:
1. Go to: https://myaccount.google.com/security
2. Enable "2-Step Verification" first
3. Wait 5 minutes
4. Try accessing App Passwords again

### Issue 2: "This setting is not available for your account"

**Possible causes**:
- **Workspace/School Account**: Managed by organization - contact admin
- **Child Account**: Need parent permission
- **Recently created account**: Wait 24 hours

**Fix for Workspace accounts**:
- Ask your Google Workspace admin to enable "Less secure apps"
- Or ask them to create an App Password for you

### Issue 3: "Invalid credentials" when testing

**Causes**:
- Wrong App Password copied
- Extra spaces or characters
- Used regular password instead of App Password

**Fix**:
1. Generate NEW App Password
2. Delete old ones at: https://myaccount.google.com/apppasswords
3. Copy NEW password carefully
4. Update .env file
5. Test again

### Issue 4: Test script shows "Connection refused"

**Causes**:
- No internet connection
- Firewall blocking port 587
- Corporate network restrictions

**Fix**:
```bash
# Test connectivity
ping smtp.gmail.com

# Test port
telnet smtp.gmail.com 587
# Or with nc:
nc -zv smtp.gmail.com 587
```

If blocked, you may need to:
- Use different network (phone hotspot to test)
- Contact IT department
- Use VPN

### Issue 5: "Username and Password not accepted"

**This usually means**:
❌ You're using regular password: `Deluxe-Leasehold-Parkway`
✅ You should use App Password: `abcd efgh ijkl mnop`

**Fix**: Generate and use App Password (Steps 1-3 above)

---

## 📋 Quick Reference

### Gmail Settings URLs

| Setting | URL |
|---------|-----|
| Account Security | https://myaccount.google.com/security |
| 2-Step Verification | https://myaccount.google.com/signinoptions/two-step-verification |
| App Passwords | https://myaccount.google.com/apppasswords |
| Account Settings | https://myaccount.google.com |

### Configuration Files

```bash
# Main config file
banking_partner-sftp-monitor/.env

# Email settings
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_FROM=roshnitraining@gmail.com
EMAIL_TO=roshni.mohandas@gmail.com
EMAIL_PASSWORD=abcd-efgh-ijkl-mnop  # ← App Password here!
```

### Test Scripts

```bash
# Quick connection test
python quick_email_test.py

# Full email test with HTML
python test_email_alert.py

# SFTP monitoring with email
python send_sftp_alert.py
```

---

## 🎯 Checklist

Before running email alerts, verify:

- [ ] 2-Factor Authentication enabled
- [ ] App Password generated (16 characters)
- [ ] .env file updated with App Password
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] quick_email_test.py passes ✅
- [ ] Test email received successfully

---

## 🔒 Security Best Practices

1. **Never commit App Passwords to Git**:
   - `.env` is in `.gitignore` - don't force add it
   - Use `.env.example` for templates

2. **Rotate passwords regularly**:
   - Delete old App Passwords
   - Generate new ones every 3-6 months

3. **Use separate App Passwords**:
   - One for SFTP Monitor
   - One for other apps
   - Easier to revoke if compromised

4. **Delete unused App Passwords**:
   - Go to: https://myaccount.google.com/apppasswords
   - Revoke any you don't recognize

5. **Monitor account activity**:
   - Check: https://myaccount.google.com/notifications
   - Review login alerts

---

## ❓ FAQ

**Q: Can I use my regular Gmail password?**
A: No. Gmail blocks regular passwords for security. You must use App Password.

**Q: Will App Password work for logging into Gmail?**
A: No. App Passwords only work for apps/scripts, not for Gmail website/app login.

**Q: How many App Passwords can I create?**
A: Unlimited. Create one for each app/device.

**Q: Can I see my App Password again after creating it?**
A: No. Copy it immediately. If lost, delete and create new one.

**Q: Will this affect my regular Gmail login?**
A: No. App Passwords are completely separate from your main password.

**Q: Do I need 2FA enabled forever?**
A: Yes. If you disable 2FA, App Passwords stop working.

**Q: Can someone use my App Password to access my account?**
A: They can send emails on your behalf, but can't:
- Read your emails
- Access your account settings
- Change your password
- Access other Google services

**Q: What if I'm using a work/school Gmail account?**
A: Contact your IT admin - they control security settings.

---

## 📧 Support

**Need help?**
- Email: roshni.mohandas@gmail.com
- Check Gmail Help: https://support.google.com/accounts/answer/185833

**Google Support Links**:
- App Passwords Guide: https://support.google.com/accounts/answer/185833
- 2FA Setup: https://support.google.com/accounts/answer/185839
- Security Checkup: https://myaccount.google.com/security-checkup

---

## ✅ Success!

Once you see "✅ SUCCESS!" from `quick_email_test.py`, you're all set!

You can now:
- Send test email alerts
- Monitor SFTP servers with automatic email notifications
- Set up automated workflows with n8n
- Deploy to production

**Happy Monitoring!** 🎉
