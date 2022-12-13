from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel

from simple_sales.api.routers.cities import CityOut, CityInByID, CityInByData
from simple_sales.api.routers.employee_types import EmployeeTypeOut, EmployeeTypeInByID

router = APIRouter()


class EmployeeOut(BaseModel):
    id: UUID
    employee_type: EmployeeTypeOut
    first_name: str
    middle_name: str | None
    last_name: str
    city: CityOut


class EmployeeIn(BaseModel):
    employee_type: EmployeeTypeInByID
    first_name: str
    middle_name: str | None
    last_name: str
    city: CityInByID | CityInByData
