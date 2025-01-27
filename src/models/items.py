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

    def to_read_model(self) -> "ProductRead":
        return ProductRead(
            id=self.id,
            name=self.name,
            type_product=self.type_product,
            description=self.description,
            components=self.components
        )


class Events(Base):
    __tablename__ = 'events'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    day: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
    start: Mapped[datetime] = mapped_column(Time, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)

    def to_read_model(self) -> "EventRead":
        return EventRead(
            id=self.id,
            name=self.name,
            start=self.start,
            description=self.description
        )


class WorkDay(Base):
    __tablename__ = 'employer_in_work_day'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    work_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    employer_fio: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[int] = mapped_column(Integer, nullable=False)

    employer: Mapped["EmployerRead"] = relationship("Employer")

    def to_read_model(self) -> "WorkDayRead":
        return WorkDayRead(
            id=self.id,
            work_time=self.work_time,
            status=self.status,
            employer_fio=self.employer_fio,
        )


class Location(Base):
    __tablename__ = 'location'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    image: Mapped[str] = mapped_column(String, nullable=False)

    def to_read_model(self) -> "LocationRead":
        return LocationRead(
            id=self.id,
            address=self.address,
            description=self.description,
            image=self.image
        )
