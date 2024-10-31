from app.core.base_schema import BaseSchema


class BenchmarkAveragePerformanceSchema(BaseSchema):
    token_count: float
    time_to_first_token: float
    time_per_output_token: float
    total_generation_time: float
