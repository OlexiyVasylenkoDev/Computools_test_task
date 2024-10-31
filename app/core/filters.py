import datetime

from pydantic import BaseModel


class DateFilter(BaseModel):
    start_time: datetime.datetime | None = None
    end_time: datetime.datetime | None = None
