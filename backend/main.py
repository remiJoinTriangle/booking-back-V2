from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_db, init_db
from .endpoints import api_router
from .models import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    await init_db()
    yield


app = FastAPI(
    title="Astra backend",
    version="2.0",
    lifespan=lifespan,
)

# Include API routers
app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Server up and running 🚀"}
