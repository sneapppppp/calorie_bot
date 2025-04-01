import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            gender TEXT,
            age INTEGER,
            height INTEGER,
            weight INTEGER,
            activity TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_user_data(user_id, data):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO users (user_id, gender, age, height, weight, activity)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, data['gender'], data['age'], data['height'], data['weight'], data['activity']))
    conn.commit()
    conn.close()