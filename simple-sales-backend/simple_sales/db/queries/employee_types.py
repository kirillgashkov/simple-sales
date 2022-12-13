from uuid import UUID

from asyncpg import Connection
from pydantic import BaseModel


class EmployeeType(BaseModel):
    id: UUID
    name: str


async def select_employee_types(db: Connection) -> list[EmployeeType]:
    records = await db.fetch(
        """
        SELECT id, name
        FROM employee_types
        """
    )
    return [EmployeeType(**r) for r in records]
