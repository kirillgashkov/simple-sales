from asyncpg import Connection
from fastapi import APIRouter, Depends

from simple_sales.api.dependencies.db import get_db
from simple_sales.api.models import EmployeeTypeOut
from simple_sales.db.models import EmployeeType
from simple_sales.db.queries.employee_types import select_employee_types

router = APIRouter()


@router.get("/employee-types", response_model=list[EmployeeTypeOut])
async def get_employee_types(db: Connection = Depends(get_db)) -> list[EmployeeTypeOut]:
    employee_types = await select_employee_types(db)

    return [employee_type_to_employee_type_out(t) for t in employee_types]


def employee_type_to_employee_type_out(
    employee_type: EmployeeType,
) -> EmployeeTypeOut:
    return EmployeeTypeOut(
        id=employee_type.id,
        name=employee_type.name,
    )
