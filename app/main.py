import uvicorn
from fastapi import FastAPI
from .db import engine
from .models import Base
from .routes import users
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(users.router)


# @app.on_event("startup")
# async def on_startup():
#     # create tables (simple approach for templates; for production use Alembic migrations)
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


@app.get("/health")
async def health():
    return {"status": "ok"}


# if __name__ == "__main__":
#     uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)