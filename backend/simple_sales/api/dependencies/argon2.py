import argon2

ph = argon2.PasswordHasher()


def get_password_hasher() -> argon2.PasswordHasher:
    return ph
