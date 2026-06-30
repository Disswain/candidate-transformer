"""
Canonical Education model.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Education(BaseModel):
    """Education entry."""

    model_config = ConfigDict(
        extra="forbid",
    )

    institution: str | None = None
    degree: str | None = None
    field: str | None = None

    start_date: str | None = None
    end_date: str | None = None