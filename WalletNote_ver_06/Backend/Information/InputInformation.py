# Backend/Information/InputInformation.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal


@dataclass
class InputInformation:
    """
    InputInformation represents a single income or expense input.

    Used by:
    - Manual input (Frontend)
    - OCR_System
    - RecordDB / EditDB

    This class only stores validated data.
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
            # Expect format YYYY-MM-DD
            self.record_date = datetime.strptime(record_date, "%Y-%m-%d").date()
