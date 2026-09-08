<!-- File path: docs/plans/002_item_passive_haste_support.md -->

# Implementation Plan: Item Passive & Specialized Haste Support (Phase 002)

## 1. Overview
- **Feature Name**: Item Passive & Specialized Haste Support
- **Business Objective**: Đảm bảo tính toán chính xác điểm hồi chiêu (CDR) và điểm hồi kỹ năng (Ability Haste) cho mọi tướng và chiêu thức khi người chơi lên các trang bị có nội tại cộng thêm Haste đặc thù (chiêu cuối, chiêu thường, phép bổ trợ).
- **Technical Objective**: 
  - Mở rộng tầng đồng bộ dữ liệu (Data Extraction) để bóc tách các dạng Haste đặc thù (`Ultimate Ability Haste`, `Basic Ability Haste`, `Summoner Spell Haste`) từ cả phần thông số cơ bản và thẻ `<passive>` của Data Dragon.
  - Thiết lập cơ chế bù đắp metadata trang bị (`item_modifiers.json`) để bổ sung các nội tại bị Riot Data Dragon bỏ sót (như nội tại *Cryocombustion* của Zeke's Convergence).
  - Nâng cấp Domain Entity `Item`, ORM `ItemORM`, DTOs và API schemas để hỗ trợ đầy đủ các trường Haste mới.
  - Cập nhật logic tính toán trong `Build` và `CooldownCalculator` để kết hợp Haste từ cả trang bị và ngọc vào chiêu cuối (R), chiêu thường (Q/W/E) và phép bổ trợ.
  - Cập nhật giao diện Frontend (Pinia store, Item Inventory badge và Cooldown Summary) để hiển thị trực quan và chính xác.
- **Expected Outcome**: Người chơi khi thêm các trang bị như Malignance, Experimental Hexplate, Fiendhunter Bolts, Zeke's Convergence, Spear of Shojin, Ionian Boots of Lucidity sẽ thấy điểm Haste và thời gian hồi chiêu giảm chính xác theo quy tắc của Liên Minh Huyền Thoại.

---

## 2. Memory Consultation Summary
- **Memory Confidence**: High (Dữ liệu Project Memory được cập nhật gần nhất vào 2026-09-08T16:54:00Z).
- **Memory Documents Read**:
  - `project-summary.md`: Khẳng định triết lý hệ thống phân định rõ các loại Haste: General AH, Ultimate Haste, Basic Ability Haste, Summoner Spell Haste.
  - `architecture/overview.md` & `modules/core-architecture.md`: Xác định ranh giới Clean Architecture 4 tầng của Backend và Vue 3 Frontend.
  - `services/cooldown-service.md`: Quy định công thức tính toán Haste độc lập cho từng nhóm kỹ năng (R = General AH + Ult Haste).
  - `entities/domain-entities.md`: Ghi nhận thực thể `Item` hiện tại chỉ có một thuộc tính `ability_haste`.
  - `lessons/known-problems.md`: Mục 1 và Mục 2 chỉ rõ Data Dragon có dữ liệu Haste không sạch và không đầy đủ, yêu cầu phải dùng cơ chế metadata mapping / overlay.
- **RAG Query Used**:
  - `"Ở phần ability haste đến từ trang bị có vấn đề như sau: Có một số trang bị có nội tại cộng thêm ability haste (như Malignance, Fiendhunter Bolts, Experimental Hexplate, Zeke's Convergence) nhưng lại bị bỏ qua khi add trang bị."`
- **RAG Results Summary**:
  - Xác định 4 tầng kỹ thuật bị nghẽn: (1) Regex parser trong `riot_client.py` chỉ bắt text cơ bản đầu tiên; (2) Data Dragon bỏ sót nội tại *Cryocombustion: Gain 15 ultimate haste* của Zeke; (3) Domain & ORM `Item` thiếu trường dữ liệu; (4) `Build.get_ultimate_haste()` và `get_summoner_haste()` chỉ tính cho ngọc mà bỏ qua trang bị.
- **Additional Source Files Inspected**:
  - `backend/app/infrastructure/external/riot_client.py`: Kiểm tra regex trích xuất và cơ chế đồng bộ hiện tại.
  - `backend/app/domain/entities/build.py`: Kiểm tra phương thức tính tổng Haste.
  - `backend/app/domain/services/cooldown_calculator.py`: Kiểm tra áp dụng Haste cho các slot Q, W, E, R.
  - `backend/app/infrastructure/database/models/item_orm.py` & `sql_item_repo.py`: Kiểm tra cấu trúc bảng SQLite và persistence logic.
  - `frontend/src/stores/calculatorStore.js` & `frontend/src/components/ItemInventory.vue`: Kiểm tra luồng dữ liệu và giao diện hiển thị badge item.
- **Key Architectural Findings**:
  - Dự án đã có sẵn enum `HasteType` (`ABILITY_HASTE`, `ULTIMATE_HASTE`, `BASIC_HASTE`, `SUMMONER_HASTE`) trong `backend/app/domain/enums.py`.
  - Dự án đã có tiền lệ triển khai cơ chế metadata overlay thành công với `rune_modifiers.json` trong `backend/app/infrastructure/external/`. Áp dụng cùng mẫu thiết kế này cho trang bị với `item_modifiers.json` sẽ đảm bảo tính nhất quán cao và giải quyết triệt để lỗi thiếu sót từ Riot Data Dragon.

---

## 3. Current Architecture
- **Tầng Infrastructure (`riot_client.py`)**:
  - Hàm `fetch_items` chỉ trích xuất duy nhất một giá trị số `ability_haste` từ mô tả bằng regex đơn vị, không phân tách các loại Haste chuyên biệt.
- **Tầng Domain (`item.py`, `build.py`, `cooldown_calculator.py`)**:
  - `Item` chỉ nắm giữ `ability_haste`.
  - `Build` chỉ lấy `ultimate_haste` và `summoner_haste` từ `self.runes`.
  - `CooldownCalculator` áp dụng `general_ah` cho Q/W/E và `general_ah + ult_haste` cho R. Chưa hỗ trợ `basic_haste` cho Q/W/E.
- **Tầng Database (`item_orm.py`, `sql_item_repo.py`)**:
  - Bảng `items` trong SQLite chỉ lưu trữ cột `ability_haste`.
- **Tầng Presentation & API (`calculate.py`, `items.py`, DTOs, Schemas)**:
  - DTO và Schema trả về của Item chỉ phản ánh `ability_haste`.
- **Tầng Frontend (`calculatorStore.js`, `ItemInventory.vue`)**:
  - Store chỉ tính tổng `item.ability_haste`. Component Inventory chỉ hiển thị badge `+X AH` khi `ability_haste > 0`.
- **Cơ hội tái sử dụng (Reuse Opportunities)**:
  - Tái sử dụng enum `HasteType` đã có sẵn trong domain.
  - Tái sử dụng mô hình metadata overlay JSON tương tự `rune_modifiers.json`.
  - Tái sử dụng cơ chế auto-calculate thông qua debounce trong Pinia store.

---

## 4. Scope

### In Scope
1. **Curated Item Overlay (`item_modifiers.json`)**:
   - Tạo tệp metadata overlay tại `backend/app/infrastructure/external/item_modifiers.json` chứa các chỉ số Haste bổ trợ hoặc sửa lỗi cho các trang bị đặc thù (đặc biệt là 15 Ultimate Haste của Zeke's Convergence ID `3050`).
2. **Nâng cấp Regex & Parser trích xuất dữ liệu (`riot_client.py`)**:
   - Nhận diện `Ultimate Ability Haste` / `ultimate haste` (cộng vào `ultimate_haste`).
   - Nhận diện `Basic Ability Haste` (cộng vào `basic_haste`).
   - Nhận diện `Summoner Spell Haste` (cộng vào `summoner_haste`).
   - Quét qua toàn bộ thẻ `<passive>` thay vì dừng lại ở thẻ `<stats>` đầu tiên.
   - Hợp nhất (merge) dữ liệu parser với `item_modifiers.json`.
3. **Mở rộng Domain Entity & Database Layer**:
   - Thêm các thuộc tính `ultimate_haste: float = 0.0`, `basic_haste: float = 0.0`, `summoner_haste: float = 0.0` vào thực thể `Item`.
   - Cập nhật SQLAlchemy model `ItemORM` và repository `SqlItemRepository` để lưu trữ/truy vấn các cột mới.
4. **Cập nhật Logic tính toán Aggregate & Service**:
   - `Build.get_ultimate_haste()`: Cộng dồn Ultimate Haste từ cả `self.items` và `self.runes`.
   - `Build.get_summoner_haste()`: Cộng dồn Summoner Haste từ cả `self.items` và `self.runes`.
   - `Build.get_basic_ability_haste()`: Tính tổng Basic Haste từ `self.items`.
   - `CooldownCalculator.calculate_build()`:
     - Q, W, E áp dụng: `General Ability Haste + Basic Ability Haste`.
     - R áp dụng: `General Ability Haste + Ultimate Haste`.
     - Phép bổ trợ áp dụng: `Summoner Spell Haste`.
5. **Cập nhật DTO, Schema & Presentation Layer**:
   - `ItemDTO` và `ItemResponseSchema` bổ sung các trường haste mới để trả về cho Frontend.
   - `CalculationResultDTO` trả về chi tiết `basic_haste` (nếu cần hiển thị).
6. **Cập nhật Giao diện Frontend**:
   - `ItemInventory.vue`: Hiển thị rõ ràng các loại haste của trang bị (ví dụ: `+15 Ult AH` hoặc `+10 Summ AH`).
   - `calculatorStore.js`: Cập nhật logic hiển thị tổng Haste hoặc tooltip chi tiết.
7. **Đồng bộ lại dữ liệu & Kiểm thử**:
   - Chạy đồng bộ lại dữ liệu patch để cập nhật dữ liệu items mới vào SQLite database.
   - Bổ sung unit tests và integration tests cho toàn bộ luồng.

### Out of Scope
- Không mô phỏng các nội tại hoàn chiêu theo điều kiện giao tranh thời gian thực (ví dụ: hoàn 10-20% hồi chiêu R của Axiom Arc khi hạ gục mục tiêu).
- Không mô phỏng các nội tại cộng Haste biến thiên theo chỉ số động trong trận (ví dụ: Endless Hunger cộng Haste theo Bonus AD).
- Không thay đổi kiến trúc Clean Architecture hiện hữu.

### Assumptions
- Dữ liệu patch đang sử dụng là phiên bản mới nhất từ Riot Data Dragon CDN.
- Các trang bị mục tiêu gồm: Malignance (`3118`), Experimental Hexplate (`3073`), Fiendhunter Bolts (`2512`), Zeke's Convergence (`3050`), Spear of Shojin (`3161`), Ionian Boots of Lucidity (`3158`).

---

## 5. Proposed Solution
Triển khai giải pháp theo cấu trúc phân tầng Clean Architecture kết hợp mô hình Hybrid Data Enrichment:
1. **Data Enrichment Layer**: Khi nạp dữ liệu từ Riot Data Dragon, hệ thống trước hết trích xuất bằng regex thông minh đa mẫu (multi-pattern matching) trên toàn bộ chuỗi mô tả (cả `<stats>` và `<passive>`). Sau đó, hệ thống tra cứu tệp `item_modifiers.json` để ghi đè hoặc bổ sung các chỉ số mà Riot Data Dragon thiếu sót (như nội tại Cryocombustion của Zeke).
2. **Domain & Persistence Layer**: Thực thể `Item` và bảng `items` mở rộng để lưu trữ đầy đủ 4 loại Haste: `ability_haste`, `ultimate_haste`, `basic_haste`, `summoner_haste`.
3. **Calculation Core**: `Build` tổng hợp Haste theo từng miền trách nhiệm:
   - Tổng Haste cho Q/W/E = $\sum \text{Item.ability\_haste} + \sum \text{Item.basic\_haste} + \sum \text{Rune.ability\_haste}$
   - Tổng Haste cho R = $\sum \text{Item.ability\_haste} + \sum \text{Item.ultimate\_haste} + \sum \text{Rune.ability\_haste} + \sum \text{Rune.ultimate\_haste}$
   - Tổng Haste cho Phép bổ trợ = $\sum \text{Item.summoner\_haste} + \sum \text{Rune.summoner\_haste}$
4. **UI Presentation**: Giao diện cập nhật thẻ Item trong kho đồ để người dùng nhận diện ngay trang bị nào mang Ultimate Haste hoặc Summoner Haste.

---

## 6. Architecture Impact
- **Tầng Domain**:
  - `Item`: Thêm `ultimate_haste`, `basic_haste`, `summoner_haste`.
  - `Build`: Thêm phương thức `get_basic_ability_haste()`, cập nhật `get_ultimate_haste()`, `get_summoner_haste()`.
  - `CooldownCalculator`: Cập nhật logic tính applicable haste cho Q/W/E bao gồm cả Basic Haste.
- **Tầng Infrastructure**:
  - Thêm tệp cấu hình tĩnh `item_modifiers.json`.
  - Mở rộng `RiotDataDragonClient.fetch_items` tích hợp overlay mapping và regex đa mẫu.
  - Cập nhật model SQLAlchemy `ItemORM` thêm 3 cột float mới.
  - Cập nhật `SqlItemRepository` trong phương thức mapping và upsert.
- **Tầng Application**:
  - Cập nhật `ItemDTO`.
  - Cập nhật `CalculateCooldownUseCase` nếu cần điều chỉnh kết quả trả về.
- **Tầng Presentation**:
  - Cập nhật Pydantic schema `ItemResponseSchema`.
- **Tầng Frontend**:
  - Cập nhật component `ItemInventory.vue` và `CooldownSummary.vue` để phản ánh đúng các chỉ số Haste mới.

---

## 7. File Impact Analysis

### Create
1. `backend/app/infrastructure/external/item_modifiers.json`:
   - *Mục đích*: Tệp cấu hình JSON định nghĩa các chỉ số Haste bổ sung/bù đắp cho các trang bị bị Riot Data Dragon bỏ sót hoặc cần chuẩn hóa cố định (như Zeke's Convergence).
   - *Độ phức tạp*: Thấp.
2. `backend/tests/unit/test_item_passive_haste.py`:
   - *Mục đích*: Bộ unit tests kiểm tra khả năng bóc tách Haste từ mô tả và overlay cho Malignance, Hexplate, Fiendhunter, Zeke, Shojin, Ionian Boots.
   - *Độ phức tạp*: Trung bình.

### Modify
1. `backend/app/domain/entities/item.py`:
   - *Mục đích*: Bổ sung các trường `ultimate_haste`, `basic_haste`, `summoner_haste`.
   - *Độ phức tạp*: Thấp.
2. `backend/app/domain/entities/build.py`:
   - *Mục đích*: Tính toán tổng Ultimate Haste, Summoner Haste, Basic Haste bao gồm cả Items.
   - *Độ phức tạp*: Thấp.
3. `backend/app/domain/services/cooldown_calculator.py`:
   - *Mục đích*: Áp dụng Basic Haste cho Q/W/E bên cạnh General AH.
   - *Độ phức tạp*: Thấp.
4. `backend/app/infrastructure/database/models/item_orm.py`:
   - *Mục đích*: Thêm 3 cột `ultimate_haste`, `basic_haste`, `summoner_haste` vào bảng `items`.
   - *Độ phức tạp*: Thấp.
5. `backend/app/infrastructure/repositories/sql_item_repo.py`:
   - *Mục đích*: Cập nhật hàm chuyển đổi `_orm_to_domain` và logic `upsert_many`.
   - *Độ phức tạp*: Thấp.
6. `backend/app/infrastructure/external/riot_client.py`:
   - *Mục đích*: Nâng cấp parser trích xuất Haste từ description và nạp `item_modifiers.json`.
   - *Độ phức tạp*: Trung bình.
7. `backend/app/application/dtos/item_dto.py`:
   - *Mục đích*: Bổ sung 3 trường Haste vào DTO.
   - *Độ phức tạp*: Thấp.
8. `backend/app/presentation/schemas/item_schema.py`:
   - *Mục đích*: Bổ sung 3 trường Haste vào Pydantic Response Schema.
   - *Độ phức tạp*: Thấp.
9. `frontend/src/stores/calculatorStore.js`:
   - *Mục đích*: Hỗ trợ tính toán và theo dõi thông tin Haste đặc thù của item.
   - *Độ phức tạp*: Thấp.
10. `frontend/src/components/ItemInventory.vue`:
    - *Mục đích*: Cập nhật badge hiển thị Haste trên item (phân biệt General AH, Ult AH, Summ AH).
    - *Độ phức tạp*: Trung bình.

### Reuse
- `backend/app/domain/enums.py`: Tái sử dụng `HasteType` và `SkillSlot`.
- `backend/app/application/use_cases/sync_patch_data.py`: Tái sử dụng luồng đồng bộ dữ liệu patch.
- `backend/app/presentation/api/v1/calculate.py`: Tái sử dụng endpoint tính toán hiện tại.

---

## 8. Implementation Phases

### Milestone 1: Metadata Overlay & Parser Enrichment
- **Mục tiêu**: Xây dựng `item_modifiers.json` và nâng cấp regex parser trong `riot_client.py`.
- **Sản phẩm bàn giao**:
  - Tệp `backend/app/infrastructure/external/item_modifiers.json` chuẩn hóa dữ liệu cho các trang bị trọng điểm.
  - Phương thức `RiotDataDragonClient.fetch_items` nhận diện được cả 4 loại Haste và áp dụng overlay metadata.
- **Phương pháp xác thực**: Chạy unit test kiểm tra đầu ra của `fetch_items` với mock dữ liệu Data Dragon.
- **Phụ thuộc**: Không.

### Milestone 2: Domain Entity, DB Model & Repository Extension
- **Mục tiêu**: Cập nhật thực thể `Item`, model `ItemORM`, mapper và repository.
- **Sản phẩm bàn giao**:
  - `Item` entity có 3 thuộc tính mới.
  - `ItemORM` có 3 cột mới trong SQLite.
  - `SqlItemRepository` lưu trữ và truy vấn chính xác các trường này.
- **Phương pháp xác thực**: Thực hiện đồng bộ lại dữ liệu patch qua script/endpoint và truy vấn SQLite kiểm tra các item 3118, 3073, 2512, 3050 có chỉ số chính xác.
- **Phụ thuộc**: Milestone 1.

### Milestone 3: Calculation Engine Update (Build & CooldownCalculator)
- **Mục tiêu**: Cập nhật logic tính toán Haste trong `Build` và `CooldownCalculator`.
- **Sản phẩm bàn giao**:
  - `Build.get_ultimate_haste()` tính cả trang bị.
  - `Build.get_summoner_haste()` tính cả trang bị.
  - `Build.get_basic_ability_haste()` được bổ sung.
  - `CooldownCalculator` tính thời gian hồi cho Q/W/E/R và Spells dựa trên tổng Haste chính xác.
- **Phương pháp xác thực**: Unit tests tính toán Cooldown cho tướng mang Malignance, Hexplate, Zeke, Shojin, Lucidity Boots.
- **Phụ thuộc**: Milestone 2.

### Milestone 4: DTO, API Schema & Presentation Synchronization
- **Mục tiêu**: Đồng bộ dữ liệu mới ra API endpoint `/api/v1/items` và `/api/v1/calculate`.
- **Sản phẩm bàn giao**:
  - `ItemDTO` và `ItemResponseSchema` trả về các trường haste mới.
- **Phương pháp xác thực**: Gọi API HTTP `GET /api/v1/items` và `POST /api/v1/calculate` kiểm tra payload JSON.
- **Phụ thuộc**: Milestone 3.

### Milestone 5: Frontend Inventory & Telemetry UI Enhancement
- **Mục tiêu**: Cập nhật hiển thị giao diện người dùng trên Vue 3.
- **Sản phẩm bàn giao**:
  - `ItemInventory.vue` hiển thị badge trực quan cho các loại Haste khác nhau (ví dụ: badge màu cam cho Ult Haste, màu xanh cho General AH).
  - Modal chọn trang bị hiển thị chi tiết các chỉ số Haste nội tại.
- **Phương pháp xác thực**: Kiểm tra tương tác trên trình duyệt, chọn Malignance / Hexplate / Zeke và kiểm tra bảng Telemetry hiển thị Ult Haste tăng tương ứng.
- **Phụ thuộc**: Milestone 4.

### Milestone 6: Regression Testing & Memory Synchronization
- **Mục tiêu**: Đảm bảo toàn bộ test suites vượt qua và đồng bộ Project Memory.
- **Sản phẩm bàn giao**:
  - Chạy toàn bộ pytest đạt 100% pass.
  - Kiểm tra không phát sinh lỗi hồi quy với các trang bị thông thường.
- **Phương pháp xác thực**: `pytest` toàn diện.
- **Phụ thuộc**: Milestone 5.

---

## 9. Testing Strategy
- **Unit Testing**:
  - Test parser trong `RiotDataDragonClient`: Kiểm tra bóc tách chính xác từ description HTML và overlay của Malignance, Hexplate, Fiendhunter, Zeke's Convergence, Spear of Shojin, Ionian Boots.
  - Test domain `Build`: Kiểm tra tính tổng Haste từng loại khi kết hợp cả Items và Runes.
  - Test `CooldownCalculator`: Kiểm tra tính thời gian hồi chiêu cuối R khi mang Malignance (+15 AH, +20 Ult Haste) đạt đúng 35 Haste cho R và 15 Haste cho Q/W/E.
- **Integration Testing**:
  - Test endpoint `POST /api/v1/calculate` với build chứa 4 trang bị: Malignance, Experimental Hexplate, Fiendhunter Bolts, Zeke's Convergence -> đảm bảo tổng Ultimate Haste trả về đạt đúng 95 (20 + 30 + 30 + 15).
- **Regression Testing**:
  - Chạy lại các tests hiện hữu `test_item_filtering.py` và `test_sync_use_case.py` đảm bảo không bị ảnh hưởng.
- **Manual Validation**:
  - Mở web app trên trình duyệt, trang bị Hexplate và Malignance cho Ahri, kiểm tra thẻ Ult Haste trong Telemetry nhảy số chính xác.

---

## 10. Risks & Mitigation
1. **Rủi ro CSDL SQLite cũ chưa có cột mới**:
   - *Nguy cơ*: Khi thêm thuộc tính vào SQLAlchemy model mà database SQLite đã tồn tại, có thể gặp lỗi `no such column`.
   - *Giải pháp*: Trong quá trình sync patch hoặc khởi động, đảm bảo bảng `items` được cập nhật cột hoặc chạy lại sync patch (xóa và tạo lại bảng sạch).
2. **Rủi ro Riot thay đổi cấu trúc thẻ HTML trong tương lai**:
   - *Nguy cơ*: Riot thay đổi cú pháp thẻ `<passive>` hoặc từ khóa Haste.
   - *Giải pháp*: Regex sử dụng các mẫu linh hoạt không phân biệt hoa thường (`IGNORECASE`) kết hợp tệp `item_modifiers.json` đóng vai trò chốt chặn (safety net) đáng tin cậy.
3. **Rủi ro trùng lặp Haste khi vừa có regex vừa có overlay**:
   - *Nguy cơ*: Trùng lặp cộng 2 lần nếu cả regex và overlay đều khai báo.
   - *Giải pháp*: Định nghĩa rõ cơ chế ưu tiên: Nếu item có trong `item_modifiers.json`, hệ thống sẽ lấy giá trị override có chủ đích hoặc cộng dồn theo quy tắc rõ ràng đã kiểm soát.

---

## 11. Acceptance Criteria
- [ ] Tệp `item_modifiers.json` được tạo với thông số chuẩn cho Zeke's Convergence (15 Ultimate Haste) và các trang bị cần thiết.
- [ ] `RiotDataDragonClient` bóc tách chính xác `ultimate_haste`, `basic_haste`, `summoner_haste` từ Data Dragon.
- [ ] Thực thể `Item` và CSDL `ItemORM` lưu trữ đầy đủ các chỉ số Haste mới.
- [ ] `Build.get_ultimate_haste()` tính toán chính xác tổng Ultimate Haste từ cả trang bị và ngọc.
- [ ] Khi chọn Malignance (`3118`), chiêu cuối R nhận đủ +35 Haste (+15 AH + 20 Ult Haste), chiêu Q/W/E nhận +15 AH.
- [ ] Khi chọn Experimental Hexplate (`3073`) hoặc Fiendhunter Bolts (`2512`), chiêu cuối R nhận đủ +30 Ult Haste, telemetry hiển thị Ult Haste = 30.
- [ ] Khi chọn Zeke's Convergence (`3050`), chiêu cuối R nhận đủ +25 Haste (+10 AH + 15 Ult Haste).
- [ ] Giao diện Inventory hiển thị rõ ràng thông tin Haste đặc thù của từng trang bị.
- [ ] Toàn bộ unit tests và integration tests liên quan đều chạy thành công (100% pass).

---

## 12. Future Extensions
- Mở rộng hỗ trợ các trang bị có Haste biến thiên theo cấp tướng hoặc chỉ số phụ khi dự án phát triển tính năng mô phỏng level và chỉ số tướng (Champion Stats Scaling).
- Bổ sung cơ chế thông báo tooltip chi tiết khi rê chuột vào từng trang bị trên giao diện.
