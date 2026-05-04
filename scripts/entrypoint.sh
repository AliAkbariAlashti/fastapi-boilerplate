#!/usr/bin/env bash
set -euo pipefail

echo "==> Waiting for database..."
until python - <<'EOF'
import asyncio, asyncpg, os, sys
async def check():
    try:
        url = os.environ["DATABASE_URL"].replace("+asyncpg", "")
        conn = await asyncpg.connect(url)
        await conn.close()
    except Exception as e:
        print(f"DB not ready: {e}", file=sys.stderr)
        sys.exit(1)
asyncio.run(check())
EOF
do
  echo "  retrying in 2s..."
  sleep 2
done

echo "==> Running Alembic migrations..."
alembic upgrade head

echo "==> Starting Uvicorn..."
exec uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers "${WORKERS:-1}" \
  --no-access-log
