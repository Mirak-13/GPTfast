import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection

from alembic import context

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from db.config import db_helper, DB_URL
from db.models import Base

target_metadata = Base.metadata

config.set_main_option("sqlalchemy.url", DB_URL)


def run_migrations_offline() -> None:
    """Запуск миграций в оффлайн-режиме."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: AsyncConnection) -> None:
    """Функция для запуска миграций в активном соединении."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Асинхронный запуск миграций."""
    async with db_helper.engine.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await db_helper.engine.dispose()


def run_migrations():
    """Выбираем онлайн или офлайн режим."""
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        asyncio.run(run_migrations_online())


run_migrations()
