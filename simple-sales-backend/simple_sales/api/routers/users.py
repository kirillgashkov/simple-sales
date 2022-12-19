from asyncpg import Connection
from fastapi import APIRouter, Depends

from simple_sales.api.dependencies.db import get_db
from simple_sales.api.dependencies.auth import (
    get_current_user as get_current_user_dependency,
)
from simple_sales.api.models import (
    CityOut,
    EmployeeOut,
    EmployeeTypeOut,
    UserOut,
    UserIn,
    EmployeeIn,
    CityIn,
    CityInReference,
    EmployeeTypeInReference,
)
from simple_sales.db.models import User, Employee
from simple_sales.db.queries.employees import select_employee, insert_employee
from simple_sales.db.queries.users import insert_user

router = APIRouter()


@router.get("/users/current", response_model=UserOut)
async def get_current_user(
    current_user: User = Depends(get_current_user_dependency),
    db: Connection = Depends(get_db),
) -> UserOut:
    employee = await select_employee(db, employee_id=current_user.employee_id)
    return _user_out_from_user_and_employee(current_user, employee)


def _user_out_from_user_and_employee(user: User, employee: Employee) -> UserOut:
    return UserOut(
        username=user.username,
        employee=EmployeeOut(
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
        ),
    )
