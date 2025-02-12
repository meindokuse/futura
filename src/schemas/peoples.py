from typing import List, Optional

from pydantic import BaseModel



class ResidentCreate(BaseModel):
    fio: str
    discount_value: int
    location_name: str



class ResidentRead(BaseModel):
    id: int
    fio: str
    discount_value: int
    location_name: str



class EmployerCreate(BaseModel):
    email: str
    fio: str
    work_type: str
    roles: List[str]
    contacts: Optional[List[str]] = None
    description: Optional[str] = None
    hashed_password: str
    location_name: str


class EmployerRead(BaseModel):
    id: int
    password: str
    email: str
    fio: str
    work_type: str
    roles: List[str]
    contacts: Optional[List[str]] = None
    description: Optional[str] = None
    location_name: str


class EmployerPut(BaseModel):
    email: str
    fio: str
    work_type: str
    contacts: Optional[List[str]] = None
    description: Optional[str] = None
    location_name: str




