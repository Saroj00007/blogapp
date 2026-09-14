from fastapi import FastAPI

from .api.v1.router import router
from .core.config import settings


app = FastAPI(
    title=settings.app_name , 
    version=settings.app_version , 
    debug=settings.debug
)



app.include_router(router=router , prefix="/api/v1")


    


