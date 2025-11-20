# 🔌 Test Real SFTP Server Connection

Your SFTP credentials have been saved in `.env` file. Here's how to test them on your local computer.

## 🔐 Your SFTP Credentials

```
Host: 103.183.96.21
Port: 2022
Username: srv.42cssmtp
Password: D]kjPL8Ccy6uGx3R
```

**Status**: ✅ Credentials saved in `.env` file (not pushed to GitHub)

## 🧪 Test Connection on Your Computer

### Step 1: Clone Repository

```bash
git clone https://github.com/roshnimohandas/banking_partner-sftp-monitor.git
cd banking_partner-sftp-monitor
```

### Step 2: Create .env File

The `.env` file should already have your credentials. If not, create it:

```bash
nano .env
```

Add:
```bash
# SFTP Configuration (Real Server)
SFTP_HOST=103.183.96.21
SFTP_PORT=2022
SFTP_USERNAME=srv.42cssmtp
SFTP_PASSWORD=D]kjPL8Ccy6uGx3R

# Email Configuration
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_FROM=roshnitraining@gmail.com
EMAIL_TO=roshni.mohandas@gmail.com
EMAIL_PASSWORD=frib eedv rkom mijs
```

### Step 3: Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 4: Test SFTP Connection

```bash
python test_real_sftp.py
```

**Expected Output:**
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
   Found X items:

   📁 Directories:
      📁 partner_a/
      📁 partner_b/
      📁 incoming/
      📁 archive/

   📄 Files:
      📄 file1.csv (1.23 MB)
      📄 file2.csv (2.45 MB)

======================================================================
✅ SFTP CONNECTION TEST SUCCESSFUL!
======================================================================
```

### Step 5: Explore Directories

Once connected, modify the script to explore specific directories:

```python
# Edit test_real_sftp.py, change this line:
files = client.list_files('/path/to/your/files')
```

Or run interactively:

```bash
python
```

```python
from src.validators.sftp_client import SFTPClient

client = SFTPClient(
    host="103.183.96.21",
    port=2022,
    username="srv.42cssmtp",
    password="D]kjPL8Ccy6uGx3R"
)

client.connect()

# List root
files = client.list_files('/')
for f in files:
    print(f"{f['filename']} - {'DIR' if f['is_dir'] else f['size']} bytes")

# Explore specific directory
files = client.list_files('/incoming')  # Change path as needed
for f in files:
    print(f)

client.disconnect()
```

## 📊 Test File Validation

Once you find where the files are:

```bash
python send_sftp_alert.py
```

This will:
1. Connect to your SFTP server
2. List all files in the specified directory
3. Validate each file against naming patterns
4. Send email alerts for invalid files

## 🎯 Next Steps After Connection Success

### 1. Identify File Locations

Find out where your partner files are stored:
```bash
# Common paths:
/incoming/
/partner_a/
/partner_b/
/uploads/
/data/
```

### 2. Update Monitoring Script

Edit `send_sftp_alert.py`:

```python
# Line ~65, change:
remote_path = '/your/actual/path'  # e.g., '/incoming'
partner = 'PARTNER_A'  # or 'PARTNER_B'
```

### 3. Test Validation

```bash
python send_sftp_alert.py
```

Check email at `roshni.mohandas@gmail.com` for validation results!

### 4. Set Up Automated Monitoring

Once working, set up cron job:

```bash
crontab -e
```

Add:
```bash
# Check every 15 minutes
*/15 * * * * cd /path/to/banking_partner-sftp-monitor && /path/to/python send_sftp_alert.py >> logs/monitor.log 2>&1
```

## ⚠️ Troubleshooting

### Connection Refused / Timeout

**Cause**: Network/firewall blocking connection

**Solutions**:
1. Check if you can ping the server:
   ```bash
   ping 103.183.96.21
   ```

2. Test port connectivity:
   ```bash
   telnet 103.183.96.21 2022
   # Or:
   nc -zv 103.183.96.21 2022
   ```

3. Check if your IP is whitelisted on the SFTP server
4. Try from different network (office network, VPN, etc.)

### Authentication Failed

**Cause**: Wrong credentials

**Solutions**:
1. Double-check username: `srv.42cssmtp`
2. Verify password: `D]kjPL8Ccy6uGx3R`
3. Check if password has special characters correctly entered
4. Confirm credentials with server admin

### Permission Denied

**Cause**: User doesn't have access to directory

**Solutions**:
1. Try listing root directory first: `client.list_files('/')`
2. Check user permissions with server admin
3. Try different paths

### Module Not Found

```bash
pip install -r requirements.txt
```

## 🔐 Security Notes

1. **Credentials are in .env**: Never commit this file to Git
2. **.env is in .gitignore**: Automatically protected
3. **Change passwords regularly**: Security best practice
4. **Use SSH keys if possible**: More secure than passwords
5. **Restrict IP access**: Configure SFTP server to allow only trusted IPs

## 📧 Email Alerts Configuration

Your email is already configured:
- **From**: roshnitraining@gmail.com
- **To**: roshni.mohandas@gmail.com
- **App Password**: Set (frib eedv rkom mijs)

When files are validated, you'll receive emails showing:
- ✅ Valid files
- ❌ Invalid files with error details
- 📊 Summary statistics

## 🎨 Example Email Alert

```
Subject: 🚨 SFTP Alert: 2 Invalid File(s) Detected

┌────────────────────────────────────────┐
│  🚨 SFTP File Monitor Alert            │
│  Invalid Files Detected                │
└────────────────────────────────────────┘

📊 Monitoring Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Files Scanned:     5
Valid Files:             3 ✅
Invalid Files:           2 ❌
Success Rate:            60.0%
Scan Time:               2024-11-20 14:30:00

❌ Invalid Files
┌──────────────────┬──────┬──────────────┐
│ Filename         │ Size │ Errors       │
├──────────────────┼──────┼──────────────┤
│ invalid_file.csv │ 8 B  │ Invalid      │
│                  │      │ filename...  │
└──────────────────┴──────┴──────────────┘
```

## ✅ Success Checklist

- [ ] Repository cloned to local computer
- [ ] .env file has SFTP credentials
- [ ] Dependencies installed
- [ ] test_real_sftp.py runs successfully
- [ ] Can list SFTP directories
- [ ] Found where partner files are located
- [ ] Updated remote_path in monitoring script
- [ ] send_sftp_alert.py validates files correctly
- [ ] Email alert received successfully
- [ ] Ready to deploy to production

## 🚀 Quick Command Reference

```bash
# Setup
git clone <repo-url>
cd banking_partner-sftp-monitor
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Test SFTP
python test_real_sftp.py

# Monitor with email alerts
python send_sftp_alert.py

# Check specific directory
python -c "from src.validators.sftp_client import SFTPClient; c = SFTPClient('103.183.96.21', 2022, 'srv.42cssmtp', 'D]kjPL8Ccy6uGx3R'); c.connect(); print(c.list_files('/your/path')); c.disconnect()"
```

## 📞 Need Help?

- **Email**: roshni.mohandas@gmail.com
- **Test email**: python test_email_alert.py
- **Test SFTP**: python test_real_sftp.py
- **Monitor files**: python send_sftp_alert.py

---

**Note**: This MUST run on your local computer with internet access. The cloud/sandbox environment cannot connect to external servers.
