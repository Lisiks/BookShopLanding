from passlib.context import CryptContext


class PasswordManager:
    __context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash_password(cls, plain_password: str) -> str:
        return cls.__context.hash(plain_password)


    @classmethod
    def verify_password(cls, plaint_password: str, hash_password: str) -> bool:
        return cls.__context.verify(plaint_password, hash_password)