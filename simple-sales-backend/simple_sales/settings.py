import os
from typing import Callable, TypeVar, overload

T = TypeVar("T")


@overload
def setting(key: str) -> str:
    ...


@overload
def setting(key: str, cast: Callable[[str], T]) -> T:
    ...


def setting(key: str, cast: Callable[[str], T] | Callable[[str], str] = str) -> T | str:
    return cast(os.environ[key])


DB_DSN = setting("SIMPLE_SALES_BACKEND_DB_DSN", str)

API_SESSION_EXPIRE_SECONDS = 60 * 60 * 24 * 14
API_SESSION_ID_COOKIE_NAME = "sid"

API_SESSION_ID_COOKIE_PATH = setting(
    "SIMPLE_SALES_BACKEND_API_SESSION_ID_COOKIE_PATH", str
)
API_SESSION_ID_COOKIE_DOMAIN = setting(
    "SIMPLE_SALES_BACKEND_API_SESSION_ID_COOKIE_DOMAIN", str
)

API_CORS_ORIGINS = setting("SIMPLE_SALES_BACKEND_API_CORS_ORIGINS", str).split(",")
