import httpx
import asyncio

async def main():
    async with httpx.AsyncClient(timeout=15.0) as client:
        # Check CommunityDragon for item 3050
        url = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/items.json"
        resp = await client.get(url)
        items = resp.json()
        
        for item in items:
            if item.get("id") == 3050:
                print("=== CommunityDragon Item 3050 ===")
                print("Name:", item.get("name"))
                print("Description:", item.get("description"))
                print("Active/Passives:", item.get("passives"))
                break

asyncio.run(main())
