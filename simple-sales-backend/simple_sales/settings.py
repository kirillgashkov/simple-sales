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

API_SESSION_ID_COOKIE_NAME = "sid"
