from uuid import UUID

from asyncpg import Connection, exceptions

from simple_sales.db.errors import (
    InsertDidNotReturnError,
    SelectDidNotReturnAfterInsertError,
    SelectDidNotReturnAfterUpdateError,
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
        id=row["id"],
        password_hash=row["password_hash"],
    )


async def select_user(db: Connection, *, user_id: UUID) -> User | None:
    row = await db.fetchrow(
        """
        SELECT
            users.id,
            users.username,
            users.password_hash,
            users.employee_id,
            employees_types.id AS employee_type_id,
            employees_types.name AS employee_type_name,
            employees.first_name AS employee_first_name,
            employees.middle_name AS employee_middle_name,
            employees.last_name AS employee_last_name,
            cities.id AS city_id,
            cities.name AS city_name,
            cities.region AS city_region
        FROM users
        JOIN employees ON employees.id = users.employee_id
        JOIN employee_types ON employee_types.id = employees.employee_type_id
        JOIN cities ON cities.id = employees.city_id
        WHERE id = $1
        """,
        user_id,
    )
    if not row:
        return None

    return User(
        id=row["id"],
        username=row["username"],
        password_hash=row["password_hash"],
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
                id=row["city_id"],
                name=row["city_name"],
                region=row["city_region"],
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
    employee_middle_name: str,
    employee_last_name: str,
    city_id: UUID,
) -> User:
    query, *params = (
        """
        INSERT INTO users (
            username,
            password_hash,
            employee_id
        )
        VALUES ($1, $2, (
            INSERT INTO employees (
                employee_type_id,
                first_name,
                middle_name,
                last_name,
                city_id
            )
            VALUES ($3, $4, $5, $6, $7)
            RETURNING id
        ))
        RETURNING id
        """,
        username,
        password_hash,
        employee_type_id,
        employee_first_name,
        employee_middle_name,
        employee_last_name,
        city_id,
    )

    try:
        user_id = await db.fetchval(query, *params)
    except exceptions.UniqueViolationError as e:
        if e.constraint_name == "users_username_lower_idx":
            raise UsernameAlreadyExistsError(username)
        raise

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
    employee_type_id: UUID,
    employee_first_name: str,
    employee_middle_name: str,
    employee_last_name: str,
    city_id: UUID,
) -> User:
    async with db.transaction():
        query, *params = (
            """
            UPDATE users
            SET username = $1
            WHERE id = $2
            RETURNING id, employee_id
            """,
            username,
            user_id,
        )

        try:
            row = await db.fetchrow(query, *params)
        except exceptions.UniqueViolationError as e:
            if e.constraint_name == "users_username_lower_idx":
                raise UsernameAlreadyExistsError(username)
            raise

        if not row:
            raise UpdateDidNotReturnError()

        returned_user_id = row["id"]
        returned_employee_id = row["employee_id"]

        row = await db.fetchrow(
            """
            UPDATE employees
            SET employee_type_id = $1, first_name = $2, middle_name = $3, last_name = $4, city_id = $5
            WHERE id = $6
            RETURNING 1
            """,
            employee_type_id,
            employee_first_name,
            employee_middle_name,
            employee_last_name,
            city_id,
            returned_employee_id,
        )
        if not row:
            raise UpdateDidNotReturnError()

        user = await select_user(db, user_id=returned_user_id)
        if not user:
            raise SelectDidNotReturnAfterUpdateError()

    return user


async def update_user_password_hash(
    db: Connection, *, user_id: UUID, password_hash: str
) -> None:
    query, *params = (
        """
        UPDATE users
        SET password_hash = $1
        WHERE id = $2
        """,
        password_hash,
        user_id,
    )

    await db.execute(query, *params)
