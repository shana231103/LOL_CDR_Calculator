# Module Memory: Core Architecture (DDD & Clean Architecture)

## Overview
The backend is structured into 4 concentric layers following Domain-Driven Design (DDD) and Clean Architecture:

1. **Domain Layer (`backend/app/domain/`)**:
   - Contains Pure Domain Entities, Value Objects, Domain Services, and Repository Ports.
   - Zero dependencies on frameworks (FastAPI, SQLAlchemy, Pydantic, HTTPX).
   - Invariants are enforced in the `Build` Aggregate Root.

2. **Application Layer (`backend/app/application/`)**:
   - Contains Use Case Interactors (`CalculateCooldownUseCase`, `SyncPatchDataUseCase`, etc.).
   - Input/Output DTOs decouple domain entities from HTTP transport.
   - External Gateway Port `IRiotDataDragonGateway`.

3. **Infrastructure Layer (`backend/app/infrastructure/`)**:
   - Database persistence with async SQLAlchemy 2.0 (`asyncpg` / `aiosqlite`).
   - Repository adapters implementing domain ports.
   - Riot Data Dragon HTTPX client with curated rune modifiers.
   - Dependency Injection container providing FastAPI dependencies.

4. **Presentation Layer (`backend/app/presentation/`)**:
   - REST API endpoints under `/api/v1/`.
   - Pydantic v2 schemas for HTTP validation and serialization.
   - Global exception handling mapping domain exceptions to HTTP 400/404.

5. **Frontend Layer (`frontend/`)**:
   - Vue 3 + TailwindCSS + Pinia single-page application.
   - "Minimalist Grunge & Tactical Cockpit" 3-column zero-scroll layout.
   - 150ms debounced optimistic calculation requests.
