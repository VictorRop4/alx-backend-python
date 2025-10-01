import sqlite3
import os

# Step 1: Define context manager
class ExecuteQuery:
    def __init__(self, db_name, query, params=()):
        self.db_name = db_name
        self.query = query
        self.params = params

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor  # give cursor back for queries

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.cursor.close()
        self.conn.close()

# Step 2: Setup database (auto-reset)
def setup_database():
    db_file = "example.db"

    # ✅ Remove old database file if it exists
    if os.path.exists(db_file):
        os.remove(db_file)
        print("🗑️ Old database deleted, starting fresh.")

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create new users table
    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER
    )
    """)

    # Insert sample users
    users = [
        ("Alice", "alice@example.com", 30),
        ("Bob", "bob@example.com", 22),
        ("Charlie", "charlie@example.com", 28),
        ("Diana", "diana@example.com", 19),
        ("Eve", "eve@example.com", 35)
    ]
    cursor.executemany("INSERT INTO users (username, email, age) VALUES (?, ?, ?)", users)

    conn.commit()
    conn.close()
    print("✅ Database setup complete with sample data!\n")

# Step 3: Run query with context manager
def run_query():
    with ExecuteQuery("example.db", "SELECT * FROM users WHERE age > ?", (25,)) as cursor:
        results = cursor.execute("SELECT * FROM users WHERE age > ?", (25,))
        print("👤 Users older than 25:\n")
        for row in results:
            print(row)

# Main
if __name__ == "__main__":
    setup_database()
    run_query()
