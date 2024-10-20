from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from backend.database import engine


# Dependency for providing database session from the SQLModel session pool
def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
