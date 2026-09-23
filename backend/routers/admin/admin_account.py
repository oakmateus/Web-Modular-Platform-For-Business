from fastapi import APIRouter, Depends, HTTPException, status

from dependencies import SessionDep
from ...database.models import Admin, AdminAccess

from ...schemas import admin_schemas

from ...validations import hash, email_validation, password_validation

from ...tokens import access, refresh

from ...config import settings

import uuid
from datetime import datetime, UTC, timedelta

router = APIRouter(prefix="/admin", tags=["Admin Account Management"])

# Administration Sing-Up

@router.post("/singup")
def admin_singup(db: SessionDep, data: admin_schemas.AdminAccount):
    email_validation.email_format(data.email)
    password_validation.requirements(data.password, data.password_confirm)

    account = db.query(Admin).filter(Admin.email == data.email).first()
    if account:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Não autorizado.")

    data.password = hash.hash(data.password)
    new_account = Admin(**data.dict())

    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account

# Administration Login

@router.post("/login")
def admin_login(db: SessionDep, data: admin_schemas.AdminAccount):
    email_validation.email_format(data)

    # Searching for an existing account and validating the credentials.

    account = db.query(Admin).filter(Admin.email == data.email).first()
    if not account:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="A senha ou e-mail são invalidos.")

    if not hash.verify(data.password, Admin.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="A senha ou e-mail são invalidos.")

    # Revoking any other past token.

    condition = db.query(AdminAccess).filter(AdminAccess.admin_id == Admin.admin_id)

    if condition:
        condition.update({"is_revoked": True})

    # Creating tokens and saving refresh token on the database.

    if data.remember_me == True:
        jti = uuid.uuid4()

        access_token = access.create_access_token(data={"admin_id": account.admin_id})
        refresh_token = refresh.create_refresh_token(data={"admin_id": account.admin_id,
                                                           "jti": str(jti)})

        db.add(
            AdminAccess(
                token_id=jti,
                admin_id=account.admin_id,
                is_revoked=False,
                expires_at=datetime.now(UTC) + timedelta(days=settings.refresh_token_expire_days),
                logout_at=None
            )
        )

        db.commit()

        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

    else:
        access_token = access.create_access_token(data={"admin_id": account.admin_id})
        return {"access_token": access_token, "token_type": "bearer"}
