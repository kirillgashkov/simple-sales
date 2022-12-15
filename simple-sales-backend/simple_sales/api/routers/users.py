from uuid import UUID

from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from simple_sales.api.dependencies.auth import get_current_user_id
from simple_sales.api.dependencies.db import get_db
from simple_sales.api.routers.cities import CityOut
from simple_sales.api.routers.employee_types import EmployeeTypeOut
from simple_sales.api.routers.employees import EmployeeOut
from simple_sales.db.queries.users import select_user_by_id

router = APIRouter()


class UserOut(BaseModel):
    username: str
    employee: EmployeeOut


@router.get("/users/current", response_model=UserOut)
async def get_current_user(
    user_id: UUID = Depends(get_current_user_id),
    db: Connection = Depends(get_db),
) -> UserOut:
    user = select_user_by_id(user_id, db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserOut(
        username=user.username,
        employee=EmployeeOut(
            id=user.employee.id,
            first_name=user.employee.first_name,
            middle_name=user.employee.middle_name,
            last_name=user.employee.last_name,
            employee_type=EmployeeTypeOut(
                id=user.employee.employee_type.id,
                name=user.employee.employee_type.name,
            ),
            city=CityOut(
                id=user.employee.city.id,
                name=user.employee.city.name,
                region=user.employee.city.region,
            ),
        ),
    )
