"""
Echo-Chess API
"""

import uvicorn

# Añadir el directorio raíz del proyecto al sys.path 
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#Devolver luego
#from dotenv import load_dotenv

from fastapi import FastAPI

from database.setup import setup_database
from routers.setup import register_routers

#Devolver luego
#load_dotenv()

setup_database()

app = FastAPI()

register_routers(app)


def main():
    """start api on script execution"""

    uvicorn.run(app, host="127.0.0.1", port=8000)
    #uvicorn.run(app, host="0.0.0.0", port=8000)
    #192.168.100.52    IPv4
    #http://192.168.100.52:8000/web/user/create


if __name__ == "__main__":
    main()