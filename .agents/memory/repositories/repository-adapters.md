# Repository Memory: SQL Repository Adapters

## Domain Ports (`backend/app/domain/repositories/`)
- `IChampionRepository`: `get_all()`, `get_by_id(id)`, `upsert_many(champions)`
- `IItemRepository`: `get_all(search)`, `get_by_ids(ids)`, `upsert_many(items)`, `delete_all()`
- `IRuneRepository`: `get_haste_runes()`, `get_by_ids(ids)`, `upsert_many(runes)`
- `ISpellRepository`: `get_all()`, `get_by_ids(ids)`, `upsert_many(spells)`
- `IPatchRepository`: `get_active_patch()`, `set_active_patch(version)`

## Infrastructure Adapters (`backend/app/infrastructure/repositories/`)
- `SqlChampionRepository`: Translates between `ChampionORM` / `AbilityORM` and Domain entities.
- `SqlItemRepository`: Translates between `ItemORM` (persisting `ability_haste`, `ultimate_haste`, `basic_haste`, `summoner_haste`, and `gold_total`) and Domain entity; implements `delete_all()` for atomic patch sync cleanup.
- `SqlRuneRepository`: Translates between `RuneORM` and Domain entity.
- `SqlSpellRepository`: Translates between `SpellORM` and Domain entity.
- `SqlPatchRepository`: Manages single-row `active_patch` version in database.
