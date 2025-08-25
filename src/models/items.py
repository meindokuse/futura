from datetime import datetime, date, time
from typing import Dict

from sqlalchemy import Integer, String, JSON, Date, DateTime, ForeignKey, Time, Index, func
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.schemas.items import EventRead, WorkDayRead, LocationRead, CardRead, WorkDayLogsRead, EventReadLogs
from src.db.database import Base
from src.schemas.items import EventReadMain
from src.schemas.items import WorkDayProfileRead
from src.schemas.logs import LogsRead
from enum import Enum
from sqlalchemy import Enum as SAEnum

from src.utils.log_enum import LogType, LogAction


class Card(Base):
    __tablename__ = 'cards'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    exp: Mapped[str] = mapped_column(String, nullable=False)
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey('location.id'), nullable=True)

    location = relationship("Location")

    def to_read_model(self) -> "CardRead":
        return CardRead(
            id=self.id,
            title=self.title,
            description=self.description,
            location_id=self.location_id,
            exp=self.exp
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

    def read_for_logs(self) -> "EventReadLogs":
        return EventReadLogs(
            id=self.id,
            name=self.name,
            date_start=self.date_start,
            description=self.description,
            location_id=self.location_id
        )


class WorkDay(Base):
    __tablename__ = 'workdays'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    employer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('employer.id', ondelete="CASCADE"),
        nullable=False,
    )
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey('location.id'), nullable=False)
    work_date: Mapped[date] = mapped_column(Date, nullable=False)
    number_work: Mapped[int] = mapped_column(Integer, nullable=True)
    __table_args__ = (
        Index('idx_workdays_location_date', 'location_id', 'work_date'),
    )
    employer = relationship("Employer", back_populates="workdays")
    location = relationship("Location")

    def to_read_model(self) -> "WorkDayRead":
        return WorkDayRead(
            id=self.id,
            work_date=self.work_date,
            employer_fio=self.employer.fio,
            employer_id=self.employer_id,
            employer_work_type=self.employer.work_type,
            number_work=self.number_work,
        )

    def to_read_for_profile(self) -> "WorkDayProfileRead":
        return WorkDayProfileRead(
            id=self.id,
            work_date=self.work_date,
            number_work=self.number_work,
            location_name=self.location.name
        )

    def read_for_logs(self) -> "WorkDayLogsRead":
        return WorkDayLogsRead(
            id=self.id,
            work_date=self.work_date,
            employer_fio=self.employer.fio,
            location_id=self.location_id,
            number_work=self.number_work,
        )


from sqlalchemy import Date, Time, Index


class Logs(Base):
    __tablename__ = 'logs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey('location.id'), nullable=True)
    admin_id: Mapped[int] = mapped_column(Integer, ForeignKey('employer.id'), nullable=False)
    type: Mapped[LogType] = mapped_column(SAEnum(LogType, native_enum=False), nullable=False)
    action: Mapped[LogAction] = mapped_column(SAEnum(LogAction, native_enum=False), nullable=False)
    object_action: Mapped[str] = mapped_column(String, nullable=False)
    date_created: Mapped[date] = mapped_column(Date, server_default=func.current_date(), nullable=False)
    time_created: Mapped[time] = mapped_column(Time, server_default=func.current_time(), nullable=False)

    employer = relationship("Employer")
    location = relationship("Location")

    __table_args__ = (
        Index('ix_logs_date_created', 'date_created'),
    )

    def to_read_model(self) -> "LogsRead":
        return LogsRead(
            id=self.id,
            admin_name=self.employer.fio,
            type=self.type.value,
            action=self.action.value,
            object_action=self.object_action,
            date_created=self.date_created,
            time_created=self.time_created,
            location_name=self.location.name if self.location else None
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
