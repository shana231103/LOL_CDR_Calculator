import sqlite3

con = sqlite3.connect("backend/cdr_lol.db")
cur = con.cursor()

# Check table columns
cur.execute("PRAGMA table_info(items)")
columns = [row[1] for row in cur.fetchall()]
print("Current columns in items:", columns)

for col in ["ultimate_haste", "basic_haste", "summoner_haste"]:
    if col not in columns:
        print(f"Adding column {col} to items...")
        cur.execute(f"ALTER TABLE items ADD COLUMN {col} FLOAT DEFAULT 0.0")
        print(f"Added {col}.")

cur.execute("PRAGMA table_info(items)")
print("Updated columns in items:", [row[1] for row in cur.fetchall()])

con.commit()
con.close()
