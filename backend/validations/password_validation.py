from fastapi import status, HTTPException
import re

def password_size(password: str):
    len_password = len(password)
    if len_password < 8:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                            detail="A senha não cumpre os requisitos.")

def password_have_number(password: str):    
    have_number = bool(re.search(r'\d', password))
    if have_number == False or have_number == None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                            detail="A senha não cumpre os requisitos.")

def password_is_upper(password: str):
    for e in password:
        if e.isupper() == True:
            break
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                            detail="A senha não cumpre os requisitos.")

def special_characters(password: str):    
    specials = "!@#$%^&*()_+"
    for e in specials:
        if bool(e in password) == True:
            break
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                            detail="A senha não cumpre os requisitos.")

def password_confirmation(password: str, confirm_password: str):
    if password != confirm_password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                            detail="As senhas precisam ser iguais.")
    
def requirements(password: str, confirm_password: str):
    password_size(password)
    password_have_number(password)
    password_is_upper(password)
    special_characters(password)
    password_confirmation(password, confirm_password)