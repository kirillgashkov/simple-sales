from datetime import datetime
from uuid import UUID

import argon2
from asyncpg import Connection
from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from simple_sales.api.dependencies.db import get_db
from simple_sales.models.authorization import Authorization
from simple_sales.models.session import Session
from simple_sales.settings import API_SESSION_ID_COOKIE_NAME

ph = argon2.PasswordHasher()


async def get_current_session(
    session_id: UUID | None = Cookie(None, alias=API_SESSION_ID_COOKIE_NAME),
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


async def get_current_authorization(
    credentials: HTTPBasicCredentials | None = Depends(HTTPBasic(auto_error=False)),
    session: Session | None = Depends(get_current_session),
    db: Connection = Depends(get_db),
) -> Authorization:
    unauthorized_headers = {"WWW-Authenticate": "Basic"}
    incorrect_username_or_password_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers=unauthorized_headers,
    )

    if credentials:
        if credentials.username.lower() == "current":
            if not session:
                raise incorrect_username_or_password_exception

            password_hash_record = await db.fetchrow(
                """
                    SELECT
                        password_hash
                    FROM users
                    WHERE id = $1
                    LIMIT 1
                    FOR UPDATE
                """,
                session.user_id,
            )

            if password_hash_record is None:
                raise incorrect_username_or_password_exception

            user_id = session.user_id
            (password_hash,) = password_hash_record
        else:
            user_id_password_hash_record = await db.fetchrow(
                """
                    SELECT
                        id, password_hash
                    FROM users
                    WHERE lower(username) = lower($1)
                    LIMIT 1
                    FOR UPDATE
                """,
                credentials.username,
            )

            if user_id_password_hash_record is None:
                raise incorrect_username_or_password_exception

            user_id, password_hash = user_id_password_hash_record

        try:
            ph.verify(password_hash, credentials.password)
        except argon2.exceptions.VerifyMismatchError:
            raise incorrect_username_or_password_exception

        if ph.check_needs_rehash(password_hash):
            await db.execute(
                """
                    UPDATE users
                    SET password_hash = $1
                    WHERE id = $2
                """,
                ph.hash(credentials.password),
                user_id,
            )

        return Authorization(user_id=user_id, is_password_proven=True)

    if session:
        return Authorization(user_id=session.user_id, is_password_proven=False)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers=unauthorized_headers,
    )
