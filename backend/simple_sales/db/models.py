from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class City(BaseModel):
    id: UUID
    name: str
    region: str | None


class Address(BaseModel):
    id: UUID
    postal_code: str
    city: City
    street: str
    house: str
    apartment: str | None
    note: str | None


class Client(BaseModel):
    id: UUID
    organization_name: str
    city: City | None


class Contact(BaseModel):
    id: UUID
    client: Client
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    phone: str | None
    email: str | None
    address: Address | None
    note: str | None


class ProductModel(BaseModel):
    id: UUID
    name: str


class Product(BaseModel):
    serial_number: str
    product_model: ProductModel


class Contract(BaseModel):
    number: str
    client: Client
    delivery_address: Address | None
    delivery_from: datetime | None
    delivery_to: datetime | None
    warranty_from: datetime | None
    warranty_to: datetime | None
    description: str | None
    products: list[Product]


class EmployeeType(BaseModel):
    id: UUID
    name: str


class Employee(BaseModel):
    id: UUID
    employee_type: EmployeeType
    first_name: str
    middle_name: str | None
    last_name: str
    city: City


class TaskPriority(BaseModel):
    id: UUID
    level: int
    name: str


class TaskType(BaseModel):
    id: UUID
    name: str


class Task(BaseModel):
    id: UUID
    task_type: TaskType
    task_priority: TaskPriority
    note: str | None
    contact: Contact
    contract: Contract | None
    product: Product | None
    created_at: datetime
    due_at: datetime | None
    completed_at: datetime | None
    created_by: Employee
    assigned_to: Employee | None


class User(BaseModel):
    id: UUID
    username: str
    employee: Employee


class UserPasswordHash(BaseModel):
    user_id: UUID
    password_hash: str


class Session(BaseModel):
    id: UUID
    user_id: UUID
    expires_at: datetime
