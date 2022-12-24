from enum import Enum

from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, Query, status

from simple_sales.api.constants import EmployeeTypeName
from simple_sales.api.dependencies.auth import get_current_user_if_exists
from simple_sales.api.dependencies.db import get_db
from simple_sales.api.models import CityOut, EmployeeOut, EmployeeTypeOut
from simple_sales.db.models import Employee, User
from simple_sales.db.queries.employees import (
    select_employees,
    select_employees_by_employee_type_name,
)

router = APIRouter()


_HTTP_403_NOT_A_MANAGER_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Not a manager",
)


class EmployeeAction(str, Enum):
    ASSIGN_TASK_TO = "assign_task_to"


@router.get("/employees", response_model=list[EmployeeOut])
async def get_employees(
    *,
    choices_for: EmployeeAction | None = Query(None),
    user: User | None = Depends(get_current_user_if_exists),
    db: Connection = Depends(get_db)
) -> list[EmployeeOut]:
    if choices_for:
        if choices_for == EmployeeAction.ASSIGN_TASK_TO:
            if not user:
                raise _HTTP_403_NOT_A_MANAGER_EXCEPTION

            if user.employee.employee_type.name != EmployeeTypeName.MANAGER:
                raise _HTTP_403_NOT_A_MANAGER_EXCEPTION

            employees = await select_employees_by_employee_type_name(
                db, employee_type_name=EmployeeTypeName.SALESPERSON
            )

            assert user.employee.id not in (e.id for e in employees)

            employees = [user.employee, *employees]
        else:
            assert False
    else:
        employees = await select_employees(db)

    return [employee_to_employee_out(e) for e in employees]


def employee_to_employee_out(employee: Employee) -> EmployeeOut:
    return EmployeeOut(
        id=employee.id,
        employee_type=EmployeeTypeOut(
            id=employee.employee_type.id,
            name=employee.employee_type.name,
        ),
        first_name=employee.first_name,
        middle_name=employee.middle_name,
        last_name=employee.last_name,
        city=CityOut(
            id=employee.city.id,
            name=employee.city.name,
            region=employee.city.region,
        ),
    )
