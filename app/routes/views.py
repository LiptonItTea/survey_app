from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ..crud import get_user_by_token_admin, get_user_by_token, get_survey_by_id
from ..db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

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
async def auth(request: Request):
    return templates.TemplateResponse(
        request=request, name="auth.html"
    )


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(requst: Request, current_user = Depends(get_user_by_token)):
    return templates.TemplateResponse(
        request=requst, name="dashboard.html"
    )


@router.get("/editSurvey/{survey_id}", response_class=HTMLResponse)
async def edit_survey(request: Request, survey_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_user_by_token)):
    survey = await get_survey_by_id(db, survey_id)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    if survey.id_user_creator != current_user.id:
        raise HTTPException(status_code=403, detail="Not your survey")
    
    return templates.TemplateResponse(
        request=request, name="editSurvey.html"
    )