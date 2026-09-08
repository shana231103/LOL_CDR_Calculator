import sqlite3
import re

con = sqlite3.connect("backend/cdr_lol.db")
cur = con.cursor()

cur.execute("SELECT id, name, ability_haste, description FROM items")
rows = cur.fetchall()

print(f"Total items in DB: {len(rows)}")

haste_pattern = re.compile(r"(\d+)\s*(?:<[^>]+>)*\s*Ultimate\s*(?:Ability)?\s*Haste", re.IGNORECASE)
bonus_ah_pattern = re.compile(r"(?:gain|grant|grants|gives)\s*(\d+)\s*(?:<[^>]+>)*\s*Ability\s*Haste", re.IGNORECASE)

print("\n--- Items mentioning Ultimate Haste or Ultimate Ability Haste ---")
for r in rows:
    desc = r[3]
    if "ultimate" in desc.lower() and "haste" in desc.lower():
        print(f"ID: {r[0]}, Name: {r[1]}, AH in DB: {r[2]}")
        # print matching snippets
        for line in desc.split("<br>"):
            if "haste" in line.lower():
                print("  ", line.strip())

print("\n--- Check all items where description has 'Haste' but ability_haste == 0 ---")
for r in rows:
    desc = r[3]
    ah = r[2]
    if ah == 0.0 and "haste" in desc.lower():
        print(f"ID: {r[0]}, Name: {r[1]}, AH in DB: {ah}")
        for line in desc.split("<br>"):
            if "haste" in line.lower():
                print("  ", line.strip())

print("\n--- Check Zeke's Convergence specifically ---")
cur.execute("SELECT id, name, ability_haste, description FROM items WHERE name LIKE '%Zeke%'")
for r in cur.fetchall():
    print(r)

con.close()
