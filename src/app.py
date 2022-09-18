# from loguru import logger
from fastapi import FastAPI
from mangum import Mangum

from .core import settings 
from .routers import router


app = FastAPI(debug=settings.DEBUG)
app.include_router(router)

handler = Mangum(app)

