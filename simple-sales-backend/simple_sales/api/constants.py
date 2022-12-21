from enum import Enum


class EmployeeTypeName(str, Enum):
    MANAGER = "manager"
    SALESPERSON = "salesperson"
