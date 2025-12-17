# Backend/System/Setting.py
from __future__ import annotations

from CYBR_404.WalletNote_ver_06.Backend.Database.SaveDB import SaveDB
from CYBR_404.WalletNote_ver_06.Backend.Information.InputUserInformation import UserInformation


class Setting:
    """
    Setting is responsible for:
    - Handling user settings logic
    - Delegating persistence to SaveDB

    IMPORTANT:
    - No direct SQL here
    - No Flask / HTML dependency
    """

    # Supported currencies (advanced countries only, per spec)
    SUPPORTED_CURRENCIES = {
        "USD",  # US Dollar
        "EUR",  # Euro
        "JPY",  # Japanese Yen
        "GBP",  # British Pound
        "CHF",  # Swiss Franc
        "CAD",  # Canadian Dollar
        "AUD",  # Australian Dollar
    }

    def __init__(self, user: UserInformation) -> None:
        self.user = user
        self.save_db = SaveDB()

    def set_currency(self, currency: str) -> None:
        """
        Set preferred currency for the user.

        :param currency: currency code (e.g., USD, JPY)
        """
        currency = currency.upper()

        if currency not in self.SUPPORTED_CURRENCIES:
            raise ValueError(f"Unsupported currency: {currency}")

        self.save_db.update_currency(self.user, currency)
