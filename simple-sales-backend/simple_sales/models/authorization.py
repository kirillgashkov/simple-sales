from uuid import UUID

from pydantic import BaseModel


class Authorization(BaseModel):
    user_id: UUID
    is_password_proven: bool
