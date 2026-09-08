<!-- File path: docs/plans/001b_ddragon_item_filtering.md -->

# Implementation Plan: Data Dragon Summoner's Rift Item Filtering & DB Hygiene

## 1. Overview

- **Feature Name**: Data Dragon Summoner's Rift Item Filtering & Clean Sync (Phase 001b).
- **Business Objective**: Đảm bảo người dùng công cụ tính toán hồi chiêu (League of Legends Cooldown Calculator) chỉ thấy và lựa chọn đúng các trang bị hiện hữu, có thể mua được trên bản đồ Summoner's Rift trong patch hiện tại; loại bỏ các trang bị gây nhiễu, lỗi thời hoặc duplicate.
- **Technical Objective**: 
  - Nâng cấp adapter `RiotDataDragonClient.fetch_items()` để áp dụng tập quy tắc lọc chuẩn: kiểm tra map ID 11, cờ `purchasable`, trạng thái hiển thị `inStore` / `hideFromAll`, loại trừ vật phẩm 0 vàng (Trinkets) và trang bị Ornn Tuyệt Phẩm.
  - Hỗ trợ cơ chế Whitelist dành riêng cho các trang bị tiến hóa từ Nước Mắt Nữ Thần (Muramana, Seraph's Embrace, Fimbulwinter).
  - Cập nhật repository `IItemRepository` / `SqlItemRepository` và use case `SyncPatchDataUseCase` để hỗ trợ cơ chế dọn dẹp các bản ghi item lỗi thời/rác đang tồn tại trong Database khi chạy sync.
- **Expected Outcome**:
  - API `GET /api/v1/items` trả về danh sách trang bị Summoner's Rift thuần khiết (~200 trang bị thay vì hàng trăm trang bị rác/chế độ phụ).
  - Không còn hiện tượng trùng lặp trang bị (như Guardian's Horn, các item Arena, hoặc duplicate Ornn).
  - Người dùng có thể chọn Muramana / Seraph's Embrace / Fimbulwinter để nhận chính xác Điểm Hồi Kỹ Năng (Ability Haste).

---

## 2. Memory Consultation Summary

- **Memory Confidence**: High (Dữ liệu Project Memory cập nhật ngày 2026-09-07T23:18:00Z, trạng thái Healthy).
- **Memory Documents Read**:
  - `.agents/memory/project-summary.md` (Tech stack, triết lý thiết kế ADR-001 Current Patch Only).
  - `.agents/memory/indexes/component-index.json` (Danh sách thành phần Domain, Application, Infrastructure, Presentation).
  - `.agents/memory/indexes/file-map.json` (Ánh xạ các tệp trong dự án).
  - `.agents/memory/lessons/known-problems.md` (Ghi nhận vấn đề trích xuất thuộc tính Item Ability Haste và Data Dragon).
  - `.agents/memory/lessons/architectural-decisions.md` (ADR-001: Current Patch Only, ADR-005: Clean Architecture Repository Ports).
- **RAG Query Used**: `Data Dragon item synchronization filtering Summoner's Rift`
- **RAG Results Summary**:
  - Xác định được nguyên nhân gốc rễ: Data Dragon giữ toàn bộ trang bị cũ và trang bị đa chế độ chơi (maps 12, 21, 30).
  - Tìm ra các thuộc tính kiểm soát: `maps["11"]`, `gold["purchasable"]`, `inStore`, `hideFromAll`, `requiredAlly`, `requiredChampion`.
- **Additional Source Files Inspected**:
  - `backend/app/infrastructure/external/riot_client.py` (Cách parse item JSON hiện tại chưa có bộ lọc).
  - `backend/app/application/use_cases/sync_patch_data.py` (Luồng gọi gateway và lưu qua repository).
  - `backend/app/domain/repositories/item_repository.py` (Cổng giao tiếp repository cho Item).
  - `backend/app/infrastructure/repositories/sql_item_repo.py` (Triển khai SQLAlchemy hiện tại chỉ upsert, chưa dọn dẹp item cũ).
- **Key Architectural Findings**:
  - Nếu chỉ lọc ở tầng nạp dữ liệu (fetch) mà không có cơ chế xóa/đồng bộ lại bảng `items` trong Database thì các item rác từ lần sync trước vẫn sẽ tồn tại trong DB do `upsert_many` chỉ cập nhật bản ghi có trong danh sách mới.
  - Phù hợp hoàn toàn với **ADR-001 (Current Patch Only)**: Bảng dữ liệu chỉ đại diện cho patch hiện hành, sẵn sàng làm sạch dữ liệu cũ khi nạp dữ liệu mới.

---

## 3. Current Architecture

- **Current Modules**:
  - `backend/app/infrastructure/external/riot_client.py`: Đang nạp tất cả entry trong `item.json` chỉ với điều kiện `i_id.isdigit()`, dẫn đến lọt trang bị ARAM, Arena, Ornn upgrade, item cũ đã xóa và item 0 vàng.
  - `backend/app/domain/repositories/item_repository.py`: Khai báo `get_all`, `get_by_ids`, `upsert_many`.
  - `backend/app/infrastructure/repositories/sql_item_repo.py`: Triển khai các phương thức ORM.
  - `backend/app/application/use_cases/sync_patch_data.py`: Điều phối việc tải và lưu dữ liệu.
- **Existing Limitations**:
  - Thiếu bộ lọc điều kiện theo bản đồ Summoner's Rift.
  - Thiếu whitelist cho các trang bị chuyển hóa (Tear-transformed items).
  - Repository chưa hỗ trợ xóa hoặc thay thế toàn bộ danh sách item khi đồng bộ patch mới.
- **Opportunities for Reuse**:
  - Tái sử dụng regex trích xuất `Ability Haste` đã hoạt động tốt.
  - Tái sử dụng `IRiotDataDragonGateway` và `Item` domain entity hiện có.

---

## 4. Scope

### In Scope
1. **Chuẩn hóa bộ lọc trong `RiotDataDragonClient.fetch_items`**:
   - `maps["11"] == True` (chỉ áp dụng cho Summoner's Rift).
   - `gold["purchasable"] == True` HOẶC nằm trong Whitelist chuyển hóa (`3042` Muramana, `3040` Seraph's Embrace, `3048` Fimbulwinter).
   - Loại trừ `requiredAlly == "Ornn"` (loại bỏ Masterwork duplicates).
   - Loại trừ `inStore is False` hoặc `hideFromAll is True`.
   - Loại trừ `gold["total"] <= 0` (loại bỏ phụ kiện / Trinket / dummy tokens).
   - Loại trừ `requiredChampion is not None` (loại bỏ item độc quyền từng tướng).
2. **Cơ chế dọn dẹp Database (DB Cleanup on Sync)**:
   - Mở rộng cổng `IItemRepository` với phương thức xóa toàn bộ hoặc làm mới danh sách item (`delete_all()` hoặc cơ chế prune items không còn trong danh sách).
   - Cập nhật `SqlItemRepository` triển khai phương thức này.
   - Cập nhật `SyncPatchDataUseCase` để làm sạch bảng item cũ trước khi nạp bộ item chuẩn.
3. **Kiểm thử**:
   - Bổ sung Unit Tests kiểm thử các kịch bản lọc item (Item SR hợp lệ, item ARAM, item Ornn, item Whitelist Muramana, item đã xóa).

### Out of Scope
- Chỉnh sửa giao diện Frontend (Frontend tự động hưởng lợi khi API `/api/v1/items` trả về dữ liệu sạch).
- Hỗ trợ các bản đồ khác ngoài Summoner's Rift (ARAM, Arena, TFT).
- Thay đổi cấu trúc bảng `items` (schema giữ nguyên).

### Assumptions
- Bản đồ Summoner's Rift luôn có ID là `"11"` trong Riot Data Dragon.
- Ba trang bị chuyển hóa từ Nước Mắt Nữ Thần có ID cố định trong Data Dragon: `3042` (Muramana), `3040` (Seraph's Embrace), `3048` (Fimbulwinter).

---

## 5. Proposed Solution

1. **Adapter Gateway Layer**:
   - Xây dựng tập hằng số và danh sách whitelist: `TRANSFORMED_TEAR_ITEM_IDS = {3042, 3040, 3048}`.
   - Bổ sung logic kiểm tra điều kiện tuần tự (fail-fast) trong vòng lặp parse `item.json`:
     - Kiểm tra map ID 11.
     - Kiểm tra `gold.purchasable` (bỏ qua nếu không phải True VÀ không nằm trong whitelist).
     - Kiểm tra `requiredAlly != "Ornn"`.
     - Kiểm tra cờ ẩn (`inStore`, `hideFromAll`).
     - Kiểm tra giá trị vàng > 0.
     - Kiểm tra không có `requiredChampion`.
2. **Repository & Use Case Layer**:
   - Khai báo thêm phương thức `delete_all()` trong `IItemRepository`.
   - Trong `SqlItemRepository`, triển khai `delete(ItemORM)` bằng SQLAlchemy Async.
   - Trong `SyncPatchDataUseCase.execute()`, gọi `await self._item_repo.delete_all()` trước khi gọi `await self._item_repo.upsert_many(items)` nhằm dọn sạch các trang bị lỗi thời khỏi database.
3. **Sync Trigger**:
   - Endpoint `/api/v1/sync?force=true` sẽ kích hoạt nạp lại toàn bộ dữ liệu sạch.

---

## 6. Architecture Impact

- **Affected Modules**:
  - `backend/app/infrastructure/external/riot_client.py`
  - `backend/app/domain/repositories/item_repository.py`
  - `backend/app/infrastructure/repositories/sql_item_repo.py`
  - `backend/app/application/use_cases/sync_patch_data.py`
- **Affected Services**: Không ảnh hưởng đến dịch vụ tính toán `CooldownCalculator`.
- **Affected Repositories**: `IItemRepository` và `SqlItemRepository`.
- **Affected APIs**: 
  - `GET /api/v1/items` (kết quả trả về sạch hơn, không duplicate).
  - `POST /api/v1/sync` (thực hiện đồng bộ dữ liệu sạch).
- **Storage Changes**: Không thay đổi schema DB (không cần Alembic migration mới). Chỉ làm sạch dữ liệu trong bảng `items`.
- **Configuration Changes**: Không có.
- **Deployment Impact**: Không gây downtime; sau khi deploy chỉ cần trigger endpoint sync một lần.

---

## 7. File Impact Analysis

### Modify

1. **`backend/app/infrastructure/external/riot_client.py`**
   - *Why it exists*: Gateway client kết nối trực tiếp Riot Data Dragon CDN.
   - *Expected responsibility*: Thêm logic lọc chuyên sâu cho Summoner's Rift, whitelist Tear-transformed items, loại trừ Ornn items và items 0 vàng.
   - *Estimated complexity*: Thấp.

2. **`backend/app/domain/repositories/item_repository.py`**
   - *Why it exists*: Định nghĩa interface hợp đồng của Item Repository.
   - *Expected responsibility*: Thêm phương thức trừu tượng `delete_all() -> None`.
   - *Estimated complexity*: Rất thấp.

3. **`backend/app/infrastructure/repositories/sql_item_repo.py`**
   - *Why it exists*: Hiện thực hóa lưu trữ dữ liệu Item bằng SQLAlchemy Async.
   - *Expected responsibility*: Triển khai `delete_all()` bằng câu lệnh `delete(ItemORM)`.
   - *Estimated complexity*: Thấp.

4. **`backend/app/application/use_cases/sync_patch_data.py`**
   - *Why it exists*: Use Case nạp dữ liệu từ CDN vào hệ thống.
   - *Expected responsibility*: Gọi `delete_all()` trước khi `upsert_many(items)` để đảm bảo bảng items luôn đồng bộ 1:1 với patch hiện tại.
   - *Estimated complexity*: Thấp.

### Create

1. **`backend/tests/unit/test_item_filtering.py`**
   - *Why it exists*: Unit test độc lập kiểm thử thuật toán lọc item của `RiotDataDragonClient`.
   - *Expected responsibility*: Giả lập các mẫu JSON từ Data Dragon (item cũ, item ARAM, item Ornn, Muramana, item chuẩn) và xác minh kết quả sau khi lọc.
   - *Estimated complexity*: Thấp.

### Reuse
- `backend/app/domain/entities/item.py`
- `backend/app/presentation/api/v1/items.py`
- `backend/app/presentation/api/v1/sync.py`

---

## 8. Implementation Phases

### Phase 1: Gateway Item Filtering Logic
- **Objective**: Hoàn thiện thuật toán lọc item trong `RiotDataDragonClient`.
- **Deliverables**: Cập nhật `backend/app/infrastructure/external/riot_client.py`.
- **Validation**: Chạy unit test kiểm tra logic lọc với dữ liệu mock.
- **Dependencies**: Không.

### Phase 2: Repository Cleanup Extension
- **Objective**: Bổ sung tính năng làm sạch danh sách item cũ trong database.
- **Deliverables**: Cập nhật `item_repository.py`, `sql_item_repo.py`, và `sync_patch_data.py`.
- **Validation**: Kiểm tra tính toàn vẹn khi gọi `delete_all()` và `upsert_many()`.
- **Dependencies**: Phase 1.

### Phase 3: Unit Testing & Verification
- **Objective**: Kiểm thử toàn diện và xác minh kết quả đồng bộ.
- **Deliverables**: Tạo `test_item_filtering.py`, chạy bộ kiểm thử `pytest`.
- **Validation**: 100% test case kiểm thử bộ lọc pass thành công.
- **Dependencies**: Phase 1, Phase 2.

---

## 9. Testing Strategy

- **Unit Testing**:
  - Mock dữ liệu Data Dragon `item.json` với các trường hợp:
    - Item hợp lệ trên Summoner's Rift (Map 11, purchasable=True, total > 0).
    - Item ARAM (Map 11=False, Map 12=True) -> Phải bị loại.
    - Item cũ đã loại bỏ (purchasable=False) -> Phải bị loại.
    - Item Tuyệt Phẩm Ornn (`requiredAlly="Ornn"`) -> Phải bị loại.
    - Item Whitelist Muramana (ID 3042, purchasable=False) -> Phải được giữ lại.
    - Item Phụ Kiện / Trinket (total=0) -> Phải bị loại.
    - Item riêng của tướng (`requiredChampion="Gangplank"`) -> Phải bị loại.
- **Integration Testing**:
  - Kiểm thử `SyncPatchDataUseCase` với in-memory session: gọi sync -> các item cũ bị xóa sạch và thay thế bởi danh sách mới.
- **Manual Validation**:
  - Gọi endpoint `POST /api/v1/sync?force=true` sau khi cập nhật mã nguồn.
  - Gọi `GET /api/v1/items` và xác minh:
    - Không còn Guardian's Horn, các item Arena.
    - Có Muramana, Seraph's Embrace.
    - Không còn item giá 0 vàng.

---

## 10. Risks & Mitigation

| Risk | Impact | Likelihood | Mitigation |
| :--- | :--- | :--- | :--- |
| Riot thay đổi ID hoặc cơ chế trang bị chuyển hóa (Muramana/Seraph's) | Thấp | Rất thấp | Khai báo hằng số `TRANSFORMED_TEAR_ITEM_IDS` ở đầu file adapter để dễ bảo trì/cấu hình. |
| Xóa nhầm item đang được tham chiếu trong build của người dùng | Thấp | Thấp | Hiện tại hệ thống hoạt động không lưu build vĩnh viễn (stateless/calculation on the fly theo ADR-001). |
| Data Dragon CDN có item thiếu trường `maps` hoặc `gold` | Trung bình | Thấp | Dùng an toàn `.get("maps", {})` và `.get("gold", {})` với default values. |

---

## 11. Acceptance Criteria

- [ ] `fetch_items()` chỉ trả về các trang bị xuất hiện trên Summoner's Rift (`maps["11"] is True`).
- [ ] Các trang bị đã xóa (`purchasable is False`) bị loại trừ hoàn toàn, trừ các trang bị thuộc whitelist chuyển hóa (Muramana, Seraph's Embrace, Fimbulwinter).
- [ ] Các trang bị nâng cấp của Ornn (`requiredAlly == "Ornn"`) bị loại bỏ hoàn toàn.
- [ ] Toàn bộ phụ kiện và vật phẩm 0 vàng bị loại bỏ khỏi danh sách.
- [ ] Bảng `items` trong Database được làm sạch mỗi khi đồng bộ patch mới hoặc force sync.
- [ ] Toàn bộ unit test mới viết đều đạt trạng thái PASS.

---

## 12. Future Extensions

- Tạo trang cấu hình whitelist/blacklist item động nếu meta game có thêm các dạng trang bị đặc thù mới.
- Bổ sung fallback sang CommunityDragon API nếu Data Dragon có sự cố về mô tả tooltip.
