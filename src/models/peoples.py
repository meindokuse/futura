from datetime import date
from typing import Optional, List

from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Integer, String, Boolean, JSON

from src.db.database import Base
from src.schemas.peoples import EmployerRead, ResidentRead, EmployerReadForBirth, EmployerReadForCards, \
    EmployerReadForValidate


class Employer(Base):
    __tablename__ = 'employer'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=True)
    roles: Mapped[List[str]] = mapped_column(JSON, default=["employee"])
    fio: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    work_type: Mapped[str] = mapped_column(String, nullable=False)
    contacts: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey('location.id'), nullable=False)

    location = relationship("Location")
    workdays = relationship("WorkDay", back_populates="employer", cascade="all, delete-orphan")  # Каскад на уровне ORM

    def to_read_model(self) -> "EmployerRead":
        return EmployerRead(
            id=self.id,
            hashed_password=self.hashed_password,
            email=self.email,
            fio=self.fio,
            roles=self.roles,
            work_type=self.work_type,
            contacts=self.contacts,
            description=self.description,
            location_name=self.location.name,
        )

    def to_read_model_for_birth(self) -> EmployerReadForBirth:
        return EmployerReadForBirth(
            id=self.id,
            date_of_birth=self.date_of_birth,
            fio=self.fio,
            work_type=self.work_type
        )

    def to_read_model_for_cards(self) -> EmployerReadForCards:
        return EmployerReadForCards(
            id=self.id,
            fio=self.fio,
            work_type=self.work_type
        )

    def to_read_model_for_validate(self) -> EmployerReadForValidate:
        return EmployerReadForValidate(
            id=self.id,
            email=self.email,
            hashed_password=self.hashed_password,
            roles=self.roles,
            fio=self.fio,
        )


class Residents(Base):
    __tablename__ = 'residents'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fio: Mapped[str] = mapped_column(String, nullable=False)
    discount_value: Mapped[int] = mapped_column(Integer, nullable=False)
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey('location.id'), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    location = relationship("Location")

    def to_read_model(self) -> "ResidentRead":
        return ResidentRead(
            id=self.id,
            fio=self.fio,
            discount_value=self.discount_value,
            location_id=self.location_id,
            description=self.description,
        )
