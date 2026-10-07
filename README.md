# Majors API

A FastAPI backend for the Majors project with MongoDB and Docker support.

## Features

- FastAPI application
- MongoDB integration
- JWT authentication
- CRUD routes for items
- Docker and Docker Compose setup

## Prerequisites

- Docker
- Docker Compose
- Git

## Run with Docker

```bash
docker compose up --build
```

The API will be available at:

- http://localhost:8000
- http://localhost:8000/health

## Authentication

### Register a user

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret123"}'
```

### Log in

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=alice&password=secret123"
```

### Access protected route

```bash
curl -H "Authorization: Bearer <token>" http://localhost:8000/auth/me
```

## Item API

### List items

```bash
curl http://localhost:8000/items/
```

### Create item

```bash
curl -X POST "http://localhost:8000/items/" \
  -H "Content-Type: application/json" \
  -d '{"name":"Laptop","description":"Gaming laptop","price":1200.99}'
```

### Get item by ID

```bash
curl http://localhost:8000/items/<item_id>
```

### Update item

```bash
curl -X PUT "http://localhost:8000/items/<item_id>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Laptop","description":"Updated","price":1299.99}'
```

### Delete item

```bash
curl -X DELETE http://localhost:8000/items/<item_id>
```

## Project Structure

```text
.
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   └── routes/
│       ├── auth.py
│       ├── health.py
│       └── items.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── main.py
└── README.md
```

## Notes

- The MongoDB password and username are configured in `docker-compose.yml`.
- The default local MongoDB URL is `mongodb://root:password123@localhost:27017/majors?authSource=admin`.
- The default JWT secret is included for local development only. Change it in `app/config.py` for production.
