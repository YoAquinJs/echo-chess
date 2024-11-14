"""board client endpoints router"""

from fastapi import APIRouter

from auth.dependencies import ClientTokenDependency

router = APIRouter(
    prefix="/client",
    tags=["board client"],
    dependencies=[ClientTokenDependency],
)
