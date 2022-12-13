from uuid import UUID

from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from simple_sales.api.dependencies.auth import get_current_user_id
from simple_sales.api.dependencies.db import get_db
from simple_sales.api.routers.cities import CityOut
from simple_sales.api.routers.employee_types import EmployeeTypeOut
from simple_sales.api.routers.employees import EmployeeOut

router = APIRouter()


class UserOut(BaseModel):
    username: str
    employee: EmployeeOut


@router.get("/users/current", response_model=UserOut)
async def get_current_user(
    user_id: UUID = Depends(get_current_user_id),
    db: Connection = Depends(get_db),
) -> UserOut:
    user_out_record = await db.fetchrow(
        """
        SELECT
            u.username,
            e.id,
            t.id as employee_type_id,
            t.name as employee_type_name,
            e.first_name,
            e.middle_name,
            e.last_name,
            c.id as city_id,
            c.city as city_name,
            c.region as city_region
        FROM users u
        JOIN employees e ON u.employee_id = e.id
        JOIN employee_types t ON e.employee_type_id = t.id
        JOIN cities c ON e.city_id = c.id
        WHERE u.id = $1
        LIMIT 1
        """,
        user_id,
    )

    if user_out_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserOut(
        username=user_out_record["username"],
        employee=EmployeeOut(
            id=user_out_record["id"],
            employee_type=EmployeeTypeOut(
                id=user_out_record["employee_type_id"],
                name=user_out_record["employee_type_name"],
            ),
            first_name=user_out_record["first_name"],
            middle_name=user_out_record["middle_name"],
            last_name=user_out_record["last_name"],
            city=CityOut(
                id=user_out_record["city_id"],
                city=user_out_record["city_name"],
                region=user_out_record["city_region"],
            ),
        ),
    )
