import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# ------------------------------------------------------------
# Add project root to sys.path so Alembic can import core.*
# ------------------------------------------------------------
current_dir = os.path.dirname(os.path.realpath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, project_root)

# ------------------------------------------------------------
# Import database Base + models so Alembic sees metadata
# ------------------------------------------------------------
from core.database import Base, DATABASE_URL
from core import models  # this ensures Project & Task are imported

# ------------------------------------------------------------
# Alembic Config object
# ------------------------------------------------------------
config = context.config

# Set sqlalchemy.url from our DATABASE_URL
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Logging setup
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# This metadata is used for 'autogenerate' support.
target_metadata = Base.metadata


# ------------------------------------------------------------
# Offline migrations
# ------------------------------------------------------------
def run_migrations_offline() -> None:
    """Run migrations without a live DB connection."""
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ------------------------------------------------------------
# Online migrations
# ------------------------------------------------------------
def run_migrations_online() -> None:
    """Run migrations with a live DB connection."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# ------------------------------------------------------------
# Entry point
# ------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
