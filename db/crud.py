from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .models import User
from .schemas import CreateTable


async def create_user_service(db: AsyncSession, user: CreateTable):
    user_table = User(name=user.name, email=user.email)
    db.add(user_table)
    await db.commit()
    await db.refresh(user_table)
    return user_table


async def get_user_service(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 20):
    query = select(User).where(User.id == user_id).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


