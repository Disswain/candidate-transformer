"""
Confidence Model

Stores confidence scores for individual fields and the overall profile.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class Confidence(BaseModel):
    """
    Confidence score (0.0 - 1.0) for every major field.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    full_name: float = Field(default=0.0, ge=0.0, le=1.0)

    emails: float = Field(default=0.0, ge=0.0, le=1.0)

    phones: float = Field(default=0.0, ge=0.0, le=1.0)

    location: float = Field(default=0.0, ge=0.0, le=1.0)

    headline: float = Field(default=0.0, ge=0.0, le=1.0)

    years_experience: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )

    skills: float = Field(default=0.0, ge=0.0, le=1.0)

    experience: float = Field(default=0.0, ge=0.0, le=1.0)

    education: float = Field(default=0.0, ge=0.0, le=1.0)

    links: float = Field(default=0.0, ge=0.0, le=1.0)

    overall: float = Field(default=0.0, ge=0.0, le=1.0)