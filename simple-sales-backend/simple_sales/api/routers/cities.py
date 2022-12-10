from uuid import UUID

from asyncpg import Connection
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from simple_sales.api.dependencies.db import get_db

router = APIRouter()


class CityOut(BaseModel):
    id: UUID
    city: str
    region: str | None


@router.get("/cities", response_model=list[CityOut])
async def get_cities(db: Connection = Depends(get_db)) -> list[CityOut]:
    records = await db.fetch("SELECT id, city, region FROM cities")
    return [CityOut(**r) for r in records]
