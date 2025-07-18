import time
import sqlite3 
import functools

#### paste your with_db_decorator here

""" your code goes here"""
def retry_on_failure(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"[RETRY] Attempt {attempts} failed: {e}")
                    if attempts == retries:
                        raise  # Re-raise exception after final attempt
                    time.sleep(delay)
        return wrapper
    return decorator

def with_db_connection(func):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('example.db')  # Open connection
        try:
            result = func(conn, *args, **kwargs)  # Pass connection to the function
            return result
        finally:
            conn.close()  # Ensure connection is closed
    return wrapper

@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)