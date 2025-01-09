from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


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
    is_active: bool = True
    image: Optional[str] = None
    contacts: Optional[List[str]] = None
    description: Optional[str] = None
    hashed_password: str


class EmployerRead(BaseModel):
    id: int
    email: str
    fio: str
    work_type: str
    roles: List[str]
    is_active: bool = True
    image: Optional[str] = None
    contacts: Optional[List[str]] = None
    description: Optional[str] = None

