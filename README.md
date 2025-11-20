
## 🧩 The FastAPI Stack

### 1. **FastAPI (Top Layer)**
- What you write: `@app.post("/shorten")`, `@app.get("/{short_code}")`
- Provides:
  - Easy route definitions
  - Automatic docs (`/docs`)
  - Dependency injection
  - Integration with Pydantic for validation

👉 FastAPI is the **interface** you use to build APIs quickly.

---

### 2. **Pydantic (Data Layer)**
- What you write: `class URLRequest(BaseModel): long_url: str`
- Provides:
  - Input validation (ensures correct types)
  - Output serialization (Python → JSON)
  - Error messages if data is invalid

👉 Pydantic is the **data validator and serializer**.

---

### 3. **Starlette (Engine Layer)**
- What you use indirectly: `RedirectResponse`, `HTTPException`
- Provides:
  - Request/response handling
  - Routing system
  - Middleware
  - Background tasks
  - WebSockets support

👉 Starlette is the **web engine** under FastAPI.

---

## 🔹 Visual Diagram

```
+-------------------+
|   FastAPI Layer   |  <-- You write routes here
|  (API interface)  |
+-------------------+
|   Pydantic Layer  |  <-- Validates input/output data
|  (Data schemas)   |
+-------------------+
|  Starlette Layer  |  <-- Handles HTTP requests/responses
|   (Web engine)    |
+-------------------+
|   Python Runtime  |  <-- Your logic, storage, DB, etc.
+-------------------+
```

---

## 🧠 Analogy
- **FastAPI** = the dashboard of a car (easy controls for the driver).
- **Pydantic** = the safety system (checks inputs, prevents bad data).
- **Starlette** = the engine (actually moves the car forward).

---

So when you write your URL Shortener:
- FastAPI gives you the decorators (`@app.post`, `@app.get`).
- Pydantic gives you `BaseModel` for request/response schemas.
- Starlette gives you `RedirectResponse` and error handling.

---

# Url shortener project overview

This is a full, end‑to‑end record of your URL Shortener project so far: from first decisions and setup, through persistence, inspection, debugging, and the next design phases. It’s written as a professional, interview‑ready design document you can adapt into your README.

---

## Goals and scope

- **Primary goal:** Build a production‑grade URL Shortener with clean API design, persistent storage, and clear observability.
- **Current scope:** Development environment with SQLite + SQLAlchemy, FastAPI‑style endpoints, basic analytics plan, validation, and tooling to inspect/debug data.
- **Constraints:** Local development, single‑process app, simple auth (optional), no distributed systems yet.

---

## Architecture and design decisions

### High-level architecture
- **Client/API:** REST endpoints to shorten URLs, redirect by short code, and view stats.
- **Service layer:** Business logic for validation, short code generation, deduplication, and analytics hooks.
- **Persistence layer:** SQLAlchemy ORM, SQLite for dev; portable design to migrate to Postgres/MySQL later.
- **Observability:** Simple logs, DB inspection via VS Code SQLite extension; plan for metrics.

### Core decisions and rationale
- **SQLAlchemy ORM over raw SQL:** Cleaner domain modeling, migrations, portability to other RDBMS.
- **SQLite for development:** Zero‑config, file‑based DB ideal for rapid iteration; easy to inspect in VS Code.
- **Short code strategy:** Deterministic or random Base62; avoids collisions and supports stable redirects.
- **Deduplication policy:** Either enforce UNIQUE on long_url or allow duplicates but normalize via lookup.
- **Stats as separate table:** Keeps `short_urls` focused; enables scalable analytics.

---

## Data model and schema

### Tables

#### short_urls
- **id:** INTEGER PRIMARY KEY
- **long_url:** TEXT (consider UNIQUE if you want one short per long)
- **short_code:** TEXT UNIQUE NOT NULL
- **created_at:** DATETIME DEFAULT current timestamp

Example SQLAlchemy model:
```python
from sqlalchemy import Column, Integer, String, DateTime, func, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ShortURL(Base):
    __tablename__ = "short_urls"

    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String, nullable=False)
    short_code = Column(String, nullable=False, unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("short_code", name="uq_short_code"),
        # Uncomment if you want one short per long:
        # UniqueConstraint("long_url", name="uq_long_url"),
    )
```

#### url_stats (planned)
- **id:** INTEGER PRIMARY KEY
- **short_url_id:** INTEGER FOREIGN KEY → short_urls.id
- **clicks:** INTEGER DEFAULT 0
- **last_accessed:** DATETIME NULL
- **user_agent/referrer/ip:** TEXT (optional for privacy‑aware analytics)

---

## Setup and persistence

### Database engine and session
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///urls.db"  # file in project root

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # for SQLite + async-ish dev servers
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables once
from your_project.models import Base
Base.metadata.create_all(bind=engine)
```

### CRUD operations (service layer)
```python
from sqlalchemy.orm import Session
from your_project.models import ShortURL

def get_by_short_code(db: Session, code: str) -> ShortURL | None:
    return db.query(ShortURL).filter(ShortURL.short_code == code).first()

def get_by_long_url(db: Session, url: str) -> ShortURL | None:
    return db.query(ShortURL).filter(ShortURL.long_url == url).first()

def create_short_url(db: Session, long_url: str, short_code: str) -> ShortURL:
    record = ShortURL(long_url=long_url, short_code=short_code)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
```

---

## API design and validation

### Endpoints

#### POST /shorten
- **Purpose:** Create or return a short URL for a given long URL.
- **Request body:** { long_url: string }
- **Response:** { short_code, long_url, created_at }
- **Logic:**
  - Validate URL format.
  - Optional: check if long_url already exists → return existing short.
  - Generate short_code (Base62 from ID or random with collision check).
  - Persist and return.

#### GET /{short_code}
- **Purpose:** Redirect to the original long URL.
- **Response:** 302 redirect to long_url.
- **Logic:**
  - Lookup by short_code.
  - If found, increment click counter (in url_stats) and update last_accessed.
  - If not found, return 404.

#### GET /stats/{short_code}
- **Purpose:** Return metadata (clicks, created_at, last_accessed).
- **Response:** { short_code, long_url, clicks, created_at, last_accessed }
- **Logic:** Join short_urls with url_stats.

### Validation rules
- **URL format:** Must be absolute (http/https), no javascript: schemes.
- **Sanitization:** Trim spaces; normalize casing for scheme/host if needed.
- **Rate limiting (future):** Prevent abuse.
- **Security:** Avoid open redirects by validating schemes and optional domain allowlist.

### Short code generation options
- **Base62 from autoincrement id:** Deterministic, compact, collision‑free.
- **Random Base62 (e.g., length 7–8):** Quick; requires uniqueness checks and retries.
- **Hash (e.g., CRC32/MD5 truncated):** Deterministic per long_url; handle collisions.

Example Base62:
```python
ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def encode_base62(n: int) -> str:
    if n == 0: return ALPHABET[0]
    s = []
    while n > 0:
        n, r = divmod(n, 62)
        s.append(ALPHABET[r])
    return "".join(reversed(s))
```

---

## Data inspection, tooling, and debugging

### Inspecting data with SQLAlchemy
```python
from sqlalchemy.orm import Session
from your_project.database import engine
from your_project.models import ShortURL

session = Session(bind=engine)
rows = session.query(ShortURL).all()
for r in rows:
    print(r.id, r.short_code, r.long_url, r.created_at)
session.close()
```

### Raw SQL via SQLAlchemy
```python
from sqlalchemy import text
from your_project.database import engine

with engine.connect() as conn:
    result = conn.execute(text("SELECT short_code, long_url FROM short_urls"))
    for row in result:
        print(row.short_code, row.long_url)
```

### VS Code SQLite extension workflow
- **Open database:** Right‑click `urls.db` → Open Database (or Command Palette → “SQLite: Open Database”).
- **New query tab:** Command Palette → “SQLite: New Query”.
- **Run query:** Right‑click in editor → Run Selected Query.
- **Examples:**
```sql
SELECT * FROM short_urls ORDER BY id DESC LIMIT 5;
SELECT DISTINCT long_url FROM short_urls;
SELECT COUNT(*) FROM short_urls;
```

### Common pitfalls and fixes
- **Tables not visible:** Ensure `Base.metadata.create_all(engine)` ran with correct `engine`.
- **Empty results:** Verify API commits (`db.commit()`); check working directory so `urls.db` path is correct.
- **Wrong SQL keyword:** Use `DISTINCT` not `UNIQUE` in SELECT.
- **Shortcut conflict:** Avoid Ctrl+Shift+Q (system logout); use Command Palette or context menu to run queries.

---

## Roadmap and next steps

### Reliability and robustness
- **Idempotency:** Return existing short for the same long_url if policy dictates.
- **Transactional safety:** Wrap create operations in a transaction; handle IntegrityError on unique violations.
- **Input validation:** Strict URL parsing, blacklist unsafe schemes.

### Analytics and metadata
- **Implement url_stats:** Track clicks, last_accessed.
- **Add `/stats/{short_code}` endpoint:** Return aggregated metrics.

### Testing and quality
- **Unit tests:** Short code generation, validation, CRUD.
- **Integration tests:** Endpoint flows (shorten → redirect → stats).
- **CI setup:** Run tests on push; lint with flake8/black.

### Documentation and DX
- **OpenAPI/Swagger:** Auto‑docs for endpoints.
- **README polish:** Setup, usage, endpoints, design decisions, trade‑offs.
- **Examples:** Curl and Python client snippets.

### Scalability and deployment
- **DB migration:** Move from SQLite to PostgreSQL/MySQL; keep SQLAlchemy models unchanged.
- **Dockerization:** Containerize app + DB; compose for local dev.
- **Cloud deploy:** Render/Fly.io/Azure/AWS; environment config via env vars.

---

## Quick usage examples

### Create a short URL (curl)
```bash
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"long_url":"https://example.com"}'
```

### Redirect test
```bash
curl -i http://localhost:8000/abc123   # replace with actual short_code
```

### Stats
```bash
curl http://localhost:8000/stats/abc123
```

---

If you want, I can convert this into a ready‑to‑commit README.md for your repo, including a concise “Setup → Run → Test → Inspect DB” section and an architectural diagram description. Would you prefer a README format with copy‑paste commands tailored to your exact project paths and module names?
