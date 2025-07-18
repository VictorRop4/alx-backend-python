import mysql.connector

def stream_user_ages():
    """
    Generator function that yields user ages one by one from the database.
    """
    connection = mysql.connector.connect(
        host='ALX_localhost',
        user='root',
        password='root',
        database='ALX_prodev'
    )
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:
        yield age

    cursor.close()
    connection.close()

def compute_average_age():
    """
    Consumes the age generator to compute the average age without loading
    the entire dataset into memory.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count > 0:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No users found.")

# Execute
compute_average_age()
