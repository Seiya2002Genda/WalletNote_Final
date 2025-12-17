# Backend/Database/RecordDB.py
from __future__ import annotations

from CYBR_404.WalletNote_ver_06.Backend.Database.ConnectDB import ConnectDB
from CYBR_404.WalletNote_ver_06.Backend.Information.InputUserInformation import UserInformation
from CYBR_404.WalletNote_ver_06.Backend.Information.InputInformation import InputInformation


class RecordDB(ConnectDB):
    """
    RecordDB is responsible for:
    - Inserting income / expense records into the database
    """

    def add_record(
        self,
        user: UserInformation,
        record: InputInformation,
        record_type: str,
    ) -> None:
        """
        Add a single income or expense record.

        :param user: logged-in user
        :param record: input data (price, service, date)
        :param record_type: 'income' or 'expense'
        """

        if record_type not in ("income", "expense"):
            raise ValueError("record_type must be 'income' or 'expense'")

        sql = """
        INSERT INTO records (
            user_id,
            record_type,
            price,
            service,
            record_date
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        params = (
            user.user_id,
            record_type,
            record.price,
            record.service,
            record.record_date,
        )

        self.execute(sql, params)
