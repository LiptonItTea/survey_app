from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import List
from ..db import get_db
from .. import crud, schemas
from ..utils.security import sanitize_string


router = APIRouter(prefix="/surveys", tags=["surveys"])


@router.post("/", response_model=schemas.SurveyRead, status_code=status.HTTP_201_CREATED)
async def create_survey(survey_in: schemas.SurveyCreate, db: AsyncSession = Depends(get_db)):
    try:
        survey = await crud.create_survey(db, sanitize_string(survey_in.name), sanitize_string(survey_in.description), survey_in.id_user_creator)
    except IntegrityError:
        raise HTTPException(status_code=404, detail="Failed to create survey: no such user found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create survey")
    return survey


@router.get("/", response_model=List[schemas.SurveyRead])
async def read_surveys(db: AsyncSession = Depends(get_db)):
    result = await crud.get_all_surveys(db)
    print(result)
    return result


@router.get("/{survey_id}", response_model=schemas.SurveyRead)
async def read_survey_by_id(survey_id: int, db: AsyncSession = Depends(get_db)):
    result = await crud.get_survey_by_id(db, survey_id)
    return result


@router.put("/{survey_id}", response_model=schemas.SurveyRead)
async def update_survey(survey_id: int, updated: schemas.SurveyUpdate, db: AsyncSession = Depends(get_db)):
    survey = await crud.update_survey(db, survey_id, sanitize_string(updated.name), sanitize_string(updated.description))
    if not survey:
        return HTTPException(status_code=404, detail="Survey not found")
    
    return survey


@router.delete("/{survey_id}")
async def delete_survey_by_id(survey_id: int, db: AsyncSession = Depends(get_db)):
    result = await crud.delete_survey(db, survey_id)
    if not result:
        raise HTTPException(status_code=404, detail="Survey not found")
    
    return "ok"