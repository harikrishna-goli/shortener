# 📘 URL Shortener API

## 📖 Overview
A production‑grade **FastAPI** service for shortening URLs with support for:
- Custom aliases
- Expiration dates
- Click tracking & stats
- Owner attribution

The project is fully containerized with **Docker Compose**, uses **MySQL** as the primary database, and includes **Alembic migrations** for schema management. It also provides **SQLite → MySQL migration scripts** for portability. Automated tests are implemented with **pytest** and isolated test databases.

---

## 🏗 Tech Stack
- **Backend:** FastAPI, SQLAlchemy, Pydantic
- **Database:** MySQL (with SQLite migration support)
- **Migrations:** Alembic
- **Containerization:** Docker, Devcontainers
- **Testing:** Pytest, FastAPI TestClient
- **Other:** dotenv for config, Redis (future caching)

---

## 📂 Project Structure
```
.
├── app/                 # Core application
│   ├── main.py           # FastAPI entrypoint
│   ├── models.py         # SQLAlchemy ORM models
│   ├── crud.py           # CRUD operations
│   ├── database.py       # DB session + engine
│   ├── schemas.py        # Pydantic request/response models
│   ├── config.py         # Centralized settings
│   └── migration/        # DB init + migration scripts
├── tests/                # Pytest test suite
│   ├── conftest.py       # Test DB setup + overrides
│   └── test_main.py      # Endpoint tests
├── alembic/              # Alembic migrations
├── docker-compose.yml    # Multi‑service setup (app + MySQL)
├── Dockerfile            # App container
├── init.sql              # MySQL init script
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
├── .env.test             # Test DB environment
├── pytest.ini            # Pytest config
└── alembic.ini           # Alembic config
```

---

## ⚙️ Installation

### 1. Clone the repo
```bash
git clone <repo-url>
cd url-shortener
```

### 2. Setup environment
Copy `.env` and adjust values if needed:
```bash
cp .env.example .env
```

### 3. Run with Docker Compose
```bash
docker-compose up --build
```

This will start:
- `app` → FastAPI service on port `8000`
- `mysql` → MySQL DB with `mydb` and `mydb_test`

---

## 🔧 Configuration
Environment variables are managed via `.env`:

```
DB_USER=devuser
DB_PASS=devpass
DB_HOST=mysql
DB_PORT=3306
DB_NAME=mydb
TEST_DB_NAME=mydb_test
APP_HOST=0.0.0.0
APP_PORT=8000
```

---

## 🚀 Usage

### Create a short URL
```bash
curl -X POST http://127.0.0.1:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://example.com"}'
```

Response:
```json
{
  "short_url": "http://127.0.0.1:8000/abc123",
  "short_code": "abc123",
  "expires_at": null,
  "owner_id": null,
  "message": "Short URL created successfully"
}
```

### Redirect
```bash
curl -i http://127.0.0.1:8000/abc123
```

### Stats
```bash
curl http://127.0.0.1:8000/stats/abc123
```

---

## 🧪 Testing
Run tests inside the container:
```bash
docker-compose run app pytest
```

Features:
- Isolated test DB (`mydb_test`)
- Automatic DB setup/teardown
- End‑to‑end flow tests for shorten → redirect → stats

---

## 📦 Deployment
- **Dockerfile** builds a lightweight Python 3.11 image
- **docker-compose.yml** orchestrates app + MySQL
- **Devcontainer** support for VS Code remote development
- Alembic migrations ensure schema consistency

---

## 🔄 Migration
- `db_init.py` → Initialize schema in MySQL
- `db_SQLite_mysqlinit.py` → Migrate data from SQLite → MySQL

---
