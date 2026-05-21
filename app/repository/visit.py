from sqlalchemy.orm import Session, joinedload
from app.repository.base import BaseRepository
from app.models.visit import Visit

class VisitRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(model_class=Visit, db=db)

    def get_by_account_number(self, account_number: str):
        record = self.db.query(Visit).filter(
            Visit.visit_account_number== account_number
        ).first()

        return record