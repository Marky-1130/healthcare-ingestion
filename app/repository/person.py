from sqlalchemy.orm import Session, joinedload
from app.repository.base import BaseRepository
from app.models.person import Person

class PersonRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(model_class=Person, db=db)