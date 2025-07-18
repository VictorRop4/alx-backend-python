import time
import sqlite3 
import functools


query_cache = {}

"""your code goes here"""
def cache_query(func):
    cache = {}

    def wrapper(query, *args, **kwargs):
        if query in cache:
            print("[CACHE] Returning cached result.")
            return cache[query]
        result = func(query, *args, **kwargs)
        cache[query] = result
        return result

    return wrapper


    return wrapper

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
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")