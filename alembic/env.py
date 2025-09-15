import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# --- Alembic Configuration Start ---

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Project-Specific Modifications ---

# 1. Add the project's root directory to the Python path.
# This ensures that the script can find and import the 'app' module.
project_root = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# 2. Import your project's models and the declarative Base.
# This is crucial for the 'autogenerate' feature to detect changes in your models.
from app.database import Base
from app import models  # Explicitly import models to ensure they are registered with Base.metadata

# 3. Set the target_metadata to your project's Base.metadata.
# This tells Alembic what the desired database schema should look like.
target_metadata = Base.metadata

# --- End of Project-Specific Modifications ---


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

