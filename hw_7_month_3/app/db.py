import sqlite3


conn = sqlite3.connect("24_KG.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS news (
id INTEGER,
news TEXT
)
""")