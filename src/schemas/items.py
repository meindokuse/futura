from datetime import datetime, date

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str
    components: dict


class ProductRead(BaseModel):
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


class WorkDayRead(BaseModel):
    id: int
    work_time: datetime
    employer_fio: str
    status: int

class LocationCreate(BaseModel):
    address: str
    description: str
    image: str

class LocationRead(BaseModel):
    id: int
    address: str
    description: str
    image: str
