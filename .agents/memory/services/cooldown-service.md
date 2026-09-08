# Service Memory: Cooldown Calculation Service

## Domain Service: `CooldownCalculator`
- **File**: `backend/app/domain/services/cooldown_calculator.py`
- **Type**: Pure Algebraic Domain Service (Stateless)
- **Formula**: `Final Cooldown = Base Cooldown * 100 / (100 + Haste)`
- **Haste Domain Segregation**:
  - Q, W, E (Basic Abilities): `Haste = General Ability Haste + Basic Ability Haste`
  - R (Ultimate Ability): `Haste = General Ability Haste + Ultimate Haste`
  - Summoner Spells: `Haste = Summoner Spell Haste`
- **Reduction Percentage**: `CDR % = (1 - Final / Base) * 100`

## Application Use Case: `CalculateCooldownUseCase`
- **File**: `backend/app/application/use_cases/calculate_cooldown.py`
- **Dependencies**: `IChampionRepository`, `IItemRepository`, `IRuneRepository`, `ISpellRepository`
- **Responsibilities**:
  1. Resolves champion, items, runes, and spells from repositories.
  2. Constructs `Build` Aggregate Root and verifies domain invariants.
  3. Executes `CooldownCalculator.calculate_build(build)`.
  4. Returns `CalculationResultDTO` (including `basic_haste`).
