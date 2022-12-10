from uuid import UUID

from asyncpg import Record
from asyncpg.pool import PoolConnectionProxy
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from simple_sales.api.dependencies.db import get_db

router = APIRouter()


class CityOut(BaseModel):
    id: UUID
    city: str
    region: str | None


@router.get("/cities", response_model=list[CityOut])
async def get_cities(
    db: "PoolConnectionProxy[Record]" = Depends(get_db),
) -> list[CityOut]:
    records = await db.fetch("SELECT id, city, region FROM cities")
    return [CityOut(**r) for r in records]  # type: ignore  # See #1
