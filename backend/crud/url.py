from __future__ import annotations

from sqids import Sqids
from sqlmodel import Session, select

from backend import models

sqids = Sqids()


def get_db_url(*, session: Session, url: str) -> models.UrlMapping | None:
    statement = select(models.UrlMapping).where(models.UrlMapping.original_url == url)
    return session.exec(statement).first()


def shrink_url(*, input_url: str) -> str:
    # turn URL into list of ASCII values
    url_in_asci = [ord(c) for c in input_url]
    # Shrink using Sqids
    short_url = sqids.encode(url_in_asci)
    # Concat with service URL
    return f"localhost:8000/{short_url}"
