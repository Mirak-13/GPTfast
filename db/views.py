
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.config import get_db
from db.crud import create_user_service, get_user_service
from db.schemas import CreateTable, Table

router = APIRouter(prefix="/db", tags=["db"])

@router.post("/", response_model=Table)
async def create_user(user: CreateTable, db: Annotated[AsyncSession, Depends(get_db)]):
    new_user = await create_user_service(db, user)
    return new_user

@router.get("/{user_id}", response_model=list[Table])
async def get_user(user_id: int, skip: int = 0, limit: int = 20, db:AsyncSession = Depends(get_db)):
    user = await get_user_service(db, user_id, skip, limit)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user