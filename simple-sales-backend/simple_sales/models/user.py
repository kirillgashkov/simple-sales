from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    id: UUID
    username: str
    password_hash: str
    employee_id: UUID
