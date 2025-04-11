from datetime import datetime, date, time
from os import times_result
from typing import Optional

from pydantic import BaseModel


class CardCreate(BaseModel):
    name: str
    description: str
    category: str
    exp: str
    location_id: int


class CardRead(BaseModel):
    id: int
    name: str
    description: str
    category: str
    exp: str
    location_id: int


class EventCreate(BaseModel):
    name: str
    date_start: datetime
    description: str
    location_id: Optional[int] = None


class EventRead(BaseModel):
    id: int
    name: str
    date_start: datetime
    description: str
    location_name: Optional[str]

    class Config:
        orm_mode = True


class EventReadMain(BaseModel):
    id: int
    name: str
    date_start: datetime
    description: str


class EventsUpdate(BaseModel):
    name: Optional[str] = None
    date_start: Optional[datetime] = None
    description: Optional[str] = None
    location_id: Optional[int] = None

class WorkDayRead(BaseModel):
    id: int
    work_time: datetime
    employer_fio: str  # ФИО из таблицы Employer
    employer_work_type: str  # Должность из Employer (work_type)
    location_name: str  # Название локации из Location
    time_end: time

    class Config:
        orm_mode = True  # Для работы с SQLAlchemy ORM

    def model_dump_ext(self, **kwargs):
        # Переопределяем метод dict для преобразования datetime и time в строки
        data = super().model_dump(**kwargs)
        for key, value in data.items():
            if isinstance(value, (datetime, time)):  # Если значение — это datetime или time
                data[key] = value.isoformat()  # Преобразуем в строку в формате ISO
        return data


class LocationCreate(BaseModel):
    name: str
    address: str
    description: str


class LocationRead(BaseModel):
    id: int
    name: str
    address: str
    description: str

    class Config:
        orm_mode = True  # Для работы с SQLAlchemy ORM


class LocationUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None



# ПРИВАТНАЯ СХЕМА

class WorkDayFilter(BaseModel):
    employer_fio: Optional[str] = None
    location_id: Optional[int] = None
    work_type: Optional[str] = None
    page: int = 1
    limit: int = 10

