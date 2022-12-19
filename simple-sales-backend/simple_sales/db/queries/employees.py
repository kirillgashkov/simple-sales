from typing import Any
from uuid import UUID

from asyncpg import Connection, Record

from simple_sales.db.errors import (
    InsertDidNotReturnError,
    SelectDidNotReturnAfterInsertError,
)
from simple_sales.db.models import City, Employee, EmployeeType


async def select_employees(
    db: Connection,
    *,
    employee_type_id: UUID | None = None,
) -> list[Employee]:
    query, params = _build_select_employees_query(
        where_employee_type_id_equals=employee_type_id,
    )
    rows = await db.fetch(query, *params)

    return [_employee_from_row(row) for row in rows]


async def select_employee(
    db: Connection,
    *,
    employee_id: UUID,
) -> Employee | None:
    query, params = _build_select_employees_query(
        where_employee_id_equals=employee_id,
        limit=1,
    )
    row = await db.fetchrow(query, *params)

    if not row:
        return None

    return _employee_from_row(row)


async def insert_employee(
    db: Connection,
    *,
    employee_type_id: UUID,
    first_name: str,
    middle_name: str | None,
    last_name: str,
    city_id: UUID,
) -> Employee:
    employee_id = await db.fetchval(
        """
        INSERT INTO employees (employee_type_id, first_name, middle_name, last_name, city_id)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id
        """,
        employee_type_id,
        first_name,
        middle_name,
        last_name,
        city_id,
    )
    if not employee_id:
        raise InsertDidNotReturnError()

    employee = await select_employee(db, employee_id=employee_id)
    if not employee:
        raise SelectDidNotReturnAfterInsertError()

    return employee


def _build_select_employees_query(
    *,
    where_employee_id_equals: UUID | None = None,
    where_employee_type_id_equals: UUID | None = None,
    limit: int | None = None,
) -> tuple[str, list[Any]]:
    params: list[Any] = []
    param_number = 0

    def param() -> str:
        nonlocal param_number
        param_number += 1
        return "$" + str(param_number)

    # Build the WHERE clause

    where_clause_conditions = []

    if where_employee_id_equals is not None:
        where_clause_conditions.append(f"employees.id = {param()}")
        params.append(where_employee_id_equals)

    if where_employee_type_id_equals is not None:
        where_clause_conditions.append(f"employee_types.id = {param()}")
        params.append(where_employee_type_id_equals)

    if where_clause_conditions:
        where_clause = "WHERE " + " AND ".join(where_clause_conditions)
    else:
        where_clause = ""

    # Build the LIMIT clause

    if limit is not None:
        limit_clause = f"LIMIT {param()}"
        params.append(limit)
    else:
        limit_clause = ""

    # Build the query

    query = f"""
        SELECT
            employees.id,
            employee_types.id AS employee_type_id,
            employee_types.name AS employee_type_name,
            employees.first_name,
            employees.middle_name,
            employees.last_name,
            cities.id AS city_id,
            cities.name AS city_name,
            cities.region AS city_region
        FROM employees
        JOIN employee_types ON employee_types.id = employees.employee_type_id
        JOIN cities ON cities.id = employees.city_id
        {where_clause}
        {limit_clause}
    """

    return query, params


def _employee_from_row(row: Record) -> Employee:
    return Employee(
        id=row["id"],
        employee_type=EmployeeType(
            id=row["employee_type_id"],
            name=row["employee_type_name"],
        ),
        first_name=row["first_name"],
        middle_name=row["middle_name"],
        last_name=row["last_name"],
        city=City(
            id=row["city_id"],
            name=row["city_name"],
            region=row["city_region"],
        ),
    )
