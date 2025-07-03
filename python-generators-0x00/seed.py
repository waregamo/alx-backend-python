#!/usr/bin/python3
import mysql.connector
import csv
import uuid
from mysql.connector import errorcode


def connect_db():
    """Connect to MySQL server"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="3Xplore@"  # Replace with your password
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_database(connection):
    """Create ALX_prodev database if it doesn't exist"""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE ALX_prodev")
        print("Database ALX_prodev created.")
    except mysql.connector.Error as err:
        print(f"Failed to create database: {err}")
    finally:
        cursor.close()


def connect_to_prodev():
    """Connect to ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="3Xplore@",  
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_table(connection):
    """Create user_data table if not exists"""
    cursor = connection.cursor()
    try:
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX(user_id)
        );
        """
        cursor.execute(create_table_sql)
        connection.commit()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    finally:
        cursor.close()


def insert_data(connection, csv_file):
    """Insert data into user_data from CSV if not already present"""
    cursor = connection.cursor()
    try:
        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Check if email already exists to prevent duplicates
                cursor.execute("SELECT * FROM user_data WHERE email = %s", (row['email'],))
                if cursor.fetchone():
                    continue  # Skip duplicates

                insert_sql = """
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s);
                """
                data = (
                    str(uuid.uuid4()),
                    row['name'],
                    row['email'],
                    row['age']
                )
                cursor.execute(insert_sql, data)
        connection.commit()
        print("Data inserted successfully.")
    except FileNotFoundError:
        print(f"File {csv_file} not found.")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    finally:
        cursor.close()
