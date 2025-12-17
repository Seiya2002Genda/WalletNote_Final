# Backend/Database/SaveDB.py
from __future__ import annotations

from CYBR_404.WalletNote_ver_06.Backend.Database.ConnectDB import ConnectDB
from CYBR_404.WalletNote_ver_06.Backend.Information.InputUserInformation import UserInformation


class SaveDB(ConnectDB):
    """
    SaveDB is responsible for:
    - Saving user-specific settings
    - Updating persistent user preferences

    NOTE:
    - This class does NOT handle records (income/expense)
    """

    # =========================
    # User Settings
    # =========================
    def update_currency(self, user: UserInformation, currency: str) -> None:
        """
        Update preferred currency for a user.

        :param user: logged-in user
        :param currency: currency code (e.g., USD, JPY)
        """

        # Ensure column exists in users table if used
        sql = """
        UPDATE users
        SET preferred_currency = %s
        WHERE id = %s
        """

        self.execute(sql, (currency, user.user_id))
