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
from simple_sales.db.queries.users import (
    select_user,
    select_user_password_hash_by_username,
    update_user_password_hash,
)
from simple_sales.settings import API_SESSION_ID_COOKIE_NAME

_AUTHENTICATE_HEADERS = {"WWW-Authenticate": "Basic"}

_HTTP_401_INVALID_USERNAME_OR_PASSWORD_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid username or password",
    headers=_AUTHENTICATE_HEADERS,
)

_HTTP_401_INVALID_SESSION_ID_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid session ID",
)

_HTTP_401_CREDENTIALS_AND_SESSION_ID_MATCH_DIFFERENT_USERS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Credentials and session ID match different users",
    headers=_AUTHENTICATE_HEADERS,
)

_HTTP_401_CREDENTIALS_WERE_PROVIDED_FOR_ANOTHER_USER_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Credentials were provided for another user",
    headers=_AUTHENTICATE_HEADERS,
)

_HTTP_401_NOT_AUTHENTICATED_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not authenticated",
    headers=_AUTHENTICATE_HEADERS,
)


async def get_current_session(
    session_id: UUID = Cookie(..., alias=API_SESSION_ID_COOKIE_NAME),
    db: Connection = Depends(get_db),
) -> Session:
    session = await _get_session_if_valid(session_id=session_id, db=db)

    if not session:
        raise _HTTP_401_INVALID_SESSION_ID_EXCEPTION

    return session


async def get_current_user(
    credentials: HTTPBasicCredentials | None = Depends(HTTPBasic(auto_error=False)),
    session_id: UUID | None = Cookie(None, alias=API_SESSION_ID_COOKIE_NAME),
    db: Connection = Depends(get_db),
    ph: argon2.PasswordHasher = Depends(get_password_hasher),
) -> User:
    if credentials:
        password_authorized_user_id = await _get_password_authorized_user_id(
            credentials=credentials,
            db=db,
            ph=ph,
        )

    if session_id:
        session = await _get_session_if_valid(session_id=session_id, db=db)

    if credentials and session:
        if password_authorized_user_id != session.user_id:
            raise _HTTP_401_CREDENTIALS_AND_SESSION_ID_MATCH_DIFFERENT_USERS_EXCEPTION

    if credentials:
        user_id = password_authorized_user_id
    elif session:
        user_id = session.user_id
    else:
        raise _HTTP_401_NOT_AUTHENTICATED_EXCEPTION

    user = await select_user(db, user_id=user_id)
    assert user is not None

    return user


async def verify_password_authorization_for_current_user(
    current_user: User = Depends(get_current_user),
    credentials: HTTPBasicCredentials = Depends(HTTPBasic(auto_error=True)),
    db: Connection = Depends(get_db),
    ph: argon2.PasswordHasher = Depends(get_password_hasher),
) -> None:
    current_password_authorized_user_id = await _get_password_authorized_user_id(
        credentials=credentials,
        db=db,
        ph=ph,
    )

    if current_password_authorized_user_id != current_user.id:
        raise _HTTP_401_CREDENTIALS_WERE_PROVIDED_FOR_ANOTHER_USER_EXCEPTION


async def _get_password_authorized_user_id(
    *, credentials: HTTPBasicCredentials, db: Connection, ph: argon2.PasswordHasher
) -> UUID:
    user_password_hash = await select_user_password_hash_by_username(
        db, username=credentials.username
    )

    if not user_password_hash:
        raise _HTTP_401_INVALID_USERNAME_OR_PASSWORD_EXCEPTION

    try:
        ph.verify(user_password_hash.password_hash, credentials.password)
    except argon2.exceptions.VerifyMismatchError:
        raise _HTTP_401_INVALID_USERNAME_OR_PASSWORD_EXCEPTION

    if ph.check_needs_rehash(user_password_hash.password_hash):
        user_password_hash = await update_user_password_hash(
            db,
            user_id=user_password_hash.user_id,
            password_hash=ph.hash(credentials.password),
        )

    return user_password_hash.user_id


async def _get_session_if_valid(*, session_id: UUID, db: Connection) -> Session | None:
    return await select_session(db, session_id=session_id, expires_after=datetime.now())
