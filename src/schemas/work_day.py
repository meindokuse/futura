from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class WorkDayCreate(BaseModel):
    work_time: datetime
    employer_id: int
    location_id: int

    def preprocess(self):
        if self.work_time.tzinfo is not None:
            self.work_time = self.work_time.replace(tzinfo=None)  # Убираем информацию о часовом поясе
        return self
