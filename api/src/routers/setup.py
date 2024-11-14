"""setup the routers in the API app"""

from fastapi import APIRouter, FastAPI

import routers

routers: list[APIRouter] = [
    routers.root.router,
    routers.user.router,
    routers.client.router,
]


def register_routers(app: FastAPI) -> None:
    """register the routers in the api app"""
    for rou in routers:
        app.include_router(rou)
