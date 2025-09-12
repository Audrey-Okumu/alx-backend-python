"""
Concurrent asynchronous database queries using aiosqlite and asyncio.gather
"""

import asyncio
import aiosqlite


async def async_fetch_users(db_name="test.db"):
    """Fetch all users from the database"""
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            print("All Users:")
            for row in rows:
                print(row)
            return rows


async def async_fetch_older_users(db_name="test.db"):
    """Fetch users older than 40 from the database"""
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            print("\nUsers older than 40:")
            for row in rows:
                print(row)
            return rows


async def fetch_concurrently():
    """Run both queries concurrently"""
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
