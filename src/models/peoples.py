from typing import Optional

from pygments.lexer import default
from sqlalchemy import Column, String, Integer, Date, Boolean, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.db.database import Base
from datetime import date, datetime

from src.schemas.items import EmployerInWorkDayRead
from src.schemas.peoples import EmployerRead, ResidentRead

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Integer, String, Boolean, JSON
from passlib.context import CryptContext


class Employer(Base):
    __tablename__ = 'employer'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    roles: Mapped[list[str]] = mapped_column(JSON, default=["employee"])
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    fio: Mapped[str] = mapped_column(String, nullable=False)
    work_type: Mapped[str] = mapped_column(String, nullable=False)
    contacts: Mapped[Optional[list[str]]] = mapped_column(JSON, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    work_days: Mapped[list["EmployerInWorkDayRead"]] = relationship("EmployerInWorkDay", back_populates="employer")

    def to_read_model(self) -> "EmployerRead":
        return EmployerRead(
            id=self.id,
            email=self.email,
            fio=self.fio,
            roles=self.roles,
            is_active=self.is_active,
            image=self.image,
            work_type=self.work_type,
            contacts=self.contacts,
            description=self.description,
            work_days=self.work_days
        )


class Residents(Base):
    __tablename__ = 'residents'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    image: Mapped[str] = mapped_column(String, nullable=False)
    fio: Mapped[str] = mapped_column(String, nullable=False)
    discount_value: Mapped[int] = mapped_column(Integer, nullable=False)

    def to_read_model(self) -> "ResidentRead":
        return ResidentRead(
            id=self.id,
            image=self.image,
            fio=self.fio,
            discount_value=self.discount_value
        )
