import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv
from .models import AstraBase

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://localhost:5432/astra"
)

# Création de l'engine asynchrone
engine = create_async_engine(DATABASE_URL, echo=True)

# Création du sessionmaker asynchrone
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(AstraBase.metadata.create_all)
