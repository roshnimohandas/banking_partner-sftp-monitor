#!/usr/bin/env python3
"""
SFTP Monitor with Email Alerts
Monitors SFTP server and sends email alerts for invalid files
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from src.validators.sftp_client import SFTPClient
from src.validators.file_validator import FileValidator

load_dotenv()

def format_bytes(bytes_size):
    """Format bytes to human readable"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"

def send_alert_email(results, sftp_path):
    """Send email alert for invalid files"""

    smtp_host = os.getenv('EMAIL_SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.getenv('EMAIL_SMTP_PORT', 587))
    from_email = os.getenv('EMAIL_FROM')
    to_email = os.getenv('EMAIL_TO', 'roshni.mohandas@gmail.com')
    password = os.getenv('EMAIL_PASSWORD')

    if not from_email or not password:
        print("❌ Email not configured in .env file")
        return False

    # Create email
    message = MIMEMultipart('alternative')

    if results['invalid']:
        message['Subject'] = f'🚨 SFTP Alert: {len(results["invalid"])} Invalid File(s) Detected'
    else:
        message['Subject'] = f'✅ SFTP Monitor: All Files Valid ({len(results["valid"])} files)'

    message['From'] = from_email
    message['To'] = to_email

    # Build invalid files table
    invalid_rows = ""
    for item in results['invalid']:
        errors = '<br>'.join([f'• {e}' for e in item['errors']])
        invalid_rows += f"""
        <tr>
          <td style="padding: 12px; border-bottom: 1px solid #ddd;">{item['file']['filename']}</td>
          <td style="padding: 12px; border-bottom: 1px solid #ddd;">{format_bytes(item['file']['size'])}</td>
          <td style="padding: 12px; border-bottom: 1px solid #ddd;">{item['file']['modified_date']}</td>
          <td style="padding: 12px; border-bottom: 1px solid #ddd; color: #dc3545;">{errors}</td>
        </tr>
        """

    # Build valid files list
    valid_rows = ""
    for file in results['valid'][:10]:  # Show first 10
        valid_rows += f"""
        <tr>
          <td style="padding: 12px; border-bottom: 1px solid #ddd;">{file['filename']}</td>
          <td style="padding: 12px; border-bottom: 1px solid #ddd;">{format_bytes(file['size'])}</td>
          <td style="padding: 12px; border-bottom: 1px solid #ddd;">{file['modified_date']}</td>
          <td style="padding: 12px; border-bottom: 1px solid #ddd; color: #28a745;">✅ Valid</td>
        </tr>
        """

    if len(results['valid']) > 10:
        valid_rows += f"""
        <tr>
          <td colspan="4" style="padding: 12px; text-align: center; font-style: italic; color: #666;">
            ... and {len(results['valid']) - 10} more valid file(s)
          </td>
        </tr>
        """

    # Determine alert color
    alert_color = "#dc3545" if results['invalid'] else "#28a745"
    alert_icon = "🚨" if results['invalid'] else "✅"
    alert_title = "Invalid Files Detected" if results['invalid'] else "All Files Valid"

    # Create HTML email
    html = f"""
    <html>
      <head>
        <style>
          body {{ font-family: Arial, sans-serif; }}
          .container {{ max-width: 800px; margin: 0 auto; }}
          .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px 10px 0 0;
            text-align: center;
          }}
          .content {{ background: #f9f9f9; padding: 30px; }}
          .alert-banner {{
            background: {alert_color};
            color: white;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
          }}
          table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            border-radius: 5px;
            overflow: hidden;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
          }}
          th {{
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
          }}
          td {{
            padding: 12px;
            border-bottom: 1px solid #ddd;
          }}
          .summary {{
            background: white;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
          }}
          .summary-item {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
          }}
          .footer {{
            background: #333;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 0 0 10px 10px;
          }}
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h1 style="margin: 0;">{alert_icon} SFTP File Monitor Alert</h1>
            <p style="margin: 10px 0 0 0;">{alert_title}</p>
          </div>

          <div class="content">
            <div class="alert-banner">
              <h2 style="margin: 0;">{len(results['invalid'])} Invalid File(s) Found</h2>
              <p style="margin: 10px 0 0 0;">SFTP Path: {sftp_path}</p>
            </div>

            <div class="summary">
              <h3 style="margin-top: 0;">📊 Monitoring Summary</h3>
              <div class="summary-item">
                <span><strong>Total Files Scanned:</strong></span>
                <span>{len(results['valid']) + len(results['invalid'])}</span>
              </div>
              <div class="summary-item">
                <span><strong>Valid Files:</strong></span>
                <span style="color: #28a745; font-weight: bold;">{len(results['valid'])} ✅</span>
              </div>
              <div class="summary-item">
                <span><strong>Invalid Files:</strong></span>
                <span style="color: #dc3545; font-weight: bold;">{len(results['invalid'])} ❌</span>
              </div>
              <div class="summary-item">
                <span><strong>Success Rate:</strong></span>
                <span>{(len(results['valid']) / max(len(results['valid']) + len(results['invalid']), 1) * 100):.1f}%</span>
              </div>
              <div class="summary-item">
                <span><strong>Scan Time:</strong></span>
                <span>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
              </div>
            </div>

            {"<h2 style='color: #dc3545;'>❌ Invalid Files</h2>" if results['invalid'] else ""}
            {f"<table><thead><tr><th>Filename</th><th>Size</th><th>Modified</th><th>Errors</th></tr></thead><tbody>{invalid_rows}</tbody></table>" if results['invalid'] else ""}

            {"<h2 style='color: #28a745;'>✅ Valid Files</h2>" if results['valid'] else ""}
            {f"<table><thead><tr><th>Filename</th><th>Size</th><th>Modified</th><th>Status</th></tr></thead><tbody>{valid_rows}</tbody></table>" if results['valid'] else ""}

            {"""
            <div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; border-radius: 5px; margin-top: 20px;">
              <h3 style="margin-top: 0; color: #856404;">⚠️ Action Required</h3>
              <p style="margin: 0; color: #856404;">Please review and correct the invalid files on the SFTP server.</p>
              <ul style="color: #856404; margin: 10px 0 0 0;">
                <li>Verify file naming conventions</li>
                <li>Check file sizes are within limits</li>
                <li>Ensure files are recent (< 24 hours)</li>
              </ul>
            </div>
            """ if results['invalid'] else ""}
          </div>

          <div class="footer">
            <p style="margin: 0; font-size: 14px;">SFTP File Monitoring System</p>
            <p style="margin: 10px 0 0 0; font-size: 12px;">Contact: roshni.mohandas@gmail.com</p>
            <p style="margin: 10px 0 0 0; font-size: 11px; opacity: 0.8;">
              Automated alert generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </p>
          </div>
        </div>
      </body>
    </html>
    """

    message.attach(MIMEText(html, 'html'))

    # Send email
    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, message.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False

def monitor_sftp(host, port, username, password, remote_path, partner):
    """Monitor SFTP and send alerts"""

    print("="*70)
    print("🔍 SFTP FILE MONITOR with EMAIL ALERTS")
    print("="*70)
    print(f"\n📡 Connecting to SFTP server...")
    print(f"   Host: {host}:{port}")
    print(f"   Path: {remote_path}")
    print(f"   Partner: {partner}")

    try:
        client = SFTPClient(host=host, port=port, username=username, password=password)

        if not client.connect():
            print("❌ Failed to connect to SFTP server")
            return

        print("✅ Connected successfully!")

        # List files
        print(f"\n📂 Scanning directory: {remote_path}")
        files = client.list_files(remote_path)

        # Filter only files
        files = [f for f in files if not f['is_dir']]
        print(f"   Found {len(files)} file(s)")

        # Validate files
        validator = FileValidator(partner=partner)
        results = {'valid': [], 'invalid': []}

        print("\n🔍 Validating files...")
        for file in files:
            result = validator.validate_all(
                filename=file['filename'],
                file_size=file['size'],
                file_mtime=file['mtime']
            )

            if result['valid']:
                results['valid'].append(file)
                print(f"  ✅ {file['filename']}")
            else:
                results['invalid'].append({
                    'file': file,
                    'errors': result['errors']
                })
                print(f"  ❌ {file['filename']}")
                for error in result['errors']:
                    print(f"     → {error}")

        client.disconnect()

        # Send email
        print("\n" + "="*70)
        print("📧 Sending email alert...")
        if send_alert_email(results, remote_path):
            print("✅ Email sent successfully!")
            print(f"📬 Check inbox: {os.getenv('EMAIL_TO', 'roshni.mohandas@gmail.com')}")
        else:
            print("❌ Failed to send email")

        print("="*70)
        print("\n📊 Summary:")
        print(f"   Total: {len(files)} files")
        print(f"   Valid: {len(results['valid'])} ✅")
        print(f"   Invalid: {len(results['invalid'])} ❌")
        print("="*70)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    # Get configuration from .env
    host = os.getenv('SFTP_HOST', 'localhost')
    port = int(os.getenv('SFTP_PORT', 2222))
    username = os.getenv('SFTP_USERNAME', 'testuser')
    password = os.getenv('SFTP_PASSWORD', 'testpass')

    # Monitor settings
    remote_path = '/upload'  # Change this to your SFTP path
    partner = 'PARTNER_A'     # Change to PARTNER_A or PARTNER_B

    monitor_sftp(host, port, username, password, remote_path, partner)
