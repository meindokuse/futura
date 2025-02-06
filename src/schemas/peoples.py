from typing import List, Optional

from pydantic import BaseModel



class ResidentCreate(BaseModel):
    fio: str
    discount_value: int


class ResidentRead(BaseModel):
    id: int
    fio: str
    discount_value: int


class EmployerCreate(BaseModel):
    email: str
    fio: str
    work_type: str
    roles: List[str]
    contacts: Optional[List[str]] = None
    description: Optional[str] = None
    hashed_password: str
    location_id: int


class EmployerRead(BaseModel):
    id: int
    password: str
    email: str
    fio: str
    work_type: str
    roles: List[str]
    contacts: Optional[List[str]] = None
    description: Optional[str] = None

class EmployerPut(BaseModel):
    email: str
    fio: str
    work_type: str
    contacts: Optional[List[str]] = None
    description: Optional[str] = None



