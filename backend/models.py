from __future__ import annotations

from datetime import datetime

from sqlmodel import Field, SQLModel


class UrlMapping(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    original_url: str = Field(index=True)
    short_url: str = Field(index=True, unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_access: datetime = Field(default=None)
    click_count: int = Field(default=0)
