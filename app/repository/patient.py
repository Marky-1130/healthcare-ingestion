from typing import List
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.base import BaseRepository
from app.models.patient import Patient

class PatientRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(model_class=Patient, db=db)

    async def get_by_mrn(self, mrn: str):
        stmt = (
            select(Patient)
            .options(joinedload(Patient.person))
            .filter(Patient.mrn == mrn)
        )
        result = await self.db.execute(stmt)

        return result.scalars().first()
    
    async def get_by_id(self, id: str):
        stmt = (
            select(Patient)
            .options(
                joinedload(Patient.person),
                joinedload(Patient.visits),
            )
            .filter(Patient.id == id)
        )

        result = await self.db.execute(stmt)

        return result.scalars().first()
    
    async def get_patients(
        self,
        skip: int = 0,
        limit: int = 10,
        mrn: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> tuple[List[Patient], int]:

        stmt = select(Patient).options(
            joinedload(Patient.person),
            joinedload(Patient.visits),
        )

        if mrn:
            stmt = stmt.filter(Patient.mrn == mrn)

        if first_name:
            stmt = stmt.filter(Patient.person.has(first_name=first_name))

        if last_name:
            stmt = stmt.filter(Patient.person.has(last_name=last_name))

        # total count
        count_stmt = select(func.count()).select_from(stmt.subquery())

        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()

        # paginated items
        stmt = stmt.offset(skip).limit(limit)

        result = await self.db.execute(stmt)

        items = result.scalars().unique().all()

        return items, total