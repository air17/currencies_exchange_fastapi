from fastapi import APIRouter

from core.authentication import fastapi_auth, auth_backend
from core.schemas.users import UserRead, UserCreate

router = APIRouter()


router.include_router(fastapi_auth.get_auth_router(auth_backend), prefix="/jwt")
router.include_router(fastapi_auth.get_register_router(UserRead, UserCreate))
