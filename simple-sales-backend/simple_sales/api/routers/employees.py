from uuid import UUID

from asyncpg import Connection
from fastapi import APIRouter
from pydantic import BaseModel

from simple_sales.api.routers.cities import CityIn, CityInReference, CityOut
from simple_sales.api.routers.employee_types import (
    EmployeeTypeInReference,
    EmployeeTypeOut,
)
from simple_sales.db.queries.cities import City
from simple_sales.db.queries.employee_types import EmployeeType

router = APIRouter()


class Employee(BaseModel):
    id: UUID
    employee_type: EmployeeType
    first_name: str
    middle_name: str | None
    last_name: str
    city: City


def insert_employee(
    employee_type_id: UUID,
    first_name: str,
    middle_name: str | None,
    last_name: str,
    city_id: UUID,
    db: Connection,
) -> UUID:
    return db.fetchval(
        """
        INSERT INTO employees (employee_type_id, first_name, middle_name, last_name, city_id)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id
        """,
        employee_type_id,
        first_name,
        middle_name,
        last_name,
        city_id,
    )


def select_employee_by_id(employee_id: UUID, db: Connection) -> Employee | None:
    record = db.fetchrow(
        """
        SELECT
            e.id,
            t.id AS employee_type_id,
            t.name AS employee_type_name,
            e.first_name,
            e.middle_name,
            e.last_name,
            c.id AS city_id,
            c.name AS city_name,
            c.region AS city_region
        FROM employees e
        JOIN employee_types t ON t.id = e.employee_type_id
        JOIN cities c ON c.id = e.city_id
        WHERE id = $1
        LIMIT 1
        """,
        employee_id,
    )

    if record is None:
        return None

    employee_type = EmployeeType(
        id=record["employee_type_id"],
        name=record["employee_type_name"],
    )

    city = City(
        id=record["city_id"],
        name=record["city_name"],
        region=record["city_region"],
    )

    return Employee(
        id=record["id"],
        employee_type=employee_type,
        first_name=record["first_name"],
        middle_name=record["middle_name"],
        last_name=record["last_name"],
        city=city,
    )


class EmployeeIn(BaseModel):
    employee_type: EmployeeTypeInReference
    first_name: str
    middle_name: str | None
    last_name: str
    city: CityIn | CityInReference


class EmployeeOut(BaseModel):
    id: UUID
    employee_type: EmployeeTypeOut
    first_name: str
    middle_name: str | None
    last_name: str
    city: CityOut
