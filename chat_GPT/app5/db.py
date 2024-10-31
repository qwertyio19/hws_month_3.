# database.py
import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        name TEXT,
                        age INTEGER,
                        choices TEXT
                      )""")
    conn.commit()
    conn.close()

def register_user(user_id, name=None, age=None):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id, name, age, choices) VALUES (?, ?, ?, ?)", 
                   (user_id, name, age, ""))
    conn.commit()
    conn.close()

def update_user(user_id, name, age):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = ?, age = ? WHERE user_id = ?", (name, age, user_id))
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def save_choice(user_id, choice):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET choices = choices  ?  '; ' WHERE user_id = ?", (choice, user_id))
    conn.commit()
    conn.close()