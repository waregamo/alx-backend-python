#!/usr/bin/env python3
import sqlite3

DB_NAME = "users.db"

def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create 'users' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')

    #  sample data 
    users = [
        ('Wanjiku', 24),
        ('Otieno', 41),
        ('Kipchoge', 36),
        ('Achieng', 52),
        ('Mwangi', 29),
        ('Chebet', 44),
        ('Kamau', 19),
        ('Moraa', 47),
        ('Mutiso', 33),
        ('Njeri', 61)
    ]

    cursor.executemany('INSERT INTO users (name, age) VALUES (?, ?)', users)
    conn.commit()
    conn.close()
    print("Database and 'users' table created successfully.")

if __name__ == "__main__":
    create_database()
