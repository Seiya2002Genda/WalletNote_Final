# WalletNote_ver_05/Backend/System/MakeGraph.py
from __future__ import annotations

from collections import defaultdict
from decimal import Decimal
from typing import Dict, List

from WalletNote_ver_05.Backend.Information.InputInformation import InputInformation


class MakeGraph:
    """
    Graph data aggregation class.

    Responsibilities:
    - Aggregate real InputInformation records only.
    - No sample data, no default values, no fallback generation.
    - Return pure aggregated results for frontend rendering.
    """

    def monthly_graph(self, records: List[InputInformation]) -> Dict[str, float]:
        """
        Aggregate records by month (YYYY-MM).

        Args:
            records: List of InputInformation objects.

        Returns:
            Dictionary mapping month to total price.
        """
        totals: Dict[str, Decimal] = defaultdict(Decimal)

        for record in records:
            key = record.date.strftime("%Y-%m")
            totals[key] += record.price

        return {k: float(v) for k, v in sorted(totals.items())}

    def yearly_graph(self, records: List[InputInformation]) -> Dict[str, float]:
        """
        Aggregate records by year (YYYY).

        Args:
            records: List of InputInformation objects.

        Returns:
            Dictionary mapping year to total price.
        """
        totals: Dict[str, Decimal] = defaultdict(Decimal)

        for record in records:
            key = str(record.date.year)
            totals[key] += record.price

        return {k: float(v) for k, v in sorted(totals.items())}

    def daily_graph(self, records: List[InputInformation]) -> Dict[str, float]:
        """
        Aggregate records by date (YYYY-MM-DD).

        Args:
            records: List of InputInformation objects.

        Returns:
            Dictionary mapping date to total price.
        """
        totals: Dict[str, Decimal] = defaultdict(Decimal)

        for record in records:
            key = record.date.isoformat()
            totals[key] += record.price

        return {k: float(v) for k, v in sorted(totals.items())}
