from datetime import datetime
from uuid import UUID

import argon2
from asyncpg import Connection
from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

from simple_sales.api.dependencies.db import get_db
from simple_sales.settings import API_SESSION_ID_COOKIE_NAME

ph = argon2.PasswordHasher()


class Session(BaseModel):
    id: UUID
    user_id: UUID
    expires_at: datetime


async def get_current_session(
    session_id: UUID | None = Cookie(None, alias=API_SESSION_ID_COOKIE_NAME),
    db: Connection = Depends(get_db),
) -> Session | None:
    if session_id is None:
        return None

    session_record = await db.fetchrow(
        """
        SELECT id, user_id, expires_at
        FROM sessions
        WHERE id = $1 AND expires_at > $2
        LIMIT 1
        """,
        session_id,
        datetime.utcnow(),
    )

    if session_record is None:
        return None

    return Session(**session_record)


_not_authenticated_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not authenticated",
    headers={"WWW-Authenticate": "Basic"},
)


_incorrect_username_or_password_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Basic"},
)


class PasswordAuthorization(BaseModel):
    user_id: UUID


async def get_current_password_authorization(
    credentials: HTTPBasicCredentials | None = Depends(HTTPBasic(auto_error=False)),
    session: Session | None = Depends(get_current_session),
    db: Connection = Depends(get_db),
) -> PasswordAuthorization | None:
    if not credentials:
        return None

    if credentials.username.lower() == "current":
        if not session:
            raise _incorrect_username_or_password_exception

        password_authorization = await _password_authorize_user(
            user_id=session.user_id, password=credentials.password, db=db
        )
    else:
        password_authorization = await _password_authorize_user(
            username=credentials.username, password=credentials.password, db=db
        )

    return password_authorization


async def _password_authorize_user(
    *, user_id: UUID | None, username: str | None, password: str, db: Connection
) -> PasswordAuthorization:
    if user_id and username:
        raise ValueError("Cannot specify both user_id and username")
    if not user_id and not username:
        raise ValueError("Must specify either user_id or username")

    with db.transaction():

        # Get user_id and password_hash

        if user_id:
            where_clause = "WHERE id = $1"
            where_clause_arg = user_id
        else:
            where_clause = "WHERE lower(username) = lower($1)"
            where_clause_arg = username

        record = await db.fetchrow(
            f"""
            SELECT id, password_hash
            FROM users
            {where_clause}
            LIMIT 1
            FOR UPDATE
            """,
            where_clause_arg,
        )

        if record is None:
            raise _incorrect_username_or_password_exception

        user_id, password_hash = record

        # Verify (and if needed rehash) password

        try:
            ph.verify(password_hash, password)
        except argon2.exceptions.VerifyMismatchError:
            raise _incorrect_username_or_password_exception

        if ph.check_needs_rehash(password_hash):
            await db.execute(
                """
                UPDATE users
                SET password_hash = $1
                WHERE id = $2
                """,
                ph.hash(password),
                user_id,
            )


class User(BaseModel):
    id: UUID
    username: str
    employee_id: UUID


async def get_current_user(
    authorization: (PasswordAuthorization | None) = Depends(
        get_current_password_authorization
    ),
    session: Session | None = Depends(get_current_session),
    db: Connection = Depends(get_db),
) -> User:
    if authorization is not None:
        user_id = authorization.user_id
    elif session is not None:
        user_id = session.user_id
    else:
        raise _not_authenticated_exception

    user_record = await db.fetchrow(
        """
        SELECT id, username, employee_id
        FROM users
        WHERE id = $1
        LIMIT 1
        """,
        user_id,
    )

    if user_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return User(**user_record)
