from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Integer, String, Boolean, JSON

from src.db.database import Base
from src.schemas.peoples import EmployerRead, ResidentRead


class Employer(Base):
    __tablename__ = 'employer'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    roles: Mapped[list[str]] = mapped_column(JSON, default=["employee"])
    # is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    fio: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    work_type: Mapped[str] = mapped_column(String, nullable=False)
    contacts: Mapped[Optional[list[str]]] = mapped_column(JSON, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    location_name: Mapped[str] = mapped_column(String, ForeignKey('location.name'), nullable=False)


    def to_read_model(self) -> "EmployerRead":
        return EmployerRead(
            id=self.id,
            password=self.hashed_password,
            email=self.email,
            fio=self.fio,
            roles=self.roles,
            work_type=self.work_type,
            contacts=self.contacts,
            description=self.description,
            location_name=self.location_name,
        )

class Residents(Base):
    __tablename__ = 'residents'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fio: Mapped[str] = mapped_column(String, nullable=False)
    discount_value: Mapped[int] = mapped_column(Integer, nullable=False)
    location_name: Mapped[str] = mapped_column(String, ForeignKey('location.name'), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)


    def to_read_model(self) -> "ResidentRead":
        return ResidentRead(
            id=self.id,
            fio=self.fio,
            discount_value=self.discount_value,
            location_name=self.location_name,
        )
