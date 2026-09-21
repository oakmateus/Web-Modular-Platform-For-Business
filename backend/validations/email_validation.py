from fastapi import HTTPException, status
from pydantic import TypeAdapter, EmailStr

def email_format(data):
    email_adapter = TypeAdapter(EmailStr)

    try:
        email_adapter.validate_python(data.email)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                            detail="Formato de e-mail invalido.")   
    