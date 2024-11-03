import sqlite3


conn = sqlite3.connect("bank_account.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
id INTEGER,
full_name VARCHAR (30), 
age VARCHAR (30),
phone_number VARCHAR (30),
balance REAL
)
""")


def get_balance(id_user):
    cursor.execute("SELECT balance FROM users WHERE id = ?", (id_user,))
    check_balance = cursor.fetchone()

    if check_balance is None:
        return None

    return check_balance[0]