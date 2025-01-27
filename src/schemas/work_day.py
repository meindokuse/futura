from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class WorkDayCreate(BaseModel):
    work_time: datetime
    employer_fio:str
    status: int

