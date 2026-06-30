"""
Canonical Experience model.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Experience(BaseModel):
    """Professional experience."""

    model_config = ConfigDict(
        extra="forbid",
    )

    company: str | None = None
    title: str | None = None

    start_date: str | None = None
    end_date: str | None = None

    description: str | None = None