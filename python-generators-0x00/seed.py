import mysql.connector
import uuid
import csv

# 1. Connect to the MySQL server
def connect_db():
    return mysql.connector.connect(
        host='ALX_localhost',
        user='root',       # ← Replace with your username
        password='root'    # ← Replace with your password
    )

# 2. Create the database if it does not exist
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()

# 3. Connect specifically to the ALX_prodev database
def connect_to_prodev():
    return mysql.connector.connect(
        host='ALX_localhost',
        user='root',       # ← Replace with your username
        password='root',   # ← Replace with your password
        database='ALX_prodev'
    )

# 4. Create the user_data table
def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) NOT NULL,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3,0) NOT NULL,
            PRIMARY KEY (user_id),
            UNIQUE KEY unique_email (email)
        )
    """)
    cursor.close()

# 5. Insert a single row if the email does not already exist
def insert_data(connection, data):
    cursor = connection.cursor()
    query = """
    INSERT INTO user_data (user_id, name, email, age)
    SELECT %s, %s, %s, %s FROM DUAL
    WHERE NOT EXISTS (SELECT 1 FROM user_data WHERE email = %s)
    """
    for row in data:
        user_id = str(uuid.uuid4())
        name = row['name']
        email = row['email']
        age = int(row['age'])

        cursor.execute(query, (user_id, name, email, age, email))
    connection.commit()
    cursor.close()

# ✅ Generator that yields one row at a time from a CSV file
def csv_row_generator(filepath):
    with open(filepath, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield row  # Each row is a dictionary: {"name": ..., "email": ..., "age": ...}
