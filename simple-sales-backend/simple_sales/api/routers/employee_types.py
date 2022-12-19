from asyncpg import Connection
from fastapi import APIRouter, Depends

from simple_sales.api.dependencies.db import get_db
from simple_sales.api.models import EmployeeTypeOut
from simple_sales.db.queries.employee_types import select_employee_types

router = APIRouter()


@router.get("/employee-types", response_model=list[EmployeeTypeOut])
async def get_employee_types(db: Connection = Depends(get_db)) -> list[EmployeeTypeOut]:
    employee_types = await select_employee_types(db)
    return [EmployeeTypeOut(**t.dict()) for t in employee_types]
