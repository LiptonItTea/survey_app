import uvicorn
from fastapi import FastAPI, APIRouter
from .db import engine
from .models import Base
from .routes import users, surveys, questions, views
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

api = APIRouter(prefix="/api", tags=["api"])
api.include_router(users.router)
api.include_router(surveys.router)
api.include_router(questions.router)

app.include_router(api)
app.include_router(views.router)

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