#!/usr/bin/env python3
"""Quick email connection test"""
import smtplib

email = "roshnitraining@gmail.com"
password = "Deluxe-Leasehold-Parkway"

print("Testing Gmail SMTP connection...")
print(f"Email: {email}")
print(f"Server: smtp.gmail.com:587")
print("-" * 50)

try:
    print("\n1. Connecting to SMTP server...")
    server = smtplib.SMTP('smtp.gmail.com', 587)

    print("2. Starting TLS encryption...")
    server.starttls()

    print("3. Attempting login...")
    server.login(email, password)

    print("4. Closing connection...")
    server.quit()

    print("\n" + "=" * 50)
    print("✅ SUCCESS! Email credentials are working!")
    print("=" * 50)
    print("\nYou can now run: python test_email_alert.py")

except smtplib.SMTPAuthenticationError as e:
    print("\n" + "=" * 50)
    print("❌ AUTHENTICATION FAILED")
    print("=" * 50)
    print("\nThis is likely because you're using a regular Gmail password.")
    print("Gmail requires an 'App Password' for programmatic access.\n")
    print("📖 How to fix:")
    print("1. Go to: https://myaccount.google.com/apppasswords")
    print("2. Sign in if needed")
    print("3. Click 'Select app' → Choose 'Mail'")
    print("4. Click 'Select device' → Choose 'Other' → Type 'SFTP Monitor'")
    print("5. Click 'Generate'")
    print("6. Copy the 16-character password (e.g., 'abcd efgh ijkl mnop')")
    print("7. Use that password instead of your regular Gmail password")
    print("\nNote: You need 2-factor authentication enabled first!")

except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print("\nPossible issues:")
    print("- Check your internet connection")
    print("- Verify email address is correct")
    print("- Make sure you're using a Gmail App Password")
