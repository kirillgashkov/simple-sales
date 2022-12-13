from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from simple_sales.api.dependencies.auth import User
from simple_sales.api.dependencies.auth import (
    get_current_user as get_current_user_dependency,
)
from simple_sales.api.dependencies.db import get_db
from simple_sales.api.routers.cities import CityOut
from simple_sales.api.routers.employees import EmployeeOut

router = APIRouter()


class UserOut(BaseModel):
    username: str
    employee: EmployeeOut


@router.get("/users/current", response_model=UserOut)
async def get_current_user(
    user: User = Depends(get_current_user_dependency),
    db: Connection = Depends(get_db),
) -> UserOut:
    employee_out_record = await db.fetchrow(
        """
        SELECT
            e.id,
            t.name as employee_type,
            e.first_name,
            e.middle_name,
            e.last_name,
            c.id as city_id,
            c.city as city_name,
            c.region as city_region
        FROM employees e
        JOIN employee_types t ON e.employee_type_id = t.id
        JOIN cities c ON e.city_id = c.id
        WHERE e.id = $1
        LIMIT 1
        """,
        user.employee_id,
    )

    if employee_out_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    return UserOut(
        username=user.username,
        employee=EmployeeOut(
            id=employee_out_record["id"],
            employee_type=employee_out_record["employee_type"],
            first_name=employee_out_record["first_name"],
            middle_name=employee_out_record["middle_name"],
            last_name=employee_out_record["last_name"],
            city=CityOut(
                id=employee_out_record["city_id"],
                city=employee_out_record["city_name"],
                region=employee_out_record["city_region"],
            ),
        ),
    )
