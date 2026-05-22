from datetime import date
from datetime import datetime
from typing import List, Generic, TypeVar
from pydantic import BaseModel

class VisitResponse(BaseModel):
    id: str
    visit_account_number: str
    visit_date: date
    reason: str

class PersonResponse(BaseModel):
    first_name: str
    last_name: str
    birth_date: date

class PatientResponse(BaseModel):
    id: str
    mrn: str
    created_at: datetime
    person: PersonResponse
    visits: list[VisitResponse]

    class Config:
        from_attributes = True

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    page: int
    size: int
    total: int
    pages: int