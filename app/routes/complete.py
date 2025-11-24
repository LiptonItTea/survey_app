from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from .. import schemas, crud
from ..db import get_db
from ..utils.security import sanitize_string

from pydantic import BaseModel
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/complete", tags=["complete"])


class AnswerComplete(BaseModel):
    id: int

class QuestionComplete(BaseModel):
    id: int
    answers: List[AnswerComplete]

class SurveyComplete(BaseModel):
    id: int
    questions: List[QuestionComplete]

class Completed(BaseModel):
    status: str


@router.post("/", response_model=Completed)
async def complete(survey: SurveyComplete, current_user = Depends(crud.get_user_by_token), db: AsyncSession = Depends(get_db)):
    for question in survey.questions:
        for answer in question.answers:
            real_answer = await crud.get_answer_by_id(db, answer.id)
            if real_answer is None:
                raise HTTPException(status_code=404, detail="Answer not found")
            
            real_question = await crud.get_question_by_id(db, real_answer.id_question)
            if real_question.id != question.id:
                raise HTTPException(status_code=403, detail="Question id is wrong")
            if not real_question.multiple_answers and len(question.answers) > 1:
                raise HTTPException(status_code=403, detail="Too much answers for a question")
            
            real_survey = await crud.get_survey_by_id(db, real_question.id_survey)
            if real_survey.id != survey.id:
                raise HTTPException(status_code=403, detail="Survey id is wrong")
            
    completed_survey = await crud.create_completed_survey(db, current_user.id)
    # validated
    for question in survey.questions:
        for answer in question.answers:
            result = await crud.create_question_answer(db, completed_survey.id, answer.id)
    return {"status": "ok"}


class Solves(BaseModel):
    count: int


@router.get("/solves/{survey_id}", response_model=Solves)
async def get_total_solves(survey_id: int, current_user = Depends(crud.get_user_by_token), db: AsyncSession = Depends(get_db)):
    survey = await crud.get_survey_by_id(db, survey_id)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    
    result = await crud.get_completed_surveys_by_survey(db, survey_id)
    return {"count": result}


# class Stat(BaseModel):
    


@router.get("/stat/{survey_id}")
async def get_survey_stat(survey_id: int, current_user = Depends(crud.get_user_by_token), db: AsyncSession = Depends(get_db)):
    survey = await crud.get_survey_by_id(db, survey_id)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    
    return {"stat": await crud.get_survey_stat(db, survey_id)}
    


# @router.post("/", response_model=schemas.AnswerRead, status_code=status.HTTP_201_CREATED)
# async def create_answer(answer_in: schemas.AnswerCreate, db: AsyncSession = Depends(get_db), current_user = Depends(crud.get_user_by_token)):
#     user = await crud.get_user_by_question_id(db, answer_in.id_question)
#     if not user:
#         raise HTTPException(status_code=404, detail="Question doesn't exist")
#     if user.id != current_user.id:
#         raise HTTPException(status_code=403, detail="Your access token doesn't match your id_user_creator")
    
#     try:
#         answer = await crud.create_answer(db, sanitize_string(answer_in.text), answer_in.id_question)
#     except IntegrityError:
#         raise HTTPException(status_code=404, detail="Failed to create answer: no such question")
#     except Exception as e:
#         print(e)
#         raise HTTPException(status_code=500, detail="Failed to create answer")
#     return answer


# @router.get("/{answer_id}", response_model=schemas.AnswerRead)
# async def read_answer_by_id(answer_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(crud.get_user_by_token)):
#     result = await crud.get_question_by_id(db, answer_id)
    
#     if not result:
#         raise HTTPException(status_code=404, detail="Answer not found")

#     return result


# @router.get("/byquestion/{question_id}", response_model=List[schemas.AnswerRead])
# async def read_answers_by_question_id(question_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(crud.get_user_by_token)):
#     result = await crud.get_answers_by_question(db, question_id)
#     return result


# @router.put("/{answer_id}", response_model=schemas.AnswerRead)
# async def update_answer(answer_id: int, updated: schemas.AnswerUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(crud.get_user_by_token)):
#     user = await crud.get_user_by_answer_id(db, answer_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="Answer doesn't exist")
#     if user.id != current_user.id:
#         raise HTTPException(status_code=403, detail="Your access token doesn't match your id_user_creator")
        
#     answer = await crud.update_answer(db, answer_id, sanitize_string(updated.text))
#     return answer


# @router.delete("/{answer_id}")
# async def delete_answer_by_id(answer_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(crud.get_user_by_token)):
#     user = await crud.get_user_by_answer_id(db, answer_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="Answer doesn't exist")
#     if user.id != current_user.id:
#         raise HTTPException(status_code=403, detail="Your access token doesn't match your id_user_creator")
    
#     result = await crud.delete_answer(db, answer_id)
#     return "ok"