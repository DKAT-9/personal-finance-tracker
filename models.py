import sqlite3

def init_db(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT CHECK(type IN ('income','expense')) NOT NULL,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()