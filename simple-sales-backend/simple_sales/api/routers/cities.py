from asyncpg import Connection
from fastapi import APIRouter, Depends

from simple_sales.api.dependencies.db import get_db
from simple_sales.api.models import CityOut
from simple_sales.db.queries.cities import select_cities

router = APIRouter()


@router.get("/cities", response_model=list[CityOut])
async def get_cities(db: Connection = Depends(get_db)) -> list[CityOut]:
    cities = await select_cities(db)
    return [CityOut(**c.dict()) for c in cities]
