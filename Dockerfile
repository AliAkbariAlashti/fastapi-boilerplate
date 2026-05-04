# ── Stage 1: builder ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml ./

# Install production deps into .venv
RUN uv venv .venv && \
    uv pip install --no-cache --python .venv/bin/python \
    "fastapi>=0.115.0" \
    "uvicorn[standard]>=0.30.0" \
    "pydantic>=2.9.0" \
    "pydantic-settings>=2.5.0" \
    "sqlalchemy>=2.0.0" \
    "asyncpg>=0.29.0" \
    "alembic>=1.13.0" \
    "python-jose[cryptography]>=3.3.0" \
    "passlib[bcrypt]>=1.7.4" \
    "httpx>=0.27.0" \
    "structlog>=24.4.0" \
    "redis>=5.0.0" \
    "python-multipart>=0.0.12"

# ── Stage 2: dev (builder + dev deps, used by override.yml) ───────────────────
FROM builder AS dev

RUN uv pip install --no-cache --python .venv/bin/python \
    "pytest>=8.3.0" \
    "pytest-asyncio>=0.24.0" \
    "pytest-cov>=5.0.0" \
    "factory-boy>=3.3.0" \
    "faker>=30.0.0" \
    "ruff>=0.6.0" \
    "mypy>=1.11.0" \
    "testcontainers[postgres]>=4.8.0"

COPY app/ app/
COPY migrations/ migrations/
COPY alembic.ini alembic.ini
COPY scripts/entrypoint.sh scripts/entrypoint.sh

RUN chmod +x scripts/entrypoint.sh

# PATH must be set here so uvicorn/pytest are found when override.yml
# overrides the command without going through entrypoint
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8000

ENTRYPOINT ["scripts/entrypoint.sh"]

# ── Stage 3: runtime (slim production image) ──────────────────────────────────
FROM python:3.12-slim AS runtime

WORKDIR /app

RUN groupadd -r appuser && useradd -r -g appuser appuser

COPY --from=builder /app/.venv .venv

COPY app/ app/
COPY migrations/ migrations/
COPY alembic.ini alembic.ini
COPY scripts/entrypoint.sh scripts/entrypoint.sh

RUN chmod +x scripts/entrypoint.sh && \
    chown -R appuser:appuser /app

USER appuser

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8000

ENTRYPOINT ["scripts/entrypoint.sh"]
