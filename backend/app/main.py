from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.routes import router
from app.api.auth import router as auth_router
from app.api.resumes import router as resumes_router
from app.api.jobs import router as job_router
from app.core.config import settings
from app.db.database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app=FastAPI(
    title=settings.APP_NAME, 
    version=settings.APP_VERSION,
    lifespan=lifespan
) 

app.include_router(router)
app.include_router(auth_router)
app.include_router(resumes_router)
app.include_router(job_router)

