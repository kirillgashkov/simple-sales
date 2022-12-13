from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel

from simple_sales.api.routers.cities import CityOut

router = APIRouter()


class EmployeeOut(BaseModel):
    id: UUID
    employee_type: str
    first_name: str
    middle_name: str | None
    last_name: str
    city: CityOut
