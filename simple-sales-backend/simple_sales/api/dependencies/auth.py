from datetime import datetime
from uuid import UUID

import argon2
from asyncpg import Connection
from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from simple_sales.api.dependencies.argon2 import get_password_hasher
from simple_sales.api.dependencies.db import get_db
from simple_sales.db.models import Session, User
from simple_sales.db.queries.sessions import select_session
from simple_sales.db.queries.users import select_user, update_user
from simple_sales.settings import API_SESSION_ID_COOKIE_NAME

_AUTHENTICATE_HEADER = {"WWW-Authenticate": "Basic"}

_INVALID_USERNAME_OR_PASSWORD_HTTP_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid username or password",
    headers=_AUTHENTICATE_HEADER,
)

_INVALID_SESSION_ID_HTTP_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid session ID",
)

_CREDENTIALS_AND_SESSION_ID_MATCH_DIFFERENT_USERS_HTTP_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Credentials and session ID match different users",
    headers=_AUTHENTICATE_HEADER,
)

_NOT_AUTHENTICATED_HTTP_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not authenticated",
    headers=_AUTHENTICATE_HEADER,
)


async def get_current_password_authorized_user(
    credentials: HTTPBasicCredentials = Depends(HTTPBasic(auto_error=True)),
    db: Connection = Depends(get_db),
    ph: argon2.PasswordHasher = Depends(get_password_hasher),
) -> User:
    return await _get_password_authorized_user(
        credentials=credentials,
        db=db,
        ph=ph,
    )


async def get_current_session(
    session_id: UUID = Cookie(..., alias=API_SESSION_ID_COOKIE_NAME),
    db: Connection = Depends(get_db),
) -> Session:
    session = await _get_session_if_valid(session_id=session_id, db=db)

    if not session:
        raise _INVALID_SESSION_ID_HTTP_EXCEPTION

    return session


async def get_current_user(
    credentials: HTTPBasicCredentials | None = Depends(HTTPBasic()),
    session_id: UUID | None = Cookie(None, alias=API_SESSION_ID_COOKIE_NAME),
    db: Connection = Depends(get_db),
    ph: argon2.PasswordHasher = Depends(get_password_hasher),
) -> User:
    if credentials:
        password_authorized_user = await _get_password_authorized_user(
            credentials=credentials,
            db=db,
            ph=ph,
        )

    if session_id:
        session = await _get_session_if_valid(session_id=session_id, db=db)

    if credentials and session:
        if password_authorized_user.id != session.user.id:
            raise _CREDENTIALS_AND_SESSION_ID_MATCH_DIFFERENT_USERS_HTTP_EXCEPTION

    if credentials:
        return password_authorized_user

    if session:
        return session.user

    raise _NOT_AUTHENTICATED_HTTP_EXCEPTION


async def _get_password_authorized_user(
    *, credentials: HTTPBasicCredentials, db: Connection, ph: argon2.PasswordHasher
) -> User:
    user = await select_user(db, username=credentials.username)

    if not user:
        raise _INVALID_USERNAME_OR_PASSWORD_HTTP_EXCEPTION

    try:
        ph.verify(user.password_hash, credentials.password)
    except argon2.exceptions.VerifyMismatchError:
        raise _INVALID_USERNAME_OR_PASSWORD_HTTP_EXCEPTION

    if ph.check_needs_rehash(user.password_hash):
        user = await update_user(
            db, user_id=user.id, new_password_hash=ph.hash(credentials.password)
        )

    return user


async def _get_session_if_valid(*, session_id: UUID, db: Connection) -> Session | None:
    return await select_session(db, id=session_id, expires_after=datetime.now())
