#!/bin/bash
#Running Poetry install
poetry install --no-root

# Wait for the database to be ready
echo "Waiting for PostgreSQL to start..."
./scripts/wait-for-it.sh db:5432 --timeout=300

# Additional check to ensure PostgreSQL is fully initialized
echo "Checking if PostgreSQL is ready..."
until PGPASSWORD=postgres psql -h "db" -U "postgres" -c '\q'; do
  >&2 echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "PostgreSQL is up - executing command"

# Run Alembic migrations
echo "Running Alembic upgrade..."
cd backend
poetry run alembic upgrade head
poetry run uvicorn main:app --host 0.0.0.0 --port 8000
sleep 5

# Start Uvicorn
#echo "Starting FastAPI..."
#poetry run fastapi dev main
