from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.base import BaseRepository
from app.models.visit import Visit

class VisitRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(model_class=Visit, db=db)

    async def get_by_account_number(self, account_number: str):
        stmt = select(Visit).filter(
            Visit.visit_account_number == account_number
        )
        result = await self.db.execute(stmt)

        return result.scalars().first()