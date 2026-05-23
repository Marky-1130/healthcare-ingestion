from typing import Any
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

class BaseRepository:
    def __init__(self, model_class, db: AsyncSession):
        self.model_class = model_class
        self.db = db

    async def add(self, record: Any):
        self.db.add(record)

        await self.db.flush()
        await self.db.refresh(record)