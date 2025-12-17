# Backend/Database/EditDB.py
from __future__ import annotations

from CYBR_404.WalletNote_ver_06.Backend.Database.ConnectDB import ConnectDB
from CYBR_404.WalletNote_ver_06.Backend.Information.InputUserInformation import UserInformation
from CYBR_404.WalletNote_ver_06.Backend.Information.InputInformation import InputInformation


class EditDB(ConnectDB):
    """
    EditDB is responsible for:
    - Updating existing income / expense records
    - Deleting existing records

    IMPORTANT:
    - Ownership is always checked by user_id
    """

    # =========================
    # Update
    # =========================
    def update_record(
        self,
        user: UserInformation,
        record_id: int,
        new_data: InputInformation,
    ) -> None:
        """
        Update a record owned by the user.

        :param user: logged-in user
        :param record_id: target record ID
        :param new_data: new input values
        """

        sql = """
        UPDATE records
        SET
            price = %s,
            service = %s,
            record_date = %s
        WHERE id = %s
          AND user_id = %s
        """

        params = (
            new_data.price,
            new_data.service,
            new_data.record_date,
            record_id,
            user.user_id,
        )

        self.execute(sql, params)

    # =========================
    # Delete
    # =========================
    def delete_record(self, user: UserInformation, record_id: int) -> None:
        """
        Delete a record owned by the user.

        :param user: logged-in user
        :param record_id: target record ID
        """

        sql = """
        DELETE FROM records
        WHERE id = %s
          AND user_id = %s
        """

        self.execute(sql, (record_id, user.user_id))
