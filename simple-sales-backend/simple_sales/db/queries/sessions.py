from datetime import datetime
from uuid import UUID

from asyncpg import Connection, exceptions

from simple_sales.db.errors import (
    ForeignKeyViolationError,
    InsertDidNotReturnError,
    ReferencedUserNotFoundError,
)
from simple_sales.db.models import Session


async def select_session(
    db: Connection,
    *,
    session_id: UUID,
    expires_after: datetime,
) -> Session | None:
    row = await db.fetchrow(
        """
        SELECT id, user_id, expires_at
        FROM sessions
        WHERE id = $1 AND expires_at > $2
        """,
        session_id,
        expires_after,
    )
    if not row:
        return None

    return Session(
        id=row["id"],
        user_id=row["user_id"],
        expires_at=row["expires_at"],
    )


async def insert_session(
    db: Connection,
    *,
    user_id: UUID,
    expires_at: datetime,
) -> Session:
    query, *params = (
        """
        INSERT INTO sessions (user_id, expires_at)
        VALUES ($1, $2)
        RETURNING id, user_id, expires_at
        """,
        user_id,
        expires_at,
    )

    try:
        row = await db.fetchrow(query, *params)
    except exceptions.ForeignKeyViolationError as e:
        if e.constraint_name == "sessions_user_id_fkey":
            raise ReferencedUserNotFoundError(user_id) from e
        raise ForeignKeyViolationError

    if not row:
        raise InsertDidNotReturnError()

    return Session(
        id=row["id"],
        user_id=row["user_id"],
        expires_at=row["expires_at"],
    )


async def delete_session(
    db: Connection,
    *,
    session_id: UUID,
) -> None:
    await db.execute(
        """
        DELETE FROM sessions
        WHERE id = $1
        """,
        session_id,
    )
