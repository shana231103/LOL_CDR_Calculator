# Architecture Overview

## System Architecture

```
[ Frontend: Vue 3 + Vite + TailwindCSS ]
                     │  HTTP / JSON
                     ▼
[ Backend API: FastAPI (Python 3) ]
     ├── Data Sync Service (Data Dragon / CommunityDragon)
     ├── Cooldown Calculation Engine
     └── PostgreSQL Database (SQLAlchemy / Alembic)
```

## Layers
1. **Frontend Layer (`frontend/`)**:
   - Single-page application built with Vue 3 and TailwindCSS.
   - Interactive UI: Champion picker, skill rank adjusters (-/+), item slot manager (max 6), rune selector (haste runes & stacks), summoner spell picker.
   - Displays real-time / debounced calculation results received from backend.

2. **Backend Layer (`backend/`)**:
   - FastAPI framework exposing clean REST APIs:
     - `GET /api/champions`, `GET /api/champions/{id}`
     - `GET /api/items?search=`
     - `GET /api/runes`
     - `GET /api/summoner-spells`
     - `POST /api/calculate`
   - **Data Sync Module**: Fetches, validates, and normalizes patch data from Data Dragon / CommunityDragon into PostgreSQL.
   - **Cooldown Engine**: Core domain logic implementing `Final Cooldown = Base Cooldown * 100 / (100 + Haste)` with proper type segregation (General, Ultimate, Basic, Summoner).

3. **Storage Layer**:
   - PostgreSQL storing current patch champions, abilities, items, runes, and summoner spells.
