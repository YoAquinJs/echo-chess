"""user endpoints router"""

from fastapi import APIRouter

from auth.dependencies import UserTokenDependency

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[UserTokenDependency],
)
