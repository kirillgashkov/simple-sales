from abc import ABC, abstractmethod
from typing import Any, TypeVar

T = TypeVar("T", bound="Service")


class Service(ABC):
    async def __aenter__(self: T) -> T:
        await self.start()
        return self

    async def __aexit__(self, *args: Any, **kwargs: Any) -> None:
        await self.stop()

    @abstractmethod
    async def start(self) -> None:
        ...

    @abstractmethod
    async def stop(self) -> None:
        ...
