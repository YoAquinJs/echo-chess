"""root endpoints router"""

from fastapi import APIRouter, Request

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="frontend/templates")


router = APIRouter(
    prefix="",
    tags=["root"],
)


#LLeva a la página home
@router.get("/")
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

#@router.get("/")
#async def root() -> str:
#    """API root"""
#    return "Echo Chess api root, check /docs for the api documentation"
