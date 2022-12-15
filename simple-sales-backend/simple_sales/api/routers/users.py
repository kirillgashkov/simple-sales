from uuid import UUID

import argon2
from asyncpg import Connection
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from simple_sales.api.dependencies.argon2 import get_password_hasher
from simple_sales.api.dependencies.auth import get_current_user_id
from simple_sales.api.dependencies.db import get_db
from simple_sales.api.routers.employees import EmployeeIn, EmployeeOut
from simple_sales.db.queries.users import User

router = APIRouter()


class UserIn(BaseModel):
    username: str
    password: str
    employee: EmployeeIn


class UserOut(BaseModel):
    username: str
    employee: EmployeeOut


@router.post("/users", response_model=UserOut)
async def create_user(
    user_in: UserIn,
    db: Connection = Depends(get_db),
    ph: argon2.PasswordHasher = Depends(get_password_hasher),
) -> UserOut:
    # async with db.transaction():
    #     if await exists_user_by_username(user_in.username, db):
    #         raise HTTPException(
    #             status_code=status.HTTP_409_CONFLICT,
    #             detail="Username already used",
    #         )

    #     if isinstance(user_in.employee.city, CityInReference):
    #         city_id = user_in.employee.city.id
    #     else:
    #         if city := await select_city_by_name_and_region(
    #             user_in.employee.city.name, user_in.employee.city.region, db
    #         ):
    #             city_id = city.id
    #         elif returned_city_id := await insert_city(
    #             user_in.employee.city.name, user_in.employee.city.region, db
    #         ):
    #             city_id = returned_city_id
    #         else:
    #             raise DatabaseError("Failed to insert city")

    #     employee_id = await insert_employee(
    #         user_in.employee.employee_type.id,
    #         user_in.employee.first_name,
    #         user_in.employee.middle_name,
    #         user_in.employee.last_name,
    #         city_id,
    #         db,
    #     )

    #     if employee_id is None:
    #         raise DatabaseError("Failed to insert employee")

    #     user_id = await insert_user(
    #         user_in.username,
    #         ph.hash(user_in.password),
    #         employee_id,
    #         db,
    #     )

    #     if user_id is None:
    #         raise DatabaseError("Failed to insert user")

    #     user = await select_user_by_id(user_id, db)

    #     if user is None:
    #         raise DatabaseError("Failed to select user")

    # return _make_user_out(user)

    # Note: The above solution requires reviewing regarding the use of the database.
    # Pay attention to possible errors that could be raised by asyncpg and city
    # insertion when it doesn't exist mechanism (what if there is parallel transaction
    # which is trying to do the same thing?).

    raise NotImplementedError()


@router.get("/users/current", response_model=UserOut)
async def get_current_user(
    user_id: UUID = Depends(get_current_user_id),
    db: Connection = Depends(get_db),
) -> UserOut:
    # user = await select_user_by_id(user_id, db)

    # if user is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="User not found",
    #     )

    # return _make_user_out(user)
    raise NotImplementedError()


def _make_user_out(user: User) -> UserOut:
    # return UserOut(
    #     username=user.username,
    #     employee=EmployeeOut(
    #         id=user.employee.id,
    #         first_name=user.employee.first_name,
    #         middle_name=user.employee.middle_name,
    #         last_name=user.employee.last_name,
    #         employee_type=EmployeeTypeOut(
    #             id=user.employee.employee_type.id,
    #             name=user.employee.employee_type.name,
    #         ),
    #         city=CityOut(
    #             id=user.employee.city.id,
    #             name=user.employee.city.name,
    #             region=user.employee.city.region,
    #         ),
    #     ),
    # )
    raise NotImplementedError()
