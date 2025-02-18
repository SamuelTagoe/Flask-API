import sqlite3

conn = sqlite3.connect("books.sqlite3")
cursor = conn.cursor()

sql_query = """
    CREATE TABLE IF NOT EXISTS book (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author TEXT NOT NULL,
        language TEXT NOT NULL,
        title TEXT NOT NULL
    )
"""
cursor.execute(sql_query)
conn.commit()
conn.close()
