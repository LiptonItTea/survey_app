from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["views"])
# router.mount("/app/static", StaticFiles(directory="./app/static"), name="static")

templates = Jinja2Templates(directory="./app/static/templates")


@router.get("/users", response_class=HTMLResponse)
async def view_users(request: Request):
    return templates.TemplateResponse(
        request=request, name="users.html"
    )


@router.get("/surveys", response_class=HTMLResponse)
async def view_surveys(request: Request):
    return templates.TemplateResponse(
        request=request, name="surveys.html"
    )