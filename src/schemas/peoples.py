from typing import List, Optional

from pydantic import BaseModel



class ResidentCreate(BaseModel):
    fio: str
    discount_value: int
    location_id: int
    description: Optional[str] = None

class ResidentRead(BaseModel):
    id: int
    fio: str
    discount_value: int
    description: Optional[str]

    class Config:
        orm_mode = True

class ResidentUpdate(BaseModel):
    fio: Optional[str] = None
    discount_value: Optional[int] = None
    location_id: Optional[int] = None
    description: Optional[str] = None



# class EmployerCreate(BaseModel):
#     email: str
#     fio: str
#     work_type: str
#     roles: List[str]
#     contacts: Optional[List[str]] = None
#     description: Optional[str] = None
#     hashed_password: str
#     location_name: str - СТАРАЯ МОДЕЛЬ

class EmployerCreate(BaseModel):
    email: str
    hashed_password: str
    roles: List[str] = ["employee"]
    fio: str
    work_type: str
    contacts: Optional[List[str]] = None
    description: Optional[str] = None
    location_id: int

class EmployerRead(BaseModel):
    id: int
    email: str
    hashed_password: str
    roles: List[str]
    fio: str
    work_type: str
    contacts: Optional[List[str]]
    description: Optional[str]
    location_name: str

    class Config:
        orm_mode = True


class EmployerUpdate(BaseModel):
    email: Optional[str] = None
    hashed_password: Optional[str] = None
    roles: Optional[List[str]] = None
    fio: Optional[str] = None
    work_type: Optional[str] = None
    contacts: Optional[List[str]] = None
    description: Optional[str] = None
    location_id: Optional[int] = None



