
---

# 📚 URL Shortener API

[![CI](https://github.com/harikrishna-goli/shortener/actions/workflows/ci.yml/badge.svg)](https://github.com/harikrishna-goli/shortener/actions/workflows/ci.yml)

## 📖 Overview
A production‑grade **FastAPI** service for shortening URLs with support for:
- Custom aliases  
- Expiration dates  
- Click tracking & stats  
- Owner attribution  

The project is fully containerized with **Docker Compose**, uses **MySQL** as the primary database, and includes **Alembic migrations** for schema management. Automated tests are implemented with **pytest** and isolated test databases.

---

## 🏗 Tech Stack
- **Backend:** FastAPI, SQLAlchemy, Pydantic  
- **Database:** MySQL  
- **Migrations:** Alembic  
- **Containerization:** Docker Compose  
- **Testing:** Pytest  

---

## 📂 Project Structure
```
.
├── app/                # Core application
├── tests/              # Pytest suite
├── alembic/            # Alembic migrations
├── docker-compose.yml  # Multi‑service setup (app + MySQL)
├── Dockerfile          # App container
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment variables
└── pytest.ini          # Pytest config
```

---

## ⚙️ Installation

### 1. Clone the repo
```bash
git clone https://github.com/harikrishna-goli/shortener.git
cd shortener
```

### 2. Setup environment
Copy `.env.example` and adjust values if needed:
```bash
cp .env.example .env
```

### 3. Run with Docker Compose
```bash
docker compose up --build
```

---

## 🚀 Usage

### Create a short URL
```bash
curl -X POST http://127.0.0.1:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://example.com"}'
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
docker compose run app pytest
```

Features:
- Isolated test DB (`mydb_test`)  
- Automatic DB setup/teardown  
- End‑to‑end flow tests for shorten → redirect → stats  

---

## 🔄 Continuous Integration (CI/CD)
This project uses **GitHub Actions** to validate every Pull Request.

### Workflow Overview
- **Trigger:** Runs on every `pull_request` targeting any branch.  
- **Steps:**
  1. Checkout repository  
  2. Build & start services with Docker Compose  
  3. Run Alembic migrations inside the app container  
  4. Execute pytest suite with coverage reporting  
  5. Upload coverage report as artifact  
  6. Tear down containers  

### Quality Gates
- ✅ Migrations must succeed  
- ✅ Tests must pass  
- ✅ Coverage report generated  

---