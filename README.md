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

- **Node.js** 20+
- **Python** 3.12+
- **PostgreSQL** 16+
- **Docker & Docker Compose** (optional)

### 🐳 Using Docker Compose (recommended)

```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your settings
docker compose -f docker/docker-compose.yml up --build
```

### 🔧 Manual Setup

<details>
<summary><strong>Backend</strong></summary>

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
# Edit .env with your database URL and secret key
alembic upgrade head
python -m app.seed  # Optional: seed demo data
uvicorn app.main:app --reload
```

</details>

<details>
<summary><strong>Frontend</strong></summary>

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

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

```bash
# 🐍 Backend (activate virtual environment first)
cd backend
source .venv/bin/activate
python -m pytest

# ⚡ Frontend unit tests
cd frontend
npm run test

# 🎭 Frontend e2e tests
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

See `backend/.env.example` and `frontend/.env.example` for all configuration options.

---

<div align="center">

**⚔️ Forged in darkness. Wired for power. ⚔️**

*Proprietary — All rights reserved.*

</div>
