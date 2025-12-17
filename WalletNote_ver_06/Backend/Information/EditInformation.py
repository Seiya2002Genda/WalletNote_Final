# Backend/Information/EditInformation.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal


@dataclass
class EditInformation:
    """
    EditInformation represents edited data for an existing record.

    Used by:
    - EditDB.update_record
    - Dashboard edit forms

    IMPORTANT:
    - This class only normalizes and stores data
    - No database or UI logic
    """

    price: Decimal
    service: str
    record_date: date

    def __init__(
        self,
        price: int | float | str | Decimal,
        service: str,
        record_date: str | date,
    ) -> None:
        # Normalize price
        self.price = Decimal(str(price))

        # Normalize service / product name
        self.service = service.strip()

        # Normalize date
        if isinstance(record_date, date):
            self.record_date = record_date
        else:
            # Expected format: YYYY-MM-DD
            self.record_date = datetime.strptime(record_date, "%Y-%m-%d").date()
