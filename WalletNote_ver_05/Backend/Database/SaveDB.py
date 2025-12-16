# WalletNote_ver_05/Backend/Database/SaveDB.py
from __future__ import annotations

from typing import List, Optional

from WalletNote_ver_05.Backend.Database.ConnectDB import ConnectDB, DBConfig
from WalletNote_ver_05.Backend.Information.InputUserInformation import UserInformation
from WalletNote_ver_05.Backend.Information.InputInformation import InputInformation


class SaveDB(ConnectDB):
    """
    Handles user-saved records.

    Responsibilities:
    - Persist records explicitly saved by the user.
    - Retrieve saved records for dashboard or export usage.
    """

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

    def save_record(
        self,
        user: UserInformation,
        record: InputInformation,
    ) -> None:
        """
        Save a record explicitly marked by the user.

        Args:
            user: UserInformation instance.
            record: InputInformation instance.
        """
        self.connect()
        user_id = self._get_user_id(user)

        if user_id is None:
            self.close()
            raise ValueError("User does not exist. Cannot save record.")

        sql = """
        INSERT INTO saved_records (user_id, price, record_date, service_or_product)
        VALUES (%s, %s, %s, %s)
        """

        try:
            self.execute(
                sql,
                (
                    user_id,
                    record.price,
                    record.date,
                    record.service_or_product,
                ),
            )
            self.commit()
        except Exception:
            self.rollback()
            raise
        finally:
            self.close()

    def fetch_saved_records(self, user: UserInformation) -> List[InputInformation]:
        """
        Fetch all saved records for a user.

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
        FROM saved_records
        WHERE user_id = %s
        ORDER BY created_at ASC
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
