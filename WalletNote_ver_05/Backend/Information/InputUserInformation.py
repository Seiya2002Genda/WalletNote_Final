# WalletNote_ver_05/Backend/Information/UserInformation.py
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from werkzeug.security import generate_password_hash, check_password_hash


@dataclass
class UserInformation:
    """
    User information model for signup and login.

    Responsibilities:
    - Store username, email, and password hash.
    - Validate input values.
    - Provide password hashing and verification.
    """

    username: str
    email: str
    _password_hash: Optional[str] = None

    def set_password(self, raw_password: str) -> None:
        """
        Hash and store a raw password.

        Args:
            raw_password: Plain text password.
        """
        if not self._is_valid_password(raw_password):
            raise ValueError("Password does not meet security requirements.")
        self._password_hash = generate_password_hash(raw_password)

    def verify_password(self, raw_password: str) -> bool:
        """
        Verify a raw password against the stored hash.

        Args:
            raw_password: Plain text password.

        Returns:
            True if password matches, otherwise False.
        """
        if self._password_hash is None:
            return False
        return check_password_hash(self._password_hash, raw_password)

    @property
    def password_hash(self) -> str:
        """
        Get the stored password hash.

        Raises:
            ValueError if password has not been set.
        """
        if self._password_hash is None:
            raise ValueError("Password hash is not set.")
        return self._password_hash

    def validate(self) -> None:
        """
        Validate username and email format.

        Raises:
            ValueError if validation fails.
        """
        if not self.username or len(self.username) < 3:
            raise ValueError("Username must be at least 3 characters long.")

        if not self._is_valid_email(self.email):
            raise ValueError("Invalid email address format.")

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """
        Basic email format validation.
        """
        pattern = r"^[^@]+@[^@]+\.[^@]+$"
        return re.match(pattern, email) is not None

    @staticmethod
    def _is_valid_password(password: str) -> bool:
        """
        Validate password strength.

        Rules:
        - At least 8 characters
        - Contains letters and numbers
        """
        if len(password) < 8:
            return False
        if not re.search(r"[A-Za-z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        return True
