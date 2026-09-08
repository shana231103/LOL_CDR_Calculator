import httpx
import asyncio

async def test():
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        # Test calculate with Ahri
        payload = {
            "champion_id": "Ahri",
            "abilities": {"Q": 1, "W": 1, "E": 1, "R": 1},
            "items": [3118, 2512, 3073, 3050], # Malignance, Fiendhunter, Hexplate, Zeke
            "runes": [],
            "summoner_spells": []
        }
        res = await client.post("/api/v1/calculate", json=payload)
        print("Status:", res.status_code)
        data = res.json()
        print("Ability Haste:", data.get("ability_haste"))
        print("Ultimate Haste:", data.get("ultimate_haste"))
        print("R Applicable Haste:", data.get("abilities", {}).get("R", {}).get("applicable_haste"))
        print("Q Applicable Haste:", data.get("abilities", {}).get("Q", {}).get("applicable_haste"))

asyncio.run(test())
