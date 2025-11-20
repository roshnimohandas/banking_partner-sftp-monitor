"""
File validation module for banking partner SFTP files
"""
import re
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path


class FileValidator:
    """Validates banking partner files for naming conventions and metadata"""

    # File naming patterns for different banking partners
    NAMING_PATTERNS = {
        'PARTNER_A': {
            'pattern': r'^PARTNER_A_\d{8}_\d{6}_(TRANSACTION|SETTLEMENT|REPORT)\.csv$',
            'description': 'PARTNER_A_YYYYMMDD_HHMMSS_TYPE.csv',
            'example': 'PARTNER_A_20231120_143000_TRANSACTION.csv'
        },
        'PARTNER_B': {
            'pattern': r'^PARTNER_B_\d{8}_\d{6}_(TXN|SETTLE|RPT)\.csv$',
            'description': 'PARTNER_B_YYYYMMDD_HHMMSS_TYPE.csv',
            'example': 'PARTNER_B_20231120_143000_TXN.csv'
        },
        'GENERIC': {
            'pattern': r'^[A-Z]+_\d{8}_\d{6}_[A-Z]+\.(csv|txt|xlsx)$',
            'description': 'PARTNER_YYYYMMDD_HHMMSS_TYPE.ext',
            'example': 'BANK_20231120_143000_DATA.csv'
        }
    }

    # File size limits (in bytes)
    MIN_FILE_SIZE = 100  # 100 bytes
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB

    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'.csv', '.txt', '.xlsx', '.xls'}

    def __init__(self, partner: str = 'GENERIC'):
        """
        Initialize validator for specific banking partner

        Args:
            partner: Banking partner code (PARTNER_A, PARTNER_B, GENERIC)
        """
        self.partner = partner.upper()
        if self.partner not in self.NAMING_PATTERNS:
            self.partner = 'GENERIC'
        self.pattern = self.NAMING_PATTERNS[self.partner]

    def validate_filename(self, filename: str) -> Tuple[bool, Optional[str]]:
        """
        Validate filename against partner's naming convention

        Args:
            filename: Name of the file to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not filename:
            return False, "Filename is empty"

        pattern = self.pattern['pattern']
        if not re.match(pattern, filename):
            return False, (
                f"Filename does not match {self.partner} pattern. "
                f"Expected: {self.pattern['description']}, "
                f"Example: {self.pattern['example']}"
            )

        return True, None

    def validate_file_extension(self, filename: str) -> Tuple[bool, Optional[str]]:
        """
        Validate file has allowed extension

        Args:
            filename: Name of the file to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        ext = Path(filename).suffix.lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            return False, (
                f"Invalid file extension '{ext}'. "
                f"Allowed: {', '.join(self.ALLOWED_EXTENSIONS)}"
            )
        return True, None

    def validate_file_size(self, file_size: int) -> Tuple[bool, Optional[str]]:
        """
        Validate file size is within acceptable range

        Args:
            file_size: Size of file in bytes

        Returns:
            Tuple of (is_valid, error_message)
        """
        if file_size < self.MIN_FILE_SIZE:
            return False, f"File too small ({file_size} bytes). Minimum: {self.MIN_FILE_SIZE} bytes"

        if file_size > self.MAX_FILE_SIZE:
            return False, f"File too large ({file_size} bytes). Maximum: {self.MAX_FILE_SIZE} bytes"

        return True, None

    def validate_file_age(self, file_mtime: float, max_age_hours: int = 24) -> Tuple[bool, Optional[str]]:
        """
        Validate file is not too old

        Args:
            file_mtime: File modification time (Unix timestamp)
            max_age_hours: Maximum file age in hours

        Returns:
            Tuple of (is_valid, error_message)
        """
        file_datetime = datetime.fromtimestamp(file_mtime)
        age_hours = (datetime.now() - file_datetime).total_seconds() / 3600

        if age_hours > max_age_hours:
            return False, f"File is too old ({age_hours:.1f} hours). Maximum age: {max_age_hours} hours"

        return True, None

    def validate_all(self, filename: str, file_size: int,
                    file_mtime: Optional[float] = None,
                    max_age_hours: int = 24) -> Dict:
        """
        Run all validations on a file

        Args:
            filename: Name of the file
            file_size: Size of file in bytes
            file_mtime: File modification time (Unix timestamp)
            max_age_hours: Maximum file age in hours

        Returns:
            Dictionary with validation results
        """
        results = {
            'filename': filename,
            'partner': self.partner,
            'valid': True,
            'errors': [],
            'warnings': []
        }

        # Validate filename
        is_valid, error = self.validate_filename(filename)
        if not is_valid:
            results['valid'] = False
            results['errors'].append(error)

        # Validate extension
        is_valid, error = self.validate_file_extension(filename)
        if not is_valid:
            results['valid'] = False
            results['errors'].append(error)

        # Validate size
        is_valid, error = self.validate_file_size(file_size)
        if not is_valid:
            results['valid'] = False
            results['errors'].append(error)

        # Validate age if timestamp provided
        if file_mtime:
            is_valid, error = self.validate_file_age(file_mtime, max_age_hours)
            if not is_valid:
                results['warnings'].append(error)

        return results


def validate_file(filename: str, file_size: int, partner: str = 'GENERIC',
                 file_mtime: Optional[float] = None) -> Dict:
    """
    Convenience function to validate a file

    Args:
        filename: Name of the file
        file_size: Size of file in bytes
        partner: Banking partner code
        file_mtime: File modification time (Unix timestamp)

    Returns:
        Dictionary with validation results
    """
    validator = FileValidator(partner)
    return validator.validate_all(filename, file_size, file_mtime)
