# WalletNote_ver_05/Backend/System/Dashboard.py
from __future__ import annotations

from typing import Dict, List

from WalletNote_ver_05.Backend.Database.RecallDB import RecallDB
from WalletNote_ver_05.Backend.Database.SaveDB import SaveDB
from WalletNote_ver_05.Backend.Information.InputUserInformation import UserInformation
from WalletNote_ver_05.Backend.Information.InputInformation import InputInformation
from WalletNote_ver_05.Backend.System.MakeGraph import MakeGraph


class Dashboard:
    """
    Dashboard controller class.

    Responsibilities:
    - Orchestrate data retrieval for the dashboard.
    - Trigger graph generation via MakeGraph.
    - Return a unified data structure for the Flask layer.
    """

    def __init__(self) -> None:
        self._recall_db = RecallDB()
        self._save_db = SaveDB()
        self._graph_maker = MakeGraph()

    def load_dashboard(self, user: UserInformation) -> Dict[str, object]:
        """
        Load all dashboard-related data for a user.

        Args:
            user: UserInformation instance.

        Returns:
            Dictionary containing records and graph data.
        """
        records: List[InputInformation] = self._recall_db.fetch_all_records(user)

        graphs = {
            "monthly": self._graph_maker.monthly_graph(records),
            "yearly": self._graph_maker.yearly_graph(records),
            "daily": self._graph_maker.daily_graph(records),
        }

        return {
            "records": records,
            "graphs": graphs,
        }

    def load_saved_records(self, user: UserInformation) -> List[InputInformation]:
        """
        Load user-saved records.

        Args:
            user: UserInformation instance.

        Returns:
            List of saved InputInformation objects.
        """
        return self._save_db.fetch_saved_records(user)
