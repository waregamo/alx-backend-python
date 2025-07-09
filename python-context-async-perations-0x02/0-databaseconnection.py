#!/usr/bin/env python3
import sqlite3

class DatabaseConnection:
    """Custom context manager for SQLite database connection."""

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """Establish connection and return cursor."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        """Close connection and handle exceptions."""
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

# Example usage
if __name__ == "__main__":
    db_name = "users.db" 

    with DatabaseConnection(db_name) as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)
