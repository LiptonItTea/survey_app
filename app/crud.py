from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from . import models
from .utils.security import hash_password, verify_password


async def get_user_by_email(db: AsyncSession, email: str):
    q = select(models.User).where(models.User.email == email)
    res = await db.execute(q)
    return res.scalars().first()


async def create_user(db: AsyncSession, nickname: str, email: str, password: str):
    hashed = hash_password(password)
    user = models.User(nickname=nickname, email=email, hashed_password=hashed)
    db.add(user)
    try:
        await db.commit()
        await db.refresh(user)
        return user
    except IntegrityError:
        await db.rollback()
        raise