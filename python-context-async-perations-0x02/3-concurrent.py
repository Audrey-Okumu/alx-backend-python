#!/usr/bin/env python3
"""
Concurrent asynchronous database queries using aiosqlite and asyncio.gather
"""

import asyncio
import aiosqlite


async def async_fetch_users(db_name="test.db"):
    """Fetch all users from the database"""
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()


async def async_fetch_older_users(db_name="test.db"):
    """Fetch users older than 40 from the database"""
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            return await cursor.fetchall()


async def fetch_concurrently():
    """Run both queries concurrently"""
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    # Print results so we can see them
    for row in results[0]:
        print(row)
    for row in results[1]:
        print(row)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
