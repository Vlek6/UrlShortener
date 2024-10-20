from __future__ import annotations

import models
from sqids import Sqids
from sqlmodel import Session, select

sqids = Sqids()


def get_db_url_with_long_url(*, session: Session, url: str) -> models.UrlMapping | None:
    statement = select(models.UrlMapping).where(models.UrlMapping.original_url == url)
    return session.exec(statement).first()


def get_db_url_with_short_url(
    *,
    session: Session,
    url: str,
) -> models.UrlMapping | None:
    statement = select(models.UrlMapping).where(models.UrlMapping.short_url == url)
    return session.exec(statement).first()
