from typing import List, Optional

from pydantic import BaseModel



class ResidentCreate(BaseModel):
    image: str
    fio: str
    discount_value: int


class ResidentRead(BaseModel):
    id: int
    image: str
    fio: str
    discount_value: int


class EmployerCreate(BaseModel):
    email: str
    fio: str
    work_type: str
    roles: List[str]
    image: Optional[str] = None
    contacts: Optional[List[str]] = None
    description: Optional[str] = None
    hashed_password: str


class EmployerRead(BaseModel):
    id: int
    password: str
    email: str
    fio: str
    work_type: str
    roles: List[str]
    image: Optional[str] = None
    contacts: Optional[List[str]] = None
    description: Optional[str] = None



