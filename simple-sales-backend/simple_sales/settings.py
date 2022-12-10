import os
from typing import Callable, TypeVar, overload

T = TypeVar("T")


@overload
def setting(key: str) -> str:
    ...


@overload
def setting(key: str, cast: Callable[[str], T]) -> T:
    ...


def setting(key, cast=str):
    return cast(os.environ[key])


DB_DSN = setting("SIMPLE_SALES_DB_DSN", str)
