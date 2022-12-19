from datetime import datetime
from typing import Any
from uuid import UUID

from asyncpg import Connection, Record

from simple_sales.db.errors import InsertDidNotReturnError
from simple_sales.db.models import Session


async def select_session(
    db: Connection,
    *,
    id: UUID,
    expires_after: datetime,
) -> Session | None:
    query, params = _build_select_sessions_query(
        where_id_equals=id,
        where_expires_at_greater_than=expires_after,
        limit=1,
    )
    row = await db.fetchrow(query, *params)

    if not row:
        return None

    return _session_from_row(row)


async def select_sessions(
    db: Connection,
    *,
    user_id: UUID | None = None,
    expires_after: datetime | None = None,
) -> list[Session]:
    query, params = _build_select_sessions_query(
        where_user_id_equals=user_id,
        where_expires_at_greater_than=expires_after,
    )
    rows = await db.fetch(query, *params)

    return [_session_from_row(row) for row in rows]


async def insert_session(
    db: Connection,
    *,
    user_id: UUID,
    expires_at: datetime,
) -> Session:
    row = await db.fetchrow(
        """
        INSERT INTO sessions (user_id, expires_at)
        VALUES ($1, $2)
        RETURNING id, user_id, expires_at
        """,
        user_id,
        expires_at,
    )
    if not row:
        raise InsertDidNotReturnError()

    return _session_from_row(row)


async def delete_session(
    db: Connection,
    *,
    id: UUID,
) -> None:
    await db.execute(
        """
        DELETE FROM sessions
        WHERE id = $1
        """,
        id,
    )


async def delete_sessions(
    db: Connection,
    *,
    user_id: UUID,
) -> None:
    await db.execute(
        """
        DELETE FROM sessions
        WHERE user_id = $1
        """,
        user_id,
    )


def _build_select_sessions_query(
    *,
    where_id_equals: UUID | None = None,
    where_user_id_equals: UUID | None = None,
    where_expires_at_greater_than: datetime | None = None,
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

    if where_id_equals is not None:
        where_clause_conditions.append(f"id = {param()}")
        params.append(where_id_equals)

    if where_user_id_equals is not None:
        where_clause_conditions.append(f"user_id = {param()}")
        params.append(where_user_id_equals)

    if where_expires_at_greater_than is not None:
        where_clause_conditions.append(f"expires_at > {param()}")
        params.append(where_expires_at_greater_than)

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
        SELECT id, user_id, expires_at
        FROM sessions
        {where_clause}
        {limit_clause}
    """

    return query, params


def _session_from_row(row: Record) -> Session:
    return Session(
        id=row["id"],
        user_id=row["user_id"],
        expires_at=row["expires_at"],
    )
