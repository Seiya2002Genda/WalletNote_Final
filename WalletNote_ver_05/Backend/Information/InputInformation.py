# WalletNote_ver_05/Backend/Information/InputInformation.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation


@dataclass
class InputInformation:
    """
    Transaction input data model.

    Responsibilities:
    - Store price, date, and service/product name.
    - Validate and normalize input values.
    """

    price: Decimal
    date: date
    service_or_product: str

    def __post_init__(self) -> None:
        """
        Validate fields after initialization.
        """
        self.price = self._validate_price(self.price)
        self.date = self._validate_date(self.date)
        self.service_or_product = self._validate_service(self.service_or_product)

    @staticmethod
    def _validate_price(value) -> Decimal:
        """
        Validate and normalize price.

        Args:
            value: Numeric or string value.

        Returns:
            Decimal value rounded to 2 decimal places.
        """
        try:
            price = Decimal(value).quantize(Decimal("0.01"))
        except (InvalidOperation, TypeError):
            raise ValueError("Invalid price value.")

        if price < 0:
            raise ValueError("Price must be non-negative.")

        return price

    @staticmethod
    def _validate_date(value) -> date:
        """
        Validate date.

        Args:
            value: datetime.date instance.

        Returns:
            datetime.date
        """
        if not isinstance(value, date):
            raise ValueError("Date must be a datetime.date instance.")
        return value

    @staticmethod
    def _validate_service(value: str) -> str:
        """
        Validate service or product name.

        Args:
            value: String value.

        Returns:
            Cleaned string.
        """
        if not value or not isinstance(value, str):
            raise ValueError("Service or product name must be a non-empty string.")
        return value.strip()
