# Backend/System/MakeGraph.py
from __future__ import annotations

from datetime import date
from typing import Dict, List

from CYBR_404.WalletNote_ver_06.Backend.Database.RecallDB import RecallDB


class MakeGraph:
    """
    MakeGraph is responsible for:
    - Preparing graph-ready data structures
    - Monthly / yearly / daily aggregations

    IMPORTANT:
    - No rendering (Chart.js 等は Frontend)
    - No SQL here except via RecallDB
    """

    def __init__(self) -> None:
        self.recall_db = RecallDB()

    # =========================
    # Monthly Graph
    # =========================
    def monthly_graph(self, user_id: int, year: int, month: int) -> Dict[str, float]:
        """
        Return monthly totals for pie chart.
        """
        rows = self.recall_db.get_monthly_summary(user_id, year, month)

        result = {"income": 0.0, "expense": 0.0}
        for record_type, total in rows:
            result[record_type] = float(total or 0)

        return result

    # =========================
    # Yearly Graph
    # =========================
    def yearly_graph(self, user_id: int, year: int) -> Dict[str, List[float]]:
        """
        Return monthly totals for bar chart (12 months).
        """
        rows = self.recall_db.get_yearly_summary(user_id, year)

        income = [0.0] * 12
        expense = [0.0] * 12

        for record_type, month, total in rows:
            index = int(month) - 1
            if record_type == "income":
                income[index] = float(total or 0)
            elif record_type == "expense":
                expense[index] = float(total or 0)

        return {
            "income": income,
            "expense": expense,
        }

    # =========================
    # Daily Graph
    # =========================
    def today_graph(self, user_id: int) -> Dict[str, float]:
        """
        Return today's totals.
        """
        today = date.today()

        rows = self.recall_db.fetch_all(
            """
            SELECT record_type, SUM(price)
            FROM records
            WHERE user_id = %s
              AND record_date = %s
            GROUP BY record_type
            """,
            (user_id, today),
        )

        result = {"income": 0.0, "expense": 0.0}
        for record_type, total in rows:
            result[record_type] = float(total or 0)

        return result
