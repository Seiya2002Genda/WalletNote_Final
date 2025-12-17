# Backend/Database/RecallDB.py
from __future__ import annotations

from typing import List, Tuple

from CYBR_404.WalletNote_ver_06.Backend.Database.ConnectDB import ConnectDB


class RecallDB(ConnectDB):
    """
    RecallDB is responsible for:
    - Fetching income / expense records from the database
    - Providing data to Dashboard / MakeGraph
    """

    # =========================
    # Basic Fetch
    # =========================
    def get_records_by_user(
        self,
        user_id: int,
        record_type: str | None = None,
        limit: int | None = None,
    ) -> List[Tuple]:
        """
        Fetch records for a user.

        :param user_id: user ID
        :param record_type: 'income', 'expense', or None (both)
        :param limit: max number of rows
        """

        base_sql = """
        SELECT
            id,
            record_type,
            price,
            service,
            record_date,
            created_at
        FROM records
        WHERE user_id = %s
        """

        params = [user_id]

        if record_type:
            base_sql += " AND record_type = %s"
            params.append(record_type)

        base_sql += " ORDER BY record_date DESC, created_at DESC"

        if limit:
            base_sql += " LIMIT %s"
            params.append(limit)

        return self.fetch_all(base_sql, params)

    # =========================
    # Aggregations (Graphs)
    # =========================
    def get_monthly_summary(self, user_id: int, year: int, month: int) -> List[Tuple]:
        """
        Get monthly aggregated totals by record type.
        """
        sql = """
        SELECT
            record_type,
            SUM(price) AS total
        FROM records
        WHERE user_id = %s
          AND YEAR(record_date) = %s
          AND MONTH(record_date) = %s
        GROUP BY record_type
        """
        return self.fetch_all(sql, (user_id, year, month))

    def get_yearly_summary(self, user_id: int, year: int) -> List[Tuple]:
        """
        Get yearly aggregated totals by record type.
        """
        sql = """
        SELECT
            record_type,
            MONTH(record_date) AS month,
            SUM(price) AS total
        FROM records
        WHERE user_id = %s
          AND YEAR(record_date) = %s
        GROUP BY record_type, MONTH(record_date)
        ORDER BY month
        """
        return self.fetch_all(sql, (user_id, year))
