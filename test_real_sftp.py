#!/usr/bin/env python3
"""
Test SFTP connection to real server
"""
import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(__file__))

from src.validators.sftp_client import SFTPClient

load_dotenv()

def test_sftp_connection():
    print("="*70)
    print("🔍 SFTP CONNECTION TEST")
    print("="*70)

    # Get credentials from .env
    host = os.getenv('SFTP_HOST')
    port = int(os.getenv('SFTP_PORT', 22))
    username = os.getenv('SFTP_USERNAME')
    password = os.getenv('SFTP_PASSWORD')

    if not all([host, username, password]):
        print("\n❌ Error: SFTP credentials not found in .env file!")
        print("\nPlease create .env file with:")
        print("SFTP_HOST=103.183.96.21")
        print("SFTP_PORT=2022")
        print("SFTP_USERNAME=srv.42cssmtp")
        print("SFTP_PASSWORD=D]kjPL8Ccy6uGx3R")
        return

    print(f"\n📡 Connection Details:")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Username: {username}")
    print(f"   Password: {'*' * len(password) if password else 'NOT SET'}")

    print(f"\n🔌 Attempting to connect...")

    try:
        client = SFTPClient(
            host=host,
            port=port,
            username=username,
            password=password
        )

        if client.connect():
            print("✅ Connected successfully!")

            # List root directory
            print("\n📂 Listing root directory (/)...")
            try:
                files = client.list_files('/')

                if files:
                    print(f"   Found {len(files)} items:\n")

                    # Separate directories and files
                    dirs = [f for f in files if f['is_dir']]
                    regular_files = [f for f in files if not f['is_dir']]

                    if dirs:
                        print("   📁 Directories:")
                        for item in dirs[:20]:  # Show first 20
                            print(f"      📁 {item['filename']}/")

                    if regular_files:
                        print("\n   📄 Files:")
                        for item in regular_files[:20]:  # Show first 20
                            size_mb = item['size'] / (1024 * 1024)
                            print(f"      📄 {item['filename']} ({size_mb:.2f} MB)")

                    if len(files) > 20:
                        print(f"\n   ... and {len(files) - 20} more items")
                else:
                    print("   ⚠️  Directory is empty or no read permissions")

            except Exception as e:
                print(f"   ⚠️  Could not list root directory: {str(e)}")
                print("\n   Trying current directory (.)...")

                try:
                    files = client.list_files('.')
                    print(f"   Found {len(files)} items in current directory")
                    for item in files[:10]:
                        icon = "📁" if item['is_dir'] else "📄"
                        print(f"      {icon} {item['filename']}")
                except Exception as e2:
                    print(f"   ⚠️  Could not list current directory: {str(e2)}")

            # Try to get current working directory
            print("\n🗂️  Attempting to get working directory info...")
            try:
                # SFTP doesn't have a direct CWD command, but we can try listing '.'
                current_files = client.list_files('.')
                print(f"   Current directory has {len(current_files)} items")
            except Exception as e:
                print(f"   ⚠️  {str(e)}")

            client.disconnect()
            print("\n" + "="*70)
            print("✅ SFTP CONNECTION TEST SUCCESSFUL!")
            print("="*70)
            print("\nNext steps:")
            print("1. Identify which directories contain your partner files")
            print("2. Update remote_path in monitoring scripts")
            print("3. Run: python send_sftp_alert.py")

        else:
            print("❌ Failed to connect to SFTP server")
            print("\nPossible issues:")
            print("- Check if host is reachable: ping", host)
            print("- Verify port", port, "is correct")
            print("- Confirm username and password")
            print("- Check firewall rules")

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nTroubleshooting:")
        print("- Verify the credentials are correct")
        print("- Check network connectivity")
        print("- Ensure SFTP service is running on the server")

if __name__ == "__main__":
    test_sftp_connection()
