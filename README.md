# my-service

Production-ready FastAPI microservice with Docker, async SQLAlchemy, Alembic, and JWT auth.

## Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI + Uvicorn |
| ORM | SQLAlchemy 2 (async) |
| DB | PostgreSQL 16 + asyncpg |
| Cache | Redis 7 |
| Migrations | Alembic (async) |
| Auth | JWT via python-jose + passlib bcrypt |
| Config | pydantic-settings |
| Logging | structlog (JSON in prod, colored in dev) |
| Testing | pytest-asyncio + httpx + testcontainers |
| Linting | ruff + mypy |
| CI | GitHub Actions |

## Quick start

```bash
# 1. Copy env file
cp .env.example .env
# Edit SECRET_KEY with: python -c "import secrets; print(secrets.token_hex(32))"

# 2. Start everything
make dev

# 3. API docs available at
open http://localhost:8000/docs
```

## Development commands

```bash
make dev          # docker compose up with hot-reload
make test         # run pytest suite
make lint         # ruff + mypy
make format       # ruff format + autofix
make migrate      # alembic upgrade head
make migrate-new  # generate new migration (prompts for message)
make migrate-down # roll back one migration
make shell        # bash inside the api container
make logs         # tail api logs
```

## Environment variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | ✓ | — | 32+ char random string for JWT signing |
| `DATABASE_URL` | ✓ | — | `postgresql+asyncpg://user:pass@host/db` |
| `REDIS_URL` | | `redis://localhost:6379/0` | Redis connection |
| `ENVIRONMENT` | | `development` | `development` / `production` |
| `DEBUG` | | `false` | SQLAlchemy echo + verbose logs |
| `ALLOWED_ORIGINS` | | `["http://localhost:3000"]` | CORS origins |

## Project structure

```
my-service/
├── app/
│   ├── api/
│   │   ├── deps.py              # DI: db session, current user
│   │   ├── middleware.py        # request ID + access log
│   │   └── v1/endpoints/       # auth, users, items
│   ├── core/
│   │   ├── config.py            # pydantic-settings
│   │   ├── security.py          # JWT + bcrypt
│   │   ├── logging.py           # structlog setup
│   │   └── events.py            # lifespan startup/shutdown
│   ├── db/
│   │   ├── session.py           # async engine + session factory
│   │   └── repositories/        # data access layer
│   ├── models/                  # SQLAlchemy ORM models
│   ├── schemas/                 # Pydantic v2 DTOs
│   ├── services/                # business logic (no HTTP/ORM imports)
│   └── main.py                  # app factory
├── migrations/                  # Alembic async migrations
├── tests/
│   ├── unit/                    # pure function tests
│   ├── integration/             # API tests via TestClient
│   └── conftest.py              # fixtures
├── scripts/entrypoint.sh        # wait-for-db → migrate → serve
├── Dockerfile                   # multi-stage builder/runtime
├── docker-compose.yml
└── Makefile
```

## API endpoints

```
POST   /api/v1/auth/register   Register a new user
POST   /api/v1/auth/token      Login → JWT token

GET    /api/v1/users/me        Get current user
PATCH  /api/v1/users/me        Update current user

GET    /api/v1/items/          List items (paginated)
POST   /api/v1/items/          Create item
GET    /api/v1/items/{id}      Get item
PATCH  /api/v1/items/{id}      Update item
DELETE /api/v1/items/{id}      Delete item

GET    /health                 Health check
```
