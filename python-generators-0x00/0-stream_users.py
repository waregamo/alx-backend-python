#!/usr/bin/python3
import mysql.connector

def stream_users():
    """Generator that yields users one by one from the database"""
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='3Xplore@',  # Replace with your real MySQL password
        database='ALX_prodev'
    )
    cursor = conn.cursor(dictionary=True)  # dictionary=True gives us rows as dicts

    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row  # Yield one user at a time

    cursor.close()
    conn.close()
