from asyncpg import Connection

from simple_sales.db.models import EmployeeType


async def select_employee_types(db: Connection) -> list[EmployeeType]:
    rows = await db.fetch(
        """
        SELECT id, name
        FROM employee_types
        """
    )
    return [EmployeeType(**row) for row in rows]
