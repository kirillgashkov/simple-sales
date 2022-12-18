class DatabaseError(Exception):
    pass


class InsertError(DatabaseError):
    pass


class InsertDidNotReturnError(InsertError):
    pass


class SelectDidNotReturnAfterInsertError(InsertError):
    pass


class UsernameAlreadyExistsError(InsertError):
    def __init__(self, username: str) -> None:
        self.username = username
