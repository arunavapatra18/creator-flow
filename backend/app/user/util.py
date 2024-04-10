from passlib.context import CryptContext

password_content = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_password_hash(password: str):
    return password_content.hash(password)


def verify_password(password: str, hashed_password: str):
    return password_content.verify(password, hashed_password)
