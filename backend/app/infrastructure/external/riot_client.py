# File: backend/app/infrastructure/external/riot_client.py

import json
import re
from pathlib import Path
from typing import Any
import httpx
from app.domain.enums import SkillSlot, HasteType
from app.domain.entities.ability import Ability
from app.domain.entities.champion import Champion
from app.domain.entities.item import Item
from app.domain.entities.rune import Rune
from app.domain.entities.spell import SummonerSpell
from app.application.ports.riot_gateway import IRiotDataDragonGateway

TRANSFORMED_TEAR_ITEM_IDS: set[int] = {3042, 3040, 3048}

BASE_AH_REGEX = re.compile(r"(?<!Ultimate\s)(?<!Basic\s)(\d+)\s*(?:<[^>]+>)*\s*Ability Haste", re.IGNORECASE)
ULT_HASTE_REGEX = re.compile(r"(\d+)\s*(?:<[^>]+>)*\s*Ultimate\s*(?:Ability)?\s*Haste", re.IGNORECASE)
BASIC_HASTE_REGEX = re.compile(r"(\d+)\s*(?:<[^>]+>)*\s*Basic\s*Ability\s*Haste", re.IGNORECASE)
SUMM_HASTE_REGEX = re.compile(r"(\d+)\s*(?:<[^>]+>)*\s*Summoner\s*Spell\s*Haste", re.IGNORECASE)
STATS_BLOCK_REGEX = re.compile(r"<stats>(.*?)</stats>", re.IGNORECASE | re.DOTALL)


class RiotDataDragonClient(IRiotDataDragonGateway):
    """HTTPX adapter for Riot Data Dragon CDN."""

    def __init__(self, cdn_base: str = "https://ddragon.leagueoflegends.com") -> None:
        self._cdn_base = cdn_base.rstrip("/")

    @staticmethod
    def _parse_item_haste(desc: str, item_id: int, overlay: dict[str, Any]) -> tuple[float, float, float, float]:
        ah, ult_h, basic_h, summ_h = 0.0, 0.0, 0.0, 0.0
        stats_m = STATS_BLOCK_REGEX.search(desc)
        if stats_m:
            if m := BASE_AH_REGEX.search(stats_m.group(1)):
                ah = float(m.group(1))
        elif m := BASE_AH_REGEX.search(desc):
            if "gain" not in desc[:m.start()].lower()[-10:]:
                ah = float(m.group(1))
        if m_u := ULT_HASTE_REGEX.search(desc):
            ult_h = float(m_u.group(1))
        if m_b := BASIC_HASTE_REGEX.search(desc):
            basic_h = float(m_b.group(1))
        if m_s := SUMM_HASTE_REGEX.search(desc):
            summ_h = float(m_s.group(1))
        if str(item_id) in overlay:
            mod = overlay[str(item_id)]
            ah = float(mod.get("ability_haste", ah))
            ult_h = float(mod.get("ultimate_haste", ult_h))
            basic_h = float(mod.get("basic_haste", basic_h))
            summ_h = float(mod.get("summoner_haste", summ_h))
        return ah, ult_h, basic_h, summ_h

    async def get_latest_version(self) -> str:
        url = f"{self._cdn_base}/api/versions.json"
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            versions = resp.json()
            return str(versions[0])

    async def fetch_champions(self, version: str) -> list[Champion]:
        url = f"{self._cdn_base}/cdn/{version}/data/en_US/championFull.json"
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json().get("data", {})

        champions: list[Champion] = []
        slots = [SkillSlot.Q, SkillSlot.W, SkillSlot.E, SkillSlot.R]
        for c_id, c_data in data.items():
            img_file = c_data.get("image", {}).get("full", f"{c_id}.png")
            champ = Champion(
                id=c_id,
                key=str(c_data.get("key", "")),
                name=c_data.get("name", c_id),
                title=c_data.get("title", ""),
                image_url=f"{self._cdn_base}/cdn/{version}/img/champion/{img_file}",
            )
            for s_idx, sp in enumerate(c_data.get("spells", [])):
                if s_idx >= 4:
                    break
                slot = slots[s_idx]
                s_img = sp.get("image", {}).get("full", "")
                raw_cds = sp.get("cooldown", [])
                cooldowns = [float(c) for c in raw_cds] if raw_cds else [0.0]
                champ.abilities[slot] = Ability(
                    id=sp.get("id", f"{c_id}_{slot.value}"),
                    slot=slot,
                    name=sp.get("name", f"Spell {slot.value}"),
                    description=sp.get("description", ""),
                    image_url=f"{self._cdn_base}/cdn/{version}/img/spell/{s_img}",
                    max_rank=int(sp.get("maxrank", len(cooldowns))),
                    cooldowns=cooldowns,
                )
            champions.append(champ)
        return champions

    async def fetch_items(self, version: str) -> list[Item]:
        url = f"{self._cdn_base}/cdn/{version}/data/en_US/item.json"
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json().get("data", {})

        overlay_path = Path(__file__).parent / "item_modifiers.json"
        item_overlay: dict[str, Any] = {}
        if overlay_path.exists():
            with open(overlay_path, encoding="utf-8") as f:
                item_overlay = json.load(f)

        items: list[Item] = []
        for i_id, i_data in data.items():
            if not i_id.isdigit():
                continue
            item_id = int(i_id)

            # Gating predicates for Summoner's Rift map 11
            if not i_data.get("maps", {}).get("11", False):
                continue
            gold_data = i_data.get("gold", {})
            if not gold_data.get("purchasable", False) and item_id not in TRANSFORMED_TEAR_ITEM_IDS:
                continue
            if i_data.get("requiredAlly") == "Ornn" or i_data.get("inStore") is False or i_data.get("hideFromAll", False):
                continue
            gold = int(gold_data.get("total", 0))
            if gold <= 0 or i_data.get("requiredChampion"):
                continue

            name = i_data.get("name", "")
            desc = i_data.get("description", "")
            img_file = i_data.get("image", {}).get("full", "")

            ah, ult_h, basic_h, summ_h = self._parse_item_haste(desc, item_id, item_overlay)

            items.append(
                Item(
                    id=item_id,
                    name=name,
                    description=desc,
                    image_url=f"{self._cdn_base}/cdn/{version}/img/item/{img_file}",
                    ability_haste=ah,
                    ultimate_haste=ult_h,
                    basic_haste=basic_h,
                    summoner_haste=summ_h,
                    gold_total=gold,
                )
            )
        return items

    async def fetch_runes(self, version: str) -> list[Rune]:
        overlay_path = Path(__file__).parent / "rune_modifiers.json"
        with open(overlay_path, encoding="utf-8") as f:
            raw_runes = json.load(f)

        runes: list[Rune] = []
        for r in raw_runes:
            icon_sub = r["icon_url"].lstrip("/")
            runes.append(
                Rune(
                    id=r["id"],
                    key=r["key"],
                    name=r["name"],
                    icon_url=f"{self._cdn_base}/cdn/img/{icon_sub}",
                    haste_type=HasteType(r["haste_type"]),
                    base_haste=float(r["base_haste"]),
                    haste_per_stack=float(r["haste_per_stack"]),
                    max_stacks=int(r["max_stacks"]),
                )
            )
        return runes

    async def fetch_spells(self, version: str) -> list[SummonerSpell]:
        url = f"{self._cdn_base}/cdn/{version}/data/en_US/summoner.json"
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json().get("data", {})

        spells: list[SummonerSpell] = []
        for s_id, s_data in data.items():
            img_file = s_data.get("image", {}).get("full", "")
            cooldowns = s_data.get("cooldown", [0.0])
            cd_val = float(cooldowns[0]) if cooldowns else 0.0
            spells.append(
                SummonerSpell(
                    id=s_id,
                    key=str(s_data.get("key", "")),
                    name=s_data.get("name", s_id),
                    description=s_data.get("description", ""),
                    cooldown=cd_val,
                    image_url=f"{self._cdn_base}/cdn/{version}/img/spell/{img_file}",
                )
            )
        return spells
