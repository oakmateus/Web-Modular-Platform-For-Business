from fastapi import status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt

from datetime import datetime, timedelta

from ..database.session import SessionDep
from ..database.models import Admin

from ..config import settings
from ..schemas import admin_inputs

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Token veifying and getting actual refresh token

def create_refresh_token(data: dict):
   to_encode = data.copy()

   expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
   to_encode.update({"admin_id": data["admin_id"],
                    "exp": expire,
                    "jti": data["jti"], 
                    "scope": "refresh",
                    "type": "refresh"})

   encoded_jwt = jwt.encode(to_encode, settings.refresh_token_secret_key, algorithm=settings.algorithm)

   return encoded_jwt

# Token current validation fields

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(
            token,
            settings.refresh_token_secret_key,
            algorithms=[settings.algorithm]
        )

        jti = payload.get("jti")

        if jti is None:
            raise credentials_exception

        admin_id = payload.get("admin_id")

        if admin_id is None:
            raise credentials_exception

        return admin_inputs.AccessTokenData(admin_id=admin_id, jti=jti)

    except JWTError:
        raise credentials_exception

def get_refresh_admin(token: str, db: SessionDep):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail="could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_token(token, credentials_exception)

    admin = db.query(Admin).filter(Admin.admin_id == token.admin_id).first()

    if not admin:
        raise credentials_exception

    return admin, token