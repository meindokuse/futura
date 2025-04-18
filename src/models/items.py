from datetime import datetime, date, time
from typing import Dict

from sqlalchemy import Integer, String, JSON, Date, DateTime, ForeignKey, Time
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.schemas.items import EventRead, WorkDayRead, LocationRead, CardRead
from src.db.database import Base
from src.schemas.items import EventReadMain


class Card(Base):
    __tablename__ = 'cards'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    exp: Mapped[str] = mapped_column(String, nullable=False)
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey('location.id'), nullable=True)

    location = relationship("Location")

    def to_read_model(self) -> "CardRead":
        return CardRead(
            id=self.id,
            name=self.name,
            description=self.description,
            category=self.category,
            location_id=self.location_id,
        )


class Events(Base):
    __tablename__ = 'events'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    date_start: Mapped[date] = mapped_column(DateTime, nullable=False, default=date.today)
    description: Mapped[str] = mapped_column(String, nullable=False)
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey('location.id'), nullable=True)

    location = relationship("Location")

    def to_read_model(self) -> "EventRead":
        return EventRead(
            id=self.id,
            name=self.name,
            date_start=self.date_start,
            description=self.description,
            location_name=self.location.name if self.location else None
        )

    def to_read_model_second(self) -> "EventReadMain":
        return EventReadMain(
            id=self.id,
            name=self.name,
            date_start=self.date_start,
            description=self.description,
        )


class WorkDay(Base):
    __tablename__ = 'workdays'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    employer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('employer.id', ondelete="CASCADE"),  # Каскадное удаление на уровне БД
        nullable=False,
        index=True
    )
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey('location.id'), nullable=False)
    work_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    time_end: Mapped[time] = mapped_column(Time, nullable=True)

    employer = relationship("Employer", back_populates="workdays")  # Обратная связь
    location = relationship("Location")

    def to_read_model(self) -> "WorkDayRead":
        return WorkDayRead(
            id=self.id,
            work_time=self.work_time,
            employer_fio=self.employer.fio,
            employer_work_type=self.employer.work_type,
            time_end=self.time_end,
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
