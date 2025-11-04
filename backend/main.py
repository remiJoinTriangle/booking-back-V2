from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .database import init_db, get_db
from .models import User
from .endpoints import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Démarrage : création des tables si elles n'existent pas
    await init_db()
    print("✅ Database initialized.")
    yield
    # Arrêt éventuel : fermeture des ressources
    print("🛑 Application shutting down.")


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
        age=23,
        account_created_at=0,
        phone_number="",
        preferred_price_per_night=3,
        recurrence_of_stay=3,
        business_or_leisure=3,
        hotel_or_villa=3,
        token_hash=1231241232,
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
