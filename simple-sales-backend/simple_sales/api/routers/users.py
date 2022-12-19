import argon2
from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, status, Response

from simple_sales.api.dependencies.argon2 import get_password_hasher
from simple_sales.api.dependencies.auth import (
    get_current_user as get_current_user_dependency,
    verify_password_authorization_for_current_user,
)
from simple_sales.api.dependencies.db import get_db
from simple_sales.api.models import (
    CityIn,
    CityInReference,
    CityOut,
    EmployeeOut,
    EmployeeTypeOut,
    UserIn,
    UserPasswordIn,
    UserOut,
)
from simple_sales.db.errors import UsernameAlreadyExistsError
from simple_sales.db.models import Employee, User
from simple_sales.db.queries.cities import select_or_insert_city
from simple_sales.db.queries.employees import insert_employee, select_employee
from simple_sales.db.queries.users import insert_user, update_user

router = APIRouter()


_HTTP_409_USERNAME_ALREADY_EXISTS = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Username already exists",
)


@router.get("/users/current", response_model=UserOut)
async def get_current_user(
    current_user: User = Depends(get_current_user_dependency),
    db: Connection = Depends(get_db),
) -> UserOut:
    employee = await select_employee(db, employee_id=current_user.employee_id)

    assert employee is not None

    return _user_out_from_user_and_employee(current_user, employee)


@router.post("/users", response_model=UserOut)
async def create_user(
    user_in: UserIn,
    db: Connection = Depends(get_db),
    ph: argon2.PasswordHasher = Depends(get_password_hasher),
) -> UserOut:
    async with db.transaction():
        if isinstance(user_in.employee.city, CityIn):
            city = await select_or_insert_city(
                db,
                name=user_in.employee.city.name,
                region=user_in.employee.city.region,
            )
            city_id = city.id
        elif isinstance(user_in.employee.city, CityInReference):
            city_id = user_in.employee.city.id
        else:
            assert False

        employee = await insert_employee(
            db,
            employee_type_id=user_in.employee.employee_type.id,
            first_name=user_in.employee.first_name,
            middle_name=user_in.employee.middle_name,
            last_name=user_in.employee.last_name,
            city_id=city_id,
        )

        try:
            user = await insert_user(
                db,
                username=user_in.username,
                password_hash=ph.hash(user_in.password),
                employee_id=employee.id,
            )
        except UsernameAlreadyExistsError:
            raise _HTTP_409_USERNAME_ALREADY_EXISTS

    return _user_out_from_user_and_employee(user, employee)


@router.put(
    "/users/current/password",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    dependencies=[Depends(verify_password_authorization_for_current_user)],
)
async def update_current_user_password(
    user_password_in: UserPasswordIn,
    current_user: User = Depends(get_current_user_dependency),
    db: Connection = Depends(get_db),
    ph: argon2.PasswordHasher = Depends(get_password_hasher),
) -> Response:
    await update_user(
        db,
        user_id=current_user.id,
        new_password_hash=ph.hash(user_password_in.password),
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


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
