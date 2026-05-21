from datetime import date
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Person(Base):
    __tablename__ = "persons"

    id: Mapped[str] = mapped_column(
        ForeignKey("patients.id"),
        primary_key=True,
    )

    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)

    patient = relationship("Patient", back_populates="person")