<!-- File path: docs/plans/prompts/001b_ddragon_item_filtering-planning-prompt.md -->

# Prompt – Generate Implementation Plan: Data Dragon Item Filtering for Summoner's Rift

## Role
You are acting as a Senior Software Architect, Product Engineer, and Technical Planner inside the current IDE workspace.
You have access to the project workspace and Project Memory.

---

## Source Feature / Improvement Request

### 1. Tổng quan yêu cầu
Hiện tại trong `backend/app/infrastructure/external/riot_client.py` khi đồng bộ dữ liệu trang bị từ Riot Data Dragon CDN (`cdn/{version}/data/en_US/item.json`), toàn bộ các đối tượng trong tệp JSON đều được chuyển thành `Item`. Điều này gây ra các lỗi nghiêm trọng:
1. **Trang bị cũ/đã bị loại bỏ (Legacy/Removed Items):** Riot vẫn giữ các ID cũ (như Cốc Quỷ Athene, Kiếm Súng Hextech, các trang bị Thần Thoại cũ...) trong `item.json` để phục vụ lịch sử đấu cũ.
2. **Duplicate trang bị do nhiều chế độ chơi (Game Modes):** Có nhiều trang bị cùng tên nhưng dành riêng cho ARAM (Map 12), Nexus Blitz (Map 21), Arena (Map 30) với giá vàng hoặc chỉ số khác nhau.
3. **Duplicate trang bị do Ornn nâng cấp (Masterwork items):** Các trang bị Tuyệt Phẩm do Ornn rèn đúc gây trùng lặp tên và icon với trang bị gốc trong cửa hàng.
4. **Trang bị rác/nội bộ/phụ kiện:** Các vật phẩm 0 vàng, Mắt Phụ Kiện (Trinket), token nhiệm vụ, hoặc vật phẩm riêng của tướng (như Đạn Pháo Gangplank, Giáo Kalista) gây rác danh sách trang bị.

Mục tiêu của Phase 001b là chuẩn hóa bộ lọc Data Dragon trong quá trình đồng bộ, đảm bảo cơ sở dữ liệu chỉ chứa các trang bị hợp lệ, có thể mua được trên bản đồ **Summoner's Rift** trong patch hiện tại, đồng thời hỗ trợ ngoại lệ cho các trang bị chuyển hóa từ Nước Mắt Nữ Thần (Muramana, Seraph's Embrace, Fimbulwinter) vì chúng cung cấp Điểm Hồi Kỹ Năng (Ability Haste).

---

## 2. Các quy tắc lọc cụ thể (Đã thống nhất với người dùng)

1. **Bản đồ Summoner's Rift:**
   - Chỉ lấy trang bị có `maps["11"] is True`.
   - Bỏ qua các trang bị chỉ có trên map 12 (ARAM), 21 (Nexus Blitz), 30 (Arena).
2. **Trạng thái có thể mua (Purchasable):**
   - Chỉ lấy trang bị có `gold["purchasable"] is True`, **ngoại trừ** danh sách Whitelist các trang bị chuyển hóa từ Nước Mắt Nữ Thần.
   - Whitelist trang bị chuyển hóa:
     - `3042`: Muramana (chuyển hóa từ Manamune, cung cấp Ability Haste).
     - `3040`: Seraph's Embrace (chuyển hóa từ Archangel's Staff, cung cấp Ability Haste).
     - `3048`: Fimbulwinter (chuyển hóa từ Winter's Approach, cung cấp Ability Haste).
3. **Loại bỏ trang bị rèn của Ornn (Masterwork Items):**
   - Bỏ qua các trang bị có `requiredAlly == "Ornn"`.
4. **Loại bỏ trang bị bị ẩn:**
   - Bỏ qua trang bị có `inStore is False` hoặc `hideFromAll is True`.
5. **Giá trị vàng và Phụ kiện (Trinkets):**
   - Chỉ lấy trang bị có `gold["total"] > 0` (loại bỏ hoàn toàn Phụ kiện/Mắt cắm 0 vàng vì không ảnh hưởng đến Haste).
6. **Trang bị dành riêng cho tướng:**
   - Bỏ qua các trang bị có trường `requiredChampion` (ví dụ: Nâng cấp Đạn Pháo Gangplank, Kalista Black Spear).
7. **Làm sạch dữ liệu đã lưu:**
   - Bổ sung cơ chế hoặc script/endpoint để đồng bộ lại dữ liệu sạch vào Database (xóa các trang bị rác hiện có hoặc làm mới bảng items).

---

## 3. Phạm vi kỹ thuật & Giới hạn
- Không thay đổi kiến trúc Clean Architecture của backend.
- Cập nhật adapter `RiotDataDragonClient` trong `infrastructure/external/riot_client.py`.
- Đảm bảo use case `SyncPatchDataUseCase` trong `application/use_cases/sync_patch_data.py` và repository `SqlItemRepository` xử lý nhất quán khi đồng bộ lại patch (làm sạch hoặc upsert đúng đắn).
- Bổ sung unit tests cho bộ lọc trang bị trong `RiotDataDragonClient`.
