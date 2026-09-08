import sqlite3

con = sqlite3.connect("backend/cdr_lol.db")
cur = con.cursor()

cur.execute("SELECT id, name, ability_haste, gold_total, description FROM items WHERE name LIKE '%Zeke%'")
for row in cur.fetchall():
    print(f"ID: {row[0]}, Name: {row[1]}, AH: {row[2]}, Gold: {row[3]}")
    print(f"Desc: {row[4][:120]}...")

con.close()
