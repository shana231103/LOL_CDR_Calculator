<!-- File path: docs/plans/designs/001_frontend_design_system.md -->

# Frontend Design System & UI Specification
## Project: League of Legends Cooldown Calculator
## Design Direction: Minimalist Grunge & Gaming Compact Cockpit

---

## 1. Design Philosophy & Aesthetic Identity

### 1.1. Core Concept: "Minimalist Grunge & Tactical Cockpit"
- **Mood**: Sạch sẽ, dứt khoát, điềm tĩnh và thực dụng. Không màu mè, không hiệu ứng phát sáng neon (anti-neon/anti-purple), không gradient bóng bẩy, không bo tròn quá đà.
- **Visual Texture**: Bề mặt đen mờ (matte charcoal), nền xám than phẳng, viền kim loại xước tối giản (1px crisp borders), các khối bo góc nhẹ (`rounded-md` 6px).
- **Spatial Rhythm**: Whitespace có chủ đích, phân tách các khu vực chức năng bằng ranh giới rõ ràng (Law of Common Region) thay vì các bóng đổ mờ ảo.
- **Information Density**: **Gaming Compact** — tối ưu hóa để toàn bộ bảng điều khiển vừa vặn trên 1 màn hình Desktop chuẩn 1080p (Zero Scroll Cockpit), phản hồi tức thì dưới 150ms (Doherty Threshold).

---

## 2. Color System (60-30-10 Rule)

### 2.1. Palette Distribution

```
┌────────────────────────────────────────────────────────────────────────┐
│  60% PRIMARY BASE (Matte Dark & Charcoal Grunge)                       │
│  • App Canvas: #111215 (Nền đen than chì mờ, chống mỏi mắt)            │
│  • Card / Surface: #181A1F (Bề mặt phẳng, độ tương phản dịu)           │
│  • Panel Inset / Slot: #131519 (Vùng trũng đặt ô item/spell)           │
├─────────────────────────────────────────┬──────────────────────────────┤
│  30% SECONDARY (Structure & Muted Text) │  10% ACCENT (Crisp Telemetry)│
│  • Border Default: #272A32 (Viền 1px)   │  • Final CD: #FFFFFF (White) │
│  • Border Subtle: #1F2228               │  • Ability Haste: #38BDF8    │
│  • Text Primary: #E6E8EC (Off-white)    │  • Ultimate Haste: #F59E0B   │
│  • Text Muted: #868C98 (Xám trung tính) │  • Active Rank: #F3F4F6      │
│  • Hover State: #21242C                 │  • Success/Delta: #10B981    │
└─────────────────────────────────────────┴──────────────────────────────┘
```

### 2.2. Semantic CSS Variables (`main.css`)

```css
:root {
  /* 60% Canvas & Surfaces */
  --bg-app: #111215;
  --bg-surface: #181A1F;
  --bg-surface-hover: #21242C;
  --bg-inset: #131519;

  /* 30% Structural Borders & Typography */
  --border-subtle: #1F2228;
  --border-default: #2A2D35;
  --border-active: #4B5162;
  --text-primary: #E6E8EC;
  --text-secondary: #868C98;
  --text-disabled: #4E5360;

  /* 10% Haste Domain Accents & Telemetry */
  --accent-ah: #38BDF8;          /* General Ability Haste (Sky 400) */
  --accent-ult: #F59E0B;         /* Ultimate Haste (Amber 500) */
  --accent-summoner: #A855F7;    /* Summoner Haste (Purple 500) */
  --accent-highlight: #FFFFFF;   /* Crisp Pure White for Final CD */
  --accent-success: #10B981;     /* CDR Reduction % */
}
```

---

## 3. Typography System

### 3.1. Font Pairing
- **Primary Interface Font**: `Inter`, `-apple-system`, `sans-serif`
  - Trực quan, trung tính, dứt khoát, độ nét cao trên màn hình gaming.
- **Data & Telemetry Font (Numbers, Cooldowns, Stats)**: `JetBrains Mono`, `ui-monospace`, `monospace`
  - Sử dụng **Tabular Figures (`font-variant-numeric: tabular-nums`)** để các con số thời gian không bị giật/nhảy layout khi người dùng tăng giảm rank hay trang bị.

### 3.2. Type Scale (Compact UI - Major Second 1.125)

| Token | Size | Line Height | Weight | Usage |
|-------|------|-------------|--------|-------|
| `text-2xs` | 10px | 14px | 500 | Slot labels (Q, W, E, R, ITEM 1-6) |
| `text-xs` | 12px | 16px | 400/500 | Badges, sub-labels, rune stack counts |
| `text-sm` | 13px | 18px | 400/500 | Champion names, item tooltips, table rows |
| `text-base` | 14px | 20px | 500 | Section headers, card titles |
| `text-lg` | 16px | 24px | 600 | Modal titles, Haste aggregate totals |
| `text-xl` | 20px | 26px | 700 | Primary final cooldown highlight |

---

## 4. Layout Architecture: "3-Column Cockpit Dashboard"

Toàn bộ ứng dụng được gói gọn trong màn hình Desktop tiêu chuẩn (`max-w-7xl mx-auto h-[calc(100vh-4rem)]`), loại bỏ việc phải cuộn trang liên tục.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Logo [LoL CDR Engine]  •  Patch: [15.4.1 (Active)]  •  [Reset Build]           │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│ COLUMN 1 (30%)             │ COLUMN 2 (38%)             │ COLUMN 3 (32% - STICKY)      │
│ [ CHAMPION & SKILLS ]      │ [ LOADOUT CONFIGURATION ]  │ [ TELEMETRY & RESULTS ]      │
│                            │                            │                              │
│ ┌────────────────────────┐ │ ┌────────────────────────┐ │ ┌──────────────────────────┐ │
│ │ Selected Champion Card │ │ │ 6 Inventory Item Slots │ │ │ Haste Summary Bar        │ │
│ │ • Avatar (64x64)       │ │ │ ┌──┐ ┌──┐ ┌──┐         │ │ │ • AH: 45  • Ult: 31      │ │
│ │ • Name & Title         │ │ │ └──┘ └──┘ └──┘         │ │ └──────────────────────────┘ │
│ │ • [Change Champion]    │ │ │ ┌──┐ ┌──┐ ┌──┐         │ │ ┌──────────────────────────┐ │
│ └────────────────────────┘ │ │ └──┘ └──┘ └──┘         │ │ Cooldown Telemetry Table   │ │
│                            │ └────────────────────────┘ │ │ Skill | Rank | Base | Final│ │
│ ┌────────────────────────┐ │                            │ │ Q     |  5   | 7.0s | 4.83s│ │
│ │ Q Ability Card         │ │ ┌────────────────────────┐ │ │ W     |  3   | 9.0s | 6.21s│ │
│ │ [-] Rank 5/5 [+]       │ │ │ Haste Runes & Stacks   │ │ │ E     |  1   | 12.0s| 8.28s│ │
│ ├────────────────────────┤ │ │ • Ultimate Hunter      │ │ │ R     |  2   | 110s | 62.5s│ │
│ │ W Ability Card         │ │ │   Stacks: [ - 3 + ]    │ │ └──────────────────────────┘ │
│ │ [-] Rank 3/5 [+]       │ │ │ • Legend: Haste        │ │ ┌──────────────────────────┐ │
│ ├────────────────────────┤ │ │ • Transcendence        │ │ │ Summoner Spells Cooldown │ │
│ │ E Ability Card         │ │ └────────────────────────┘ │ │ • Flash: 260.9s (-13%)   │ │
│ │ [-] Rank 1/5 [+]       │ │                            │ │ • Ignite: 156.5s (-13%)  │ │
│ ├────────────────────────┤ │ ┌────────────────────────┐ │ └──────────────────────────┘ │
│ │ R Ability Card         │ │ │ 2 Summoner Spell Slots │ │ ┌──────────────────────────┐ │
│ │ [-] Rank 2/3 [+]       │ │ │ ┌──────┐  ┌──────┐     │ │ │ % CDR Gauge Bar          │ │
│ └────────────────────────┘ │ │ └──────┘  └──────┘     │ │ │ Visual progress bars     │ │
│                            │ └────────────────────────┘ │ └──────────────────────────┘ │
└────────────────────────────┴────────────────────────────┴──────────────────────────────┘
```

---

## 5. Component Anatomy & Interaction Specs

### 5.1. Champion & Skill Stepper (Column 1)
- **Champion Picker Trigger**:
  - Khi chưa chọn: Thẻ trống viền đứt nét với nút `+ Select Champion`.
  - Khi đã chọn: Avatar tròn 56px với viền xám mờ, tên tướng in hoa dứt khoát, kèm nút nhỏ `[Switch]`.
- **Skill Card Component (`AbilityPanel.vue`)**:
  - Kích thước icon: 44x44px, bo góc `rounded` (4px).
  - Tên skill và phím tắt (Q/W/E/R) gắn badge nhỏ góc trên icon.
  - **Stepper Controls**:
    - Nút `[-]` và `[+]`: Kích thước 32x32px, phông chữ đậm, nền `#21242C`, viền `#2A2D35`.
    - Khi rank = 1: Nút `[-]` bị disable (màu mờ `#4E5360`, con trỏ `not-allowed`).
    - Khi rank = max_rank: Nút `[+]` bị disable.
    - Hiển thị rank: `5 / 5` hoặc các nốt pips trực quan (● ● ● ● ●).

### 5.2. Item Inventory Grid (`ItemInventory.vue` - Column 2)
- **Layout**: Lưới 2x3 ô trang bị mô phỏng giao diện túi đồ client LMHT.
- **Item Slot (48x48px)**:
  - Ô trống: Nền `#131519`, viền `#2A2D35`, dấu cộng mờ ở giữa.
  - Ô có item: Hiển thị icon item Data Dragon, nhấp vào để thay thế hoặc nút `x` nhỏ ở góc để tháo trang bị.
  - Tooltip: Hover hiển thị tên trang bị và lượng `+X Ability Haste`.
- **Item Search Popover**:
  - Ô input tìm kiếm focus tự động, gõ tên trang bị (ví dụ "Liandry", "Zhonya") lọc tức thì.
  - Danh sách cuộn mượt mà hiển thị icon + tên + chỉ số Haste.

### 5.3. Haste Rune Manager (`RuneSection.vue` - Column 2)
- Chỉ hiển thị các Rune có liên quan trực tiếp đến Haste (theo quy tắc Prompt v2):
  - **Ultimate Hunter**: Kèm stepper `[-] [3 Stacks] [+]` (giới hạn 0 - 5 stacks).
  - **Legend: Haste**: Kèm stepper `[-] [10 Stacks] [+]` (giới hạn 0 - 10 stacks).
  - **Transcendence**: Checkbox kích hoạt cấp độ (Lv 5 / Lv 8 / Lv 11).
  - **Haste Stat Shard**: Checkbox `+8 Ability Haste`.

### 5.4. Cooldown Telemetry Display (`CooldownSummary.vue` - Column 3)
- **Tổng quan Haste**:
  - Card nhỏ gọn hiển thị: `Ability Haste: 45` (màu Sky Blue) | `Ultimate Haste: 31` (màu Amber).
- **Bảng số liệu chi tiết**:
  - Dòng Q, W, E, R:
    - Base CD: Số nhỏ màu xám (`7.00s`).
    - Haste áp dụng: `+45 AH` (cho Q/W/E) hoặc `+76 AH` (cho R: 45 AH + 31 Ult Haste).
    - **Final Cooldown**: Số lớn font monospace màu trắng nổi bật (`4.83s`).
    - Tỷ lệ giảm: Badge nhỏ xanh lục `(-31.0%)`.
- **Thanh đo CDR trực quan (Gauge Bar)**:
  - Thanh tiến trình mỏng 4px nằm ngay dưới mỗi kỹ năng, hiển thị phần trăm cooldown đã được giảm.

---

## 6. UX Psychology & Behavioral Optimization

| Nguyên lý | Ứng dụng cụ thể trong thiết kế |
|-----------|--------------------------------|
| **Fitts' Law** | Nút `[-]` và `[+]` có kích thước 32x32px, đặt sát cạnh số rank, không cần di chuyển chuột xa. |
| **Hick's Law** | Không hiển thị toàn bộ 100+ rune không liên quan. Chỉ lọc sẵn 4-5 rune cung cấp Haste để người dùng chọn nhanh trong 3 giây. |
| **Doherty Threshold (<150ms)** | Cập nhật số rank và giao diện ngay lập tức khi click (Optimistic UI), debounced 150ms gửi request tính toán lên backend. |
| **Von Restorff Effect** | Giá trị **Final Cooldown** ở Cột 3 có kích thước lớn nhất và màu trắng sáng tuyệt đối trên nền đen mờ để đập vào mắt người dùng đầu tiên. |
| **Jakob's Law** | Giữ đúng thứ tự Q-W-E-R và cụm 6 ô trang bị như game thủ quen thuộc từ client LMHT. |

---

## 7. Anti-Patterns Avoided (Tuân thủ nghiêm ngặt kỹ năng `frontend-design`)

- ❌ **Không dùng Bento Grid rập khuôn**: Thay vào đó dùng bố cục Cockpit 3 cột khoa học, phù hợp với luồng thao tác công cụ phân tích.
- ❌ **Không dùng Mesh / Aurora Gradients**: Nền hoàn toàn phẳng (Flat Matte), tập trung vào dữ liệu và icon của game.
- ❌ **Không dùng hiệu ứng Neon / Glow tím xanh tràn lan**: Tránh phong cách lòe loẹt; màu sắc chỉ dùng có chủ đích cho các chỉ số quan trọng.
- ❌ **Không bo tròn quá mức (`rounded-full` everywhere)**: Sử dụng các góc bo nhẹ sắc nét (`rounded-md` 6px) tạo cảm giác dứt khoát, chuyên nghiệp.
