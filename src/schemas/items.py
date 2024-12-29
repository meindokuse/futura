from datetime import datetime, date

from pydantic import BaseModel

from src.schemas.peoples import EmployerRead


class ProductSchemaCreate(BaseModel):
    name: str
    description: str
    components: dict


class ProductSchemaRead(BaseModel):
    name: str
    description: str
    type_product: str
    components: dict


class EventCreate(BaseModel):
    name: str
    start: datetime
    description: str


class EventRead(BaseModel):
    id: int
    name: str
    start: datetime
    day: date
    description: str


class EmployerInWorkDayRead(BaseModel):
    id: int
    work_time: datetime
    status: int
    employer: EmployerRead


class EmployerInWorkDayCreate(BaseModel):
    work_time: datetime
    status: int
    employer: EmployerRead
