from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ..crud import get_user_by_token_admin

router = APIRouter(tags=["views"])
# router.mount("/app/static", StaticFiles(directory="./app/static"), name="static")

templates = Jinja2Templates(directory="./app/static/templates")


@router.get("/users", response_class=HTMLResponse)
async def view_users(request: Request, current_user = Depends(get_user_by_token_admin)):
    return templates.TemplateResponse(
        request=request, name="users.html"
    )


@router.get("/surveys", response_class=HTMLResponse)
async def view_surveys(request: Request, current_user = Depends(get_user_by_token_admin)):
    return templates.TemplateResponse(
        request=request, name="surveys.html"
    )


@router.get("/questions", response_class=HTMLResponse)
async def view_questions(request: Request, current_user = Depends(get_user_by_token_admin)):
    return templates.TemplateResponse(
        request=request, name="questions.html"
    )

@router.get("/", response_class=HTMLResponse)
async def base(request: Request):
    return templates.TemplateResponse(
        request=request, name="auth.html"
    )