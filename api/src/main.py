"""
Echo-Chess API
"""

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from database.setup import setup_database
from routers.setup import register_routers

load_dotenv()

setup_database()

app = FastAPI()

register_routers(app)


def main():
    """start api on script execution"""

    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
