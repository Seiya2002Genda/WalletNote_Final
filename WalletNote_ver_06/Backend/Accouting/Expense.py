# Backend/Accounting/Expense.py
from __future__ import annotations

from CYBR_404.WalletNote_ver_06.Backend.Database.RecordDB import RecordDB
from CYBR_404.WalletNote_ver_06.Backend.Database.EditDB import EditDB
from CYBR_404.WalletNote_ver_06.Backend.Information.InputUserInformation import UserInformation
from CYBR_404.WalletNote_ver_06.Backend.Information.InputInformation import InputInformation
from CYBR_404.WalletNote_ver_06.Backend.Information.EditInformation import EditInformation


class Expense:
    """
    Expense use-case layer.

    Responsibilities:
    - Add expense
    - Update expense
    - Delete expense

    IMPORTANT:
    - This class does NOT contain SQL
    - Delegates DB operations to RecordDB / EditDB
    """

    def __init__(self) -> None:
        self.record_db = RecordDB()
        self.edit_db = EditDB()

    # =========================
    # Create
    # =========================
    def add(
        self,
        user: UserInformation,
        data: InputInformation,
    ) -> None:
        """
        Add a new expense record.
        """
        self.record_db.add_record(
            user=user,
            record=data,
            record_type="expense",
        )

    # =========================
    # Update
    # =========================
    def update(
        self,
        user: UserInformation,
        record_id: int,
        new_data: EditInformation,
    ) -> None:
        """
        Update an existing expense record.
        """
        self.edit_db.update_record(
            user=user,
            record_id=record_id,
            new_data=new_data,
        )

    # =========================
    # Delete
    # =========================
    def delete(self, user: UserInformation, record_id: int) -> None:
        """
        Delete an expense record.
        """
        self.edit_db.delete_record(
            user=user,
            record_id=record_id,
        )
