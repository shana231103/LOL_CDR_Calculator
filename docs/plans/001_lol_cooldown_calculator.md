<!-- File path: docs/plans/001_lol_cooldown_calculator.md -->

# Implementation Plan — League of Legends Cooldown Calculator (Phase 1)

## 1. Overview
- **Feature Name**: League of Legends Cooldown Calculator Core
- **Business Objective**: Provide League of Legends players and theorycrafters with a fast, accurate, and lightweight web-based cooldown calculator for the current active game patch.
- **Technical Objective**: Establish a modern, decoupled web architecture consisting of a FastAPI backend, PostgreSQL database, Riot Data Dragon / CommunityDragon automated patch data synchronization pipeline, and a responsive Vue 3 + TailwindCSS frontend.
- **Expected Outcome**: A functional web application where users can select any champion from the current patch, independently adjust ability ranks (Q, W, E, R), select items (up to 6), select relevant runes (with stack support like Ultimate Hunter), select summoner spells, and receive accurate, rounded cooldown metrics calculated by the authoritative backend engine.

---

## 2. Memory Consultation Summary
- **Memory Confidence**: High (Initialized baseline in `.agents/memory/`)
- **Memory Documents Read**:
  - [project-summary.md](file:///c:/Users/LAPTOP/OneDrive/Tài%20liệu/GitHub/cdr_calculate_lol/.agents/memory/project-summary.md)
  - [overview.md](file:///c:/Users/LAPTOP/OneDrive/Tài%20liệu/GitHub/cdr_calculate_lol/.agents/memory/architecture/overview.md)
  - [architectural-decisions.md](file:///c:/Users/LAPTOP/OneDrive/Tài%20liệu/GitHub/cdr_calculate_lol/.agents/memory/lessons/architectural-decisions.md)
  - [known-problems.md](file:///c:/Users/LAPTOP/OneDrive/Tài%20liệu/GitHub/cdr_calculate_lol/.agents/memory/lessons/known-problems.md)
  - [file-map.json](file:///c:/Users/LAPTOP/OneDrive/Tài%20liệu/GitHub/cdr_calculate_lol/.agents/memory/indexes/file-map.json)
- **RAG Query Used**: `LoL cooldown calculator architecture, data dragon sync, haste calculation engine, items and runes model`
- **RAG Results Summary**: Greenfield project structure. Identified need for decoupled frontend/backend, authoritative backend calculation engine, automated patch synchronization mechanism, and strict domain separation between Haste types.
- **Additional Source Files Inspected**:
  - [001_lol_cooldown_calculator-planning-prompt.md](file:///c:/Users/LAPTOP/OneDrive/Tài%20liệu/GitHub/cdr_calculate_lol/docs/plans/prompts/001_lol_cooldown_calculator-planning-prompt.md)
  - [league_of_legends_cooldown_calculator_prompt_v2.md](file:///c:/Users/LAPTOP/OneDrive/Tài%20liệu/GitHub/cdr_calculate_lol/docs/league_of_legends_cooldown_calculator_prompt_v2.md)
- **Key Architectural Findings**:
  - Single-patch focus: only active patch data is maintained in PostgreSQL; patch selector or historical data is explicitly out of scope.
  - Calculation logic must reside centrally on the backend (`POST /api/calculate`), while the frontend maintains the user selection state and renders computed responses.
  - Multi-charge abilities are simplified to single-charge recharge times.
  - Special scaling passives (e.g. Sona Accelerando) and unique stat-scaling CDRs (e.g. Yasuo/Yone Q) are explicitly excluded from this version.

---

## 3. Current Architecture
- **Current Modules**:
  - `backend/`: Greenfield directory (currently empty).
  - `frontend/`: Greenfield directory (currently empty).
  - `docs/`: Product requirements and planning prompts.
- **Current Responsibilities**: Repository is in inception stage; no business logic or runtime services exist yet.
- **Existing Limitations**: No build configuration, no database setup, no API routes, and no UI components.
- **Opportunities for Reuse**: Standard modern tooling patterns (FastAPI + Pydantic v2 + SQLAlchemy for Python, Vite + Vue 3 Composition API + Pinia + TailwindCSS for Frontend).

---

## 4. Scope

### In Scope
1. **Patch Data Ingestion & Synchronization**:
   - Query Riot Data Dragon API to detect latest patch version.
   - Fetch, parse, normalize, and store champions, abilities (Q/W/E/R max rank, base cooldown per rank), items (ability haste stats), runes (haste attributes, stack rules), and summoner spells.
   - Supplement with CommunityDragon or curated metadata for runes with complex stack mechanics (e.g. Ultimate Hunter).
2. **PostgreSQL Relational Schema**:
   - Entities for Champions, Abilities, Items, Runes, Summoner Spells, and Patch Metadata.
3. **Authoritative Calculation Engine**:
   - Segregation of Haste types: General Ability Haste, Ultimate Haste, Basic Ability Haste, Summoner Spell Haste.
   - Standard League cooldown formula: `Final Cooldown = Base Cooldown * 100 / (100 + Applicable Haste)`.
   - Single-charge calculation for recharge-based skills.
   - Preserved internal numeric precision with standardized 2-decimal presentation rounding (e.g. `6.67s`).
4. **REST API (FastAPI)**:
   - `GET /api/champions` & `GET /api/champions/{id}`
   - `GET /api/items?search=`
   - `GET /api/runes`
   - `GET /api/summoner-spells`
   - `POST /api/calculate`
   - Data sync trigger/status endpoints.
5. **Interactive Frontend (Vue 3 + TailwindCSS)**:
   - Champion selection grid with instant search/filter.
   - Ability panels with independent `[-] Rank [+]` controls bounded by skill max ranks.
   - 6-slot Item inventory with item search, selection, removal, and duplicate restrictions.
   - Rune selection section filtering runes that grant Haste, with stack input sliders/counters where applicable.
   - 2-slot Summoner Spell picker.
   - Real-time / debounced calculation summary card showing base cooldowns, applied haste breakdown, and final cooldowns.

### Out of Scope
- Champion level selector (1–18) and skill point allocation progression rules.
- Historical patch storage or patch comparison.
- Full combat simulation, DPS calculation, mana/energy simulation, damage numbers, or item active damage effects.
- Complex champion passives that alter cooldowns conditionally (e.g. Sona Accelerando stacks, Katarina reset on kill, Ezreal Q cooldown refund on hit).
- Special stat-scaling cooldowns (e.g. Yasuo/Yone Q scaling with Attack Speed).
- User authentication, cloud accounts, or saving builds to user profiles.

### Assumptions
1. Local development uses a local PostgreSQL instance running natively on the host (e.g. `localhost:5432`). Docker containerization is deferred to a future phase.
2. Data Dragon endpoints remain reachable; network timeouts will fall back to existing database contents.
3. For runes where Data Dragon omits structured numerical haste attributes, a curated configuration mapping will supply the haste type, base value, and per-stack increments.
4. Frontend communicates with backend via a standard base URL (configurable via environment variable `VITE_API_URL`).

---

## 5. Proposed Solution
The project will be structured as a two-tier monorepo:

1. **Backend Service (`backend/`)**:
   - **Framework**: FastAPI running under Uvicorn.
   - **ORM & Migrations**: SQLAlchemy 2.0 (async or sync) with Alembic migrations.
   - **Data Sync Worker / Service**:
     - Fetches `https://ddragon.leagueoflegends.com/api/versions.json` to identify active patch.
     - Downloads champion full detail, item catalog, and rune trees.
     - Normalizes cooldown arrays into structured database rows.
   - **Cooldown Domain Engine**:
     - Pure functional calculation module taking validated request payloads and returning exact base, haste breakdown, and final values.
     - Fully unit-testable without database dependencies.

2. **Frontend Client (`frontend/`)**:
   - **Framework**: Vue 3 (Vite, `<script setup>` Composition API).
   - **State Management**: Pinia store managing the active build state (selected champion, skill ranks, item slots, selected runes with stacks, summoner spells).
   - **Styling**: TailwindCSS with modern dark-mode gaming aesthetics (League-inspired hextech blues, gold accents, glassmorphic cards).
   - **API Client**: Axios/Fetch with debounced trigger to `POST /api/calculate` whenever user selections mutate.

---

## 6. Architecture Impact
- **Affected Modules**:
  - `backend/app/core/`: Configuration, database session, logging.
  - `backend/app/models/`: SQLAlchemy database entities.
  - `backend/app/schemas/`: Pydantic request/response schemas.
  - `backend/app/services/`: Data sync service, Cooldown calculation engine.
  - `backend/app/api/`: FastAPI route handlers.
  - `frontend/src/components/`: Champion picker, Skill rank controls, Item slots, Rune selectors, Summary view.
  - `frontend/src/stores/`: Pinia build store.
  - `frontend/src/services/`: API client service.
- **Affected Repositories / Storage**:
  - PostgreSQL database containing `champions`, `abilities`, `items`, `runes`, `summoner_spells`, and `patch_sync_history`.
- **Deployment Impact**:
  - Local process execution: PostgreSQL service runs locally on the host machine, FastAPI server runs via `uvicorn app.main:app --reload`, and Vue 3 frontend runs via `npm run dev` (Vite dev server). Docker containerization is deferred.

---

## 7. File Impact Analysis

### Create
1. **Infrastructure & Environment**:
   - `.env.example`: Template for environment variables (`DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/cdr_lol`, `DATA_DRAGON_URL`, `PORT`).
2. **Backend Core & Database**:
   - `backend/pyproject.toml` or `backend/requirements.txt`: Python package dependencies.
   - `backend/app/main.py`: FastAPI application entrypoint and middleware.
   - `backend/app/core/config.py`: Environment settings via Pydantic Settings.
   - `backend/app/core/database.py`: SQLAlchemy engine and session factory.
   - `backend/app/models/champion.py`: Champion and Ability SQL entities.
   - `backend/app/models/item.py`: Item SQL entity with haste attributes.
   - `backend/app/models/rune.py`: Rune SQL entity with haste type, base, and stack metadata.
   - `backend/app/models/spell.py`: Summoner spell SQL entity.
   - `backend/app/models/sync_meta.py`: Patch version tracker entity.
   - `backend/alembic.ini` & `backend/alembic/`: Database migration environment.
3. **Backend Business Logic & API**:
   - `backend/app/services/data_sync.py`: Riot Data Dragon / CommunityDragon ingestion logic.
   - `backend/app/services/cooldown_engine.py`: Cooldown calculation logic with haste segregation.
   - `backend/app/schemas/calculate.py`: Pydantic input/output schemas for `/api/calculate`.
   - `backend/app/schemas/champion.py`, `item.py`, `rune.py`, `spell.py`: DTO schemas.
   - `backend/app/api/routes.py`: API route registrations.
4. **Frontend Core & State**:
   - `frontend/package.json`: Vue 3, Vite, TailwindCSS, Pinia, Axios dependencies.
   - `frontend/vite.config.js`: Vite build configuration.
   - `frontend/tailwind.config.js` & `frontend/src/assets/main.css`: Styling rules and theme colors.
   - `frontend/src/App.vue`: Main layout container.
   - `frontend/src/stores/calculatorStore.js`: Pinia state management for user selections.
   - `frontend/src/services/api.js`: HTTP client talking to FastAPI backend.
5. **Frontend UI Components**:
   - `frontend/src/components/ChampionSelect.vue`: Champion grid with modal / search.
   - `frontend/src/components/AbilityPanel.vue`: Skill display (Q/W/E/R) with `[-] Rank [+]` buttons.
   - `frontend/src/components/ItemSelector.vue`: 6 inventory item slots with search popover.
   - `frontend/src/components/RuneSelector.vue`: Rune selection with stack steppers for stacking runes.
   - `frontend/src/components/SummonerSpellSelect.vue`: 2 summoner spell slots.
   - `frontend/src/components/CooldownDisplay.vue`: Results breakdown table and haste summary card.

### Modify
- None (Greenfield project).

### Reuse
- Official Riot Data Dragon image CDN assets (e.g. `https://ddragon.leagueoflegends.com/cdn/{patch}/img/...`) to avoid storing massive image binary blobs in PostgreSQL.

---

## 8. Implementation Phases

### Phase 1: Environment & Project Scaffolding
- **Objective**: Establish development environment, dependency declarations, and local database connection configuration.
- **Deliverables**:
  - `.env.example` setup with local PostgreSQL configuration instructions (`DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/cdr_lol`).
  - `backend/requirements.txt` with FastAPI, SQLAlchemy, Alembic, asyncpg/psycopg2-binary, Pydantic, httpx, uvicorn.
  - `frontend/` initialized with Vite, Vue 3, TailwindCSS, and Pinia.
- **Validation**: Backend starts cleanly; Frontend dev server renders placeholder; Local PostgreSQL accepts connections.
- **Dependencies**: None.

### Phase 2: Database Schema & Entity Models
- **Objective**: Model the database tables to hold current patch champions, skills, items, runes, and spells.
- **Deliverables**:
  - SQLAlchemy models for all entities with appropriate indexing on `champion_id`, `item_id`, `rune_id`.
  - Initial Alembic migration script.
- **Validation**: Migrations run successfully against PostgreSQL; tables created with expected constraints.
- **Dependencies**: Phase 1.

### Phase 3: Data Dragon & Rune Metadata Ingestion Pipeline
- **Objective**: Automate data ingestion from Riot Data Dragon and CommunityDragon to populate PostgreSQL with active patch data.
- **Deliverables**:
  - Data ingestion service capable of:
    - Checking latest version from `versions.json`.
    - Fetching `championFull.json`, `item.json`, `runesReforged.json`, `summoner.json`.
    - Extracting ability cooldowns per rank (e.g. `[10, 9, 8, 7, 6]`).
    - Extracting item ability haste.
    - Applying curated stack rules for runes like Ultimate Hunter.
    - Upserting current patch records into database.
  - CLI command or endpoint to trigger sync.
- **Validation**: Script populates database with ~168+ champions, items with Haste, and cooldown-affecting runes.
- **Dependencies**: Phase 2.

### Phase 4: Cooldown Calculation Engine & API Endpoints
- **Objective**: Build the core calculation engine and FastAPI routes.
- **Deliverables**:
  - `cooldown_engine.py`:
    - Aggregates General Ability Haste, Ultimate Haste, Basic Ability Haste, Summoner Spell Haste.
    - Calculates `Final Cooldown = Base Cooldown * 100 / (100 + Applicable Haste)`.
    - Enforces max rank boundaries and single-charge recharge handling.
    - Returns exact float and 2-decimal rounded presentation values.
  - REST endpoints (`/api/champions`, `/api/items`, `/api/runes`, `/api/summoner-spells`, `/api/calculate`).
  - Request validation and HTTP 422/400 error handling.
- **Validation**: Unit tests verifying known champion calculations (e.g. Ahri Q/W/E/R cooldowns under varied Haste amounts).
- **Dependencies**: Phase 3.

### Phase 5: Frontend UI Development
- **Objective**: Create the interactive, responsive user interface in Vue 3.
- **Deliverables**:
  - Pinia store managing build state (champion, ranks, items, runes, summoner spells).
  - Champion selection modal with quick search and icon display.
  - Ability list showing Q/W/E/R with max rank indicators and `[-]` `[+]` controls.
  - Item selector with 6 slots, name search, item icons, and ability haste tooltips.
  - Rune section focusing on haste runes with stack sliders.
  - Summoner spell selectors (2 slots).
  - Real-time results panel displaying Base Cooldown, Total Applied Haste, and Final Cooldown.
- **Validation**: Manual UI walkthrough in browser; smooth interaction without UI lag or layout glitches.
- **Dependencies**: Phase 4.

### Phase 6: Integration, Polish & End-to-End Verification
- **Objective**: Connect frontend with backend, implement loading/error states, and verify calculations against live patch values.
- **Deliverables**:
  - Debounced API requests from frontend to `/api/calculate`.
  - Loading skeleton states and network failure notifications.
  - Visual refinements: Hextech theme, dark mode styling, mobile responsive layout.
- **Validation**: End-to-end user flow: select champion -> change ranks -> add 3 items -> add Ultimate Hunter -> check R cooldown matches expected formula.
- **Dependencies**: Phase 5.

---

## 9. Testing Strategy
- **Unit Testing (Backend)**:
  - Calculation formula verification: Test various base cooldowns (e.g. 10s, 100s) with 0, 25, 50, 100 Haste.
  - Haste segregation tests: Confirm Ultimate Haste only modifies Ultimate cooldown and leaves Q/W/E unaffected.
  - Stacking rune tests: Verify Ultimate Hunter at 0, 1, 3, and 5 stacks computes exact incremental Ultimate Haste.
  - Boundary tests: Rank adjustments outside `1 <= rank <= max_rank` rejected with validation error.
- **Integration Testing (Backend)**:
  - API endpoint tests using `pytest` and `httpx.AsyncClient`.
  - Data sync service parser test against mock Data Dragon JSON fixture.
- **Frontend Component & Store Testing**:
  - Pinia store state transitions (adding/removing items, bumping skill rank).
  - Item limit enforcement (cannot add 7th item; duplicate check).
- **Manual End-to-End Validation**:
  - Verify against live League client stats for identical champion + items + runes combinations.

---

## 10. Risks & Mitigations
| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **Data Dragon Rune format lacks explicit haste numbers** | High | High | Supplement Data Dragon with CommunityDragon and a curated JSON metadata overlay specifically defining Haste type and per-stack values for runes affecting cooldowns. |
| **Data Dragon CDN rate limiting or downtime** | Medium | Low | Cache ingested patch data permanently in PostgreSQL; only query Data Dragon during sync routines. |
| **Floating point precision drift in cooldown calculation** | Low | Medium | Keep raw float calculations with high precision throughout the engine pipeline; perform `round(val, 2)` only at schema serialization/display. |
| **Skill with multiple charges or unique CDR mechanics** | Medium | Medium | Explicitly adhere to Section 9 & 10 of requirements: compute only single-charge cooldown and ignore special stat scaling (e.g. Yasuo Q). |

---

## 11. Acceptance Criteria
- [ ] User can search and select any Champion from the active patch.
- [ ] Q, W, E, R abilities render with icons, names, and current rank.
- [ ] User can increment and decrement skill ranks independently within `[1, max_rank]`.
- [ ] User can search, add, and remove items up to 6 slots.
- [ ] User can select Haste-related runes and configure stack counts where applicable.
- [ ] User can select 2 Summoner Spells.
- [ ] Backend calculates correct cooldown values using `Base * 100 / (100 + Haste)`.
- [ ] Ultimate Haste affects only R; General Ability Haste affects basic skills and R.
- [ ] Calculation results display Base Cooldown, Applicable Haste, and Final Cooldown rounded to 2 decimals.
- [ ] Backend sync mechanism successfully updates data when a new patch is detected.
- [ ] No game simulation, level curves, or combat mechanics are included.

---

## 12. Future Extensions (Post-MVP)
- Docker & Container orchestration (Dockerfiles and Docker Compose for production deployment).
- Shareable build URLs (e.g. `?build=ahri_q5w5e5r3_items=...`).
- Historical patch selector and patch-to-patch cooldown diffs.
- Special stat scaling calculations (Attack Speed scaling for Yasuo/Yone Q).
- Champion passive stack tracking (e.g. Sona Accelerando).
