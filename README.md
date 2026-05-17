<div align="center">

<img src="specs/001-blackdragon-platform/blackdragon_logo.png" alt="BlackDragon Logo" width="180" />

# 🐉 BlackDragon

**Smart Home Automation Platform**

*Visual programming meets industrial power — drag, wire, deploy.*

[![Vue 3.5](https://img.shields.io/badge/Vue-3.5-4FC08D?style=flat-square&logo=vuedotjs&logoColor=white)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=flat-square&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docs.docker.com/compose/)

---

</div>

## ⚡ Overview

BlackDragon is a full-stack SaaS platform for visual smart home programming targeting **ESP32/ESPHome** and **Home Assistant**. Design automation logic with a drag-and-drop blocks-and-wires editor, compile visual diagrams into production YAML, and deploy over-the-air to your devices.

> *Ultra-dark backgrounds. Metallic accents. Circuit-board patterns. Engineering-grade UI for engineering-grade automation.*

---

## 🏗️ Architecture

| Layer | Stack |
|:------|:------|
| **Frontend** | Vue 3.5 · TypeScript 5.x · Vite 5.4 · Tailwind CSS 3.4 · Vue Flow 1.41 |
| **Backend** | Python 3.14 · FastAPI 0.115 · SQLAlchemy 2.0 (async) · Pydantic 2.10 |
| **Database** | PostgreSQL 16 · Alembic async migrations · Shared-schema multi-tenancy |
| **Compiler** | Visual Graph → Validation → IR → Optimization → Code Generation |
| **Targets** | ESPHome YAML (ESP32 boards) · Home Assistant YAML (automations) |

---

## 🔥 Key Features

| | Feature | Description |
|:--|:--------|:------------|
| 🧩 | **Visual Programming** | Drag-and-drop node editor for smart home automation logic |
| 🏢 | **Multi-Tenant** | Shared-schema multi-tenancy with row-level security |
| ⚙️ | **Compiler Pipeline** | Graph → Validation → IR → Optimization → Code Generation |
| 🎯 | **Dual Targets** | ESPHome YAML for ESP32 boards, Home Assistant YAML for automations |
| 📡 | **OTA Deployment** | Over-the-air firmware deployment to ESP32 devices |
| 🔄 | **Version Control** | Save, compare, and rollback project versions |
| 🛡️ | **Admin Dashboard** | User management, board catalog, blog CMS, audit logs |

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** 20+ (`node --version`)
- **Python** 3.12+ (`python3 --version`)
- **Docker** (for PostgreSQL, or a local PostgreSQL 16+ instance)

### 🐳 Using Docker Compose

> Requires `docker-compose` (standalone) or `docker compose` (plugin).  
> Check which one you have: `docker-compose --version` or `docker compose version`

```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your settings

# Standalone (docker-compose):
docker-compose -f docker/docker-compose.yml up --build

# Plugin (docker compose):
docker compose -f docker/docker-compose.yml up --build
```

### 🔧 Manual Setup

<details>
<summary><strong>1. Start PostgreSQL</strong></summary>

```bash
# Option A: Plain Docker (no Compose needed)
docker run -d --name blackdragon-db \
  -e POSTGRES_DB=blackdragon \
  -e POSTGRES_USER=blackdragon \
  -e POSTGRES_PASSWORD=blackdragon \
  -p 5432:5432 \
  postgres:16-alpine

# Option B: docker-compose (standalone)
docker-compose -f docker/docker-compose.yml up postgres -d

# Option C: docker compose (plugin)
docker compose -f docker/docker-compose.yml up postgres -d

# Option D: Use an existing local PostgreSQL and configure backend/.env
```

</details>

<details>
<summary><strong>2. Backend</strong></summary>

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
# Edit .env if your DB credentials differ from the defaults
alembic upgrade head
python -m app.seed  # Optional: seed demo data
uvicorn app.main:app --reload
```

The backend runs at **http://localhost:8000**.

</details>

<details>
<summary><strong>3. Frontend</strong></summary>

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at **http://localhost:3000** and proxies `/api` requests to the backend.

</details>

---

## 📂 Project Structure

```
blackdragon/
├── backend/
│   ├── app/
│   │   ├── api/            # 🔌 FastAPI route handlers
│   │   ├── compiler/       # ⚙️ Visual graph → code pipeline
│   │   │   ├── generators/ #    ESPHome & Home Assistant generators
│   │   │   ├── nodes/      #    Node type definitions & registry
│   │   │   ├── ir.py       #    Intermediate representation
│   │   │   ├── optimizer.py#    Dead-node elimination, constant folding
│   │   │   ├── pipeline.py #    Orchestration entry point
│   │   │   └── validator.py#    Graph validation & cycle detection
│   │   ├── core/           # 🛡️ Security, tenancy, exceptions
│   │   ├── models/         # 🗃️ SQLAlchemy models (16 entities)
│   │   ├── schemas/        # 📋 Pydantic request/response schemas
│   │   └── services/       # 💼 Business logic
│   ├── alembic/            # 🔄 Database migrations
│   └── tests/              # 🧪 pytest test suite
├── frontend/
│   ├── src/
│   │   ├── components/     # 🧩 Vue components (ui/, editor/, layout/)
│   │   ├── composables/    # 🪝 Vue composables
│   │   ├── services/       # 🌐 API client services
│   │   ├── stores/         # 📦 Pinia stores
│   │   ├── types/          # 📝 TypeScript type definitions
│   │   └── views/          # 📄 Page components (public/, auth/, portal/)
│   └── tests/              # 🧪 Vitest + Playwright tests
├── docker/                 # 🐳 Docker configs
└── specs/                  # 📐 Feature specifications
```

---

## 🧪 Testing

### 🐍 Backend tests (85 tests)

No external services needed — tests use an in-memory SQLite database.

```bash
cd backend
source .venv/bin/activate
python -m pytest
```

> **Note:** The bare `pytest` command won't work unless the venv's `bin/` is on your PATH.  
> Always use `python -m pytest` to be safe.

### ⚡ Frontend unit tests (55 tests)

No servers needed — tests run in jsdom with mocked services.

```bash
cd frontend
npm run test
```

### 🎭 Frontend e2e tests (5 tests)

E2e tests use Playwright to drive a real Chromium browser. Some tests (public page navigation) work with only the frontend; others (auth, forms, portal) require the full stack with PostgreSQL.

**Step 1 — Install Playwright browsers** (first time only):

```bash
cd frontend
npx playwright install chromium
```

**Step 2 — Run e2e tests:**

```bash
cd frontend
npx playwright test
```

The Playwright config auto-starts the frontend dev server.
Tests that need the database skip automatically if PostgreSQL/backend aren't running.

**To run ALL e2e tests** (including auth and form submission), start PostgreSQL and the backend first:

```bash
# Terminal 1: Start PostgreSQL (see Quick Start above)
docker run -d --name blackdragon-db \
  -e POSTGRES_DB=blackdragon \
  -e POSTGRES_USER=blackdragon \
  -e POSTGRES_PASSWORD=blackdragon \
  -p 5432:5432 \
  postgres:16-alpine

# Terminal 2: Start backend
cd backend
source .venv/bin/activate
alembic upgrade head
uvicorn app.main:app --reload

# Terminal 3: Run e2e tests
cd frontend
npx playwright test
```

---

## 📖 API Documentation

Start the backend and visit:
- **Swagger UI** → [`/docs`](http://localhost:8000/docs)
- **ReDoc** → [`/redoc`](http://localhost:8000/redoc)

---

## 🔐 Environment Variables

See `backend/.env.example` for all backend configuration options (database URL, JWT secret, CORS origins, Fernet key).

---

<div align="center">

**⚔️ Forged in darkness. Wired for power. ⚔️**

*Proprietary — All rights reserved.*

</div>
