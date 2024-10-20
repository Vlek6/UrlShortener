from collections.abc import Generator
from typing import Annotated

from database import engine
from fastapi import Depends
from sqlmodel import Session


# Dependency for providing database session from the SQLModel session pool
def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
