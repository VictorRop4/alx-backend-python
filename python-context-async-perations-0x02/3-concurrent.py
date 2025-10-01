import asyncio
import aiosqlite

# Async function to fetch all users
async def async_fetch_users(db_name="example.db"):
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            print("👥 All Users:")
            for row in rows:
                print(row)
            return rows

# Async function to fetch users older than 40
async def async_fetch_older_users(db_name="example.db"):
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            print("\n🧓 Users older than 40:")
            for row in rows:
                print(row)
            return rows

# Main coroutine that runs both concurrently
async def fetch_concurrently():
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results

# Run the import asyncio
import aiosqlite

# Async function to fetch all users
async def async_fetch_users(db_name="example.db"):
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            print("👥 All Users:")
            for row in rows:
                print(row)
            return rows

# Async function to fetch users older than 40
async def async_fetch_older_users(db_name="example.db"):
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            print("\n🧓 Users older than 40:")
            for row in rows:
                print(row)
            return rows

# Run both queries concurrently
async def fetch_concurrently():
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())

