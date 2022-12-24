from asyncpg import Connection, Record

from simple_sales.db.models import EmployeeType


async def select_employee_types(db: Connection) -> list[EmployeeType]:
    rows = await db.fetch(
        """
        SELECT id, name
        FROM employee_types
        """
    )

    def row_to_employee_type(row: Record) -> EmployeeType:
        return EmployeeType(
            id=row["id"],
            name=row["name"],
        )

    return [row_to_employee_type(row) for row in rows]
