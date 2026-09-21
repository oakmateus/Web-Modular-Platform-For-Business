from sqlmodel import SQLModel 
from pydantic import EmailStr
from typing import Optional
from uuid import UUID

class AdminInput(SQLModel):
    email: EmailStr
    password: str
    password_confirm: Optional[str] = None
    remember_me: Optional[bool] = None

class AccessTokenData(SQLModel):
    admin_id: Optional[int] = None

class RefreshTokenData(SQLModel):
    admin_id: Optional[int] = None
    jti: UUID | None = None