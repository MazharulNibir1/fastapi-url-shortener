# FastAPI URL Shortener

A high-performance URL shortening service built with FastAPI, backed by PostgreSQL for durable storage and Redis for low-latency redirects.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=flat&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7-DC382D?style=flat&logo=redis&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=flat&logo=sqlalchemy&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-Migrations-6BA81E?style=flat)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

---

## Overview

This service converts long URLs into short, shareable codes and redirects users to the original destination. PostgreSQL acts as the system of record; Redis caches active mappings to keep redirect latency minimal.

## Features

- Short code generation with collision-safe retry logic
- Redis-backed caching for sub-millisecond redirect lookups
- Async database access via SQLAlchemy 2.0 + asyncpg
- Click tracking per short code
- Schema-managed migrations with Alembic
- Fully containerized dependencies (Postgres, Redis)

## Tech Stack

| Layer            | Technology              |
|------------------|--------------------------|
| API Framework    | FastAPI                 |
| Language         | Python 3.11              |
| Database         | PostgreSQL               |
| Cache            | Redis                    |
| ORM              | SQLAlchemy 2.0 (async)   |
| Migrations       | Alembic                  |
| Containerization | Docker                   |

## Architecture

```
Client → FastAPI → Redis (cache check) → PostgreSQL (source of truth)
                         ↓ (on miss, repopulate cache)
```

Writes go to PostgreSQL first, then populate Redis. Reads check Redis before falling back to PostgreSQL.

## Project Structure

```
app/
├── main.py          # FastAPI app entrypoint
├── config.py         # Environment-based settings
├── db.py              # Async database session
├── cache.py           # Redis client
├── models.py          # SQLAlchemy models
├── schemas.py          # Pydantic request/response models
├── crud.py             # Database operations
├── shortener.py         # Short code generation logic
└── routes/
    ├── shorten.py        # POST /shorten
    └── redirect.py        # GET /{code}
alembic/                    # Database migrations
```

## Getting Started

### Prerequisites
- Python 3.10+
- Docker

### Installation

```bash
git clone https://github.com/<your-username>/fastapi-url-shortener.git
cd fastapi-url-shortener

python3.10 -m venv env
source env/bin/activate

pip install -r requirements.txt
```

### Run dependencies

```bash
docker run -d --name pg -e POSTGRES_PASSWORD=yourpass -e POSTGRES_DB=yourdbname -p 5432:5432 postgres
docker run -d --name redis -p 6379:6379 redis
```

### Apply migrations

```bash
alembic upgrade head
```

### Start the server

```bash
uvicorn app.main:app --reload
```

API available at `http://localhost:8000`, interactive docs at `http://localhost:8000/docs`.

## API Endpoints

| Method | Endpoint     | Description                     |
|--------|--------------|----------------------------------|
| POST   | `/shorten`   | Create a short URL               |
| GET    | `/{code}`    | Redirect to original URL         |

## Roadmap

- [ ] Expiring links (TTL)
- [ ] Custom aliases
- [ ] User authentication
- [ ] Analytics dashboard

## License

MIT