#!/usr/bin/env python3
import sqlite3
import functools


# Global query cache
query_cache = {}


# Decorator: open and close database connection automatically
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


# Decorator: cache query results based on SQL query string
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get("query") or (args[0] if args else None)

        if query in query_cache:
            print(f"Using cached result for query: {query}")
            return query_cache[query]

        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        print(f"Caching result for query: {query}")
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# Example usage
if __name__ == "__main__":
    # First call: hits the DB
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)

    # Second call: uses cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)
