from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from .. import schemas, crud
from ..db import get_db
from ..utils.security import sanitize_string

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/answers", tags=["questions"])


@router.post("/", response_model=schemas.AnswerRead, status_code=status.HTTP_201_CREATED)
async def create_answer(answer_in: schemas.AnswerCreate, db: AsyncSession = Depends(get_db), current_user = Depends(crud.get_user_by_token)):
    user = await crud.get_user_by_question_id(db, answer_in.id_question)
    if not user:
        raise HTTPException(status_code=404, detail="Question doesn't exist")
    if user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Your access token doesn't match your id_user_creator")
    
    try:
        answer = await crud.create_answer(db, sanitize_string(answer_in.text), answer_in.id_question)
    except IntegrityError:
        raise HTTPException(status_code=404, detail="Failed to create answer: no such question")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to create answer")
    return answer


# @router.get("/", response_model=List[schemas.AnswerRead])
# async def read_answers(db: AsyncSession = Depends(get_db), current_user = Depends(crud.get_user_by_token_admin)):
#     result = await crud.getanswers(db)
#     return result


@router.get("/{answer_id}", response_model=schemas.AnswerRead)
async def read_answer_by_id(answer_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(crud.get_user_by_token)):
    result = await crud.get_question_by_id(db, answer_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Answer not found")

    return result


# @router.get("/byquestion/{question_id}", response_model=List[schemas.AnswerRead])
# async def read_answers_by_question_id(question_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(crud.get_user_by_token)):
#     result = await crud.getques(db, question_id)
#     return result


@router.put("/{answer_id}", response_model=schemas.AnswerRead)
async def update_answer(answer_id: int, updated: schemas.AnswerUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(crud.get_user_by_token)):
    user = await crud.get_user_by_answer_id(db, answer_id)
    if not user:
        raise HTTPException(status_code=404, detail="Answer doesn't exist")
    if user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Your access token doesn't match your id_user_creator")
        
    answer = await crud.update_answer(db, answer_id, sanitize_string(updated.text))
    return answer


@router.delete("/{answer_id}")
async def delete_answer_by_id(answer_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(crud.get_user_by_token)):
    user = await crud.get_user_by_answer_id(db, answer_id)
    if not user:
        raise HTTPException(status_code=404, detail="Answer doesn't exist")
    if user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Your access token doesn't match your id_user_creator")
    
    result = await crud.delete_answer_by_id(db, answer_id)
    return "ok"