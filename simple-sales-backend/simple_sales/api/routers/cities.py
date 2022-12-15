from uuid import UUID

from asyncpg import Connection
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from simple_sales.api.dependencies.db import get_db

router = APIRouter()


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
    # cities = await select_cities(db)
    # return [CityOut(**c.dict()) for c in cities]
    return []
