from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str
    type_product: str
    components: dict
    location_id: int


class ProductRead(BaseModel):
    id:int
    name: str
    description: str
    type_product: str
    components: dict

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

    class Config:
        orm_mode = True  # Для работы с SQLAlchemy ORM

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

