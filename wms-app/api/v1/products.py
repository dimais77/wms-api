from fastapi import APIRouter


router = APIRouter(tags=["Products"])


@router.get("")
async def get_products():
    pass
