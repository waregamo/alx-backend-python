#!/usr/bin/env python3
import time
import sqlite3
import functools

# Global cache for queries
query_cache = {}

# Decorator to manage DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Decorator to cache query results based on SQL string
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get("query") or (args[0] if args else None)
        if query in query_cache:
            print("Returning cached result for query:", query)
            return query_cache[query]
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call: query executed and result cached
users = fetch_users_with_cache(query="SELECT * FROM users")
print("First call result:", users)

# Second call: result returned from cache
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print("Second call (cached) result:", users_again)
