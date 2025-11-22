import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from .db import engine
from .models import Base
from .routes import users, surveys, questions, answers, views, auth
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

api = APIRouter(prefix="/api", tags=["api"])
api.include_router(users.router)
api.include_router(surveys.router)
api.include_router(questions.router)
api.include_router(answers.router)

app.include_router(api)
app.include_router(views.router)
app.include_router(auth.router)

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