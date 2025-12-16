# WalletNote_ver_05/Backend/Database/RecallDB.py
from __future__ import annotations

from typing import List, Optional

from WalletNote_ver_05.Backend.Database.ConnectDB import ConnectDB, DBConfig
from WalletNote_ver_05.Backend.Information.InputInformation import InputInformation
from WalletNote_ver_05.Backend.Information.InputUserInformation import UserInformation


class RecallDB(ConnectDB):
    """
    Read-only access class for dashboard data retrieval.

    Responsibilities:
    - Fetch records linked to a user.
    - Convert database rows into InputInformation objects.
    """

    def __init__(self, db_name: str = "walletnote_db") -> None:
        super().__init__(DBConfig(database=db_name))

    def _get_user_id(self, user: UserInformation) -> Optional[int]:
        """
        Resolve user_id from the users table.

        Args:
            user: UserInformation instance.

        Returns:
            user_id if found, otherwise None.
        """
        sql = """
        SELECT user_id
        FROM users
        WHERE username = %s AND email = %s
        """
        row = self.fetch_one(sql, (user.username, user.email))
        return row["user_id"] if row else None

    def fetch_all_records(self, user: UserInformation) -> List[InputInformation]:
        """
        Fetch all records for a given user.

        Args:
            user: UserInformation instance.

        Returns:
            List of InputInformation objects.
        """
        self.connect()

        user_id = self._get_user_id(user)
        if user_id is None:
            self.close()
            return []

        sql = """
        SELECT price, record_date, service_or_product
        FROM records
        WHERE user_id = %s
        ORDER BY record_date ASC
        """

        rows = self.fetch_all(sql, (user_id,))
        self.close()

        return [
            InputInformation(
                price=row["price"],
                date=row["record_date"],
                service_or_product=row["service_or_product"],
            )
            for row in rows
        ]

    def fetch_records_by_date(
        self,
        user: UserInformation,
        target_date,
    ) -> List[InputInformation]:
        """
        Fetch records for a specific date.

        Args:
            user: UserInformation instance.
            target_date: datetime.date

        Returns:
            List of InputInformation objects.
        """
        self.connect()

        user_id = self._get_user_id(user)
        if user_id is None:
            self.close()
            return []

        sql = """
        SELECT price, record_date, service_or_product
        FROM records
        WHERE user_id = %s AND record_date = %s
        ORDER BY created_at ASC
        """

        rows = self.fetch_all(sql, (user_id, target_date))
        self.close()

        return [
            InputInformation(
                price=row["price"],
                date=row["record_date"],
                service_or_product=row["service_or_product"],
            )
            for row in rows
        ]
