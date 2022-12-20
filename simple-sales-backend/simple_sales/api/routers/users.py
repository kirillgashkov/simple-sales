import argon2
from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, Response, status

from simple_sales.api.dependencies.argon2 import get_password_hasher
from simple_sales.api.dependencies.auth import (
    get_current_user as get_current_user_dependency,
)
from simple_sales.api.dependencies.auth import (
    verify_password_authorization_for_current_user,
)
from simple_sales.api.dependencies.db import get_db
from simple_sales.api.models import (
    CityOut,
    EmployeeOut,
    EmployeeTypeOut,
    UserInCreate,
    UserInUpdate,
    UserOut,
    UserPasswordIn,
)
from simple_sales.db.errors import (
    ReferencedCityNotFoundError,
    ReferencedEmployeeTypeNotFoundError,
    UsernameAlreadyExistsError,
)
from simple_sales.db.models import User
from simple_sales.db.queries.users import (
    insert_user,
    update_user,
    update_user_password_hash,
)

router = APIRouter()


_HTTP_409_USERNAME_ALREADY_EXISTS = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Username already exists",
)

_HTTP_400_REFERENCED_CITY_DOES_NOT_EXIST = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Referenced city does not exist",
)

_HTTP_400_REFERENCED_EMPLOYEE_TYPE_DOES_NOT_EXIST = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Referenced employee type does not exist",
)


@router.get("/users/current", response_model=UserOut)
async def get_current_user(
    current_user: User = Depends(get_current_user_dependency),
    db: Connection = Depends(get_db),
) -> UserOut:
    return user_to_user_out(current_user)


@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in_create: UserInCreate,
    db: Connection = Depends(get_db),
    ph: argon2.PasswordHasher = Depends(get_password_hasher),
) -> UserOut:
    try:
        user = await insert_user(
            db,
            username=user_in_create.username,
            password_hash=ph.hash(user_in_create.password),
            employee_type_id=user_in_create.employee.employee_type.id,
            employee_first_name=user_in_create.employee.first_name,
            employee_middle_name=user_in_create.employee.middle_name,
            employee_last_name=user_in_create.employee.last_name,
            employee_city_id=user_in_create.employee.city.id,
        )
    except UsernameAlreadyExistsError:
        raise _HTTP_409_USERNAME_ALREADY_EXISTS
    except ReferencedCityNotFoundError:
        raise _HTTP_400_REFERENCED_CITY_DOES_NOT_EXIST
    except ReferencedEmployeeTypeNotFoundError:
        raise _HTTP_400_REFERENCED_EMPLOYEE_TYPE_DOES_NOT_EXIST

    return user_to_user_out(user)


@router.put("/users/current", response_model=UserOut)
async def update_current_user(
    user_in_update: UserInUpdate,
    current_user: User = Depends(get_current_user_dependency),
    db: Connection = Depends(get_db),
) -> UserOut:
    try:
        user = await update_user(
            db,
            user_id=current_user.id,
            username=user_in_update.username,
            employee_type_id=user_in_update.employee.employee_type.id,
            employee_first_name=user_in_update.employee.first_name,
            employee_middle_name=user_in_update.employee.middle_name,
            employee_last_name=user_in_update.employee.last_name,
            employee_city_id=user_in_update.employee.city.id,
        )
    except UsernameAlreadyExistsError:
        raise _HTTP_409_USERNAME_ALREADY_EXISTS
    except ReferencedCityNotFoundError:
        raise _HTTP_400_REFERENCED_CITY_DOES_NOT_EXIST
    except ReferencedEmployeeTypeNotFoundError:
        raise _HTTP_400_REFERENCED_EMPLOYEE_TYPE_DOES_NOT_EXIST

    return user_to_user_out(user)


@router.put(
    "/users/current/password",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_password_authorization_for_current_user)],
)
async def update_current_user_password(
    user_password_in: UserPasswordIn,
    current_user: User = Depends(get_current_user_dependency),
    db: Connection = Depends(get_db),
    ph: argon2.PasswordHasher = Depends(get_password_hasher),
) -> Response:
    await update_user_password_hash(
        db,
        user_id=current_user.id,
        password_hash=ph.hash(user_password_in.password),
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


def user_to_user_out(user: User) -> UserOut:
    return UserOut(
        username=user.username,
        employee=EmployeeOut(
            id=user.employee.id,
            employee_type=EmployeeTypeOut(
                id=user.employee.employee_type.id,
                name=user.employee.employee_type.name,
            ),
            first_name=user.employee.first_name,
            middle_name=user.employee.middle_name,
            last_name=user.employee.last_name,
            city=CityOut(
                id=user.employee.city.id,
                name=user.employee.city.name,
                region=user.employee.city.region,
            ),
        ),
    )
