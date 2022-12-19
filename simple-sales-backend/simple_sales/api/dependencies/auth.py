from datetime import datetime
from uuid import UUID

import argon2
from asyncpg import Connection
from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from simple_sales.api.dependencies.argon2 import get_password_hasher
from simple_sales.api.dependencies.db import get_db
from simple_sales.db.models import User, Session
from simple_sales.db.queries.sessions import select_session
from simple_sales.db.queries.users import select_user, update_user
from simple_sales.settings import API_SESSION_ID_COOKIE_NAME


async def get_current_session(
    session_id: UUID | None = Cookie(None, alias=API_SESSION_ID_COOKIE_NAME),
    db: Connection = Depends(get_db),
) -> Session | None:
    if not session_id:
        return None

    session = await select_session(db, id=session_id, expires_after=datetime.now())

    if not session:
        return None

    return session


async def get_current_password_authorized_user(
    credentials: HTTPBasicCredentials | None = Depends(HTTPBasic()),
    db: Connection = Depends(get_db),
    ph: argon2.PasswordHasher = Depends(get_password_hasher),
) -> User | None:
    if not credentials:
        return None

    user = await select_user(db, username=credentials.username)

    if not user:
        return None

    try:
        ph.verify(user.password_hash, credentials.password)
    except argon2.exceptions.VerifyMismatchError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    if ph.check_needs_rehash(user.password_hash):
        user = await update_user(
            db, user_id=user.id, new_password_hash=ph.hash(credentials.password)
        )

    return user
