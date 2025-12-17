from CYBR_404.WalletNote_ver_06.Backend.Database.RecallDB import RecallDB


class Dashboard:
    def __init__(self):
        self.recall_db = RecallDB()

    def get_recent_records(self, user_id: int):
        rows = self.recall_db.get_records_by_user(user_id)

        results = []
        for r in rows:
            results.append({
                "record_date": r[0],
                "record_type": r[1],
                "service": r[2],
                "price": float(r[3]),
            })
        return results

    def get_summary_by_type(self, user_id: int):
        rows = self.recall_db.fetch_all(
            """
            SELECT record_type, SUM(price)
            FROM records
            WHERE user_id = %s
            GROUP BY record_type
            """,
            (user_id,),
        )

        summary = {"income": 0, "expense": 0}
        for r in rows:
            summary[r[0]] = float(r[1])
        return summary

    def get_expense_by_service(self, user_id: int):
        rows = self.recall_db.fetch_all(
            """
            SELECT service, SUM(price)
            FROM records
            WHERE user_id = %s AND record_type = 'expense'
            GROUP BY service
            """,
            (user_id,),
        )

        return [{"service": r[0], "total": float(r[1])} for r in rows]
