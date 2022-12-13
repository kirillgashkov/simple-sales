from uuid import UUID

from asyncpg import Connection
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from simple_sales.api.dependencies.db import get_db

router = APIRouter()


class EmployeeTypeOut(BaseModel):
    id: UUID
    name: str


class EmployeeTypeInReference(BaseModel):
    id: UUID


@router.get("/employee-types", response_model=list[EmployeeTypeOut])
async def get_employee_types(db: Connection = Depends(get_db)) -> list[EmployeeTypeOut]:
    records = await db.fetch("SELECT id, name FROM employee_types")
    return [EmployeeTypeOut(**r) for r in records]
