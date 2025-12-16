# WalletNote_ver_05/Backend/System/Setting.py
from __future__ import annotations

from typing import Optional

from WalletNote_ver_05.Backend.Database.ConnectDB import ConnectDB, DBConfig
from WalletNote_ver_05.Backend.Information.InputUserInformation import UserInformation


class Setting(ConnectDB):
    """
    User settings manager.

    Responsibilities:
    - Store and retrieve user-specific settings.
    - Currently supports currency configuration.
    - No UI or presentation logic.
    """

    # Supported major currencies (advanced economies)
    SUPPORTED_CURRENCIES = {
        "USD",  # United States
        "EUR",  # Eurozone
        "JPY",  # Japan
        "GBP",  # United Kingdom
        "CHF",  # Switzerland
        "CAD",  # Canada
        "AUD",  # Australia
        "NZD",  # New Zealand
        "SEK",  # Sweden
        "NOK",  # Norway
    }

    def __init__(self, db_name: str = "walletnote_db") -> None:
        super().__init__(DBConfig(database=db_name))

    def _get_user_id(self, user: UserInformation) -> Optional[int]:
        """
        Resolve user_id from the users table.
        """
        sql = """
        SELECT user_id
        FROM users
        WHERE username = %s AND email = %s
        """
        row = self.fetch_one(sql, (user.username, user.email))
        return row["user_id"] if row else None

    def get_currency(self, user: UserInformation) -> str:
        """
        Get the user's currency setting.

        Args:
            user: UserInformation instance.

        Returns:
            Currency code (default: USD).
        """
        self.connect()
        user_id = self._get_user_id(user)

        if user_id is None:
            self.close()
            return "USD"

        sql = """
        SELECT currency
        FROM user_settings
        WHERE user_id = %s
        """
        row = self.fetch_one(sql, (user_id,))
        self.close()

        return row["currency"] if row and row.get("currency") else "USD"

    def set_currency(self, user: UserInformation, currency: str) -> None:
        """
        Set or update the user's currency setting.

        Args:
            user: UserInformation instance.
            currency: Currency code (e.g., USD, JPY).

        Raises:
            ValueError if currency is not supported or user not found.
        """
        currency = currency.upper()
        if currency not in self.SUPPORTED_CURRENCIES:
            raise ValueError("Unsupported currency.")

        self.connect()
        user_id = self._get_user_id(user)

        if user_id is None:
            self.close()
            raise ValueError("User does not exist.")

        # Upsert pattern
        sql = """
        INSERT INTO user_settings (user_id, currency)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE currency = VALUES(currency)
        """

        try:
            self.execute(sql, (user_id, currency))
            self.commit()
        except Exception:
            self.rollback()
            raise
        finally:
            self.close()
