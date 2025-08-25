import json
from datetime import datetime, time, date
from typing import List, Optional

from pydantic import BaseModel


class WorkDayCreate(BaseModel):
    work_date: date
    employer_id: int
    location_id: int
    number_work: int


class WorkDayUpdate(BaseModel):
    id:int
    employer_id: int




class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        elif isinstance(obj, BaseModel):
            return obj.dict()
        return super().default(obj)
