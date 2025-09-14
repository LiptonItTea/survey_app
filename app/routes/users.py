from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import get_db
from .. import crud, schemas


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