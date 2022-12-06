import fastapi

router = fastapi.APIRouter()


@router.post("/sessions")
def create_session() -> None:
    # - Body: 'username' (required), 'password' (required)
    # - Sets a session ID cookie
    ...


@router.delete("/sessions/current")
def delete_current_session() -> None:
    # - Authentication: required
    ...


@router.delete("/sessions")
def delete_sessions() -> None:
    # - Query parameters: 'user_id' (required) (could be 'current')
    # - Authentication: required
    ...
