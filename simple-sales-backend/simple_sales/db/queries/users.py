from uuid import UUID

from asyncpg import Connection, Record
from pydantic import BaseModel

from simple_sales.db.queries.cities import City
from simple_sales.db.queries.employee_types import EmployeeType
from simple_sales.db.queries.employees import Employee


class User(BaseModel):
    id: UUID
    username: str
    password_hash: str
    employee: Employee


def insert_user(
    username: str, password_hash: str, employee_id: UUID, db: Connection
) -> UUID | None:
    return db.fetchval(
        """
        INSERT INTO users (username, password_hash, employee_id)
        VALUES ($1, $2, $3)
        RETURNING id
        """,
        username,
        password_hash,
        employee_id,
    )


def select_user_by_id(user_id: UUID, db: Connection) -> User | None:
    record = db.fetchrow(
        """
        SELECT
            u.id,
            u.username,
            u.password_hash,
            e.id AS employee_id,
            t.id AS employee_type_id,
            t.name AS employee_type_name,
            e.first_name,
            e.middle_name,
            e.last_name,
            c.id AS city_id,
            c.name AS city_name,
            c.region AS city_region
        FROM users u
        JOIN employees e ON e.id = u.employee_id
        JOIN employee_types t ON t.id = e.employee_type_id
        JOIN cities c ON c.id = e.city_id
        WHERE u.id = $1
        LIMIT 1
        """,
        user_id,
    )
    return _make_user(record) if record else None


def select_user_by_username(username: str, db: Connection) -> User | None:
    record = db.fetchrow(
        """
        SELECT
            u.id,
            u.username,
            u.password_hash,
            e.id AS employee_id,
            t.id AS employee_type_id,
            t.name AS employee_type_name,
            e.first_name,
            e.middle_name,
            e.last_name,
            c.id AS city_id,
            c.name AS city_name,
            c.region AS city_region
        FROM users u
        JOIN employees e ON e.id = u.employee_id
        JOIN employee_types t ON t.id = e.employee_type_id
        JOIN cities c ON c.id = e.city_id
        WHERE lower(u.username) = lower($1)
        LIMIT 1
        """,
        username,
    )
    return _make_user(record) if record else None


def exists_user_by_username(username: str, db: Connection) -> bool:
    return db.fetchval(
        """
        SELECT EXISTS (
            SELECT 1
            FROM users u
            WHERE lower(u.username) = lower($1)
            LIMIT 1
        )
        """,
        username,
    )


def _make_user(record: Record) -> User:
    employee_type = EmployeeType(
        id=record["employee_type_id"],
        name=record["employee_type_name"],
    )

    city = City(
        id=record["city_id"],
        name=record["city_name"],
        region=record["city_region"],
    )

    employee = Employee(
        id=record["employee_id"],
        employee_type=employee_type,
        first_name=record["first_name"],
        middle_name=record["middle_name"],
        last_name=record["last_name"],
        city=city,
    )

    return User(
        id=record["id"],
        username=record["username"],
        password_hash=record["password_hash"],
        employee=employee,
    )
