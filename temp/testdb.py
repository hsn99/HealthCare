import sqlite3

conn = sqlite3.connect("healthcare.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM patients")
rows = cursor.fetchall()
print(rows)
conn.close()
