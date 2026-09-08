# Architectural Decisions (ADRs)

## ADR-001: Current Patch Only
- **Context**: LoL patch cycles are bi-weekly and storing historical versions drastically increases data complexity.
- **Decision**: Only retain current patch data in the database. When a new patch is detected, backend sync updates the active dataset.

## ADR-002: Authoritative Backend Calculation Engine
- **Context**: Calculation logic could be duplicated on frontend and backend, risking drift.
- **Decision**: Calculation logic lives definitively in the backend (`/api/calculate`), ensuring consistent rules, validations, and precision handling.

## ADR-003: Strict Separation of Haste Domains
- **Context**: LoL has Ability Haste, Ultimate Haste, Basic Ability Haste, and Summoner Spell Haste. Conflating them creates bugs.
- **Decision**: Data models explicitly categorize Haste into typed buckets and apply them strictly according to cooldown targets.

## ADR-004: Build as Domain Aggregate Root
- **Context**: Ability ranks, items, runes, and summoner spells must satisfy gameplay invariants simultaneously.
- **Decision**: Encapsulated within `Build` aggregate root to ensure validation occurs within the domain core before calculation.

## ADR-005: Clean Architecture Repository Ports and ORM Adapters
- **Context**: Directly coupling ORM models to calculation services prevents isolated unit testing and leaks persistence details.
- **Decision**: Repository interfaces defined in `domain/repositories/` and implemented via async SQLAlchemy in `infrastructure/repositories/`.

## ADR-006: Dual-Driver Async Storage Engine
- **Context**: Production deployment requires PostgreSQL (`asyncpg`), while local development and rapid automated tests benefit from zero-configuration async SQLite (`aiosqlite`).
- **Decision**: Configured `DATABASE_URL` to dynamically support both drivers via SQLAlchemy 2.0 without changing repository code.

## ADR-007: Strict Summoner's Rift Gateway Filtering with Tear Whitelist
- **Context**: Riot Data Dragon preserves removed legacy items (`purchasable: false`) and multi-mode variants (ARAM, Arena) with duplicated names/icons. Transformed items from Tear of the Goddess (Muramana, Seraph's Embrace, Fimbulwinter) are flagged `purchasable: false` even though players need them for Ability Haste calculations.
- **Decision**: Filter items at `RiotDataDragonClient.fetch_items()` by: Map 11 (`maps["11"] is True`), purchasable or whitelisted in `TRANSFORMED_TEAR_ITEM_IDS = {3042, 3040, 3048}`, excluding Ornn masterwork items (`requiredAlly == 'Ornn'`), excluding hidden items (`inStore is False` or `hideFromAll is True`), excluding 0-gold trinkets (`gold.total <= 0`), and excluding champion-specific items (`requiredChampion`).

## ADR-008: Atomic Clean Sync on Patch Update
- **Context**: `IItemRepository.upsert_many()` only updates incoming items. If dirty, legacy, or multi-mode items were previously saved in the database, a standard upsert leaves them lingering as orphans.
- **Decision**: Added `delete_all()` to `IItemRepository` and `SqlItemRepository`. `SyncPatchDataUseCase` executes `await item_repo.delete_all()` before `upsert_many(items)` within the same transaction to guarantee a 100% clean item table matching the active patch.

## ADR-009: Hybrid Multi-Regex Parser and Curated Modifier Overlay for Item Haste
- **Context**: Several critical items offer specialized haste (e.g. Ultimate Haste from Malignance, Fiendhunter Bolts, Hexplate, Zeke's Convergence; Basic Ability Haste from Spear of Shojin; Summoner Spell Haste from Ionian Boots). DDragon embeds these values in HTML passive tags, and in the case of Zeke's Convergence (`3050`), omits the Cryocombustion text entirely.
- **Decision**: Implement a two-tiered extraction strategy: (1) Regex parser with negative lookbehinds in `riot_client.py` targeting `<stats>` for base AH and `<passive>` descriptions for specialized haste types; (2) Curated JSON overlay in `backend/app/infrastructure/external/item_modifiers.json` to inject missing Data Dragon metadata (such as Zeke's +15 Ultimate Haste).



