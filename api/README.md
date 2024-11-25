# Backend API

API which handles communication between board clients, user data BD storage, and provides
endpoints for data retrieval and board config to the web interface.

## Configuration

TODO

## Usage

The API is built using python and FastAPI framework, it's dependencies are listed in the
requirements.txt, it's advised to run it in it's own virtual environment.

```bash
cd api

virtualenv
pip install -r requirements.txt

cd src

# run with interpreter
python3 main.py

# or with uvicorn
uviron main:app
```

after that the API will be running on `http://127.0.0.1:8000`

## Endpoints

FastAPI provides a documentation page for testing the endpoints manually,
it's under `http://127.0.0.1:8000/docs`

TODO list endpoint and intended use cases
