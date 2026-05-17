# Quickstart: BlackDragon SaaS Platform

**Feature**: 001-blackdragon-platform
**Date**: 2026-05-16

## Prerequisites

- Python 3.12+
- Node.js 20+ and npm
- Docker and Docker Compose
- Git

## 1. Clone and Setup

```bash
git clone <repository-url> blackdragon
cd blackdragon
```

## 2. Start Infrastructure

```bash
# Start PostgreSQL
docker compose -f docker/docker-compose.dev.yml up -d postgres

# Wait for database to be ready
docker compose -f docker/docker-compose.dev.yml exec postgres pg_isready
```

## 3. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -e ".[dev]"

# Copy environment file
cp .env.example .env
# Edit .env with your database URL and secret key

# Run database migrations
alembic upgrade head

# Seed initial data (admin user, board catalog)
python -m app.seed

# Start development server
uvicorn app.main:app --reload --port 8000
```

Backend runs at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

## 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env
# Edit .env with API URL (default: http://localhost:8000)

# Start development server
npm run dev
```

Frontend runs at: `http://localhost:5173`

## 5. Verify Setup

1. Open `http://localhost:5173` — public website should render
2. Navigate to `/register` — create a test account
3. Log in — dashboard should display
4. Create a property and project
5. Open the visual editor — drag blocks onto canvas
6. Connect blocks and configure properties
7. Compile — view generated ESPHome YAML

## 6. Run Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test        # unit tests
npm run test:e2e    # end-to-end tests (requires running backend)
```

## 7. Full Docker Stack

```bash
# Build and run everything
docker compose -f docker/docker-compose.yml up --build

# Access the application at http://localhost
```

## 8. Lint and Format

```bash
# Backend
cd backend
ruff check .
ruff format .
mypy app/

# Frontend
cd frontend
npm run lint
npm run format
npm run typecheck
```

## Default Credentials (Development Seed)

- **Admin**: admin@blackdragon.io / changeme123
- **Test Client**: client@test.com / changeme123

## Key URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 |

## Environment Variables

### Backend (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | postgresql+asyncpg://blackdragon:blackdragon@localhost:5432/blackdragon |
| SECRET_KEY | JWT signing key | (required, no default) |
| ACCESS_TOKEN_EXPIRE_MINUTES | JWT expiry | 30 |
| FERNET_KEY | Credential encryption key | (required, no default) |
| CORS_ORIGINS | Allowed frontend origins | http://localhost:5173 |

### Frontend (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| VITE_API_URL | Backend API base URL | http://localhost:8000 |
