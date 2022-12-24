from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CityIn(BaseModel):
    name: str
    region: str | None


class CityInReference(BaseModel):
    id: UUID


class CityOut(BaseModel):
    id: UUID
    name: str
    region: str | None


class CityOutReference(BaseModel):
    id: UUID


class AddressIn(BaseModel):
    postal_code: str
    city: CityIn | CityInReference
    street: str
    house: str
    apartment: str | None
    note: str | None


class AddressInReference(BaseModel):
    id: UUID


class AddressOut(BaseModel):
    id: UUID
    postal_code: str
    city: CityOut
    street: str
    house: str
    apartment: str | None
    note: str | None


class AddressOutReference(BaseModel):
    id: UUID


class ClientIn(BaseModel):
    organization_name: str
    city: CityIn | CityInReference | None


class ClientInReference(BaseModel):
    id: UUID


class ClientOut(BaseModel):
    id: UUID
    city: CityOut | None


class ClientOutReference(BaseModel):
    id: UUID


class ContactIn(BaseModel):
    client: ClientInReference
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    phone: str | None
    email: str | None
    address: AddressIn | AddressInReference | None
    note: str | None


class ContactInReference(BaseModel):
    id: UUID


class ContactOut(BaseModel):
    id: UUID
    client: ClientOut
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    phone: str | None
    email: str | None
    address: AddressOut | None
    note: str | None


class ContactOutReference(BaseModel):
    id: UUID


class ProductModelIn(BaseModel):
    name: str


class ProductModelInReference(BaseModel):
    id: UUID


class ProductModelOut(BaseModel):
    id: UUID
    name: str


class ProductModelOutReference(BaseModel):
    id: UUID


class ProductIn(BaseModel):
    serial_number: str
    product_model: ProductModelIn | ProductModelInReference


class ProductInReference(BaseModel):
    serial_number: str


class ProductOut(BaseModel):
    serial_number: str
    product_model: ProductModelOut


class ProductOutReference(BaseModel):
    serial_number: str


class ContractIn(BaseModel):
    number: str
    client: ClientInReference
    delivery_address: AddressIn | AddressInReference | None
    delivery_from: datetime | None
    delivery_to: datetime | None
    warranty_from: datetime | None
    warranty_to: datetime | None
    description: str | None
    products: list[ProductIn | ProductInReference]


class ContractInReference(BaseModel):
    number: str


class ContractOut(BaseModel):
    number: str
    client: ClientOut
    delivery_address: AddressOut | None
    delivery_from: datetime | None
    delivery_to: datetime | None
    warranty_from: datetime | None
    warranty_to: datetime | None
    description: str | None
    products: list[ProductOut]


class ContractOutReference(BaseModel):
    number: str


class EmployeeTypeIn(BaseModel):
    name: str


class EmployeeTypeInReference(BaseModel):
    id: UUID


class EmployeeTypeOut(BaseModel):
    id: UUID
    name: str


class EmployeeTypeOutReference(BaseModel):
    id: UUID


class EmployeeInCreate(BaseModel):
    employee_type: EmployeeTypeInReference
    first_name: str
    middle_name: str | None
    last_name: str
    city: CityInReference


class EmployeeInUpdate(BaseModel):
    first_name: str
    middle_name: str | None
    last_name: str
    city: CityInReference


class EmployeeInReference(BaseModel):
    id: UUID


class EmployeeOut(BaseModel):
    id: UUID
    employee_type: EmployeeTypeOut
    first_name: str
    middle_name: str | None
    last_name: str
    city: CityOut


class EmployeeOutReference(BaseModel):
    id: UUID


class TaskPriorityIn(BaseModel):
    level: int
    name: str


class TaskPriorityInReference(BaseModel):
    id: UUID


class TaskPriorityOut(BaseModel):
    id: UUID
    level: int
    name: str


class TaskPriorityOutReference(BaseModel):
    id: UUID


class TaskTypeIn(BaseModel):
    name: str


class TaskTypeInReference(BaseModel):
    id: UUID


class TaskTypeOut(BaseModel):
    id: UUID
    name: str


class TaskTypeOutReference(BaseModel):
    id: UUID


class TaskIn(BaseModel):
    task_type: TaskTypeInReference
    task_priority: TaskPriorityInReference
    note: str | None
    contact: ContactInReference
    contract: ContractInReference | None
    product: ProductInReference | None
    due_at: datetime | None
    assigned_to: EmployeeInReference | None


class TaskInReference(BaseModel):
    id: UUID


class TaskOut(BaseModel):
    id: UUID
    task_type: TaskTypeOut
    task_priority: TaskPriorityOut
    note: str | None
    contact: ContactOut
    contract: ContractOut | None
    product: ProductOut | None
    created_at: datetime
    due_at: datetime | None
    completed_at: datetime | None
    created_by: EmployeeOut
    assigned_to: EmployeeOut | None


class TaskOutReference(BaseModel):
    id: UUID


class UserInCreate(BaseModel):
    username: str
    password: str
    employee: EmployeeInCreate


class UserInUpdate(BaseModel):
    username: str
    employee: EmployeeInUpdate


class UserInReference(BaseModel):
    username: str


class UserPasswordIn(BaseModel):
    password: str


class UserOut(BaseModel):
    username: str
    employee: EmployeeOut


class UserOutReference(BaseModel):
    username: str
