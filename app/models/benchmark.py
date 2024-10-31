import datetime

from app.core.db import Base
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column


class Benchmark(Base):
    request_id: Mapped[str] = mapped_column(String, primary_key=True, nullable=False)
    prompt_text: Mapped[str] = mapped_column(String, nullable=False)
    generated_text: Mapped[str] = mapped_column(String, nullable=False)
    token_count: Mapped[int] = mapped_column(Integer, nullable=False)
    time_to_first_token: Mapped[int] = mapped_column(Integer, nullable=False)
    time_per_output_token: Mapped[int] = mapped_column(Integer, nullable=False)
    total_generation_time: Mapped[int] = mapped_column(Integer, nullable=False)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
