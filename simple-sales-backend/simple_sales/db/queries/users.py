from typing import Any
from uuid import UUID

from asyncpg import Connection, Record, exceptions

from simple_sales.db.errors import (
    InsertDidNotReturnError,
    UpdateDidNotReturnError,
    UsernameAlreadyExistsError,
)
from simple_sales.db.models import User


async def select_user(
    db: Connection,
    *,
    user_id: UUID | None = None,
    username: str | None = None,
) -> User | None:
    if not user_id and not username:
        raise ValueError("Must specify user_id or username")

    query, params = _build_select_users_query(
        where_user_id_equals=user_id,
        where_username_equals=username,
        limit=1,
    )
    row = await db.fetchrow(query, *params)

    if not row:
        return None

    return _user_from_row(row)


async def insert_user(
    db: Connection,
    *,
    username: str,
    password_hash: str,
    employee_id: UUID,
) -> User:
    query, *params = (
        """
        INSERT INTO users (username, password_hash, employee_id)
        VALUES ($1, $2, $3)
        RETURNING id, username, password_hash, employee_id
        """,
        username,
        password_hash,
        employee_id,
    )

    try:
        row = await db.fetchrow(query, *params)
    except exceptions.UniqueViolationError as e:
        if e.constraint_name == "users_username_lower_idx":
            raise UsernameAlreadyExistsError(username)
        else:
            raise

    if not row:
        raise InsertDidNotReturnError()

    return _user_from_row(row)


async def update_user(
    db: Connection,
    *,
    user_id: UUID,
    new_username: str | None = None,
    new_password_hash: str | None = None,
) -> User:
    if not new_username and not new_password_hash:
        raise ValueError("Must specify at least one field to update")

    query, params = _build_update_users_query(
        set_username=new_username,
        set_password_hash=new_password_hash,
        where_user_id_equals=user_id,
    )
    row = await db.fetchrow(query, *params)

    if not row:
        raise UpdateDidNotReturnError()

    return _user_from_row(row)


def _build_update_users_query(
    *,
    set_username: str | None = None,
    set_password_hash: str | None = None,
    where_user_id_equals: UUID,
) -> tuple[str, list[Any]]:
    params: list[Any] = []
    param_number = 0

    def param() -> str:
        nonlocal param_number
        param_number += 1
        return "$" + str(param_number)

    # Build the SET clause

    set_clause_assignments = []

    if set_username is not None:
        set_clause_assignments.append(f"username = {param()}")
        params.append(set_username)

    if set_password_hash is not None:
        set_clause_assignments.append(f"password_hash = {param()}")
        params.append(set_password_hash)

    if not set_clause_assignments:
        raise ValueError("Must specify at least one field to update")

    set_clause = "SET " + ", ".join(set_clause_assignments)

    # Build the WHERE clause

    where_clause = f"WHERE id = {param()}"
    params.append(where_user_id_equals)

    # Build the query

    query = f"""
        UPDATE users
        {set_clause}
        {where_clause}
        RETURNING id, username, password_hash, employee_id
    """

    return query, params


def _build_select_users_query(
    *,
    where_user_id_equals: UUID | None = None,
    where_username_equals: str | None = None,
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

    if where_user_id_equals is not None:
        where_clause_conditions.append(f"id = {param()}")
        params.append(where_user_id_equals)

    if where_username_equals is not None:
        where_clause_conditions.append(f"lower(username) = lower({param()})")
        params.append(where_username_equals)

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
        SELECT id, username, password_hash, employee_id
        FROM users
        {where_clause}
        {limit_clause}
    """

    return query, params


def _user_from_row(row: Record) -> User:
    return User(**row)
