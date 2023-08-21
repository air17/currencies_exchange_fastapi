from fastapi import APIRouter

from api_v1.users import router as users_router
from api_v1.rates import router as rates_router

api_router = APIRouter()


api_router.include_router(users_router, prefix="/auth", tags=["auth"])
api_router.include_router(rates_router, prefix="/rates", tags=["rates"])
