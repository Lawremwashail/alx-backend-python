#!/usr/bin/env python3
import sqlite3

class DatabaseConnection:
    """Custom context manager for handling database connection."""

    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self.cursor  # return cursor so queries can be run inside `with`

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


if __name__ == "__main__":
    # Example usage
    with DatabaseConnection("users.db") as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
