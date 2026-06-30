"""
Canonical Links model.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class Links(BaseModel):
    """External profile links."""

    model_config = ConfigDict(
        extra="forbid",
    )

    linkedin: HttpUrl | None = None
    github: HttpUrl | None = None
    portfolio: HttpUrl | None = None

    other: list[HttpUrl] = Field(default_factory=list)