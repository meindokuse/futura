from datetime import datetime, date

from sqlalchemy import Integer, String, JSON, Date, DateTime, ForeignKey, Time
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.schemas.items import EventRead, ProductRead, WorkDayRead, LocationRead
from src.db.database import Base
from src.schemas.peoples import EmployerRead


class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    type_product: Mapped[str] = mapped_column(String, nullable=False) 
    description: Mapped[str] = mapped_column(String, nullable=False)
    components: Mapped[dict] = mapped_column(JSON, nullable=False)  # например вода:400ml (key:val)
    location_name: Mapped[str] = mapped_column(String, ForeignKey('location.name'), nullable=False)

    def to_read_model(self) -> "ProductRead":
        return ProductRead(
            id=self.id,
            name=self.name,
            type_product=self.type_product,
            description=self.description,
            components=self.components,
            location_name=self.location_name
        )


class Events(Base):
    __tablename__ = 'events'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    date_start: Mapped[date] = mapped_column(DateTime, nullable=False, default=date.today)
    description: Mapped[str] = mapped_column(String, nullable=False)
    location_name: Mapped[str] = mapped_column(String, ForeignKey('location.name'), nullable=True)

    def to_read_model(self) -> "EventRead":
        return EventRead(
            id=self.id,
            name=self.name,
            date_start=self.date_start,
            description=self.description,
            location_name=self.location_name
        )


class WorkDay(Base):
    __tablename__ = 'workdays'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    work_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    employer_fio: Mapped[str] = mapped_column(String, ForeignKey('employer.fio'), nullable=False)
    employer_work_type: Mapped[str] = mapped_column(String, ForeignKey('employer.work_type'), nullable=True) # Потом исправить на False!!!
    location_name: Mapped[str] = mapped_column(String, ForeignKey('location.name'), nullable=False)

    employer: Mapped["EmployerRead"] = relationship("Employer")

    def to_read_model(self) -> "WorkDayRead":
        return WorkDayRead(
            id=self.id,
            work_time=self.work_time,
            employer_fio=self.employer_fio,
            work_type=self.employer_work_type,
            location_name=self.location_name
        )


class Location(Base):
    __tablename__ = 'location'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    address: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)

    def to_read_model(self) -> "LocationRead":
        return LocationRead(
            id=self.id,
            name=self.name,
            address=self.address,
            description=self.description,
        )
