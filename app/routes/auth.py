from fastapi import APIRouter, Depends, HTTPException, status, Response 
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from ..db import get_db
from .. import crud, schemas
from ..utils.security import hash_password, create_access_token

from typing import List
from pydantic import BaseModel


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_login_password(db, form_data.username, hash_password(form_data.password))
    if not user:
        raise HTTPException(status_code=400, detail="No such user found.")
    role = "user"
    if user.nickname == "meow":
        role = "admin"

    access_token = create_access_token(data={"sub": user.nickname, "role": role})

    response.set_cookie(
        key="access_token",
        value=f"{access_token}",
        httponly=True,
        max_age=1800,
        expires=1800,
        samesite="lax",
        secure=False
    )

    return {"access_token": access_token, "token_type": "bearer"}

# @router.get("/test")
# async def test(current_user = Depends(crud.get_user_by_token)):
#     return current_user