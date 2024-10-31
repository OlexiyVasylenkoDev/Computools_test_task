import json
from datetime import datetime
from pathlib import Path

from sqlalchemy import select, func

from app.core.db import async_session_maker
from app.core.filters import DateFilter
from app.models.benchmark import Benchmark
from app.schemas.benchmark import BenchmarkAveragePerformanceSchema
from app.core.config import settings


class BenchmarkRepository:
    def get_average(self, debug: bool, date_filter: DateFilter = None):
        if not date_filter.start_time or not date_filter.end_time:
            date_filter = None
        if debug:
            return self.get_average_from_json(date_filter)
        return self.get_average_from_db(date_filter)

    @staticmethod
    async def get_average_from_json(
        date_filter: DateFilter = None,
    ) -> BenchmarkAveragePerformanceSchema:
        json_path = Path(settings.DB_FILE)
        with json_path.open("r") as file:
            data = json.load(file)

        benchmarks = data.get("benchmarking_results", [])
        if date_filter:
            start_time = date_filter.start_time
            end_time = date_filter.end_time
            benchmarks = [
                b
                for b in benchmarks
                if start_time <= datetime.fromisoformat(b["timestamp"]) <= end_time
            ]

        if not benchmarks:
            return BenchmarkAveragePerformanceSchema(
                token_count=0,
                time_to_first_token=0,
                time_per_output_token=0,
                total_generation_time=0,
            )

        token_count = sum(b["token_count"] for b in benchmarks) / len(benchmarks)
        time_to_first_token = sum(b["time_to_first_token"] for b in benchmarks) / len(
            benchmarks
        )
        time_per_output_token = sum(
            b["time_per_output_token"] for b in benchmarks
        ) / len(benchmarks)
        total_generation_time = sum(
            b["total_generation_time"] for b in benchmarks
        ) / len(benchmarks)

        return BenchmarkAveragePerformanceSchema(
            token_count=token_count,
            time_to_first_token=time_to_first_token,
            time_per_output_token=time_per_output_token,
            total_generation_time=total_generation_time,
        )

    @staticmethod
    async def get_average_from_db(date_filter: DateFilter = None):
        async with async_session_maker() as session:
            query = select(
                func.avg(Benchmark.token_count),
                func.avg(Benchmark.time_to_first_token),
                func.avg(Benchmark.time_per_output_token),
                func.avg(Benchmark.total_generation_time),
            )
            if date_filter:
                query = query.filter(
                    Benchmark.timestamp.between(
                        date_filter.start_time, date_filter.end_time
                    )
                )
            result = await session.execute(query)
            return result()
