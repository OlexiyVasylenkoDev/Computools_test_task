from fastapi import APIRouter

from . import benchmark

router = APIRouter()
router.include_router(benchmark.router, prefix="/results")
