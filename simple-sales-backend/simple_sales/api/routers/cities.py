from uuid import UUID

from asyncpg import Connection
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from simple_sales.api.dependencies.db import get_db

router = APIRouter()


class City(BaseModel):
    id: UUID
    name: str
    region: str | None


async def insert_city(name: str, region: str, db: Connection) -> City | None:
    record = await db.fetchrow(
        """
        INSERT INTO cities (name, region)
        VALUES ($1, $2)
        RETURNING id, name, region
        """,
        name,
        region,
    )
    return City(**record) if record is not None else None


async def select_cities(db: Connection) -> list[City]:
    records = await db.fetch(
        """
        SELECT id, name, region
        FROM cities
        """
    )
    return [City(**r) for r in records]


async def select_city_by_id(city_id: UUID, db: Connection) -> City | None:
    record = await db.fetchrow(
        """
        SELECT id, name, region
        FROM cities
        WHERE id = $1
        LIMIT 1
        """,
        city_id,
    )
    return City(**record) if record is not None else None


async def select_city_by_name_and_region(
    name: str, region: str | None, db: Connection
) -> City | None:
    record = await db.fetchrow(
        """
        SELECT id, name, region
        FROM cities
        WHERE name = $1 AND region = $2
        LIMIT 1
        """,
        name,
        region,
    )
    return City(**record) if record is not None else None


class CityIn(BaseModel):
    name: str
    region: str | None


class CityInReference(BaseModel):
    id: UUID


class CityOut(BaseModel):
    id: UUID
    name: str
    region: str | None


@router.get("/cities", response_model=list[CityOut])
async def get_cities(db: Connection = Depends(get_db)) -> list[CityOut]:
    cities = await select_cities(db)
    return [CityOut(**c.dict()) for c in cities]
