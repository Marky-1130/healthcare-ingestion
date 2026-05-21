import uuid
from datetime import date
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Visit(Base):
    __tablename__ = "visits"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    visit_account_number: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    patient_id: Mapped[str] = mapped_column(
        ForeignKey("patients.id"),
        nullable=False,
    )

    visit_date: Mapped[date] = mapped_column(Date, nullable=False)
    reason: Mapped[str] = mapped_column(String(500), nullable=False)

    patient = relationship("Patient", back_populates="visits")