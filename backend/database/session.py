from sqlmodel import Session, create_engine
from ..config import settings
from typing import Annotated
from fastapi import Depends

DATABASE_URL = f"{settings.database_url}"

engine = create_engine(
    DATABASE_URL,
    echo=True
)

def get_db():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]