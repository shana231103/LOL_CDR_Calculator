import httpx
import asyncio
import re

async def main():
    async with httpx.AsyncClient() as client:
        v_resp = await client.get("https://ddragon.leagueoflegends.com/api/versions.json")
        latest = v_resp.json()[0]
        resp = await client.get(f"https://ddragon.leagueoflegends.com/cdn/{latest}/data/en_US/item.json")
        data = resp.json().get("data", {})
        
        haste_items = []
        for i_id, item in data.items():
            desc = item.get("description", "")
            name = item.get("name", "")
            maps = item.get("maps", {})
            gold = item.get("gold", {})
            
            # check if summoner's rift map 11
            if not maps.get("11", False):
                continue
            if not gold.get("purchasable", False) and int(i_id) not in [3042, 3040, 3048]:
                continue
            if item.get("requiredAlly") == "Ornn" or item.get("inStore") is False or item.get("hideFromAll", False):
                continue
            if gold.get("total", 0) <= 0:
                continue
            if item.get("requiredChampion"):
                continue
                
            if "haste" in desc.lower():
                haste_items.append((i_id, name, desc))
                
        print(f"Found {len(haste_items)} valid SR items mentioning 'haste'")
        for i_id, name, desc in haste_items:
            # check patterns: Ultimate Haste, Basic Ability Haste, Item Haste, Ability Haste
            print(f"\n--- [{i_id}] {name} ---")
            for part in desc.split("<br>"):
                if "haste" in part.lower():
                    print("  ", part.strip())

asyncio.run(main())
