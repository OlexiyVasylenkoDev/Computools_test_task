import app.api as api
from fastapi import FastAPI

app = FastAPI()
app.include_router(api.router)
