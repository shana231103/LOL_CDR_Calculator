import sqlite3

conn = sqlite3.connect("cdr_lol.db")
c = conn.cursor()
c.execute("""
SELECT id, name, ability_haste, ultimate_haste, basic_haste, summoner_haste 
FROM items 
WHERE id IN ('3118', '3073', '2512', '3050', '3161', '3158')
ORDER BY name
""")
rows = c.fetchall()
print("ID | Name | Base AH | Ult Haste | Basic Haste | Summ Haste")
print("-" * 65)
for r in rows:
    print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]}")
conn.close()
