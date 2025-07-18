import sqlite3 
import functools

def transactional(func):
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)  # Execute the database operation
            conn.commit()  # Commit if no error occurs
            return result
        except Exception as e:
            conn.rollback()  # Rollback if any error occurs
            raise e  # Re-raise the exception to propagate it
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
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
#### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')