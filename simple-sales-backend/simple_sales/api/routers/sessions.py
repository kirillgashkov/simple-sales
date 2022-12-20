from datetime import datetime, timedelta

from asyncpg import Connection
from fastapi import APIRouter, Depends, Response, status

from simple_sales.api.dependencies.auth import (
    get_current_session_if_valid,
    get_current_user,
    verify_password_authorization_for_current_user,
)
from simple_sales.api.dependencies.db import get_db
from simple_sales.db.models import Session, User
from simple_sales.db.queries.sessions import delete_session as delete_session_from_db
from simple_sales.db.queries.sessions import insert_session
from simple_sales.settings import (
    API_SESSION_EXPIRE_SECONDS,
    API_SESSION_ID_COOKIE_DOMAIN,
    API_SESSION_ID_COOKIE_NAME,
    API_SESSION_ID_COOKIE_PATH,
)

router = APIRouter()


@router.post(
    "/sessions",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_password_authorization_for_current_user)],
)
async def create_session(
    current_user: User = Depends(get_current_user),
    db: Connection = Depends(get_db),
) -> Response:
    session = await insert_session(
        db,
        user_id=current_user.id,
        expires_at=datetime.utcnow() + timedelta(seconds=API_SESSION_EXPIRE_SECONDS),
    )

    response = Response()
    response.set_cookie(
        key=API_SESSION_ID_COOKIE_NAME,
        value=session.id.hex,
        max_age=API_SESSION_EXPIRE_SECONDS,
        path=API_SESSION_ID_COOKIE_PATH,
        domain=API_SESSION_ID_COOKIE_DOMAIN,
        secure=True,
        httponly=True,
        samesite="lax",
    )

    return response


@router.delete(
    "/sessions/current",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_session(
    current_session: Session | None = Depends(get_current_session_if_valid),
    db: Connection = Depends(get_db),
) -> Response:
    if current_session is None:
        return Response()

    await delete_session_from_db(db, session_id=current_session.id)

    response = Response()
    response.delete_cookie(
        key=API_SESSION_ID_COOKIE_NAME,
        path=API_SESSION_ID_COOKIE_PATH,
        domain=API_SESSION_ID_COOKIE_DOMAIN,
    )

    return response
