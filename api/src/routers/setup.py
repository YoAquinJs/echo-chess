"""setup the routers in the API app"""

from fastapi import APIRouter, FastAPI

from routers.root import router as root_router 
from routers.user import router as user_router 
from routers.board_client import router as board_client_router

routers: list[APIRouter] = [ 
    root_router,
    user_router,
    board_client_router
]


def register_routers(app: FastAPI) -> None:
    """register the routers in the api app"""
    for rou in routers:
        app.include_router(rou)
