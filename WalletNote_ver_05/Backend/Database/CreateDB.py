# WalletNote_ver_05/Backend/Database/CreateDB.py
from __future__ import annotations

from typing import Optional

from WalletNote_ver_05.Backend.Database.ConnectDB import ConnectDB, DBConfig


class CreateDB(ConnectDB):
    """
    Database and table creator.

    Responsibilities:
    - Create the WalletNote database if it does not exist.
    - Create required tables if they do not exist.
    - This class does NOT insert or query business data.
    """

    DEFAULT_DB_NAME = "walletnote_db"

    def __init__(self, db_name: Optional[str] = None) -> None:
        """
        Initialize with a target database name.

        Args:
            db_name: Name of the database to create/use.
                     If None, DEFAULT_DB_NAME is used.
        """
        self.db_name = db_name or self.DEFAULT_DB_NAME

        # Step 1: connect to MySQL server (no database yet)
        super().__init__(DBConfig(database=None))

    def create_database(self) -> None:
        """
        Create the database if it does not already exist.
        """
        self.connect()
        sql = f"CREATE DATABASE IF NOT EXISTS `{self.db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        self.execute(sql)
        self.commit()
        self.close()

    def _reconnect_with_database(self) -> None:
        """
        Reconnect using the target database.
        """
        self.close()
        self._config = DBConfig(database=self.db_name)
        self.connect()

    def create_tables(self) -> None:
        """
        Create all required tables for WalletNote.
        """
        self._reconnect_with_database()

        # Users table (for UserInformation)
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

        # Records table (for InputInformation)
        create_records_table = """
        CREATE TABLE IF NOT EXISTS records (
            record_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            record_date DATE NOT NULL,
            service_or_product VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
                ON DELETE CASCADE
        )
        """

        # User settings table
        create_settings_table = """
        CREATE TABLE IF NOT EXISTS user_settings (
            setting_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            currency VARCHAR(10) DEFAULT 'USD',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
                ON DELETE CASCADE
        )
        """

        self.execute(create_users_table)
        self.execute(create_records_table)
        self.execute(create_settings_table)

        self.commit()
        self.close()

    def initialize_all(self) -> None:
        """
        Public method to initialize database and tables in order.
        """
        self.create_database()
        self.create_tables()
