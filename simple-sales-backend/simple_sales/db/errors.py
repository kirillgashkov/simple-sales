from uuid import UUID


class DatabaseError(Exception):
    pass


class InsertError(DatabaseError):
    pass


class InsertDidNotReturnError(InsertError):
    pass


class SelectDidNotReturnAfterInsertError(InsertError):
    pass


class UpdateError(DatabaseError):
    pass


class UpdateDidNotReturnError(UpdateError):
    pass


class SelectDidNotReturnAfterUpdateError(UpdateError):
    pass


class ConstraintViolationError(DatabaseError):
    pass


class UniqueViolationError(ConstraintViolationError):
    pass


class ForeignKeyViolationError(ConstraintViolationError):
    pass


class UsernameAlreadyExistsError(UniqueViolationError):
    def __init__(self, username: str) -> None:
        self.username = username


class ReferencedUserNotFoundError(ForeignKeyViolationError):
    def __init__(self, user_id: UUID) -> None:
        self.user_id = user_id


class ReferencedCityNotFoundError(ForeignKeyViolationError):
    def __init__(self, city_id: UUID) -> None:
        self.city_id = city_id


class ReferencedEmployeeTypeNotFoundError(ForeignKeyViolationError):
    def __init__(self, employee_type_id: UUID) -> None:
        self.employee_type_id = employee_type_id
