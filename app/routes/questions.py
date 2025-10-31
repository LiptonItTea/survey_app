from fastapi import APIRouter, Depends, HTTPException
from typing import List

from .. import schemas, crud

from ..db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/questions", tags=["questions"])

@router.get("/{question_id}", response_model=schemas.QuestionRead)
async def read_question_by_id(question_id: int, db: AsyncSession = Depends(get_db)):
    result = await crud.get_question_by_id(db, question_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Question not found")

    return result


@router.get("/bysurvey/{survey_id}", response_model=List[schemas.QuestionRead])
async def read_question_by_survey_id(survey_id: int, db: AsyncSession = Depends(get_db)):
    result = await crud.get_questions_by_survey(db, survey_id)
    return result