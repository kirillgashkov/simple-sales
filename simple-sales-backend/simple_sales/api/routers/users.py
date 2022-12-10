from fastapi import APIRouter

router = APIRouter()


@router.post("/users")
def create_user() -> None:
    # - Body:
    #   - 'username' (required)
    #   - 'password' (required)
    #   - 'employee' (required)
    # - Sets a session ID cookie
    ...


@router.get("/users/current")
def get_current_user() -> None:
    # - Authentication: required
    ...


@router.delete("/users/current")
def delete_current_user() -> None:
    # - Body: 'password' (required)
    # - Authentication: required
    ...


@router.patch("/users/current")
def update_current_user() -> None:
    # - Body:
    #   - 'username' (optional)
    #   - 'employee' (optional, with optional sub-fields)
    # - Authentication: required
    ...


@router.put("/users/current/password")
def update_current_user_password() -> None:
    # - Body:
    #   - 'old_password' (required)
    #   - 'new_password' (required)
    # - Authentication: required
    ...
