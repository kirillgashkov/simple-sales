from uuid import UUID

from asyncpg import Connection
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from simple_sales.api.dependencies.db import get_db

router = APIRouter()


class EmployeeTypeInReference(BaseModel):
    id: UUID


class EmployeeTypeOut(BaseModel):
    id: UUID
    name: str


@router.get("/employee-types", response_model=list[EmployeeTypeOut])
async def get_employee_types(db: Connection = Depends(get_db)) -> list[EmployeeTypeOut]:
    # employee_types = await select_employee_types(db)
    # return [EmployeeTypeOut(**t.dict()) for t in employee_types]
    return []
