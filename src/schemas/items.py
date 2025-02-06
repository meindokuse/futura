from datetime import datetime, date

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str
    type_product: str
    components: dict



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


class EventRead(BaseModel):
    id: int
    name: str
    date_start: datetime
    description: str


class WorkDayRead(BaseModel):
    id: int
    work_time: datetime
    employer_fio: str
    status: int

class LocationCreate(BaseModel):
    name:str
    address: str
    description: str

class LocationRead(BaseModel):
    id: int
    name: str
    address: str
    description: str
