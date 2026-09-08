# League of Legends Cooldown Calculator Core (LoL CDR Engine)

A high-performance, authoritative cooldown calculation tool for League of Legends (Current Patch), built with **Domain-Driven Design (DDD)** and **Clean Architecture**.

---

## Architecture Overview

- **Backend**: Python 3.13 / FastAPI (Clean Architecture: Domain, Application, Infrastructure, Presentation)
- **Database**: PostgreSQL / SQLite (async via asyncpg / aiosqlite)
- **Frontend**: Vue 3 + TailwindCSS + Pinia + Vite (3-Column Cockpit Dashboard)
- **Data Source**: Riot Data Dragon CDN

---

## Quick Start Guide (Hướng dẫn chạy dự án)

### 1. Khởi chạy Backend (API)

Mở một Terminal (PowerShell) và di chuyển vào thư mục `backend`:

```powershell
cd backend
```

#### Cách 1: Chạy trực tiếp với Python của máy (Khuyến nghị nếu đã có sẵn thư viện)
```powershell
python -m uvicorn app.main:app --reload --port 8000
```

#### Cách 2: Tạo và kích hoạt môi trường ảo riêng (`.venv`)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

> **API Documentation (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)  
> **Health Check**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

---

### 2. Đồng bộ dữ liệu tướng & trang bị (Riot Data Dragon)

Lần đầu chạy, database chưa có dữ liệu tướng. Bạn có thể đồng bộ nhanh bằng 1 trong 2 cách:
- **Cách 1**: Bấm nút **`Sync CDN`** ngay trên thanh Header của giao diện web.
- **Cách 2**: Chạy lệnh curl qua terminal:
  ```powershell
  curl -X POST "http://localhost:8000/api/v1/sync?force=true"
  ```

---

### 3. Khởi chạy Frontend (Giao diện)

Mở một Terminal thứ 2 và chạy:

```powershell
cd frontend
npm install   # nếu chưa cài đặt dependencies
npm run dev
```

> **Truy cập ứng dụng**: [http://localhost:5173](http://localhost:5173)

---

### 4. Chạy Unit & Integration Tests

```powershell
pytest backend/tests -v
```
