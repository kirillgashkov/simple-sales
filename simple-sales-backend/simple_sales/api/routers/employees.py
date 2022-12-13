from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel

from simple_sales.api.routers.cities import City, CityIn, CityInReference, CityOut
from simple_sales.api.routers.employee_types import (
    EmployeeType,
    EmployeeTypeInReference,
    EmployeeTypeOut,
)

router = APIRouter()


class Employee(BaseModel):
    id: UUID
    employee_type: EmployeeType
    first_name: str
    middle_name: str | None
    last_name: str
    city: City


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
