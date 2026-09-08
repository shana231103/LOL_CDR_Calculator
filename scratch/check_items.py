import sqlite3
import json

con = sqlite3.connect("backend/cdr_lol.db")
cur = con.cursor()

names = ["Malignance", "Fiendhunter Bolts", "Experimental Hexplate", "Zeke's Convergence"]

print("=== Items in SQLite DB ===")
for name in names:
    cur.execute("SELECT id, name, ability_haste, description FROM items WHERE name LIKE ?", (f"%{name}%",))
    rows = cur.fetchall()
    if not rows:
        print(f"NOT FOUND: {name}")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, AH: {row[2]}")
        print(f"Description:\n{row[3]}\n{'-'*40}")

con.close()
