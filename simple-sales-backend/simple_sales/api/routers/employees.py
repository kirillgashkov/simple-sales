from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel

from simple_sales.api.routers.cities import CityInByData, CityInByID, CityOut
from simple_sales.api.routers.employee_types import EmployeeTypeInByID, EmployeeTypeOut

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
