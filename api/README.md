# Backend API

API which handles communication between board clients, user data BD storage, and provides
endpoints for data retrieval and board config to the web interface.

## Configuration

Configured with an env file in `./src/.env`, with this format

```env
ECHO_CHESS_DB_URL="sqlite:///path/to/database.db"
```

## Usage

The API is built using python and FastAPI framework.

The dependency management is handled by [poetry](https://python-poetry.org/)

```bash
cd api

poetry install --no-dev --user

# run with interpreter
poetry run -- python3 src/main.py

# or with uvicorn
cd src
poetry run -- uviron main:app
```

after that the API will be running on `http://127.0.0.1:8000`

## Endpoints

FastAPI provides a OpenAPI documentation page, and request testing of the endpoints
it's under `http://127.0.0.1:8000/docs`

TODO list endpoint and intended use cases
