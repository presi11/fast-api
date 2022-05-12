
  
from fastapi import APIRouter

from app.api.routers import (
  
    dog,

    root,

)

api_router = APIRouter()
api_router.include_router(root.router, prefix="/healt-check", tags=["Healt Check"])

api_router.include_router(dog.router, prefix="/dogs", tags=["Dogs"])
