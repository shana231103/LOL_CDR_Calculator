import sys
sys.path.insert(0, ".")
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

payload = {
    "champion_id": "Ahri",
    "champion_level": 11,
    "ability_ranks": {"Q": 5, "W": 3, "E": 1, "R": 2},
    "items": [3118, 3050, 3161, 3158], # Malignance + Zeke's + Shojin + Ionian
    "summoner_spells": ["SummonerFlash"],
    "stat_shard_ids": [],
    "summoner_spell_ids": [],
    "cloud_drake_count": 0,
    "has_chemtech_blight": False
}

response = client.post("/api/v1/calculate", json=payload)
print("Status Code:", response.status_code)
if response.status_code == 200:
    data = response.json()
    print("Total Ability Haste:", data["ability_haste"])
    print("Total Ultimate Haste:", data["ultimate_haste"])
    print("Total Basic Haste:", data["basic_haste"])
    print("Total Summoner Haste:", data["summoner_haste"])
    for slot, ab in data["abilities"].items():
        print(f"Skill {slot}: Base CD={ab['base_cooldown']}, Final CD={ab['final_cooldown']}, Applicable Haste={ab['applicable_haste']}")
    for sp in data["summoner_spells"]:
        print(f"Spell {sp['name']}: Base CD={sp['base_cooldown']}, Final CD={sp['final_cooldown']}, Applicable Haste={sp['applicable_haste']}")
else:
    print("Error:", response.text)
