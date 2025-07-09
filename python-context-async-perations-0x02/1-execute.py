#!/usr/bin/env python3
import sqlite3

class ExecuteQuery:
    """Custom context manager to execute a query with parameters."""

    def __init__(self, db_name, query, params):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """Open the database and execute the query."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the cursor and connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

# Example usage
if __name__ == "__main__":
    db_name = "users.db"  # Adjust path if needed
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery(db_name, query, params) as results:
        for row in results:
            print(row)
