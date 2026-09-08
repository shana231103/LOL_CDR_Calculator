# Prompt Version 2 — League of Legends Cooldown Calculator

## 1. Tổng quan dự án

Xây dựng một website **League of Legends Cooldown Calculator** với mục đích chính là tính toán thời gian hồi chiêu của kỹ năng dựa trên:

- Champion được chọn.
- Rank của từng skill.
- Ability Haste từ Item.
- Ability Haste hoặc các loại Haste phù hợp từ Rune.
- Haste phù hợp từ Summoner Spell/Rune nếu có tác động đến cooldown.
- Các giá trị cooldown cơ bản của skill theo dữ liệu của patch hiện tại.

Đây là một **công cụ tính cooldown đơn giản**, không phải công cụ mô phỏng trận đấu hoặc mô phỏng combat.

### Tech stack

- Frontend: Vue 3 + TailwindCSS.
- Backend: FastAPI.
- Database: PostgreSQL.
- Data source chính: Riot Data Dragon.
- Có thể sử dụng CommunityDragon khi Data Dragon không cung cấp đủ dữ liệu cần thiết.

---

# 2. Phạm vi phiên bản này

## 2.1. Chỉ hỗ trợ patch hiện tại

Hệ thống chỉ làm việc với **patch hiện tại**.

Không cần:

- Patch selector.
- So sánh cooldown giữa các patch.
- Lưu build theo từng patch.
- Tính toán historical patch.

Backend cần có khả năng cập nhật dữ liệu theo patch mới thay vì hard-code dữ liệu của một patch cố định.

---

# 3. Luồng sử dụng chính

Người dùng thực hiện theo thứ tự:

1. Chọn Champion.
2. Điều chỉnh rank của từng skill bằng nút `-` và `+`.
3. Chọn Item.
4. Chọn Rune.
5. Chọn Summoner Spell.
6. Hệ thống tổng hợp các nguồn Haste phù hợp.
7. Tính cooldown của từng skill.
8. Hiển thị kết quả cooldown.

Người dùng **không cần chọn level 1–18 của champion** và hệ thống **không mô phỏng skill point progression**.

Mỗi skill được điều chỉnh rank độc lập.

Ví dụ:

- Q rank 5.
- W rank 3.
- E rank 1.
- R rank 2.

Đây là trạng thái hợp lệ.

---

# 4. Champion và Skill

Hệ thống cần lấy dữ liệu Champion từ nguồn dữ liệu phù hợp.

Mỗi Champion cần có:

- Champion ID.
- Champion name.
- Champion key.
- Champion icon.
- Passive.
- Q.
- W.
- E.
- R.
- Skill icon.
- Skill rank tối đa.
- Cooldown theo từng rank nếu dữ liệu có cung cấp.

## 4.1. Skill rank

Mỗi skill có nút:

```text
[-] Rank [+]
```

Ví dụ:

```text
Q
[-] 3 [+]

Cooldown: 8.50s
```

Giới hạn rank:

- Q/W/E: theo max rank thực tế của skill.
- R: theo max rank thực tế của ultimate.

Không cho phép rank nhỏ hơn 1 hoặc lớn hơn max rank.

Không cần kiểm tra tổng skill point.

---

# 5. Cooldown calculation

Công thức cooldown cơ bản khi Ability Haste tác động lên skill:

```text
Final Cooldown = Base Cooldown × 100 / (100 + Haste)
```

Ví dụ:

```text
Base Cooldown = 10
Ability Haste = 50

Final Cooldown
= 10 × 100 / (100 + 50)
= 6.67 seconds
```

Hệ thống cần phân biệt loại Haste khi cần thiết.

Không được mặc định mọi nguồn Haste đều tác động lên mọi cooldown.

Ví dụ:

- Ability Haste thông thường → tác động lên basic abilities và ultimate theo cơ chế hiện hành.
- Ultimate Haste → chỉ tác động lên ultimate.
- Các loại Haste khác → chỉ áp dụng cho đúng loại cooldown mà chúng tác động.

---

# 6. Rune

Hệ thống cần hỗ trợ Rune có ảnh hưởng đến cooldown/Haste.

Không nên lưu Rune chỉ dưới dạng:

```text
rune_name
haste_value
```

Mà cần xác định:

- Rune type.
- Haste type.
- Giá trị.
- Điều kiện áp dụng.
- Stack nếu Rune có cơ chế stack.

## 6.1. Ví dụ Ultimate Hunter

Ultimate Hunter không phải Ability Haste thông thường.

Hệ thống cần hiểu rằng đây là:

```text
Haste type: Ultimate Haste
Target: Ultimate
```

Nếu Rune có giá trị thay đổi theo stack, cần lưu được:

```text
value_per_stack
max_stacks
current_stacks
```

Ví dụ logic:

```text
Ultimate Hunter
Current stacks: 3
```

Hệ thống tính đúng lượng Ultimate Haste tương ứng với 3 stack.

Ultimate Haste chỉ được cộng vào cooldown của ultimate, không cộng vào Q/W/E.

## 6.2. Rune không ảnh hưởng cooldown

Nếu Rune không cung cấp Haste hoặc không có hiệu ứng liên quan đến cooldown thì không đưa nó vào phép tính.

---

# 7. Item

Hệ thống cần hỗ trợ lựa chọn Item.

Người dùng có thể:

- Tìm Item theo tên.
- Chọn Item.
- Xóa Item đã chọn.
- Chọn tối đa 6 Item.

Mỗi Item cần lấy dữ liệu hiện tại, bao gồm các chỉ số liên quan đến Haste.

Ví dụ:

```text
Item A: +20 Ability Haste
Item B: +15 Ability Haste
Item C: +10 Ability Haste
```

Tổng:

```text
Ability Haste = 45
```

Ability Haste từ các nguồn phù hợp được cộng theo cơ chế hiện hành.

Không cần mô phỏng các hiệu ứng combat phức tạp của Item trong phiên bản này.

Chỉ xử lý các chỉ số trực tiếp cần thiết cho cooldown calculator.

---

# 8. Summoner Spells

Hệ thống cần hỗ trợ lựa chọn 2 Summoner Spells.

Ví dụ:

```text
Flash
Ignite
```

Mỗi Summoner Spell cần có:

- Name.
- Icon.
- Base cooldown.
- Các modifier/Haste liên quan nếu có trong patch hiện tại.

Không được mặc định Ability Haste của champion tác động lên Summoner Spell nếu cơ chế hiện tại không cho phép.

Cooldown của Summoner Spell phải được tính theo đúng loại Haste/modifier mà spell đó thực sự nhận.

---

# 9. Những skill có nhiều charge

Một số skill có nhiều charge hoặc có cơ chế tích trữ charge.

Trong phiên bản này:

**Chỉ cần tính cooldown của 1 charge.**

Không cần mô phỏng:

- Thời gian để hồi đủ tất cả charge.
- Số charge hiện tại.
- Charge regeneration riêng biệt.
- Chuỗi sử dụng nhiều charge.
- Trạng thái charge trong combat.

Ví dụ một skill có:

```text
2 charges
Recharge time: 10s
```

Calculator chỉ cần sử dụng:

```text
Cooldown = 10s
```

cho một charge.

---

# 10. Skill có cooldown scale đặc biệt

Một số skill có cách xác định cooldown đặc biệt, không đơn giản là một giá trị cooldown cố định theo rank.

Ví dụ:

- Q của Yasuo.
- Q của Yone.
- Các skill có cooldown phụ thuộc Attack Speed hoặc một stat khác.
- Các skill có công thức cooldown riêng.

Trong phiên bản này:

**Không cần triển khai công thức cooldown đặc biệt của từng skill.**

Nếu cooldown của skill không bị ảnh hưởng bởi Ability Haste, hoặc cooldown scale theo cơ chế riêng không thuộc phạm vi calculator, hãy sử dụng giá trị cooldown phù hợp từ dữ liệu nguồn làm giá trị hiển thị/cơ sở và không cố gắng mô phỏng công thức scale riêng.

Mục tiêu của phiên bản này là tính cooldown thông thường dựa trên Haste, không phải mô phỏng toàn bộ công thức gameplay của từng champion.

---

# 11. Champion Passive đặc biệt

Các passive của Champion có thể cung cấp Haste hoặc trực tiếp giảm cooldown.

Trong phiên bản này:

**Không tính các hiệu ứng passive đặc biệt của Champion.**

Ví dụ:

### Sona — Accelerando

Không tính:

- Accelerando stacks.
- Basic Ability Haste từ Accelerando.
- Cooldown reduction của Crescendo sau khi đạt giới hạn stack.
- Các hiệu ứng cooldown đặc biệt phát sinh từ passive.

Sona được xử lý giống một Champion bình thường:

```text
Cooldown
+
Ability Haste từ Item/Rune
```

Nếu Sona có Ability Haste từ Item/Rune thì vẫn tính bình thường.

## Mục tiêu

Không cần tạo hệ thống mô phỏng:

- Champion passive stacks.
- Combat events.
- Hit count.
- Kill/takedown.
- Reset cooldown.
- Refund cooldown.
- Current cooldown manipulation.

Các cơ chế này có thể được phát triển ở phiên bản sau.

---

# 12. Nguyên tắc xử lý Haste

Hệ thống phải phân biệt:

```text
General Ability Haste
Ultimate Haste
Basic Ability Haste
Summoner Spell Haste
```

Không gộp tất cả thành một biến duy nhất nếu điều đó làm sai logic.

Ví dụ:

```text
General Ability Haste = 50
Ultimate Haste = 20
```

Q/W/E:

```text
Applicable Haste = 50
```

R:

```text
Applicable Haste = 50 + 20
```

Engine cần xác định loại cooldown của ability trước khi quyết định Haste nào được áp dụng.

---

# 13. Cooldown Engine

Backend cần có một logic tính toán tập trung.

Input tối thiểu:

```text
champion
skill ranks
selected items
selected runes
selected summoner spells
```

Engine thực hiện:

1. Lấy cooldown cơ bản của skill theo rank.
2. Lấy các Haste từ Item.
3. Lấy các Haste từ Rune.
4. Xác định loại cooldown của skill.
5. Xác định Haste nào áp dụng cho skill.
6. Tính final cooldown.
7. Trả kết quả.

Ví dụ:

```text
Champion: Ahri

Q Rank: 5
W Rank: 5
E Rank: 5
R Rank: 3

Items:
+40 Ability Haste

Runes:
+10 Ability Haste
+Ultimate Haste

Result:
Q → calculated cooldown
W → calculated cooldown
E → calculated cooldown
R → calculated cooldown with applicable Ultimate Haste
```

---

# 14. Data source

## 14.1. Riot Data Dragon

Ưu tiên Riot Data Dragon cho dữ liệu:

- Champion.
- Champion abilities.
- Item.
- Rune.
- Summoner Spell.
- Icon.
- Patch version.

Data phải được lấy theo patch hiện tại.

Không hard-code toàn bộ dữ liệu Champion/Item/Rune vào source code.

## 14.2. CommunityDragon

Có thể sử dụng CommunityDragon khi Data Dragon không cung cấp đủ thông tin cần thiết.

CommunityDragon chỉ là nguồn bổ sung dữ liệu gameplay/client khi cần thiết.


---

# 15. Data synchronization

Backend cần có cơ chế cập nhật dữ liệu khi Riot phát hành patch mới.

Quy trình mong muốn:

```text
Detect latest patch
        ↓
Download current game data
        ↓
Parse required data
        ↓
Normalize data
        ↓
Save/update PostgreSQL
        ↓
Application sử dụng dữ liệu mới
```

Không cần hỗ trợ dữ liệu của nhiều patch cùng lúc.

Database chỉ cần giữ dữ liệu cần thiết cho patch hiện tại.

---

# 16. PostgreSQL data model

Database cần lưu tối thiểu các nhóm dữ liệu:

### Champions

```text
id
key
name
icon
```

### Abilities

```text
id
champion_id
slot
name
icon
max_rank
cooldown_by_rank
cooldown_type
```

### Items

```text
id
name
icon
ability_haste
```

### Runes

```text
id
name
tree
type
haste_type
haste_value
value_per_stack
max_stacks
```

### Summoner Spells

```text
id
name
icon
base_cooldown
cooldown_type
```

Có thể mở rộng schema khi dữ liệu thực tế yêu cầu.

---

# 17. API

Backend cần cung cấp các API cần thiết cho frontend.

## Champion

```http
GET /api/champions
```

Lấy danh sách Champion.

```http
GET /api/champions/{champion_id}
```

Lấy thông tin Champion và abilities.

## Items

```http
GET /api/items
```

Hỗ trợ search Item.

Ví dụ:

```http
GET /api/items?search=...
```

## Runes

```http
GET /api/runes
```

Lấy danh sách Rune và thông tin Haste liên quan.

## Summoner Spells

```http
GET /api/summoner-spells
```

Lấy danh sách Summoner Spells.

## Calculate

```http
POST /api/calculate
```

Request cần chứa:

```json
{
  "champion_id": "...",
  "abilities": {
    "Q": 5,
    "W": 5,
    "E": 5,
    "R": 3
  },
  "items": [],
  "runes": [],
  "summoner_spells": []
}
```

Response cần trả về:

```json
{
  "champion": "...",
  "ability_haste": 50,
  "ultimate_haste": 20,
  "abilities": {
    "Q": {
      "rank": 5,
      "base_cooldown": 6,
      "final_cooldown": 4
    },
    "W": {
      "rank": 5,
      "base_cooldown": 8,
      "final_cooldown": 5.33
    },
    "E": {
      "rank": 5,
      "base_cooldown": 10,
      "final_cooldown": 6.67
    },
    "R": {
      "rank": 3,
      "base_cooldown": 100,
      "final_cooldown": 58.82
    }
  },
  "summoner_spells": []
}
```

Các con số trong ví dụ chỉ mang tính minh họa; không hard-code chúng.

---

# 18. Validation

Backend cần kiểm tra:

- Champion tồn tại.
- Ability tồn tại.
- Rank hợp lệ.
- Item tồn tại.
- Rune tồn tại.
- Summoner Spell tồn tại.
- Không vượt quá 6 Item.
- Không chọn duplicate Item nếu gameplay hiện tại không cho phép.
- Dữ liệu Haste phải hợp lệ.
- Không áp dụng sai loại Haste cho cooldown.

Nếu request không hợp lệ, trả HTTP error phù hợp.

---

# 19. Kết quả cần hiển thị

Kết quả cuối cùng cần cho người dùng thấy:

### Champion

```text
Champion Name
```

### Ability

```text
Q
Rank: 5
Base Cooldown: XXs
Applicable Haste: XX
Final Cooldown: XXs
```

Tương tự:

```text
W
E
R
```

### Haste summary

Ví dụ:

```text
Ability Haste: 50
Ultimate Haste: 20
```

### Summoner Spells

```text
Flash
Base Cooldown: XXs
Final Cooldown: XXs

Ignite
Base Cooldown: XXs
Final Cooldown: XXs
```

---

# 20. Làm tròn số

Cooldown có thể xuất hiện dưới dạng số thập phân.

Nên thống nhất quy tắc hiển thị, ví dụ:

```text
6.666666 → 6.67s
10 → 10s
5.5 → 5.5s
```

Không làm tròn giá trị trung gian nếu không cần thiết.

Nên giữ precision trong calculation và chỉ round ở bước trả kết quả/display.

---

# 21. Tiêu chí hoàn thành

Project được xem là đạt yêu cầu khi:

1. Người dùng chọn được Champion.
2. Hệ thống hiển thị Q/W/E/R.
3. Người dùng có thể tăng/giảm rank từng skill độc lập.
4. Người dùng có thể tìm và chọn Item.
5. Người dùng có thể chọn tối đa 6 Item.
6. Người dùng có thể chọn Rune.
7. Hệ thống nhận diện đúng loại Haste của Rune.
8. Ultimate Haste chỉ áp dụng cho Ultimate.
9. Người dùng có thể chọn Summoner Spells.
10. Hệ thống tính tổng các Haste phù hợp.
11. Hệ thống tính cooldown theo rank.
12. Hệ thống áp dụng công thức Ability Haste đúng khi cooldown nhận Ability Haste.
13. Skill nhiều charge chỉ tính cooldown của một charge.
14. Không mô phỏng các cooldown scale đặc biệt như Yasuo/Yone.
15. Không tính Champion passive đặc biệt như Sona Accelerando.
16. Dữ liệu sử dụng thuộc patch hiện tại.
17. Kết quả cuối cùng hiển thị rõ base cooldown, Haste áp dụng và final cooldown.
18. Backend là nơi chịu trách nhiệm calculation logic.
19. Frontend gửi state hiện tại lên backend và nhận kết quả calculation.
20. Không hard-code dữ liệu gameplay quan trọng trong frontend.

---

# 23. Nguyên tắc cốt lõi

Đây là một **League of Legends Cooldown Calculator**, không phải game simulator.

Ưu tiên:

```text
Đơn giản
→ Dễ bảo trì
→ Dữ liệu đúng patch
→ Công thức cooldown đúng
→ Phân biệt đúng loại Haste
→ Kết quả dễ kiểm tra
```

Không cố gắng xử lý mọi mechanic trong League of Legends.

Nếu một Champion có mechanic cooldown quá đặc biệt và không thuộc phạm vi cooldown thông thường, hãy **bỏ qua mechanic đặc biệt đó** thay vì xây dựng một hệ thống phức tạp chỉ để xử lý một trường hợp riêng.

Kiến trúc dữ liệu nên đủ linh hoạt để có thể mở rộng các mechanic đặc biệt trong tương lai, nhưng **phiên bản hiện tại chỉ cần tập trung vào việc tính cooldown thông thường dựa trên rank + các nguồn Haste được hỗ trợ**.
