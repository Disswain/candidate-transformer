"""
Application Configuration Service.

Loads and validates runtime configuration.

Supports:
- default.json
- custom.json

Provides one configuration object to the
entire application.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


# ==========================================================
# Projection Models
# ==========================================================


class ProjectionField(BaseModel):
    """
    One projected output field.
    """

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    path: str

    from_: str | None = Field(
        default=None,
        alias="from",
    )


class ProjectionConfig(BaseModel):
    """
    Projection configuration.
    """

    model_config = ConfigDict(extra="forbid")

    include_confidence: bool = True

    include_provenance: bool = True

    on_missing: str = "null"


# ==========================================================
# Normalization
# ==========================================================


class NormalizationConfig(BaseModel):
    """
    Normalization configuration.
    """

    model_config = ConfigDict(extra="forbid")

    default_country: str = "IN"

    proper_case_names: bool = True

    deduplicate_skills: bool = True


# ==========================================================
# Application Config
# ==========================================================


class AppConfig(BaseModel):
    """
    Root application configuration.
    """

    model_config = ConfigDict(extra="forbid")

    confidence_weights: dict[str, float]

    source_priority: list[str]

    fields: list[ProjectionField] = Field(
        default_factory=list
    )

    projection: ProjectionConfig

    normalization: NormalizationConfig


# ==========================================================
# Config Service
# ==========================================================


class ConfigService:

    def __init__(
        self,
        default_path: str,
        custom_path: str | None = None,
    ) -> None:

        config = self._load(default_path)

        if custom_path:

            custom = self._load(custom_path)

            config = self._merge(
                config,
                custom,
            )

        self._config = AppConfig.model_validate(config)

    # --------------------------------------------------

    @staticmethod
    def _load(
        path: str,
    ) -> dict:

        file = Path(path)

        if not file.exists():
            raise FileNotFoundError(path)

        with file.open(
            "r",
            encoding="utf-8",
        ) as f:

            return json.load(f)

    # --------------------------------------------------

    @staticmethod
    def _merge(
        base: dict,
        override: dict,
    ) -> dict:

        merged = deepcopy(base)

        for key, value in override.items():

            if (
                key in merged
                and isinstance(merged[key], dict)
                and isinstance(value, dict)
            ):

                merged[key] = ConfigService._merge(
                    merged[key],
                    value,
                )

            else:

                merged[key] = value

        return merged

    # --------------------------------------------------

    @property
    def config(
        self,
    ) -> AppConfig:

        return self._config

    # --------------------------------------------------

    def get(
        self,
        path: str,
        default: Any = None,
    ) -> Any:

        value: Any = self._config.model_dump(
            by_alias=True
        )

        for key in path.split("."):

            if not isinstance(value, dict):
                return default

            value = value.get(key)

            if value is None:
                return default

        return value