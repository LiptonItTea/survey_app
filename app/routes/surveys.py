from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..db import get_db
from .. import crud, schemas
router = APIRouter(prefix="/surveys", tags=["surveys"])

@router.get("/", response_model=List[schemas.SurveyRead])
async def read_survey(db: AsyncSession = Depends(get_db)):
    result = await crud.get_all_surveys(db)
    print(result)
    return result

@router.get("/{survey_id}", response_model=schemas.SurveyRead)
async def read_survey_by_id(survey_id: int, db: AsyncSession = Depends(get_db)):
    result = await crud.get_survey_by_id(db, survey_id)
    return result