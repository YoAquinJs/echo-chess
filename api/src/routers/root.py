"""root endpoints router"""

from fastapi import APIRouter

router = APIRouter(
    prefix="",
    tags=["root"],
)


@router.get("/")
async def root() -> str:
    """API root"""
    return "Echo Chess api root, check /docs for the api documentation"
