from __future__ import annotations

from CYBR_404.WalletNote_ver_06.Backend.Database.ConnectDB import ConnectDB, DBConfig

class CreateDB(ConnectDB):
    """
    Database and table initializer.
    GUARANTEES database selection before table creation.
    """

    def __init__(self, database_name: str = "walletnote_db") -> None:
        super().__init__(DBConfig(database=None))
        self.database_name = database_name

    def create_database(self) -> None:
        self.execute(
            f"""
            CREATE DATABASE IF NOT EXISTS {self.database_name}
            CHARACTER SET utf8mb4
            COLLATE utf8mb4_unicode_ci
            """
        )

    def create_tables(self) -> None:
        # 🔑 reconnect WITH database selected
        self._config = DBConfig(database=self.database_name)
        self._connect()

        self._create_users_table()
        self._create_records_table()

    def _create_users_table(self) -> None:
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                preferred_currency VARCHAR(10) DEFAULT 'USD',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

    def _create_records_table(self) -> None:
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS records (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                record_type ENUM('income', 'expense') NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                service VARCHAR(255) NOT NULL,
                record_date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_records_user
                    FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
            )
            """
        )

    def initialize(self) -> None:
        self.create_database()
        self.create_tables()
