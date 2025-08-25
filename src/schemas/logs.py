from datetime import datetime, date, time
from typing import Optional

from pydantic import BaseModel

from src.utils.log_enum import LogType, LogAction


class LogsCreate(BaseModel):
    admin_id: int
    type: LogType
    action: LogAction
    object_action: str
    location_id: Optional[int] = None


class LogsRead(BaseModel):
    id: int
    admin_name: str
    type: LogType
    action: LogAction
    object_action: str
    date_created: date
    time_created: time
    location_name: Optional[str] = None



class LogsFilters(BaseModel):
    type: Optional[str] = None
    action: Optional[str] = None
    date_created: Optional[date] = None
    location_id: Optional[int] = None
    page: int = 1
    limit: int = 20


