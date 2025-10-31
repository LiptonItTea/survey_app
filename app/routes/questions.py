from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from .. import schemas, crud
from ..db import get_db
from ..utils.security import sanitize_string

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/questions", tags=["questions"])


@router.post("/", response_model=schemas.QuestionRead, status_code=status.HTTP_201_CREATED)
async def create_question(question_in: schemas.QuestionCreate, db: AsyncSession = Depends(get_db)):
    try:
        question = await crud.create_question(db, sanitize_string(question_in.text), question_in.multiple_answers, question_in.id_survey)
    except IntegrityError:
        raise HTTPException(status_code=404, detail="Failed to create question: no such survey")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to create question")
    return question


@router.get("/", response_model=List[schemas.QuestionRead])
async def read_questions(db: AsyncSession = Depends(get_db)):
    result = await crud.get_questions(db)
    return result


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


@router.put("/{question_id}", response_model=schemas.QuestionRead)
async def update_question(question_id: int, updated: schemas.QuestionUpdate, db: AsyncSession = Depends(get_db)):
    question = await crud.update_question(db, question_id, sanitize_string(updated.text), updated.multiple_answers)
    if not question:
        return HTTPException(status_code=404, detail="Question not found")
    
    return question


@router.delete("/{question_id}")
async def delete_question_by_id(question_id: int, db: AsyncSession = Depends(get_db)):
    result = await crud.delete_question(db, question_id)
    if not result:
        raise HTTPException(status_code=404, detail="Question not found")
    
    return "ok"