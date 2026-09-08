import sqlite3

con = sqlite3.connect("backend/cdr_lol.db")
cur = con.cursor()

cur.execute("SELECT id, name, gold_total FROM items WHERE id > 100000")
rows = cur.fetchall()
print(f"Items with ID > 100000: {len(rows)}")
for r in rows:
    print(r)

con.close()
