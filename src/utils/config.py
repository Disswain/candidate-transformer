"""
Configuration Manager

Loads runtime configuration used throughout the application.

Features
--------
- Default configuration
- Custom configuration override
- Deep dictionary merge
- Validation
- Singleton pattern

Author:
    Candidate Transformer
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any


class ConfigError(Exception):
    """Raised when configuration is invalid."""


class ConfigManager:
    """
    Central configuration manager.

    Usage:
        config = ConfigManager("config/default.json")
        country = config.get("normalization.default_country")
    """

    def __init__(self, default_config: str, custom_config: str | None = None):
        self._config = self._load_json(default_config)

        if custom_config:
            override = self._load_json(custom_config)
            self._config = self._deep_merge(self._config, override)

        self._validate()

    @staticmethod
    def _load_json(path: str) -> dict:
        file = Path(path)

        if not file.exists():
            raise ConfigError(f"Configuration file not found: {path}")

        try:
            with file.open("r", encoding="utf-8") as f:
                return json.load(f)

        except json.JSONDecodeError as exc:
            raise ConfigError(f"Invalid JSON in {path}") from exc

    @staticmethod
    def _deep_merge(base: dict, override: dict) -> dict:
        """
        Recursively merge dictionaries.
        """

        merged = deepcopy(base)

        for key, value in override.items():

            if (
                key in merged
                and isinstance(merged[key], dict)
                and isinstance(value, dict)
            ):
                merged[key] = ConfigManager._deep_merge(
                    merged[key],
                    value,
                )
            else:
                merged[key] = value

        return merged

    def _validate(self) -> None:
        required = [
            "confidence_weights",
            "source_priority",
            "projection",
            "normalization",
        ]

        for key in required:
            if key not in self._config:
                raise ConfigError(
                    f"Missing required configuration key: {key}"
                )

    def get(self, path: str, default: Any = None) -> Any:
        """
        Retrieve nested config values.

        Example:
            get("projection.include_confidence")
        """

        current = self._config

        for part in path.split("."):
            if not isinstance(current, dict):
                return default

            current = current.get(part)

            if current is None:
                return default

        return current

    @property
    def raw(self) -> dict:
        return deepcopy(self._config)