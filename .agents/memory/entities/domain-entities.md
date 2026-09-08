# Entity Memory: Domain Entities & Value Objects

## Value Objects (`backend/app/domain/value_objects.py`)
- `Cooldown(seconds: float)`: Non-negative floating point duration.
- `AbilityHaste(value: float)`: Non-negative ability haste value.
- `SkillRank(rank: int, max_rank: int)`: Validates `1 <= rank <= max_rank`.
- `PatchVersion(version: str)`: Validates non-empty patch string.

## Aggregate Root: `Build` (`backend/app/domain/entities/build.py`)
- **Properties**: `champion`, `skill_ranks`, `items`, `runes`, `spells`
- **Invariants**:
  - Max 6 items allowed (`ItemLimitError`).
  - Max 2 summoner spells allowed (`SpellLimitError`).
  - Skill ranks must not exceed ability maximum rank (`InvalidRankError`).
- **Haste Aggregation Methods**:
  - `get_total_ability_haste()`: Combines base item ability haste and runes.
  - `get_ultimate_haste()`: Combines item ultimate haste and rune ultimate haste (e.g. Ultimate Hunter).
  - `get_basic_ability_haste()`: Combines item basic ability haste (e.g. Spear of Shojin).
  - `get_summoner_haste()`: Combines item summoner haste (e.g. Ionian Boots) and rune summoner haste.

## Domain Entities
- `Champion`: id, key, name, title, image_url, abilities dict.
- `Ability`: id, slot (Q/W/E/R), name, description, image_url, max_rank, cooldowns list.
- `Item`: id, name, description, image_url, ability_haste, ultimate_haste, basic_haste, summoner_haste, gold_total.
- `Rune`: id, key, name, icon_url, haste_type, base_haste, haste_per_stack, max_stacks.
- `RuneSelection`: rune, stacks (validates stack boundaries).
- `SummonerSpell`: id, key, name, description, cooldown, image_url.
