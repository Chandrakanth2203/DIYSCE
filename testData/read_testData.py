import sqlite3

DB_PATH = "testData/CustomerDB.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Read all rows
cur.execute("SELECT * FROM customers;")
rows = cur.fetchall()

for row in rows:
    print(row)

cur.close()
conn.close()