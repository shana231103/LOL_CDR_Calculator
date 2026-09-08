import sqlite3
import re
import json
from pathlib import Path

con = sqlite3.connect("backend/cdr_lol.db")
cur = con.cursor()
cur.execute("SELECT id, name, description FROM items")
rows = cur.fetchall()

ult_haste_regex = re.compile(r"(\d+)\s*(?:<[^>]+>)*\s*Ultimate\s*(?:Ability)?\s*Haste", re.IGNORECASE)
basic_haste_regex = re.compile(r"(\d+)\s*(?:<[^>]+>)*\s*Basic\s*Ability\s*Haste", re.IGNORECASE)
summ_haste_regex = re.compile(r"(\d+)\s*(?:<[^>]+>)*\s*Summoner\s*Spell\s*Haste", re.IGNORECASE)
base_haste_regex = re.compile(r"(?<!Ultimate\s)(?<!Basic\s)(\d+)\s*(?:<[^>]+>)*\s*Ability Haste", re.IGNORECASE)

# load item_modifiers
item_overlay_path = Path("backend/app/infrastructure/external/item_modifiers.json")
overlay = {}
if item_overlay_path.exists():
    with open(item_overlay_path, encoding="utf-8") as f:
        overlay = json.load(f)

for item_id, name, desc in rows:
    str_id = str(item_id)
    ah = 0.0
    ult_h = 0.0
    basic_h = 0.0
    summ_h = 0.0
    
    # Check stats block first if present
    stats_match = re.search(r"<stats>(.*?)</stats>", desc, re.IGNORECASE | re.DOTALL)
    if stats_match:
        m = base_haste_regex.search(stats_match.group(1))
        if m:
            ah = float(m.group(1))
    else:
        # fallback for items without stats tag
        # check that it's not conditional passive haste
        m = base_haste_regex.search(desc)
        if m and "gain" not in desc[:m.start()].lower()[-10:]:
            ah = float(m.group(1))
            
    # Specialized hastes from passives / description
    m_ult = ult_haste_regex.search(desc)
    if m_ult:
        ult_h = float(m_ult.group(1))
        
    m_basic = basic_haste_regex.search(desc)
    if m_basic:
        basic_h = float(m_basic.group(1))
        
    m_summ = summ_haste_regex.search(desc)
    if m_summ:
        summ_h = float(m_summ.group(1))
        
    # Apply overlay if present
    if str_id in overlay:
        item_mod = overlay[str_id]
        if "ability_haste" in item_mod:
            ah = float(item_mod["ability_haste"])
        if "ultimate_haste" in item_mod:
            ult_h = float(item_mod["ultimate_haste"])
        if "basic_haste" in item_mod:
            basic_h = float(item_mod["basic_haste"])
        if "summoner_haste" in item_mod:
            summ_h = float(item_mod["summoner_haste"])
            
    if ult_h > 0 or basic_h > 0 or summ_h > 0:
        print(f"[{item_id}] {name} -> AH: {ah}, UltH: {ult_h}, BasicH: {basic_h}, SummH: {summ_h}")

con.close()
