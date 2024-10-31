import sqlite3


conn = sqlite3.connect("register.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
id INTEGER,
full_name VARCHAR (30), 
age VARCHAR (30),
phone_number VARCHAR (30)
)
""")


def get_info(id_user):
    cursor.execute("SELECT * FROM users WHERE id = ?", (id_user,))
    info = cursor.fetchone()
    return f"Id:{info[0]}, ФИО:{info[1]}, Возраст:{info[2]}, Номер телефона:{info[3]}"