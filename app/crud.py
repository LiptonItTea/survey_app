from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from .models import (
    User,
    Survey,
    Question,
    Answer,
    CompletedSurvey,
    QuestionAnswer
)
from .utils.security import hash_password, verify_password, get_token_nickname, get_token_nickname_admin, oauth2_scheme

from fastapi import Request, Depends
from .db import get_db

from .schemas import UserRead

from typing import Optional, List


# =======================
# USER CRUD
# =======================


async def get_user_by_id(db: AsyncSession, id: int) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == id))
    return result.scalars().first()


async def get_user_by_token(request: Request, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)) -> Optional[User]:
    nickname = get_token_nickname(request, token)
    return await get_user_by_nickname(db, nickname)


async def get_user_by_token_admin(request: Request, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)) -> Optional[User]:
    nickname = get_token_nickname_admin(request, token)
    return await get_user_by_nickname(db, nickname)


async def get_user_by_nickname(db: AsyncSession, nickname: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.nickname == nickname))
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def get_user_by_login_password(db: AsyncSession, nickname: str, password: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.nickname == nickname and User.hashed_password == password))
    return result.scalars().first()


async def get_users(db: AsyncSession) -> List[User]:
    result = await db.execute(select(User))
    return result.scalars().all()


async def create_user(db: AsyncSession, nickname: str, email: str, password: str) -> User:
    hashed = hash_password(password)
    user = User(nickname=nickname, email=email, hashed_password=hashed)
    db.add(user)

    try:
        await db.commit()
        await db.refresh(user)
        return user
    except IntegrityError:
        await db.rollback()
        raise


async def update_user(db: AsyncSession, user_id: int, nickname: str, email: str, password: str) -> User:
    user = await get_user_by_id(db, user_id)
    if not user:
        return None

    user.nickname = nickname
    user.email = email
    if password:
        user.hashed_password = hash_password(password)

    try:
        await db.commit()
        await db.refresh(user)
        return user
    except IntegrityError:
        await db.rollback()
        raise


async def delete_user(db: AsyncSession, id: int) -> bool:
    user = await get_user_by_id(db, id)
    if not user:
        return False
    
    try:
        await db.delete(user)
        await db.commit()
        return True
    except IntegrityError:
        await db.rollback()
        raise


# =======================
# SURVEY CRUD
# =======================


async def create_survey(db: AsyncSession, name: str, description: Optional[str], id_user_creator: int) -> Survey:
    survey = Survey(name=name, description=description, id_user_creator=id_user_creator)
    db.add(survey)
    try:
        await db.commit()
        await db.refresh(survey)
        return survey
    except IntegrityError:
        await db.rollback()
        raise


async def get_survey_by_id(db: AsyncSession, survey_id: int) -> Optional[Survey]:
    result = await db.execute(select(Survey).where(Survey.id == survey_id))
    return result.scalars().first()


async def get_all_surveys(db: AsyncSession) -> List[Survey]:
    result = await db.execute(select(Survey))
    return result.scalars().all()


async def update_survey(db: AsyncSession, survey_id: int, name: str, description: str) -> Survey:
    survey = await get_survey_by_id(db, survey_id)
    if not survey:
        return None
    
    survey.name = name
    if description:
        survey.description = description

    try:
        await db.commit()
        await db.refresh(survey)
        return survey
    except IntegrityError:
        await db.rollback()
        raise


async def delete_survey(db: AsyncSession, survey_id: int) -> bool:
    survey = await get_survey_by_id(db, survey_id)
    if not survey:
        return False
    try:
        await db.delete(survey)
        await db.commit()
        return True
    except IntegrityError:
        await db.rollback()
        raise


# =======================
# QUESTION CRUD
# =======================


async def create_question(db: AsyncSession, text: str, multiple_answers: bool, id_survey: int) -> Question:
    question = Question(text=text, multiple_answers=multiple_answers, id_survey=id_survey)
    db.add(question)
    try:
        await db.commit()
        await db.refresh(question)
        return question
    except IntegrityError:
        await db.rollback()
        raise


async def get_question_by_id(db: AsyncSession, question_id: int) -> Optional[Question]:
    result = await db.execute(select(Question).where(Question.id == question_id))
    return result.scalars().first()


async def get_questions_by_survey(db: AsyncSession, survey_id: int) -> List[Question]:
    result = await db.execute(select(Question).where(Question.id_survey == survey_id))
    return result.scalars().all()


async def get_questions(db: AsyncSession) -> List[Question]:
    result = await db.execute(select(Question))
    return result.scalars().all()


async def update_question(db: AsyncSession, question_id: int, text: str, multiple_answers: bool) -> Question:
    question = await get_question_by_id(db, question_id)
    if not question:
        return None
    
    question.text = text
    question.multiple_answers = multiple_answers

    try:
        await db.commit()
        await db.refresh(question)
        return question
    except IntegrityError:
        await db.rollback()
        raise


async def delete_question(db: AsyncSession, question_id: int) -> bool:
    question = await get_question_by_id(db, question_id)
    if not question:
        return False
    try:
        await db.delete(question)
        await db.commit()
        return True
    except IntegrityError:
        await db.rollback()
        raise


# =======================
# ANSWER CRUD
# =======================


async def create_answer(db: AsyncSession, text: str, id_question: int) -> Answer:
    answer = Answer(text=text, id_question=id_question)
    db.add(answer)
    try:
        await db.commit()
        await db.refresh(answer)
        return answer
    except IntegrityError:
        await db.rollback()
        raise


async def get_answer_by_id(db: AsyncSession, answer_id: int) -> Optional[Answer]:
    result = await db.execute(select(Answer).where(Answer.id == answer_id))
    return result.scalars().first()


async def get_answers_by_question(db: AsyncSession, question_id: int) -> List[Answer]:
    result = await db.execute(select(Answer).where(Answer.id_question == question_id))
    return result.scalars().all()


async def delete_answer(db: AsyncSession, answer_id: int) -> bool:
    answer = await get_answer_by_id(db, answer_id)
    if not answer:
        return False
    try:
        await db.delete(answer)
        await db.commit()
        return True
    except IntegrityError:
        await db.rollback()
        raise


# =======================
# COMPLETED SURVEY CRUD
# =======================


async def create_completed_survey(db: AsyncSession, id_user: int) -> CompletedSurvey:
    completed_survey = CompletedSurvey(id_user=id_user)
    db.add(completed_survey)
    try:
        await db.commit()
        await db.refresh(completed_survey)
        return completed_survey
    except IntegrityError:
        await db.rollback()
        raise


async def get_completed_survey_by_id(db: AsyncSession, cs_id: int) -> Optional[CompletedSurvey]:
    result = await db.execute(select(CompletedSurvey).where(CompletedSurvey.id == cs_id))
    return result.scalars().first()


async def get_completed_surveys_by_user(db: AsyncSession, user_id: int) -> List[CompletedSurvey]:
    result = await db.execute(select(CompletedSurvey).where(CompletedSurvey.id_user == user_id))
    return result.scalars().all()


async def delete_completed_survey(db: AsyncSession, completed_survey_id: int) -> bool:
    completed_survey = await get_completed_survey_by_id(db, completed_survey_id)
    if not completed_survey:
        return False
    try:
        await db.delete(completed_survey)
        await db.commit()
        return True
    except IntegrityError:
        await db.rollback()
        raise


# =======================
# QUESTION ANSWER CRUD
# =======================


async def create_question_answer(db: AsyncSession, id_completed_survey: int, id_answer: int) -> QuestionAnswer:
    question_answer = QuestionAnswer(id_completed_survey=id_completed_survey, id_answer=id_answer)
    db.add(question_answer)
    try:
        await db.commit()
        await db.refresh(question_answer)
        return question_answer
    except IntegrityError:
        await db.rollback()
        raise


async def get_question_answer_by_id(db: AsyncSession, qa_id: int) -> Optional[QuestionAnswer]:
    result = await db.execute(select(QuestionAnswer).where(QuestionAnswer.id == qa_id))
    return result.scalars().first()


async def get_question_answers_by_completed_survey(db: AsyncSession, cs_id: int) -> List[QuestionAnswer]:
    result = await db.execute(select(QuestionAnswer).where(QuestionAnswer.id_completed_survey == cs_id))
    return result.scalars().all()


async def delete_question_answer(db: AsyncSession, question_answer_id: int) -> bool:
    question_answer = await get_question_answer_by_id(db, question_answer_id)
    if not question_answer:
        return False
    try:
        await db.delete(question_answer)
        await db.commit()
        return True
    except IntegrityError:
        await db.rollback()
        raise