from datetime import date
from pydantic import BaseModel, field_validator

class VisitIngestSchema(BaseModel):
    mrn: str
    first_name: str
    last_name: str
    birth_date: date
    visit_account_number: str
    visit_date: date
    reason: str

    @field_validator("mrn")
    @classmethod
    def validate_mrn(cls, value: str):
        if not value.startswith("MRN-"):
            raise ValueError(
                "MRN must start with 'MRN-'"
            )
        return value
    
    @field_validator("visit_account_number")
    @classmethod
    def validate_visit_account_number(cls, value: str):
        if not value.startswith("VST-"):
            raise ValueError(
            "Visit account number must start with 'VST-'"
        )

        return value

    @field_validator("first_name", "last_name", "reason")
    @classmethod
    def validate_required_strings(cls, value: str):
        if not value.strip():
            raise ValueError("Field cannot be empty")
        
        return value.strip()