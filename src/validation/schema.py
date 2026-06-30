"""
Validation schemas.

Contains reusable schema models used by the validation layer.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ValidationResult(BaseModel):
    """
    Stores validation results.
    """

    model_config = ConfigDict(extra="forbid")

    valid: bool = True

    errors: list[str] = Field(default_factory=list)

    warnings: list[str] = Field(default_factory=list)


class ProjectionValidation(BaseModel):
    """
    Projection configuration validation.
    """

    model_config = ConfigDict(extra="forbid")

    include_confidence: bool = True

    include_provenance: bool = True

    on_missing: Literal[
        "null",
        "omit",
        "error",
    ] = "null"