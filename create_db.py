import sqlite3

# Create users database
conn = sqlite3.connect("users.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT
)
""")

conn.commit()
conn.close()


# Create feedback database
conn = sqlite3.connect("data.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    delivery_time INTEGER,
    product_quality INTEGER,
    service_rating INTEGER,
    support_rating INTEGER
)
""")

conn.commit()
conn.close()

print("Databases created successfully!")
