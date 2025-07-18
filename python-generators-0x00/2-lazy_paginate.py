import mysql.connector

def paginate_users(page_size, offset):
    """
    Fetches a page of user data from the database given a page size and offset.
    Returns a list of dictionaries representing user records.
    """
    connection = mysql.connector.connect(
        host='ALX_localhost',
        user='root',
        password='root',
        database='ALX_prodev'
    )
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
    cursor.execute(query, (page_size, offset))
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return users


def lazy_paginate(page_size):
    """
    Generator that lazily fetches user data one page at a time.
    Uses only one loop and yields each page as it is requested.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
