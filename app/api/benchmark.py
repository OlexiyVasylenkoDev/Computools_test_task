from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv

from app.core.filters import DateFilter
from app.repositories.benchmark import BenchmarkRepository
from app.schemas.benchmark import BenchmarkAveragePerformanceSchema
from app.core.config import settings

router = APIRouter()


@cbv(router)
class AveragePerformanceView:
    @router.get("/average")
    async def get(
        self, date_filter: Optional[DateFilter] = Depends(DateFilter)
    ) -> BenchmarkAveragePerformanceSchema:
        if not settings.DEBUG:
            raise HTTPException(
                status_code=403, detail="The feature is not ready for live yet"
            )
        result = await BenchmarkRepository().get_average(settings.DEBUG, date_filter)
        return result
