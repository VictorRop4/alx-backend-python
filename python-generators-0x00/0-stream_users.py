import mysql.connector

def stream_users():
    connection = mysql.connector.connect(
        host='ALX_localhost',
        user='root',       # ← replace with your actual username
        password='root',   # ← replace with your actual password
        database='ALX_prodev'
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row

    cursor.close()
    connection.close()
