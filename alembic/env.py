import os
import sys
from logging.config import fileConfig
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

from alembic import context

# ---------------------------------------------------------------------------
# Load environment and import models
# ---------------------------------------------------------------------------
ROOT_PATH = Path(__file__).resolve().parents[2]
if str(ROOT_PATH) not in sys.path:
    sys.path.insert(0, str(ROOT_PATH))

from backend.models import AstraBase  # noqa: E402

# Alembic Config object
config = context.config

# Load .env variables
load_dotenv()

# Set SQLAlchemy URL (convert async to sync if necessary)
database_url = os.getenv("DATABASE_URL", "")
if "+asyncpg" in database_url:
    database_url = database_url.replace("+asyncpg", "")

config.set_main_option("sqlalchemy.url", str(database_url))

# Configure logging
if config.config_file_name:
    fileConfig(config.config_file_name)

# Metadata for 'autogenerate' support
target_metadata = AstraBase.metadata


# ---------------------------------------------------------------------------
# Migration functions
# ---------------------------------------------------------------------------
def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


# ---------------------------------------------------------------------------
# Run migrations
# ---------------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
