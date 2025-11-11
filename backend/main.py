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


# --- Exemple de route ---
@app.post("/users", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_user(name: str, db: AsyncSession = Depends(get_db)):
    user = User(
        name=name,
        last_name="",
        age=32,
        account_created_at=0,
        phone_number="",
        preferred_price_per_night=3,
        recurrence_of_stay=3,
        business_or_leisure=3,
        hotel_or_villa=3,
        token_hash=5396349060120187031,
        avatar_asset_id=1,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"id": user.id, "name": user.name}


@app.get("/users/{user_id}", response_model=dict)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name}


@app.get("/")
async def root():
    return {"message": "Server up and running 🚀"}
