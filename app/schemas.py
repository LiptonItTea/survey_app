from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# =======================
# USER SCHEMAS
# =======================

class UserBase(BaseModel):
    nickname: str
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    registration_date: datetime

    model_config = {"from_attributes": True}


class UserUpdate(UserBase):
    password: Optional[str] = None

# =======================
# SURVEY SCHEMAS
# =======================

class SurveyBase(BaseModel):
    name: str
    description: Optional[str] = None


class SurveyCreate(SurveyBase):
    id_user_creator: int


class SurveyRead(SurveyBase):
    id: int
    id_user_creator: int

    class Config:
        orm_mode = True


class SurveyUpdate(SurveyBase):
    pass


# =======================
# QUESTION SCHEMAS
# =======================

class QuestionBase(BaseModel):
    text: str
    multiple_answers: bool = False


class QuestionCreate(QuestionBase):
    id_survey: int


class QuestionRead(QuestionBase):
    id: int
    id_survey: int

    class Config:
        orm_mode = True


class QuestionUpdate(QuestionBase):
    pass


# =======================
# ANSWER SCHEMAS
# =======================

class AnswerBase(BaseModel):
    text: str


class AnswerCreate(AnswerBase):
    id_question: int


class AnswerRead(AnswerBase):
    id: int
    id_question: int

    class Config:
        orm_mode = True


class AnswerUpdate(AnswerBase):
    pass


# =======================
# COMPLETED SURVEY SCHEMAS
# =======================

class CompletedSurveyBase(BaseModel):
    id_user: int


class CompletedSurveyCreate(CompletedSurveyBase):
    pass


class CompletedSurveyRead(CompletedSurveyBase):
    id: int

    class Config:
        orm_mode = True


# =======================
# QUESTION ANSWER SCHEMAS
# =======================

class QuestionAnswerBase(BaseModel):
    id_completed_survey: int
    id_answer: int


class QuestionAnswerCreate(QuestionAnswerBase):
    pass


class QuestionAnswerRead(QuestionAnswerBase):
    id: int

    class Config:
        orm_mode = True


# =======================
# NESTED RELATIONSHIP VARIANTS (optional)
# =======================

class AnswerNested(AnswerRead):
    pass


class QuestionNested(QuestionRead):
    answers: List[AnswerNested] = []


class SurveyNested(SurveyRead):
    questions: List[QuestionNested] = []


class UserNested(UserRead):
    created_surveys: List[SurveyNested] = []
    completed_surveys: List[CompletedSurveyRead] = []