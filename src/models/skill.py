"""
Canonical Skill model.

Represents a normalized skill in the candidate profile.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Skill(BaseModel):
    """Normalized skill."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str