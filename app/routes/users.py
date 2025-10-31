from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from ..db import get_db
from .. import crud, schemas

from typing import List
from pydantic import BaseModel


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(user_in: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await crud.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    try:
        user = await crud.create_user(db, user_in.nickname, user_in.email, user_in.password)
    except Exception as e:
        # You can refine exception handling (e.g. IntegrityError)
        print(e)
        raise HTTPException(status_code=500, detail="Failed to create user")
    return user


@router.get("/", response_model=List[schemas.UserRead])
async def read_users(db: AsyncSession = Depends(get_db)):
    users = await crud.get_users(db)
    return users


@router.get("/{user_id}", response_model=schemas.UserRead)
async def read_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user