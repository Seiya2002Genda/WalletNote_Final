# Backend/System/OCR_System.py
from __future__ import annotations

from pathlib import Path
from typing import Dict, Any

from CYBR_404.WalletNote_ver_06.Backend.Database.RecordDB import RecordDB
from CYBR_404.WalletNote_ver_06.Backend.Information.InputInformation import InputInformation
from CYBR_404.WalletNote_ver_06.Backend.Information.InputUserInformation import UserInformation


class OCRSystem:
    """
    OCRSystem is responsible for:
    - Receiving an image file
    - Extracting structured data (price, service, date)
    - Saving the result to database via RecordDB

    NOTE:
    - This is a SAFE placeholder implementation
    - Real OCR engines can replace `_run_ocr()` later
    """

    def __init__(self) -> None:
        self.record_db = RecordDB()

    # =========================
    # Public API
    # =========================
    def process_image(self, user: UserInformation, image_path: Path) -> None:
        """
        Process a receipt image and save extracted data.

        :param user: logged-in user
        :param image_path: path to uploaded image
        """

        extracted = self._run_ocr(image_path)

        record = InputInformation(
            price=extracted["price"],
            service=extracted["service"],
            record_date=extracted["date"],
        )

        # Default OCR records are treated as expenses
        self.record_db.add_record(
            user=user,
            record=record,
            record_type="expense",
        )

    # =========================
    # Internal (Stub OCR)
    # =========================
    def _run_ocr(self, image_path: Path) -> Dict[str, Any]:
        """
        Dummy OCR logic.

        This method MUST return:
        - price
        - service
        - date (YYYY-MM-DD)

        Replace this logic with real OCR later.
        """

        # Placeholder values (safe defaults)
        return {
            "price": 0,
            "service": f"OCR Import ({image_path.name})",
            "date": "2025-01-01",
        }
