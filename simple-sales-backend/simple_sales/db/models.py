from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Address(BaseModel):
    id: UUID
    postal_code: str
    city_id: UUID
    street: str
    house: str
    apartment: str | None
    note: str | None


class City(BaseModel):
    id: UUID
    name: str
    region: str | None


class Client(BaseModel):
    id: UUID
    organization_name: str
    city_id: UUID | None


class Contact(BaseModel):
    id: UUID
    client_id: UUID
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    phone: str | None
    email: str | None
    address_id: UUID | None
    note: str | None


class Contract(BaseModel):
    number: str
    client_id: UUID
    delivery_address_id: UUID | None
    delivery_from: datetime | None
    delivery_to: datetime | None
    warranty_from: datetime | None
    warranty_to: datetime | None
    description: str | None
    product_serial_numbers: list[str]


class EmployeeType(BaseModel):
    id: UUID
    name: str


class Employee(BaseModel):
    id: UUID
    employee_type_id: UUID
    first_name: str
    middle_name: str | None
    last_name: str
    city_id: UUID


class ProductModel(BaseModel):
    id: UUID
    name: str


class Product(BaseModel):
    serial_number: str
    product_model_id: UUID


class Session(BaseModel):
    id: UUID
    user_id: UUID
    expires_at: datetime


class TaskPriority(BaseModel):
    id: UUID
    level: int
    name: str


class TaskType(BaseModel):
    id: UUID
    name: str


class Task(BaseModel):
    id: UUID
    task_type_id: UUID
    task_priority_id: UUID
    note: str | None
    contact_id: UUID
    contract_number: str | None
    product_serial_number: str | None
    created_at: datetime
    due_at: datetime | None
    completed_at: datetime | None
    created_by: UUID
    assigned_to: UUID | None


class User(BaseModel):
    id: UUID
    username: str
    password_hash: str
    employee_id: UUID
