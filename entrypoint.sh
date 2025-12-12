#!/bin/bash
set -e

миграции Alembic
echo "миграции..."
alembic upgrade head

echo "Запуск FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
