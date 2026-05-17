# BlackDragon — Smart Home Automation Platform

A full-stack SaaS platform for visual smart home programming with ESP32/ESPHome and Home Assistant targets.

## Architecture

- **Frontend**: Vue 3.5 + TypeScript + Vite + Tailwind CSS + Vue Flow
- **Backend**: Python 3.12 + FastAPI + SQLAlchemy 2.0 (async) + PostgreSQL 16
- **Compiler**: Visual graph → IR → optimized code (ESPHome YAML / Home Assistant YAML)

## Quick Start

### Prerequisites

- Node.js 20+
- Python 3.12+
- PostgreSQL 16+
- Docker & Docker Compose (optional)

### Using Docker Compose (recommended)

```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your settings
docker compose -f docker/docker-compose.yml up --build
```

### Manual Setup

#### Backend

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

#### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Project Structure

```
blackdragon/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI route handlers
│   │   ├── compiler/     # Visual graph → code pipeline
│   │   ├── core/         # Security, tenancy, exceptions
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic request/response schemas
│   │   └── services/     # Business logic
│   ├── alembic/          # Database migrations
│   └── tests/            # pytest test suite
├── frontend/
│   ├── src/
│   │   ├── components/   # Vue components (ui/, editor/, layout/)
│   │   ├── composables/  # Vue composables
│   │   ├── services/     # API client services
│   │   ├── stores/       # Pinia stores
│   │   ├── types/        # TypeScript type definitions
│   │   └── views/        # Page components (public/, auth/, portal/)
│   └── tests/            # Vitest + Playwright tests
├── docker/               # Docker configs
└── specs/                # Feature specifications
```

## API Documentation

Start the backend and visit `/docs` for interactive Swagger UI or `/redoc` for ReDoc.

## Key Features

- **Visual Programming**: Drag-and-drop node editor for smart home automation
- **Multi-Tenant**: Shared-schema multi-tenancy with row-level security
- **Compiler Pipeline**: Graph → Validation → IR → Optimization → Code Generation
- **Dual Targets**: ESPHome YAML for ESP32 boards, Home Assistant YAML for automations
- **OTA Deployment**: Over-the-air firmware deployment to ESP32 devices
- **Version Control**: Save, compare, and rollback project versions
- **Admin Dashboard**: User management, board catalog, blog CMS, audit logs

## Testing

```bash
# Backend
cd backend && pytest

# Frontend unit tests
cd frontend && npm run test

# Frontend e2e tests
cd frontend && npx playwright test
```

## Environment Variables

See `backend/.env.example` and `frontend/.env.example` for all configuration options.

## License

Proprietary — All rights reserved.
