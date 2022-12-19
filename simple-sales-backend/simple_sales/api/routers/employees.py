from asyncpg import Connection
from fastapi import APIRouter, Depends

from simple_sales.api.dependencies.db import get_db
from simple_sales.api.models import CityOut, EmployeeOut, EmployeeTypeOut
from simple_sales.db.models import Employee
from simple_sales.db.queries.employees import select_employees

router = APIRouter()


@router.get("/employees", response_model=list[EmployeeOut])
async def get_employees(db: Connection = Depends(get_db)) -> list[EmployeeOut]:
    employees = await select_employees(db)
    return [_employee_out_from_employee(e) for e in employees]


def _employee_out_from_employee(employee: Employee) -> EmployeeOut:
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
