"""
Canonical Links model.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class Links(BaseModel):
    """
    Normalized external profile links.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    linkedin: str | None = None

    github: str | None = None

    portfolio: str | None = None

    other: list[str] = Field(
        default_factory=list,
    )