#!/usr/bin/env python3
import sqlite3
import functools


#decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = None
        if "query" in kwargs:
            query = kwargs["query"]
        elif len(args) > 0:
            query = args[0]

        if query:
            print(f"Executing SQL query: {query}")

        return func(*args, **kwargs)
    return wrapper


#create users table if does not exists
def setup_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
    )
    """)

    cursor.executemany(
            "INSERT INTO users (name, age) VALUES (?, ?)",
            [("Lawre", 24), ("Ambu", 22), ("Jose", 23)]
        )
    conn.commit()
    conn.close()


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


if __name__ == "__main__":
    setup_db()
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
