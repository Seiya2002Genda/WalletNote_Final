# Backend/Information/UserInformation.py
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class UserInformation:
    """
    UserInformation stores authenticated user data.

    This class is used across:
    - Authentication (login / signup)
    - RecordDB / RecallDB / EditDB
    - Setting / SaveDB

    IMPORTANT:
    - This class holds data only
    - No database logic is included here
    """

    user_id: int
    username: str
    email: str
    password: str = ""
