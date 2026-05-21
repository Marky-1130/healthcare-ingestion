from datetime import date
from pydantic import BaseModel

class VisitIngestSchema(BaseModel):
    mrn: str
    first_name: str
    last_name: str
    birth_date: date
    visit_account_number: str
    visit_date: date
    reason: str