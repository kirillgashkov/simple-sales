from uuid import UUID

from asyncpg import Connection

from simple_sales.db.models import City, Employee, EmployeeType


async def select_employees(db: Connection) -> list[Employee]:
    rows = await db.fetch(
        """
        SELECT
            employees.id,
            employee_types.id AS employee_type_id,
            employee_types.name AS employee_type_name,
            employees.first_name,
            employees.middle_name,
            employees.last_name,
            cities.id AS city_id,
            cities.name AS city_name,
            cities.region AS city_region
        FROM employees
        JOIN employee_types ON employee_types.id = employees.employee_type_id
        JOIN cities ON cities.id = employees.city_id
        """
    )

    def row_to_employee(row):
        return Employee(
            id=row["id"],
            employee_type=EmployeeType(
                id=row["employee_type_id"], name=row["employee_type_name"]
            ),
            first_name=row["first_name"],
            middle_name=row["middle_name"],
            last_name=row["last_name"],
            city=City(
                id=row["city_id"],
                name=row["city_name"],
                region=row["city_region"],
            ),
        )

    return [row_to_employee(row) for row in rows]


async def select_employees_by_employee_type_id(
    db: Connection, *, employee_type_id: UUID
) -> list[Employee]:
    rows = await db.fetch(
        """
        SELECT
            employees.id,
            employee_types.id AS employee_type_id,
            employee_types.name AS employee_type_name,
            employees.first_name,
            employees.middle_name,
            employees.last_name,
            cities.id AS city_id,
            cities.name AS city_name,
            cities.region AS city_region
        FROM employees
        JOIN employee_types ON employee_types.id = employees.employee_type_id
        JOIN cities ON cities.id = employees.city_id
        WHERE employee_types.id = $1
        """,
        employee_type_id,
    )

    def row_to_employee(row):
        return Employee(
            id=row["id"],
            employee_type=EmployeeType(
                id=row["employee_type_id"], name=row["employee_type_name"]
            ),
            first_name=row["first_name"],
            middle_name=row["middle_name"],
            last_name=row["last_name"],
            city=City(
                id=row["city_id"],
                name=row["city_name"],
                region=row["city_region"],
            ),
        )

    return [row_to_employee(row) for row in rows]
