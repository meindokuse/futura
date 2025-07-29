from datetime import datetime, time, date
from typing import List, Optional

from pydantic import BaseModel


class WorkDayCreate(BaseModel):
    work_date: date
    employer_id: int
    location_id: int
    number_work: int



class WorkDayUpdate(BaseModel):
    work_date: date
    employer_id: int
    location_id: int
    number_work: int
