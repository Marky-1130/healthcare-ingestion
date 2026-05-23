import uuid
from datetime import datetime, UTC
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    mrn: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    person = relationship(
        "Person",
        uselist=False,
        back_populates="patient",
        cascade="all, delete-orphan",
    )

    visits = relationship(
        "Visit",
        back_populates="patient",
        cascade="all, delete-orphan",
    )