from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class ResidentCreate(BaseModel):
    fio: str
    discount_value: int
    description: Optional[str] = None


class ResidentRead(BaseModel):
    id: int
    fio: str
    discount_value: int
    description: Optional[str]

    class Config:
        orm_mode = True




class ResidentReadForCards(BaseModel):
    id: int
    fio: str
    discount_value: int


class ResidentUpdate(BaseModel):
    fio: Optional[str] = None
    discount_value: Optional[int] = None
    description: Optional[str] = None


class EmployerCreate(BaseModel):
    email: str
    is_admin: bool
    date_of_birth: date
    fio: str
    work_type: str
    contacts: Optional[List[str]] = None
    description: Optional[str] = None
    location_id: int


class EmployerRead(BaseModel):
    id: int
    email: str
    hashed_password: str
    date_of_birth: date
    is_admin: bool
    fio: str
    work_type: str
    contacts: Optional[List[str]]
    description: Optional[str]
    location_name: str

    class Config:
        orm_mode = True


class EmployerReadForValidate(BaseModel):
    id: int
    email: str
    hashed_password: str
    is_admin: bool
    fio: str

    class Config:
        orm_mode = True


class EmployerReadForBirth(BaseModel):
    id: int
    fio: str
    work_type: str
    date_of_birth: date


class EmployerReadForCards(BaseModel):
    id: int
    fio: str
    work_type: str
    is_admin: bool

class EmployerReadLogs(BaseModel):
    id: int
    fio: str
    work_type: str
    is_admin: bool
    location_id: int


class EmployerUpdateAdmin(BaseModel):
    is_admin: Optional[bool] = None
    work_type: Optional[str] = None
    location_id: Optional[int] = None

class EmployerUpdateBasic(BaseModel):
    fio: Optional[str] = None
    contacts: Optional[List[str]] = None
    description: Optional[str] = None

