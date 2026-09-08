# File: backend/tests/unit/test_item_filtering.py

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.infrastructure.external.riot_client import RiotDataDragonClient, TRANSFORMED_TEAR_ITEM_IDS


@pytest.fixture
def mock_item_json_data():
    return {
        "3071": {
            "name": "Black Cleaver",
            "description": "<mainText>Grants <attention>20 Ability Haste</attention> and Armor Penetration.</mainText>",
            "gold": {"purchasable": True, "total": 3000},
            "maps": {"11": True, "12": True, "21": True},
            "image": {"full": "3071.png"},
            "inStore": True,
        },
        "2051": {
            "name": "Guardian's Horn",
            "description": "ARAM starting item.",
            "gold": {"purchasable": True, "total": 950},
            "maps": {"11": False, "12": True},
            "image": {"full": "2051.png"},
            "inStore": True,
        },
        "3128": {
            "name": "Deathfire Grasp",
            "description": "Removed item from old patches.",
            "gold": {"purchasable": False, "total": 3100},
            "maps": {"11": True},
            "image": {"full": "3128.png"},
            "inStore": True,
        },
        "3042": {
            "name": "Muramana",
            "description": "<mainText>Grants <attention>15 Ability Haste</attention> and Shock.</mainText>",
            "gold": {"purchasable": False, "total": 2900},
            "maps": {"11": True},
            "image": {"full": "3042.png"},
            "inStore": True,
        },
        "3040": {
            "name": "Seraph's Embrace",
            "description": "<mainText>Grants <attention>25 Ability Haste</attention> and Lifeline shield.</mainText>",
            "gold": {"purchasable": False, "total": 2900},
            "maps": {"11": True},
            "image": {"full": "3040.png"},
            "inStore": True,
        },
        "3048": {
            "name": "Fimbulwinter",
            "description": "<mainText>Grants <attention>15 Ability Haste</attention> and Bonus Health.</mainText>",
            "gold": {"purchasable": False, "total": 2400},
            "maps": {"11": True},
            "image": {"full": "3048.png"},
            "inStore": True,
        },
        "7001": {
            "name": "Forgefire Crest",
            "description": "Ornn Masterwork item.",
            "gold": {"purchasable": True, "total": 3000},
            "maps": {"11": True},
            "image": {"full": "7001.png"},
            "requiredAlly": "Ornn",
            "inStore": True,
        },
        "3340": {
            "name": "Stealth Ward",
            "description": "Trinket item with 0 gold.",
            "gold": {"purchasable": True, "total": 0},
            "maps": {"11": True},
            "image": {"full": "3340.png"},
            "inStore": True,
        },
        "9999": {
            "name": "Hidden Item",
            "description": "Item hidden from store.",
            "gold": {"purchasable": True, "total": 1000},
            "maps": {"11": True},
            "image": {"full": "9999.png"},
            "inStore": False,
        },
        "8888": {
            "name": "Dev Item",
            "description": "Developer item hidden from all.",
            "gold": {"purchasable": True, "total": 1000},
            "maps": {"11": True},
            "image": {"full": "8888.png"},
            "hideFromAll": True,
        },
        "3901": {
            "name": "Fire at Will",
            "description": "Gangplank cannon upgrade.",
            "gold": {"purchasable": True, "total": 500},
            "maps": {"11": True},
            "image": {"full": "3901.png"},
            "requiredChampion": "Gangplank",
        },
    }


@pytest.mark.anyio
async def test_fetch_items_filtering(mock_item_json_data):
    client = RiotDataDragonClient()
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"data": mock_item_json_data}
    mock_resp.raise_for_status.return_value = None

    with patch("httpx.AsyncClient.get", new=AsyncMock(return_value=mock_resp)):
        items = await client.fetch_items("15.4.1")

    items_by_id = {item.id: item for item in items}

    # 1. Valid Summoner's Rift item is included
    assert 3071 in items_by_id
    assert items_by_id[3071].name == "Black Cleaver"
    assert items_by_id[3071].ability_haste == 20.0

    # 2. ARAM exclusive is excluded
    assert 2051 not in items_by_id

    # 3. Removed legacy item is excluded
    assert 3128 not in items_by_id

    # 4. Transformed Tear items in whitelist are included
    assert 3042 in items_by_id  # Muramana
    assert items_by_id[3042].ability_haste == 15.0
    assert 3040 in items_by_id  # Seraph's Embrace
    assert items_by_id[3040].ability_haste == 25.0
    assert 3048 in items_by_id  # Fimbulwinter
    assert items_by_id[3048].ability_haste == 15.0

    # 5. Ornn Masterwork item is excluded
    assert 7001 not in items_by_id

    # 6. Zero gold trinket is excluded
    assert 3340 not in items_by_id

    # 7. Hidden items are excluded
    assert 9999 not in items_by_id
    assert 8888 not in items_by_id

    # 8. Champion specific item is excluded
    assert 3901 not in items_by_id

    # Total included: 4 items (Black Cleaver, Muramana, Seraph's Embrace, Fimbulwinter)
    assert len(items) == 4
