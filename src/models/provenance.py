"""
Provenance Model

Tracks where every value originated.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Provenance(BaseModel):
    """
    Provenance information for a field.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    field: str

    source: str

    method: str