# Known Problems & Edge Cases

1. **Rune Data Extraction from Riot Data Dragon**:
   - Data Dragon does not always provide clean, machine-readable structured Ability Haste numbers for runes (e.g. Ultimate Hunter stack formulas are embedded in HTML descriptions).
   - *Mitigation*: Use CommunityDragon or a curated fallback metadata mapping for runes affecting cooldowns.

2. **Item Ability Haste Attributes**:
   - Item stats in Data Dragon often place Haste under `FlatSpellBlockMod` in older formats or custom stats.
   - *Mitigation*: Data sync normalizer must parse both structured stats and description tooltips to accurately extract `Ability Haste`.

3. **Multi-charge Skills and Dynamic Cooldowns**:
   - Abilities like Teemo R, Corki R, or Amumu Q charge systems.
   - *Decision*: Only calculate recharge time of a single charge. Ignore special scale factors (e.g. Yasuo Q CDR via Attack Speed).

4. **Data Dragon Obsolete, Multi-mode, and Duplicate Items**:
   - Riot retains deprecated items (`purchasable: false`) for historical matches, includes non-SR items (ARAM Map 12, Arena Map 30), and exposes Ornn upgrades duplicate with base items.
   - *Mitigation*: Implemented multi-condition filtering in `RiotDataDragonClient.fetch_items`: gating on Map 11, requiring `purchasable` with Tear-transformed whitelist (`Muramana`, `Seraph's Embrace`, `Fimbulwinter`), rejecting `requiredAlly == "Ornn"`, rejecting zero-gold trinkets, and calling `item_repo.delete_all()` prior to upserting in `SyncPatchDataUseCase`.

5. **Specialized and Passive Ability Haste on Items**:
   - Items like Malignance (+20 Ultimate Haste), Experimental Hexplate (+30 Ultimate Haste), Fiendhunter Bolts (+30 Ultimate Haste), Spear of Shojin (+25 Basic Ability Haste), and Ionian Boots of Lucidity (+10 Summoner Spell Haste) specify haste within passive descriptions or special attributes rather than base ability haste.
   - Data Dragon Tooltip Inconsistency: Riot Data Dragon completely omits the `Cryocombustion: Gain 15 ultimate haste` text from the description of Zeke's Convergence (Item ID `3050`).
   - *Mitigation*: Implemented a multi-regex parser in `RiotDataDragonClient` with lookbehinds `(?<!Ultimate\s)(?<!Basic\s)` to prevent double-counting between base stats and passives, coupled with a curated override overlay in `item_modifiers.json` to inject missing Data Dragon passive haste attributes.


