import sqlite3
import functools

#### decorator to lof SQL queries

""" YOUR CODE GOES HERE"""
def log_queries():
    def decorator(func):
        def wrapper(query, *args, **kwargs):
            print(f"[LOG] Executing SQL Query: {query}")
            return func(query, *args, **kwargs)
        return wrapper
    return decorator



@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")