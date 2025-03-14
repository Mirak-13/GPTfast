import os
from dotenv import load_dotenv

from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped
from sqlalchemy.testing.schema import mapped_column

load_dotenv()

DB_URL = os.getenv("DB_URL")


class Settings(BaseSettings):
    db_url: str = DB_URL
    db_echo: bool = False


settings = Settings()


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = True):
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )


db_helper = DatabaseHelper(url=settings.db_url, echo=settings.db_echo)


async def get_db():
    async with db_helper.session_factory() as session:
        yield session


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)
