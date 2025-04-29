from fastapi import APIRouter

from core import settings

router = APIRouter(
    prefix=settings.api.prefix
)
