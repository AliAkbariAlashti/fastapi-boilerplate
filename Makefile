.PHONY: dev stop test lint format migrate shell build

# ── Local development ─────────────────────────────────────────────────────────
dev:
	docker compose up --build -d

stop:
	docker compose down

# ── Testing ───────────────────────────────────────────────────────────────────
test:
	docker compose run --rm api pytest -v

test-cov:
	docker compose run --rm api pytest --cov=app --cov-report=html

# ── Code quality ──────────────────────────────────────────────────────────────
lint:
	ruff check app tests
	mypy app

format:
	ruff format app tests
	ruff check --fix app tests

# ── Database ──────────────────────────────────────────────────────────────────
migrate:
	docker compose run --rm api alembic upgrade head -d

migrate-new:
	@read -p "Migration message: " msg; \
	docker compose run --rm api alembic revision --autogenerate -m "$$msg"

migrate-down:
	docker compose run --rm api alembic downgrade -1

# ── Utilities ─────────────────────────────────────────────────────────────────
shell:
	docker compose run --rm api bash

build:
	docker build --target runtime -t my-service:local .

logs:
	docker compose logs -f api

# ── Setup ─────────────────────────────────────────────────────────────────────
install:
	pip install uv && uv pip install -e ".[dev]"
	pre-commit install
