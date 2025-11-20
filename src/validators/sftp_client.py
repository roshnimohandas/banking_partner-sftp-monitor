"""
SFTP client module for connecting and managing SFTP operations
"""
import paramiko
import os
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SFTPClient:
    """SFTP client for banking partner file operations"""

    def __init__(self, host: str, port: int = 22,
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 private_key_path: Optional[str] = None):
        """
        Initialize SFTP client

        Args:
            host: SFTP server hostname
            port: SFTP server port (default: 22)
            username: Username for authentication
            password: Password for authentication
            private_key_path: Path to private key file for key-based auth
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.private_key_path = private_key_path
        self.client = None
        self.sftp = None

    def connect(self) -> bool:
        """
        Connect to SFTP server

        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            connect_kwargs = {
                'hostname': self.host,
                'port': self.port,
                'username': self.username
            }

            if self.private_key_path and os.path.exists(self.private_key_path):
                key = paramiko.RSAKey.from_private_key_file(self.private_key_path)
                connect_kwargs['pkey'] = key
                logger.info(f"Connecting to {self.host} with key-based auth")
            elif self.password:
                connect_kwargs['password'] = self.password
                logger.info(f"Connecting to {self.host} with password auth")
            else:
                logger.error("No authentication method provided")
                return False

            self.client.connect(**connect_kwargs)
            self.sftp = self.client.open_sftp()
            logger.info(f"Successfully connected to {self.host}")
            return True

        except Exception as e:
            logger.error(f"Failed to connect to {self.host}: {str(e)}")
            return False

    def disconnect(self):
        """Disconnect from SFTP server"""
        if self.sftp:
            self.sftp.close()
        if self.client:
            self.client.close()
        logger.info(f"Disconnected from {self.host}")

    def list_files(self, remote_path: str = '.') -> List[Dict]:
        """
        List files in remote directory

        Args:
            remote_path: Remote directory path

        Returns:
            List of file information dictionaries
        """
        if not self.sftp:
            logger.error("Not connected to SFTP server")
            return []

        try:
            files = []
            for attr in self.sftp.listdir_attr(remote_path):
                file_info = {
                    'filename': attr.filename,
                    'size': attr.st_size,
                    'mtime': attr.st_mtime,
                    'is_dir': paramiko.sftp_attr.S_ISDIR(attr.st_mode),
                    'permissions': oct(attr.st_mode)[-3:],
                    'modified_date': datetime.fromtimestamp(attr.st_mtime).isoformat()
                }
                files.append(file_info)
            return files

        except Exception as e:
            logger.error(f"Failed to list files in {remote_path}: {str(e)}")
            return []

    def file_exists(self, remote_path: str) -> bool:
        """
        Check if file exists on SFTP server

        Args:
            remote_path: Remote file path

        Returns:
            True if file exists, False otherwise
        """
        if not self.sftp:
            logger.error("Not connected to SFTP server")
            return False

        try:
            self.sftp.stat(remote_path)
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            logger.error(f"Error checking file existence {remote_path}: {str(e)}")
            return False

    def get_file_metadata(self, remote_path: str) -> Optional[Dict]:
        """
        Get file metadata

        Args:
            remote_path: Remote file path

        Returns:
            Dictionary with file metadata or None if file doesn't exist
        """
        if not self.sftp:
            logger.error("Not connected to SFTP server")
            return None

        try:
            attr = self.sftp.stat(remote_path)
            return {
                'size': attr.st_size,
                'mtime': attr.st_mtime,
                'modified_date': datetime.fromtimestamp(attr.st_mtime).isoformat(),
                'permissions': oct(attr.st_mode)[-3:],
                'is_dir': paramiko.sftp_attr.S_ISDIR(attr.st_mode)
            }
        except FileNotFoundError:
            logger.warning(f"File not found: {remote_path}")
            return None
        except Exception as e:
            logger.error(f"Error getting file metadata {remote_path}: {str(e)}")
            return None

    def download_file(self, remote_path: str, local_path: str) -> bool:
        """
        Download file from SFTP server

        Args:
            remote_path: Remote file path
            local_path: Local file path

        Returns:
            True if download successful, False otherwise
        """
        if not self.sftp:
            logger.error("Not connected to SFTP server")
            return False

        try:
            # Create local directory if it doesn't exist
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            self.sftp.get(remote_path, local_path)
            logger.info(f"Downloaded {remote_path} to {local_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to download {remote_path}: {str(e)}")
            return False

    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()
