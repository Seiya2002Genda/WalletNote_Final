# WalletNote_ver_05/Backend/Database/RecordDB.py
from __future__ import annotations

from typing import Optional

from WalletNote_ver_05.Backend.Database.ConnectDB import ConnectDB, DBConfig
from WalletNote_ver_05.Backend.Information.InputUserInformation import UserInformation
from WalletNote_ver_05.Backend.Information.InputInformation import InputInformation


class RecordDB(ConnectDB):
    """
    Handles inserting business records into the database.

    Responsibilities:
    - Persist InputInformation linked to a UserInformation.
    - This class does NOT perform aggregation or analytics.
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

    def insert_record(self, user: UserInformation, record: InputInformation) -> None:
        """
        Insert a single record linked to a user.

        Args:
            user: UserInformation instance.
            record: InputInformation instance.

        Raises:
            ValueError: if the user does not exist.
        """
        self.connect()

        user_id = self._get_user_id(user)
        if user_id is None:
            self.close()
            raise ValueError("User does not exist. Cannot insert record.")

        insert_sql = """
        INSERT INTO records (user_id, price, record_date, service_or_product)
        VALUES (%s, %s, %s, %s)
        """

        try:
            self.execute(
                insert_sql,
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

    def insert_record_from_ocr(
        self,
        user: UserInformation,
        record: InputInformation,
    ) -> None:
        """
        Insert a record coming from OCR processing.

        This method exists for semantic clarity and future OCR-specific hooks,
        but currently behaves the same as insert_record().

        Args:
            user: UserInformation instance.
            record: InputInformation instance.
        """
        self.insert_record(user, record)
