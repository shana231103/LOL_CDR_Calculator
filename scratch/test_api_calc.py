import requests

payload = {
    "champion_id": "Ahri",
    "champion_level": 11,
    "ability_ranks": {"Q": 5, "W": 3, "E": 1, "R": 2},
    "item_ids": ["3118", "3050"], # Malignance (15 AH, 20 Ult Haste) + Zeke's Convergence (10 AH, 15 Ult Haste)
    "rune_selections": [],
    "stat_shard_ids": [],
    "summoner_spell_ids": [],
    "cloud_drake_count": 0,
    "has_chemtech_blight": False
}

r = requests.post("http://127.0.0.1:8000/api/v1/calculate", json=payload)
print("Status:", r.status_code)
if r.status_code == 200:
    data = r.json()
    print("Total Ability Haste:", data["total_ability_haste"])
    print("Total Ultimate Haste:", data["total_ultimate_haste"])
    print("Total Basic Haste:", data["basic_haste"])
    for ab in data["abilities"]:
        print(f"Skill {ab['slot']}: Base CD={ab['base_cooldown']}, CD={ab['cooldown']}, Applicable Haste={ab['applicable_haste']}")
else:
    print(r.text)
