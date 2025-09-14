import os
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


# create async engine
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False, future=True)


# async session factory
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


# dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session