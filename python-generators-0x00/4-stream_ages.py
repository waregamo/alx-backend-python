import mysql.connector

def stream_user_ages():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="3Xplore@",  # Replace with your actual password
        database="ALX_prodev"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:
        yield row[0]  # Yield the age

    cursor.close()
    conn.close()

def average_user_age():
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("No users found.")
    else:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")

if __name__ == "__main__":
    average_user_age()
