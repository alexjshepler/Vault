import os
import sqlite3 as sql

from typing import Optional

from Logger import logger as log

DATABASE_NAME = 'database.db'

class Database:
    def __init__(self, db_path=DATABASE_NAME):
        self.db_path = db_path
        self.conn: Optional[sql.Connection] = None
        self.cursor: Optional[sql.Cursor] = None

        if not os.path.exists(self.db_path):
            log.warning("Database doesn't exist, creating it now.")
            sql.connect(self.db_path).close()

    def connect(self):
        log.debug('Connecting to database')
        self.conn = sql.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.conn:
            log.debug('Disconnecting from database')
            self.conn.close()
            return

        log.warning('Database not connected, nothing to disconnect.')

    def list_tables(self) -> list[str]:
        # Connect to database
        self.connect()

        # Get tables or empty list
        if self.cursor:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = self.cursor.fetchall()

            for i, table in enumerate(tables):
                tables[i] = table[0]
        else:
            tables = []

        # Disconnect from database
        self.disconnect()

        log.info(f"Database has {len(tables):02d} table(s)")

        return tables

    def create_table(self, table_name: str, columns: dict):
        # Connect to database
        self.connect()

        columns_str = ", ".join([f"{col} {dtype}" for col, dtype in columns.items()])
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str});"

        try:
            self.cursor.execute(create_table_sql)
            self.conn.commit()
            log.info(f'Table "{table_name}" created successfully.')
        except sql.Error as e:
            log.error(f'Error creating table: {e}')
        # Discconect from database
        finally:
            self.disconnect()

    def get_entries(self, table_name):
        # Connect to database
        self.connect()

        try:
            # Get column names
            self.cursor.execute(f"PRAGMA table_info({table_name});")
            columns = [row[1] for row in self.cursor.fetchall()]  # Extract column names

            # Get all entries
            self.cursor.execute(f"SELECT * FROM {table_name};")
            entries = self.cursor.fetchall()

        except sql.Error as e:
            log.error(f"Failed to retrieve entries: {e}")
            columns, entries = [], []

        # Disconnect from database
        self.disconnect()

        return columns, entries

    def get_columns(self, table_name):
        """Fetch column names of a given table."""
        self.connect()
        try:
            self.cursor.execute(f"PRAGMA table_info({table_name});")
            columns = [
                row[1] for row in self.cursor.fetchall()
            ]  # Column names are in the second field
        except sql.Error as e:
            log.error(f"Failed to retrieve columns: {e}")
            columns = []
        finally:
            self.disconnect()
        return columns


    def insert_entry(self, table_name, data):
        """Insert a new row into the specified table."""
        self.connect()
        try:
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["?"] * len(data))
            values = tuple(data.values())

            sql_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"
            self.cursor.execute(sql_query, values)
            self.conn.commit()
            log.info("New entry added successfully.")
        except sql.Error as e:
            log.error(f"Failed to insert entry: {e}")
        finally:
            self.disconnect()
