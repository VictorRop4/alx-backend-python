import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that yields rows from the user_data table in batches.
    Each batch is a list of rows (dictionaries).
    """
    connection = mysql.connector.connect(
        host='ALX_localhost',
        user='root',       # Replace with actual credentials
        password='root',
        database='ALX_prodev'
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch  # Yield the current batch of rows

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Processes each batch from the database and yields users over age 25.
    Uses the stream_users_in_batches generator.
    """
    for batch in stream_users_in_batches(batch_size):  # Loop 1
        for row in batch:                              # Loop 2
            if row['age'] > 25:
                yield row
