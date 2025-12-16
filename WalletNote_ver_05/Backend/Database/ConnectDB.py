# WalletNote_ver_05/Backend/Database/ConnectDB.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor


ParamsType = Optional[Union[Sequence[Any], Dict[str, Any]]]


@dataclass(frozen=True)
class DBConfig:
    """
    Immutable configuration for a MySQL connection.
    """
    host: str = "127.0.0.1"
    port: int = 3306
    user: str = "root"
    password: str = "root1234"
    database: Optional[str] = None
    autocommit: bool = False


class ConnectDB:
    """
    Base class for connecting to MySQL and executing SQL statements.

    Notes:
    - This class does NOT create databases/tables. That is handled by CreateDB.py.
    - It can connect either to a specific database (database=<name>) or to the server only (database=None).
    """

    def __init__(self, config: Optional[DBConfig] = None) -> None:
        self._config: DBConfig = config or DBConfig()
        self._conn: Optional[MySQLConnection] = None

    @property
    def config(self) -> DBConfig:
        return self._config

    @property
    def is_connected(self) -> bool:
        return self._conn is not None and self._conn.is_connected()

    def connect(self) -> None:
        """
        Establish a connection to MySQL if not already connected.
        """
        if self.is_connected:
            return

        self._conn = mysql.connector.connect(
            host=self._config.host,
            port=self._config.port,
            user=self._config.user,
            password=self._config.password,
            database=self._config.database,
            autocommit=self._config.autocommit,
        )

    def close(self) -> None:
        """
        Close the current connection if it exists.
        """
        if self._conn is not None:
            try:
                if self._conn.is_connected():
                    self._conn.close()
            finally:
                self._conn = None

    def cursor(self, dictionary: bool = True) -> MySQLCursor:
        """
        Create a cursor for the active connection.

        Args:
            dictionary: If True, returns rows as dicts (recommended).

        Returns:
            A MySQLCursor.
        """
        self.connect()
        assert self._conn is not None  # for type checkers
        return self._conn.cursor(dictionary=dictionary)

    def commit(self) -> None:
        """
        Commit the current transaction.
        """
        if not self.is_connected:
            return
        assert self._conn is not None
        self._conn.commit()

    def rollback(self) -> None:
        """
        Roll back the current transaction.
        """
        if not self.is_connected:
            return
        assert self._conn is not None
        self._conn.rollback()

    def execute(self, sql: str, params: ParamsType = None) -> int:
        """
        Execute a single SQL statement.

        Args:
            sql: SQL statement.
            params: Optional parameters (tuple/list for %s placeholders, or dict for named placeholders).

        Returns:
            Number of affected rows.
        """
        cur = self.cursor(dictionary=False)
        try:
            cur.execute(sql, params)
            return cur.rowcount
        finally:
            cur.close()

    def executemany(self, sql: str, seq_params: Sequence[Sequence[Any]]) -> int:
        """
        Execute the same SQL statement for multiple parameter sets.

        Args:
            sql: SQL statement.
            seq_params: List of parameter tuples/lists.

        Returns:
            Number of affected rows (sum may vary by driver; rowcount may be -1 in some cases).
        """
        cur = self.cursor(dictionary=False)
        try:
            cur.executemany(sql, seq_params)
            return cur.rowcount
        finally:
            cur.close()

    def fetch_all(self, sql: str, params: ParamsType = None) -> List[Dict[str, Any]]:
        """
        Execute a query and return all rows as a list of dictionaries.

        Args:
            sql: SQL query.
            params: Optional parameters.

        Returns:
            List of rows as dicts.
        """
        cur = self.cursor(dictionary=True)
        try:
            cur.execute(sql, params)
            rows = cur.fetchall()
            return list(rows) if rows else []
        finally:
            cur.close()

    def fetch_one(self, sql: str, params: ParamsType = None) -> Optional[Dict[str, Any]]:
        """
        Execute a query and return a single row as a dictionary.

        Args:
            sql: SQL query.
            params: Optional parameters.

        Returns:
            A single row dict, or None if not found.
        """
        cur = self.cursor(dictionary=True)
        try:
            cur.execute(sql, params)
            row = cur.fetchone()
            return dict(row) if row else None
        finally:
            cur.close()

    def __enter__(self) -> "ConnectDB":
        """
        Context manager entry: ensures connection is established.
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        """
        Context manager exit:
        - commits if no exception
        - rollbacks if exception
        - closes connection
        """
        try:
            if exc is None:
                self.commit()
            else:
                self.rollback()
        finally:
            self.close()
