#!/usr/bin/env python3
import aiosqlite
import asyncio

DB_NAME = "users.db"  

async def async_fetch_users():
    """Fetch all users from the database."""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("All users:")
            for user in users:
                print(user)
            return users

async def async_fetch_older_users():
    """Fetch users older than 40 from the database."""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            older_users = await cursor.fetchall()
            print("\nUsers older than 40:")
            for user in older_users:
                print(user)
            return older_users

async def fetch_concurrently():
    """Run both queries concurrently."""
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# Entry point
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
