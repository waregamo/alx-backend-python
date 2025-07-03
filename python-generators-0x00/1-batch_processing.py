import mysql.connector

def stream_users_in_batches(batch_size):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="3Xplore@",  # ← Replace with your actual password
        database="ALX_prodev"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch

    cursor.close()
    conn.close()

def batch_processing(batch_size):
    filtered_users = []
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user["age"] > 25:
                filtered_users.append(user)
    return filtered_users

