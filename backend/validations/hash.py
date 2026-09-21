from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash(credential: str):
    return pwd_context.hash(credential)

def verify(plain_credential, hashed_credential):
    return pwd_context.verify(plain_credential, hashed_credential)