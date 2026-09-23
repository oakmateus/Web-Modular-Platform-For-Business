from fastapi import status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt

from datetime import datetime, timedelta

from ..database.session import SessionDep
from ..database.models import Admin

from ..config import settings
from ..schemas import admin_schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Access token creation

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire, 
                    "scope": "access"})

    encoded_jwt = jwt.encode(to_encode, settings.access_token_secret_key, algorithm=settings.algorithm)

    return encoded_jwt

# Token veifying and getting actual access token

def verify_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(
            token,
            settings.access_token_secret_key,
            algorithms=[settings.algorithm]
        )

        admin_id = payload.get("admin_id")

        if admin_id is None:
            raise credentials_exception

        return admin_schemas.AccessTokenData(admin_id=admin_id)

    except JWTError:
        raise credentials_exception

def get_access_admin(token: str, db: SessionDep):
   
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials.", headers={"WWW-Authenticate": "Bearer"})

    token = verify_token(token, credentials_exception)

    admin = db.query(Admin).filter(Admin.admin_id == token.admin_id).first()

    if not admin:
        raise credentials_exception

    return admin