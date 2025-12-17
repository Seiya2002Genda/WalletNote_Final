from __future__ import annotations

import mysql.connector
from dataclasses import dataclass
from typing import Any, Iterable


@dataclass
class DBConfig:
    host: str = "localhost"
    user: str = "root"
    password: str = "root1234"
    database: str | None = "walletnote_db"


class ConnectDB:
    """
    Base MySQL connection handler.
    Ensures database is ALWAYS selected when required.
    """

    def __init__(self, config: DBConfig | None = None) -> None:
        self._config = config or DBConfig()
        self._conn = None

    def _connect(self) -> None:
        self._conn = mysql.connector.connect(
            host=self._config.host,
            user=self._config.user,
            password=self._config.password,
            database=self._config.database,
            autocommit=True,
        )

    def _get_cursor(self):
        if not self._conn or not self._conn.is_connected():
            self._connect()
        return self._conn.cursor()

    def execute(self, sql: str, params: Iterable[Any] | None = None) -> None:
        cur = self._get_cursor()
        cur.execute(sql, tuple(params) if params else ())
        cur.close()

    def fetch_one(self, sql: str, params: Iterable[Any] | None = None):
        cur = self._get_cursor()
        cur.execute(sql, tuple(params) if params else ())
        row = cur.fetchone()
        cur.close()
        return row

    def fetch_all(self, sql: str, params: Iterable[Any] | None = None):
        cur = self._get_cursor()
        cur.execute(sql, tuple(params) if params else ())
        rows = cur.fetchall()
        cur.close()
        return rows
