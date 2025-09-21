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

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

users = fetch_all_users(query="SELECT * FROM users")
