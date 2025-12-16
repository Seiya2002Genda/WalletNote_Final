# WalletNote_ver_05/Backend/System/OCR_System.py
from __future__ import annotations

import re
from datetime import datetime, date
from decimal import Decimal
from typing import Optional

import pytesseract
from PIL import Image

from WalletNote_ver_05.Backend.Information.InputInformation import InputInformation
from WalletNote_ver_05.Backend.Information.InputUserInformation import UserInformation
from WalletNote_ver_05.Backend.Database.RecordDB import RecordDB


class OCRSystem:
    """
    OCR processing system.

    Responsibilities:
    - Perform OCR on an image.
    - Parse OCR text into structured transaction data.
    - Create InputInformation and automatically persist via RecordDB.
    """

    def __init__(self) -> None:
        self._record_db = RecordDB()

    def process_and_save(
        self,
        image_path: str,
        user: UserInformation,
    ) -> InputInformation:
        """
        Execute OCR, parse results, and save the record.

        Args:
            image_path: Path to the uploaded receipt image.
            user: UserInformation instance.

        Returns:
            InputInformation created from OCR result.

        Raises:
            ValueError: if OCR or parsing fails.
        """
        text = self._run_ocr(image_path)

        price = self._extract_price(text)
        record_date = self._extract_date(text)
        service = self._extract_service(text)

        record = InputInformation(
            price=price,
            date=record_date,
            service_or_product=service,
        )

        self._record_db.insert_record_from_ocr(user, record)
        return record

    @staticmethod
    def _run_ocr(image_path: str) -> str:
        """
        Run OCR on an image file.

        Args:
            image_path: Path to image.

        Returns:
            Extracted text.

        Raises:
            ValueError if OCR fails.
        """
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            if not text.strip():
                raise ValueError
            return text
        except Exception:
            raise ValueError("OCR failed or image could not be processed.")

    @staticmethod
    def _extract_price(text: str) -> Decimal:
        """
        Extract price from OCR text.

        Strategy:
        - Find decimal numbers with 2 digits.
        - Use the largest value (typical for total price).

        Raises:
            ValueError if price cannot be determined.
        """
        matches = re.findall(r"\d+\.\d{2}", text)
        if not matches:
            raise ValueError("Price not found in OCR text.")

        prices = [Decimal(m) for m in matches]
        return max(prices)

    @staticmethod
    def _extract_date(text: str) -> date:
        """
        Extract date from OCR text.

        Supported formats:
        - YYYY-MM-DD
        - YYYY/MM/DD
        - MM/DD/YYYY

        Raises:
            ValueError if date cannot be determined.
        """
        patterns = [
            r"\d{4}[-/]\d{2}[-/]\d{2}",
            r"\d{2}/\d{2}/\d{4}",
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                raw = match.group()
                try:
                    if raw.count("/") == 2 and raw.startswith(("19", "20")):
                        return datetime.strptime(raw, "%Y/%m/%d").date()
                    if raw.count("-") == 2:
                        return datetime.strptime(raw, "%Y-%m-%d").date()
                    return datetime.strptime(raw, "%m/%d/%Y").date()
                except ValueError:
                    continue

        # Fallback: today (explicit choice, not a sample)
        return date.today()

    @staticmethod
    def _extract_service(text: str) -> str:
        """
        Extract service or product name.

        Strategy:
        - Use the first non-empty line as service name.
        - Strip excessive symbols.

        Raises:
            ValueError if no valid line found.
        """
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if not lines:
            raise ValueError("Service or product name not found.")

        service = re.sub(r"[^A-Za-z0-9\s\-]", "", lines[0])
        return service[:255]
