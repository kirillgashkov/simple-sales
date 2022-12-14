from uuid import UUID

from asyncpg import Connection, exceptions

from simple_sales.db.errors import (
    ForeignKeyViolationError,
    InsertDidNotReturnError,
    ReferencedCityNotFoundError,
    ReferencedEmployeeTypeNotFoundError,
    SelectDidNotReturnAfterInsertError,
    SelectDidNotReturnAfterUpdateError,
    UniqueViolationError,
    UpdateDidNotReturnError,
    UsernameAlreadyExistsError,
)
from simple_sales.db.models import City, Employee, EmployeeType, User, UserPasswordHash


async def select_user_password_hash_by_username(
    db: Connection, *, username: str
) -> UserPasswordHash | None:
    row = await db.fetchrow(
        """
        SELECT id, password_hash
        FROM users
        WHERE lower(username) = lower($1)
        """,
        username,
    )
    if not row:
        return None

    return UserPasswordHash(
        user_id=row["id"],
        password_hash=row["password_hash"],
    )


async def select_user(db: Connection, *, user_id: UUID) -> User | None:
    row = await db.fetchrow(
        """
        SELECT
            users.id,
            users.username,
            employees.id AS employee_id,
            employee_types.id AS employee_type_id,
            employee_types.name AS employee_type_name,
            employees.first_name AS employee_first_name,
            employees.middle_name AS employee_middle_name,
            employees.last_name AS employee_last_name,
            cities.id AS employee_city_id,
            cities.name AS employee_city_name,
            cities.region AS employee_city_region
        FROM users
        JOIN employees ON employees.id = users.employee_id
        JOIN employee_types ON employee_types.id = employees.employee_type_id
        JOIN cities ON cities.id = employees.city_id
        WHERE users.id = $1
        """,
        user_id,
    )
    if not row:
        return None

    return User(
        id=row["id"],
        username=row["username"],
        employee=Employee(
            id=row["employee_id"],
            employee_type=EmployeeType(
                id=row["employee_type_id"],
                name=row["employee_type_name"],
            ),
            first_name=row["employee_first_name"],
            middle_name=row["employee_middle_name"],
            last_name=row["employee_last_name"],
            city=City(
                id=row["employee_city_id"],
                name=row["employee_city_name"],
                region=row["employee_city_region"],
            ),
        ),
    )


async def insert_user(
    db: Connection,
    *,
    username: str,
    password_hash: str,
    employee_type_id: UUID,
    employee_first_name: str,
    employee_middle_name: str | None,
    employee_last_name: str,
    employee_city_id: UUID,
) -> User:
    async with db.transaction():
        insert_employees_query, *insert_employees_params = (
            """
            INSERT INTO employees (
                employee_type_id,
                first_name,
                middle_name,
                last_name,
                city_id
            )
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id
            """,
            employee_type_id,
            employee_first_name,
            employee_middle_name,
            employee_last_name,
            employee_city_id,
        )

        try:
            employee_id = await db.fetchval(
                insert_employees_query, *insert_employees_params
            )
        except exceptions.ForeignKeyViolationError as e:
            if e.constraint_name == "employees_city_id_fkey":
                raise ReferencedCityNotFoundError(employee_city_id)
            elif e.constraint_name == "employees_employee_type_id_fkey":
                raise ReferencedEmployeeTypeNotFoundError(employee_type_id)
            raise ForeignKeyViolationError()

        if not employee_id:
            raise InsertDidNotReturnError()

        insert_users_query, *insert_users_params = (
            """
            INSERT INTO users (
                username,
                password_hash,
                employee_id
            )
            VALUES ($1, $2, $3)
            RETURNING id
            """,
            username,
            password_hash,
            employee_id,
        )

        try:
            user_id = await db.fetchval(insert_users_query, *insert_users_params)
        except exceptions.UniqueViolationError as e:
            if e.constraint_name == "users_username_lower_idx":
                raise UsernameAlreadyExistsError(username)
            raise UniqueViolationError()

        if not user_id:
            raise InsertDidNotReturnError()

    user = await select_user(db, user_id=user_id)
    if not user:
        raise SelectDidNotReturnAfterInsertError()

    return user


async def update_user(
    db: Connection,
    *,
    user_id: UUID,
    username: str,
    employee_first_name: str,
    employee_middle_name: str | None,
    employee_last_name: str,
    employee_city_id: UUID,
) -> User:
    async with db.transaction():
        update_employees_query, *update_employees_params = (
            """
            UPDATE employees
            SET first_name = $1, middle_name = $2, last_name = $3, city_id = $4
            WHERE id = (SELECT employee_id FROM users WHERE id = $5)
            RETURNING 1
            """,
            employee_first_name,
            employee_middle_name,
            employee_last_name,
            employee_city_id,
            user_id,
        )

        try:
            update_employees_row = await db.fetchrow(
                update_employees_query, *update_employees_params
            )
        except exceptions.ForeignKeyViolationError as e:
            if e.constraint_name == "employees_city_id_fkey":
                raise ReferencedCityNotFoundError(employee_city_id)
            raise ForeignKeyViolationError()

        if not update_employees_row:
            raise UpdateDidNotReturnError()

        update_users_query, *update_users_params = (
            """
            UPDATE users
            SET username = $1
            WHERE id = $2
            RETURNING id
            """,
            username,
            user_id,
        )

        try:
            returned_user_id = await db.fetchval(
                update_users_query, *update_users_params
            )
        except exceptions.UniqueViolationError as e:
            if e.constraint_name == "users_username_lower_idx":
                raise UsernameAlreadyExistsError(username)
            raise UniqueViolationError()

        if not returned_user_id:
            raise UpdateDidNotReturnError()

    user = await select_user(db, user_id=returned_user_id)
    if not user:
        raise SelectDidNotReturnAfterUpdateError()

    return user


async def update_user_password_hash(
    db: Connection, *, user_id: UUID, password_hash: str
) -> UserPasswordHash:
    row = await db.fetchrow(
        """
        UPDATE users
        SET password_hash = $1
        WHERE id = $2
        RETURNING id, password_hash
        """,
        password_hash,
        user_id,
    )
    if not row:
        raise UpdateDidNotReturnError()

    return UserPasswordHash(
        user_id=row["id"],
        password_hash=row["password_hash"],
    )
