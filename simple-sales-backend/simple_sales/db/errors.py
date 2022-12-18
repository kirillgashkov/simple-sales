class DatabaseError(Exception):
    pass


class InsertError(DatabaseError):
    pass


class InsertDidNotReturnError(InsertError):
    pass


class SelectDidNotReturnAfterInsertError(InsertError):
    pass
