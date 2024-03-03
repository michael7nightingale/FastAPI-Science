from random import randint

from passlib.hash import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.verify(password, hashed)


def generate_activation_code() -> str:
    return "".join(str(randint(0, 9)) for _ in range(6))
