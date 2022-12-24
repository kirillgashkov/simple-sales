from asyncpg import Connection
from fastapi import APIRouter, Depends

from simple_sales.api.dependencies.db import get_db
from simple_sales.api.models import CityOut
from simple_sales.db.models import City
from simple_sales.db.queries.cities import select_cities

router = APIRouter()


@router.get("/cities", response_model=list[CityOut])
async def get_cities(db: Connection = Depends(get_db)) -> list[CityOut]:
    cities = await select_cities(db)

    return [city_to_city_out(c) for c in cities]


def city_to_city_out(city: City) -> CityOut:
    return CityOut(
        id=city.id,
        name=city.name,
        region=city.region,
    )
