"""
Canonical Location model.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Location(BaseModel):
    """Normalized location."""

    model_config = ConfigDict(
        extra="forbid",
    )

    city: str | None = None
    region: str | None = None
    country: str | None = None