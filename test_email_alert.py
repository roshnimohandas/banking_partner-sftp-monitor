#!/usr/bin/env python3
"""
Simple Email Alert Test for SFTP Monitor
Run this to test email notifications
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def send_test_email():
    """Send a test email alert"""
    print("="*70)
    print("📧 EMAIL ALERT TEST - SFTP Monitor")
    print("="*70)

    # Get email configuration from .env
    smtp_host = os.getenv('EMAIL_SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.getenv('EMAIL_SMTP_PORT', 587))
    from_email = os.getenv('EMAIL_FROM')
    to_email = os.getenv('EMAIL_TO', 'roshni.mohandas@gmail.com')
    password = os.getenv('EMAIL_PASSWORD')

    if not from_email or not password:
        print("\n❌ ERROR: Email not configured!")
        print("\nPlease add to your .env file:")
        print("EMAIL_FROM=your-email@gmail.com")
        print("EMAIL_TO=roshni.mohandas@gmail.com")
        print("EMAIL_PASSWORD=your-gmail-app-password")
        print("\n📖 Get Gmail App Password:")
        print("1. Go to: https://myaccount.google.com/apppasswords")
        print("2. Generate password for 'Mail'")
        print("3. Copy the 16-character password")
        print("4. Add to .env file")
        return False

    print(f"\n📤 Sending test email...")
    print(f"   From: {from_email}")
    print(f"   To: {to_email}")
    print(f"   SMTP: {smtp_host}:{smtp_port}")

    # Create email message
    message = MIMEMultipart('alternative')
    message['Subject'] = '🧪 SFTP Monitor - Email Alert Test'
    message['From'] = from_email
    message['To'] = to_email

    # Create beautiful HTML email
    html = f"""
    <html>
      <head>
        <style>
          body {{ font-family: Arial, sans-serif; }}
          .container {{ max-width: 600px; margin: 0 auto; }}
          .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px 10px 0 0;
            text-align: center;
          }}
          .content {{ background: #f9f9f9; padding: 30px; }}
          .alert-box {{
            background: white;
            border-left: 4px solid #dc3545;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
          }}
          .success-box {{
            background: #d4edda;
            border-left: 4px solid #28a745;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
          }}
          .info {{
            background: white;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
          }}
          table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
          }}
          th {{
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
          }}
          td {{
            padding: 12px;
            border-bottom: 1px solid #ddd;
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
            <h1 style="margin: 0;">🧪 Email Alert Test</h1>
            <p style="margin: 10px 0 0 0;">SFTP File Monitoring System</p>
          </div>

          <div class="content">
            <div class="success-box">
              <h2 style="margin: 0; color: #28a745;">✅ Email System Working!</h2>
              <p style="margin: 10px 0 0 0;">If you're reading this, your email alerts are configured correctly.</p>
            </div>

            <h2>📋 Sample Alert: Invalid File Detected</h2>

            <div class="alert-box">
              <h3 style="color: #dc3545; margin-top: 0;">❌ File Validation Failed</h3>
              <table>
                <tr>
                  <th>Property</th>
                  <th>Value</th>
                </tr>
                <tr>
                  <td><strong>Filename</strong></td>
                  <td>invalid_file.csv</td>
                </tr>
                <tr>
                  <td><strong>Partner</strong></td>
                  <td>PARTNER_A</td>
                </tr>
                <tr>
                  <td><strong>Status</strong></td>
                  <td style="color: #dc3545;">❌ Invalid</td>
                </tr>
                <tr>
                  <td><strong>Error</strong></td>
                  <td>Filename does not match PARTNER_A pattern</td>
                </tr>
                <tr>
                  <td><strong>Expected Pattern</strong></td>
                  <td>PARTNER_A_YYYYMMDD_HHMMSS_TYPE.csv</td>
                </tr>
                <tr>
                  <td><strong>Detected Time</strong></td>
                  <td>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td>
                </tr>
              </table>
            </div>

            <div class="info">
              <h3>📊 Summary</h3>
              <ul>
                <li><strong>Total Files Checked:</strong> 5</li>
                <li><strong>Valid Files:</strong> <span style="color: #28a745;">4 ✅</span></li>
                <li><strong>Invalid Files:</strong> <span style="color: #dc3545;">1 ❌</span></li>
                <li><strong>Success Rate:</strong> 80%</li>
              </ul>
            </div>

            <div class="info">
              <h3>⚡ What Triggers Email Alerts?</h3>
              <ul>
                <li>❌ Invalid file naming pattern detected</li>
                <li>📏 File size outside acceptable range</li>
                <li>⏰ File older than 24 hours</li>
                <li>📁 Expected file missing from SFTP</li>
                <li>🚫 File extension not allowed</li>
              </ul>
            </div>

            <div class="success-box">
              <h3 style="color: #28a745; margin-top: 0;">🎉 Next Steps</h3>
              <ol>
                <li>Set up your SFTP server (see TESTING_DEMO.md)</li>
                <li>Upload test files</li>
                <li>Run the monitoring script</li>
                <li>Receive real-time alerts for invalid files!</li>
              </ol>
            </div>
          </div>

          <div class="footer">
            <p style="margin: 0; font-size: 14px;">SFTP File Monitoring System</p>
            <p style="margin: 10px 0 0 0; font-size: 12px;">Contact: roshni.mohandas@gmail.com</p>
            <p style="margin: 10px 0 0 0; font-size: 11px; opacity: 0.8;">
              Sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </p>
          </div>
        </div>
      </body>
    </html>
    """

    message.attach(MIMEText(html, 'html'))

    # Send email
    try:
        print("\n🔐 Connecting to SMTP server...")
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()

        print("🔑 Authenticating...")
        server.login(from_email, password)

        print("📨 Sending email...")
        server.sendmail(from_email, to_email, message.as_string())
        server.quit()

        print("\n" + "="*70)
        print("✅ SUCCESS! Email sent successfully!")
        print("="*70)
        print(f"\n📬 Check your inbox: {to_email}")
        print("\nThe email includes:")
        print("  • Sample invalid file alert")
        print("  • Validation error details")
        print("  • Summary statistics")
        print("  • Next steps guide")
        print("\n" + "="*70)
        return True

    except smtplib.SMTPAuthenticationError:
        print("\n❌ AUTHENTICATION FAILED!")
        print("\nPossible issues:")
        print("1. Incorrect email or password")
        print("2. Need to use Gmail App Password (not regular password)")
        print("3. 2-factor authentication not enabled")
        print("\n📖 Fix:")
        print("1. Go to: https://myaccount.google.com/apppasswords")
        print("2. Generate password for 'Mail'")
        print("3. Update EMAIL_PASSWORD in .env with the 16-character code")
        return False

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nCheck your .env file settings:")
        print("  EMAIL_SMTP_HOST=smtp.gmail.com")
        print("  EMAIL_SMTP_PORT=587")
        print("  EMAIL_FROM=your-email@gmail.com")
        print("  EMAIL_TO=roshni.mohandas@gmail.com")
        print("  EMAIL_PASSWORD=your-app-password")
        return False

if __name__ == "__main__":
    send_test_email()
