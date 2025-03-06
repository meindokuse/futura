from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str
    type_product: str
    components: dict
    location_name: str



class ProductRead(BaseModel):
    id:int
    name: str
    description: str
    type_product: str
    components: dict
    location_name: str



class EventCreate(BaseModel):
    name: str
    date_start: datetime
    description: str
    location_name: Optional[str]



class EventRead(BaseModel):
    id: int
    name: str
    date_start: datetime
    description: str
    location_name: Optional[str]



class WorkDayRead(BaseModel):
    id: int
    work_time: datetime
    employer_fio: str
    employer_work_type: str
    location_name: str


class LocationCreate(BaseModel):
    name:str
    address: str
    description: str


class LocationRead(BaseModel):
    id: int
    name: str
    address: str
    description: str

