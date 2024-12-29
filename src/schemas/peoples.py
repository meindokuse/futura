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
    image: str
    fio: str
    work_type: str
    contacts: str
    description: str


class EmployerRead(BaseModel):
    id: int
    image: str
    fio: str
    work_type: str
    contacts: str
    description: str
    work_days: list
