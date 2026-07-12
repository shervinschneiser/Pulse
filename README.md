# Pulse

Pulse is a production-grade webhook gateway and event delivery platform

## Project Status

Early development (Foundation)

## Development

### Start API

```bash
uv run uvicorn app.main:app --reload
```

### Run Celery Worker

```bash
uv run celery -A app.core.celery:celery_app worker --loglevel=info
```

### Run Celery Beat

```bash
uv run celery -A app.core.celery:celery_app beat --loglevel=info
```

### Run Database Migrations

```bash
uv run alembic upgrade head
```

### Create Migration

```bash
uv run alembic revision --autogenerate -m "migration name"
```

### Start with Docker

### Start Services

```bash
docker compose up -d
```

### View Logs

```bash
docker compose logs -f
```

### Stop Services

```bash
docker compose down
```