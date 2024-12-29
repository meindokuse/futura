from datetime import datetime, date

from sqlalchemy import Integer, String, JSON, Date, DateTime, ForeignKey, Time
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.models.peoples import Employer
from src.schemas.items import EventRead, ProductSchemaRead, EmployerInWorkDayRead
from src.db.database import Base


class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, auto_increment=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    type_product: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    components: Mapped[dict] = mapped_column(JSON, nullable=False)  # например вода:400ml (key:val)

    def to_read_model(self) -> "ProductSchemaRead":
        return ProductSchemaRead(
            id=self.id,
            name=self.name,
            type_product=self.type_product,
            description=self.description,
            components=self.components
        )


class Events(Base):
    __tablename__ = 'events'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, auto_increment=True)
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


# ОДИН ИЗ ВАРИАНТОВ ОСТАВИТЬ
class EmployerInWorkDay(Base):
    __tablename__ = 'employer_in_work_day'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, auto_increment=True)
    work_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    employer_id: Mapped[int] = mapped_column(Integer, ForeignKey('employer.id'), nullable=False)
    status: Mapped[int] = mapped_column(Integer, nullable=False)

    employer: Mapped["Employer"] = relationship("Employer", back_populates="work_days")

    def to_read_model(self) -> "EmployerInWorkDayRead":
        return EmployerInWorkDayRead(
            id=self.id,
            work_time=self.work_time,
            status=self.status,
            employer_id=self.employer_id,
        )
