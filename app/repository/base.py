from typing import Any
from sqlalchemy.orm import Session

class BaseRepository:
    def __init__(self, model_class, db: Session):
        self.model_class = model_class
        self.db = db

    def add(self, record: Any):
        self.db.add(record)
        self.db.flush()
        self.db.refresh(record)