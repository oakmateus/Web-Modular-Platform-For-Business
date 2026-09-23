from fastapi import Depends
from sqlmodel import Session
from typing import Annotated

from tokens import access, refresh
from database.session import get_db

# Access token dependency

AccessTokenDep = Annotated[str, Depends(access.get_access_admin)]

# Refresh token dependency

RefreshTokenDep = Annotated[str, Depends(refresh.get_refresh_admin)]

# Session dependency

SessionDep = Annotated[Session, Depends(get_db)]