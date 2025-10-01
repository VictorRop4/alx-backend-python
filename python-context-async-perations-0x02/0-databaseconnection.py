
import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        # Open the connection and return a cursor
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Commit if no exception, rollback otherwise
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
            print(f"An error occurred: {exc_val}")
        # Close the connection in all cases
        self.conn.close()

# Create a sample database and table for demonstration
with DatabaseConnection("example.db") as cursor:
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
    cursor.execute("INSERT INTO users (name) VALUES (?)", ("Bob",))

# Use the context manager to fetch results
with DatabaseConnection("example.db") as cursor:
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print("Users in database:")
    for row in results:
        print(row)
