from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    nickname: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    nickname: str
    email: EmailStr
    registration_date: Optional[datetime]


class Config:
    orm_mode = True