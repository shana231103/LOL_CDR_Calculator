<!-- File path: docs/plans/prompts/002_item_passive_haste_support-planning-prompt.md -->

# Prompt – Generate Implementation Plan: Item Passive & Specialized Haste Support

## Role
You are acting as a Senior Software Architect, Product Engineer, and Technical Planner inside the current IDE workspace.
You have full access to the project workspace and Project Memory.

---

## Source Idea

### 1. Vấn đề thực tế từ người dùng
Ở phần tính toán điểm hồi kỹ năng (Ability Haste) đến từ trang bị, hiện tại có nhiều trang bị có nội tại cộng thêm Ability Haste đặc thù nhưng lại bị bỏ qua hoàn toàn khi người dùng thêm trang bị vào bảng tính:
- **Malignance (ID 3118):** Có 15 Ability Haste cơ bản và nội tại *Scorn* cộng **20 Ultimate Ability Haste**, nhưng chiêu cuối R chỉ nhận 15 Haste (bỏ qua 20 Ultimate Haste).
- **Experimental Hexplate (ID 3073):** Không có Ability Haste cơ bản, nội tại *Hexcharged* cộng **30 Ultimate Ability Haste**, nhưng khi trang bị thì điểm Haste nhận được là 0.
- **Fiendhunter Bolts (ID 2512):** Không có Ability Haste cơ bản, nội tại *Night Vigil* cộng **30 Ultimate Ability Haste**, nhưng khi trang bị thì điểm Haste nhận được là 0.
- **Zeke's Convergence (ID 3050):** Có 10 Ability Haste cơ bản và nội tại *Cryocombustion* cộng **15 Ultimate Haste** (theo wiki chính thức), nhưng chỉ nhận 10 AH cơ bản và bị thiếu 15 Ultimate Haste (do tooltip của Riot Data Dragon bị sót nội tại Cryocombustion).
- **Các trang bị tương tự khác:**
  - **Spear of Shojin (ID 3161):** Nội tại *Dragonforce* cộng **25 Basic Ability Haste** (Haste cho các chiêu Q/W/E).
  - **Ionian Boots of Lucidity (ID 3158):** 10 Ability Haste cơ bản và nội tại cộng **10 Summoner Spell Haste** (Haste cho phép bổ trợ).

### 2. Nguyên nhân kỹ thuật đã xác định qua RAG & Code Analysis
1. **Tầng trích xuất dữ liệu (Data Extraction):**
   - `RiotDataDragonClient.fetch_items` chỉ dùng regex đơn giản `(\d+)\s*(?:<[^>]+>)*\s*Ability Haste` và phương thức `.search()`, chỉ bắt được chỉ số cơ bản đầu tiên trong thẻ `<stats>`, bỏ qua toàn bộ thẻ `<passive>` và các loại Haste đặc thù (`Ultimate Ability Haste`, `Basic Ability Haste`, `Summoner Spell Haste`).
   - Riot Data Dragon bị thiếu text nội tại của một số trang bị (điển hình là nội tại *Cryocombustion: Gain 15 ultimate haste* của Zeke's Convergence). Chưa có cơ chế tệp bù đắp metadata trang bị (`item_modifiers.json`) tương tự như `rune_modifiers.json`.
2. **Tầng thực thể Domain & Database Model:**
   - Thực thể `Item` và `ItemORM` chỉ có một trường `ability_haste: float = 0.0`. Chưa có các trường `ultimate_haste`, `basic_haste`, `summoner_haste`.
3. **Tầng tính toán (Calculation Engine):**
   - Trong `backend/app/domain/entities/build.py`, các hàm `get_ultimate_haste()` và `get_summoner_haste()` chỉ duyệt qua danh sách ngọc (`self.runes`), hoàn toàn bỏ qua trang bị (`self.items`).
   - `CooldownCalculator` chưa tính toán `basic_haste` cho các chiêu thức cơ bản Q, W, E.
4. **Tầng Frontend:**
   - Store `calculatorStore.js` và component `ItemInventory.vue` chỉ hiển thị `item.ability_haste`, chưa phản ánh được các loại haste đặc thù của trang bị (như Ultimate Haste).

---

## Objective

Generate a production-ready implementation planning document from the source idea.

Do not write source code.
Do not create the Technical Blueprint yet.

Save the generated planning document to:

```text
docs/plans/002_item_passive_haste_support.md
```

---

## Workspace Awareness

Before writing the plan:

1. Inspect the current workspace:
   - Python 3.13 / FastAPI backend with Clean Architecture (`domain/`, `application/`, `infrastructure/`, `presentation/`).
   - SQLAlchemy 2.0 Async ORM with SQLite/PostgreSQL.
   - Vue 3 + Vite + TailwindCSS frontend with Pinia store.
   - Project Memory in `.agents/memory/` and existing plans in `docs/plans/`.
2. Reuse existing project conventions (như cách triển khai `rune_modifiers.json` cho ngọc).
3. Prefer extending existing modules over creating duplicates.
4. If something is unclear, make a safe assumption and document it.

---

## Required Planning Document Structure

The planning document must include:

### 1. Overview
* Feature name: **Item Passive & Specialized Haste Support (Phase 002)**
* Purpose
* Problem being solved
* Expected outcome

### 2. Current State Analysis
* Existing related files/modules (`riot_client.py`, `item.py`, `build.py`, `cooldown_calculator.py`, `item_orm.py`, `sql_item_repo.py`, `ItemInventory.vue`, `calculatorStore.js`, etc.)
* Current behavior & code snippets
* Technical gaps
* Constraints

### 3. Scope
* In scope:
  - Mở rộng Data Extraction (regex parser + tệp bù đắp metadata `item_modifiers.json`).
  - Mở rộng Domain Entity `Item` & DB `ItemORM` với các loại haste: `ultimate_haste`, `basic_haste`, `summoner_haste`.
  - Cập nhật logic tính toán `Build` và `CooldownCalculator` cho Q/W/E/R và Summoner Spells.
  - Cập nhật DTOs, API Schemas và Frontend Inventory/Telemetry display.
  - Viết unit tests & integration tests cho việc đồng bộ và tính toán.
* Out of scope:
  - Giữ nguyên triết lý không mô phỏng các nội tại phức tạp thay đổi theo thời gian thực (combat simulator) hoặc tỷ lệ hoàn chiêu theo sát thương/hạ gục (như hoàn chiêu của Axiom Arc).
* Assumptions

### 4. Proposed Solution
Describe the intended approach at a high level across all layers.

### 5. Architecture Impact
Explain:
* Affected layers (Domain, Infrastructure, Application, Presentation, Frontend).
* Affected modules and entities.
* Interfaces required.
* Data flow changes.
* Dependency boundaries.

### 6. File Plan
List files likely to be:
* Created (e.g., `item_modifiers.json`, new test files).
* Modified (`riot_client.py`, `item.py`, `build.py`, `cooldown_calculator.py`, `item_orm.py`, `sql_item_repo.py`, `item_dto.py`, `item_schema.py`, `calculatorStore.js`, `ItemInventory.vue`, `CooldownSummary.vue`, etc.).
* Reused.

### 7. Implementation Phases
Break the work into small steps:
* Phase 1: Item Metadata Overlay & Extraction Normalizer
* Phase 2: Domain Entity & Database Layer Extension
* Phase 3: Calculation Engine Update (Build & CooldownCalculator)
* Phase 4: Application DTOs & API Presentation Layer
* Phase 5: Frontend Inventory & Telemetry UI Update
* Phase 6: Testing & Verification

### 8. Testing Plan
* Unit tests for item parsing and regex extraction.
* Unit tests for domain `Build` and `CooldownCalculator` with Malignance, Hexplate, Fiendhunter Bolts, Zeke's Convergence, Spear of Shojin, Ionian Boots.
* Integration tests for `/api/v1/calculate` endpoint.
* Frontend manual verification.

### 9. Risks & Mitigation
List technical risks (database migration/sync overwrite, Riot tooltip variations, duplicate item IDs) and mitigations.

### 10. Acceptance Criteria
Checklist for completion.

---

## Output Rules

The generated planning document must:
* be Markdown
* be saved under `docs/plans/002_item_passive_haste_support.md`
* start with:
```html
<!-- File path: docs/plans/002_item_passive_haste_support.md -->
```
* not include source code
* not create blueprint
* not modify implementation files
