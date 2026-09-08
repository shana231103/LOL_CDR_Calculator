import httpx
import asyncio

async def main():
    async with httpx.AsyncClient() as client:
        # Get versions
        v_resp = await client.get("https://ddragon.leagueoflegends.com/api/versions.json")
        latest = v_resp.json()[0]
        print("Latest version:", latest)
        
        # Get items
        resp = await client.get(f"https://ddragon.leagueoflegends.com/cdn/{latest}/data/en_US/item.json")
        data = resp.json().get("data", {})
        
        for item_id in ["3050", "323050", "3118", "2512", "3073", "3161"]:
            if item_id in data:
                item = data[item_id]
                print(f"--- Item {item_id}: {item.get('name')} ---")
                print("Maps:", item.get("maps"))
                print("InStore:", item.get("inStore"))
                print("Gold:", item.get("gold"))
                print("Stats:", item.get("stats"))
                print("Description:", item.get("description"))
            else:
                print(f"Item {item_id} NOT found in ddragon")

asyncio.run(main())
