from datetime import datetime
from uuid import UUID

from asyncpg import Connection
from fastapi import Cookie, Depends

from simple_sales.api.dependencies.db import get_db
from simple_sales.models.session import Session
from simple_sales.settings import API_SESSION_COOKIE_NAME


async def get_current_session(
    session_id: UUID | None = Cookie(None, alias=API_SESSION_COOKIE_NAME),
    db: Connection = Depends(get_db),
) -> Session | None:
    if session_id is None:
        return None

    record = await db.fetchrow(
        """
            SELECT
                id, user_id, created_at, expires_at
            FROM sessions
            WHERE id = $1 AND expires_at > $2
            LIMIT 1
        """,
        session_id,
        datetime.utcnow(),
    )

    if record is None:
        return None

    return Session(*record)
